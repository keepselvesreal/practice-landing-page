"""
E2E Test Configuration

Environment variables:
- TEST_ENV: 'local', 'docker', or 'production' (required)
"""
import os
import time
import subprocess
import pytest
from playwright.sync_api import Page
from dotenv import load_dotenv


@pytest.fixture(scope="session")
def test_env():
    """Get test environment from environment variable."""
    env = os.getenv('TEST_ENV')
    if not env:
        raise ValueError(
            "TEST_ENV environment variable must be set. "
            "Valid values: 'local', 'docker', 'production'"
        )

    valid_envs = ['local', 'docker', 'production']
    if env not in valid_envs:
        raise ValueError(
            f"Invalid TEST_ENV='{env}'. "
            f"Valid values: {valid_envs}"
        )

    return env


@pytest.fixture(scope="session")
def base_url(test_env):
    """Get base URL from BASE_URL environment variable."""
    env_base_url = os.getenv('BASE_URL')
    if not env_base_url:
        raise ValueError(
            "BASE_URL environment variable must be set.\n"
            "Example:\n"
            "  Local: export BASE_URL=http://localhost:8080\n"
            "  Docker: set in docker-compose.test.yml\n"
            "  CI/CD: set in GitHub Actions workflow"
        )
    return env_base_url


@pytest.fixture(scope="session")
def api_url(test_env, base_url):
    """Get API URL based on test environment."""
    # For production, API is accessed via /api path
    if test_env == 'production':
        return f"{base_url}/api"

    # For local/docker, API runs on separate port
    urls = {
        'local': 'http://localhost:8000',
        'docker': 'http://localhost:8000',  # Test runs on host, accesses via port mapping
    }
    return urls[test_env]


@pytest.fixture(scope="session")
def postgres_container(test_env):
    """
    Start PostgreSQL container for local environment only.
    Docker uses docker-compose, production uses Cloud SQL.
    """
    if test_env in ['docker', 'production']:
        yield None
        return

    container_name = 'kbeauty-test-postgres'

    # Check if container already running
    check_cmd = f"docker ps -q -f name={container_name}"
    result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)

    if result.stdout.strip():
        print(f"✓ PostgreSQL container already running: {container_name}")
        yield container_name
        return

    # Start PostgreSQL container
    print(f"Starting PostgreSQL container: {container_name}")
    subprocess.run([
        'docker', 'run', '-d',
        '--name', container_name,
        '--rm',
        '-e', 'POSTGRES_DB=kbeauty_test',
        '-e', 'POSTGRES_USER=test_user',
        '-e', 'POSTGRES_PASSWORD=test_pass',
        '-p', '5432:5432',  # Use default port (local postgres removed)
        'postgres:15'
    ], check=True)

    # Wait for PostgreSQL to be ready
    print("Waiting for PostgreSQL to be ready...")
    time.sleep(5)

    # Run migrations
    print("Running database migrations...")
    os.environ['DATABASE_URL'] = 'postgresql://test_user:test_pass@localhost:5432/kbeauty_test'
    backend_path = os.path.join(os.path.dirname(__file__), '..', '..')
    subprocess.run(['uv', 'run', 'alembic', 'upgrade', 'head'], cwd=backend_path, check=True)

    yield container_name

    # Cleanup
    print(f"Stopping PostgreSQL container: {container_name}")
    subprocess.run(['docker', 'stop', container_name], check=False)


@pytest.fixture(scope="session")
def backend_server(test_env, postgres_container):
    """
    Start Backend FastAPI server.

    - local: Start uvicorn in subprocess (reads from .env)
    - docker: Started by docker-compose
    - production: Already deployed
    """
    if test_env in ['docker', 'production']:
        yield None
        return

    # local environment: Load .env and start Backend server
    print("Loading environment variables from .env...")
    env_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env')
    load_dotenv(env_path)

    print("Starting Backend server (uvicorn)...")
    backend_path = os.path.join(os.path.dirname(__file__), '..', '..')
    process = subprocess.Popen(
        ['uv', 'run', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000'],
        cwd=backend_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for server to be ready
    print("Waiting for Backend to be ready...")
    time.sleep(5)

    # Verify server is running
    try:
        import requests
        response = requests.get('http://localhost:8000/health', timeout=5)
        assert response.status_code == 200
        print("✓ Backend server is ready")
    except Exception as e:
        process.terminate()
        raise RuntimeError(f"Backend server failed to start: {e}")

    yield process

    # Cleanup
    print("Stopping Backend server...")
    process.terminate()
    process.wait(timeout=5)


@pytest.fixture(scope="session")
def frontend_server(test_env, backend_server):
    """
    Start Frontend server.

    - local: Start Python HTTP server (after injecting env vars)
    - docker: Started by docker-compose (nginx)
    - production: Already deployed (Firebase)
    """
    if test_env in ['docker', 'production']:
        yield None
        return

    # local environment: Start Frontend server
    # Note: Config is now loaded dynamically from /api/config endpoint
    print("Starting Frontend server (http.server)...")
    root_path = os.path.join(os.path.dirname(__file__), '..', '..', '..')
    frontend_path = os.path.join(root_path, 'frontend')
    process = subprocess.Popen(
        ['python', '-m', 'http.server', '8080'],
        cwd=frontend_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for server to be ready
    print("Waiting for Frontend to be ready...")
    time.sleep(3)

    # Verify server is running
    try:
        import requests
        response = requests.get('http://localhost:8080', timeout=5)
        assert response.status_code == 200
        print("✓ Frontend server is ready")
    except Exception as e:
        process.terminate()
        raise RuntimeError(f"Frontend server failed to start: {e}")

    yield process

    # Cleanup
    print("Stopping Frontend server...")
    process.terminate()
    process.wait(timeout=5)


@pytest.fixture
def page(page: Page, base_url, frontend_server):
    """
    Configure Playwright page with base URL.

    Depends on frontend_server to ensure all servers are started.
    """
    page.set_default_timeout(10000)  # 10 seconds
    return page


@pytest.fixture(autouse=True)
def cleanup_database(test_env, postgres_container):
    """Clean up database after each test."""
    if test_env == 'production':
        # Don't cleanup production DB
        yield
        return

    yield

    # Cleanup after test - truncate tables
    from sqlalchemy import create_engine, text

    # Get database URL based on environment
    if test_env == 'local':
        # Local: conftest.py starts postgres on port 5432
        db_url = 'postgresql://test_user:test_pass@localhost:5432/kbeauty_test'
    elif test_env == 'docker':
        # Docker: docker-compose uses POSTGRES_PORT env var
        postgres_port = os.getenv('POSTGRES_PORT', '5432')
        db_url = f'postgresql://test_user:test_pass@localhost:{postgres_port}/kbeauty_test'
    else:
        return

    engine = create_engine(db_url)
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE orders, email_logs RESTART IDENTITY CASCADE"))
        conn.commit()
    engine.dispose()

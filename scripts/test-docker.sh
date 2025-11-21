#!/bin/bash
set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# 스크립트 디렉토리 및 프로젝트 루트
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

log_info "도커 컴포즈 기반 E2E 테스트 시작"
echo "========================================"

# .env 파일 처리
if [ ! -f ".env" ]; then
    # CI 환경: 환경변수로부터 .env 파일 생성
    log_info ".env 파일이 없습니다. 환경변수로부터 생성합니다."
    cat > .env << EOF
# Test Environment
TEST_ENV=docker

# URLs
BASE_URL=http://localhost:8080

# Database
POSTGRES_PORT=5432

# API Keys
GOOGLE_PLACES_API_KEY=${GOOGLE_PLACES_API_KEY}

# PayPal
PAYPAL_API_BASE=${PAYPAL_API_BASE}
PAYPAL_CLIENT_ID=${PAYPAL_CLIENT_ID}
PAYPAL_CLIENT_SECRET=${PAYPAL_CLIENT_SECRET}

# Email
GMAIL_ADDRESS=${GMAIL_ADDRESS}
GMAIL_APP_PASSWORD=${GMAIL_APP_PASSWORD}
SMTP_HOST=${SMTP_HOST}
SMTP_PORT=${SMTP_PORT}
EOF
    log_info ".env 파일 생성 완료"
else
    # 로컬 환경: 기존 .env 파일 사용
    log_info "기존 .env 파일을 사용합니다."
fi

# 도커 컴포즈 서비스 시작
log_info "도커 컴포즈 서비스 시작 중..."
docker compose -f docker-compose.test.yml up -d

# 서비스 준비 대기
log_info "서비스 준비 대기 중..."
timeout 60 bash -c 'until docker compose -f docker-compose.test.yml ps | grep -q "healthy"; do sleep 2; done' || {
    log_error "서비스 시작 타임아웃"
    docker compose -f docker-compose.test.yml ps
    docker compose -f docker-compose.test.yml logs
    docker compose -f docker-compose.test.yml down -v
    exit 1
}

log_info "서비스 준비 완료"
docker compose -f docker-compose.test.yml ps

# E2E 테스트 실행
log_info "E2E 테스트 실행 중..."

# .env 파일 로드
log_info ".env 파일 로드 중..."
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
fi

log_info "TEST_ENV=$TEST_ENV"
log_info "BASE_URL=$BASE_URL"

# 테스트 실행 (환경변수 명시적 전달)
cd backend
if TEST_ENV=docker BASE_URL=http://localhost:8080 uv run pytest tests/e2e/ -v --tb=short; then
    log_info "E2E 테스트 성공! ✓"
    TEST_RESULT=0
else
    log_error "E2E 테스트 실패!"
    TEST_RESULT=1
fi
cd ..

# 실패 시 로그 출력
if [ $TEST_RESULT -ne 0 ]; then
    echo ""
    log_error "테스트 실패 - 서비스 로그:"
    echo "========================================"
    echo "=== Backend logs ==="
    docker compose -f docker-compose.test.yml logs backend
    echo "=== Frontend logs ==="
    docker compose -f docker-compose.test.yml logs frontend
    echo "=== Postgres logs ==="
    docker compose -f docker-compose.test.yml logs postgres
fi

# 정리
log_info "도커 컴포즈 정리 중..."
docker compose -f docker-compose.test.yml down -v

echo "========================================"
if [ $TEST_RESULT -eq 0 ]; then
    log_info "도커 테스트 완료! ✓"
    exit 0
else
    log_error "도커 테스트 실패!"
    exit 1
fi

# pytest 기반 프로젝트 구조 설계 (현업 베스트 프랙티스)

**작성일:** 2025-11-06
**목적:** Walking Skeleton 구축을 위한 pytest 테스트 구조 설계

---

## 목차

1. [현업 베스트 프랙티스 원칙](#1-현업-베스트-프랙티스-원칙)
2. [pytest 전략 (프로젝트 전체 정책)](#2-pytest-전략-프로젝트-전체-정책)
3. [전체 프로젝트 구조](#3-전체-프로젝트-구조)
4. [tests/ 디렉토리 상세 구조](#4-tests-디렉토리-상세-구조)
5. [pytest 설정 파일들](#5-pytest-설정-파일들)
6. [구체적인 파일별 구현 예시](#6-구체적인-파일별-구현-예시)
7. [요약: 핵심 베스트 프랙티스](#7-요약-핵심-베스트-프랙티스)

---

## 1. 현업 베스트 프랙티스 원칙

### 1.1 테스트 조직화 기준

**관심사의 분리 (Separation of Concerns)**
- 테스트 타입별로 명확히 분리 (unit/integration/e2e)
- 각 레벨은 독립적으로 실행 가능해야 함
- 빠른 피드백: unit → integration → e2e 순으로 실행

**DRY (Don't Repeat Yourself)**
- 공통 fixture는 상위 conftest.py로 승격
- 테스트 데이터는 재사용 가능하게 중앙화
- 헬퍼 함수는 별도 모듈로 분리

**명확성 (Clarity)**
- 테스트 이름만 봐도 무엇을 테스트하는지 알 수 있어야 함
- fixture 이름은 역할을 명확히 표현
- 테스트 데이터는 의도를 드러내야 함 ("obviously canned values")

### 1.2 디렉토리 구조 설계 원칙

**원칙 1: 미러링 (Mirroring)**
```
backend/
├── api/
│   └── routes.py
└── services/
    └── email_service.py

tests/
├── unit/
│   ├── api/
│   │   └── test_routes.py
│   └── services/
│       └── test_email_service.py
```
- 소스 코드 구조와 테스트 구조가 일치

**원칙 2: 계층적 conftest.py**
```
tests/
├── conftest.py              # 전역 fixture
├── unit/
│   └── conftest.py          # unit 전용 fixture
├── integration/
│   └── conftest.py          # integration 전용 fixture
└── e2e/
    └── conftest.py          # e2e 전용 fixture
```
- pytest는 하위에서 상위로 conftest.py를 탐색
- 상위 conftest.py의 fixture는 하위에서 사용 가능

**원칙 3: 격리된 테스트 데이터**
```
tests/
├── fixtures/                # 공통 테스트 데이터
│   ├── factories.py         # Factory 패턴
│   └── builders.py          # Builder 패턴
└── data/
    ├── valid_emails.json
    └── invalid_emails.json
```

---

## 2. pytest 전략 (프로젝트 전체 정책)

### 2.1 Fixture 스코프 전략

**스코프 레벨:**
```python
# function (기본값): 각 테스트마다 새로 생성
@pytest.fixture(scope="function")
def user_data():
    return {"email": "test@example.com"}

# class: 클래스 내 테스트들이 공유
@pytest.fixture(scope="class")
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()

# module: 모듈(.py 파일) 내 모든 테스트가 공유
@pytest.fixture(scope="module")
def app():
    app = create_app()
    yield app
    app.shutdown()

# session: 전체 테스트 세션 동안 1번만 생성
@pytest.fixture(scope="session")
def playwright_browser():
    browser = sync_playwright().start().chromium.launch()
    yield browser
    browser.close()
```

**우리 프로젝트 적용 전략:**
- `session`: Playwright 브라우저, 테스트 DB 스키마
- `module`: FastAPI 앱 인스턴스, HTTP 클라이언트
- `function`: 테스트 데이터, DB 트랜잭션 (기본값)

### 2.2 테스트 마킹 전략

**마커 정의:**
```python
# pytest.ini
[pytest]
markers =
    unit: Unit tests (빠른 테스트, 외부 의존성 없음)
    integration: Integration tests (DB, 외부 서비스 포함)
    e2e: End-to-end tests (전체 스택, 가장 느림)
    slow: 느린 테스트 (1초 이상)
    smoke: Smoke tests (배포 후 기본 동작 확인)
```

**사용 예시:**
```python
@pytest.mark.unit
def test_email_validation():
    assert is_valid_email("test@example.com")

@pytest.mark.integration
@pytest.mark.slow
def test_database_write():
    db.save(user)
    assert db.get(user.id) == user

@pytest.mark.e2e
@pytest.mark.smoke
def test_user_registration_flow():
    # 전체 플로우 테스트
    pass
```

**실행 전략:**
```bash
# 개발 중: unit만 빠르게
pytest -m unit

# CI: unit → integration
pytest -m "unit or integration"

# 배포 전: 전체
pytest

# 프로덕션 smoke test
pytest -m smoke --base-url=https://production.com
```

### 2.3 테스트 실행 전략

**로컬 개발:**
```bash
# 1. 빠른 피드백 (unit만, 병렬)
pytest -m unit -n auto

# 2. 변경된 파일만
pytest --lf  # last failed
pytest --ff  # failed first, then others

# 3. 특정 테스트만
pytest tests/unit/api/test_routes.py::test_register_email
```

**CI/CD 파이프라인:**
```yaml
# Stage 1: Unit (빠름, 병렬)
- pytest -m unit -n auto --cov

# Stage 2: Integration (중간 속도)
- pytest -m integration

# Stage 3: E2E (느림, 배포 후)
- pytest -m e2e --base-url=$DEPLOYED_URL
```

### 2.4 테스트 커버리지 전략

#### 커버리지 측정 원칙

**무엇을 측정하는가:**
- 테스트 케이스 실행 비율 ❌
- **애플리케이션 코드 실행 비율** ✅

```python
# backend/main.py - 10줄
def register(email):
    if not email:        # 라인 2
        return error     # 라인 3
    save_to_db(email)    # 라인 4
    return success       # 라인 5

# 테스트가 라인 2, 4, 5만 실행
# → 커버리지: 75% (3/4줄, 라인 3 누락)
```

#### 목표 및 기준

**프로젝트 단계별 목표:**
```
Walking Skeleton:  60%+  (기본 흐름만)
MVP 단계:         75%+  (주요 기능)
Production Ready: 80%+  (엣지 케이스 포함)
Critical Path:    95%+  (결제, 인증 등)
```

**측정 기준:**
- **Line Coverage** (기본): 실행된 코드 라인 비율
- **Branch Coverage** (권장): 조건문 분기 커버리지
- **Function Coverage**: 호출된 함수 비율

#### 측정 빈도 및 시점

| 환경 | 빈도 | 목적 | 실행 방법 |
|------|------|------|-----------|
| **로컬** | 필요 시 | 현재 작업 확인 | `pytest --cov` |
| **CI/CD** | **매 커밋** | 지속적 모니터링 | 자동 |
| **PR 리뷰** | PR마다 | 변경 영향 확인 | 자동 코멘트 |
| **릴리스** | 필수 | 최종 검증 | Quality Gate |

#### 측정 도구 및 설정

**도구 선택:**
```bash
# Python 표준
pip install pytest-cov

# 추가 도구
pip install coverage[toml]  # 상세 설정용
```

**pytest.ini 설정:**
```ini
[pytest]
addopts =
    --cov=backend                  # 측정 대상
    --cov-report=term-missing      # 터미널: 누락 라인 표시
    --cov-report=html              # HTML 리포트
    --cov-fail-under=80            # 80% 미만이면 실패
    --cov-branch                   # Branch coverage (권장)
```

**pyproject.toml 설정:**
```toml
[tool.coverage.run]
source = ["backend"]
omit = [
    "*/tests/*",
    "*/conftest.py",
    "*/__init__.py",
    "*/migrations/*",
]
branch = true  # Branch coverage 활성화

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if __name__ == .__main__.:",
    "raise AssertionError",
    "raise NotImplementedError",
    "@abstractmethod",
]
precision = 2
skip_empty = true
```

#### CI/CD 통합

**GitHub Actions 예시:**
```yaml
# .github/workflows/ci-cd.yml
jobs:
  test:
    steps:
      # 1. 테스트 실행 with 커버리지
      - name: Run tests with coverage
        run: |
          pytest --cov=backend \
                 --cov-report=xml \
                 --cov-report=term \
                 --cov-fail-under=80

      # 2. 커버리지 리포트 업로드
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          fail_ci_if_error: true

      # 3. PR에 커버리지 코멘트
      - name: Coverage comment
        uses: py-cov-action/python-coverage-comment-action@v3
        with:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          MINIMUM_GREEN: 80
          MINIMUM_ORANGE: 70

      # 4. 커버리지 감소 방지
      - name: Check coverage didn't drop
        run: |
          current=$(coverage report | grep TOTAL | awk '{print $4}' | sed 's/%//')
          if [ "$current" -lt 80 ]; then
            echo "Coverage dropped below 80%"
            exit 1
          fi
```

#### 레벨별 커버리지 전략

**Unit Tests (높은 커버리지 목표):**
```bash
pytest tests/unit/ --cov=backend --cov-report=term

# 목표: 90%+
# 이유: 빠르고 격리되어 있어 높은 커버리지 달성 쉬움
```

**Integration Tests (중간 커버리지):**
```bash
pytest tests/integration/ --cov=backend --cov-append

# 목표: 70%+
# 이유: 복잡한 상호작용, 일부는 E2E에서 커버
```

**E2E Tests (낮은 커버리지 허용):**
```bash
pytest tests/e2e/ --cov=backend --cov-append

# 목표: 50%+
# 이유: 주요 사용자 시나리오만, 세부는 unit에서
```

**전체 통합:**
```bash
# 모든 테스트 실행 후 종합
pytest --cov=backend --cov-report=html

# htmlcov/index.html 에서 시각적 확인
```

#### 커버리지 해석 및 개선

**예시 1: Walking Skeleton 초기**
```bash
$ pytest tests/e2e/test_walking_skeleton.py --cov=backend

Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
backend/main.py      25     12    52%   7-10, 15-22
backend/db.py        15     15     0%   1-15
-----------------------------------------------
TOTAL               40     27    32.5%
```

**분석:**
- ✅ 32.5%는 Walking Skeleton 단계에서 정상
- ✅ 성공 경로(happy path)만 커버됨
- ⚠️ db.py 0%는 예상됨 (E2E만 실행)

**예시 2: 개선 후**
```bash
$ pytest --cov=backend

Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
backend/main.py      25      3    88%   20-22
backend/db.py        15      2    86%   14-15
-----------------------------------------------
TOTAL               40      5    87.5%
```

**개선 방법:**
- Unit 테스트 추가 → db.py 커버리지 증가
- 에러 케이스 테스트 → main.py 라인 7-10 커버
- 엣지 케이스 추가 → 라인 20-22 커버

#### 커버리지 vs 품질

**주의사항:**
```
❌ 100% 커버리지 = 완벽한 테스트 (X)
✅ 80% 커버리지 + 의미있는 테스트 (O)
```

**나쁜 예 (100% 커버리지, 나쁜 테스트):**
```python
def test_register():
    register("test@example.com")  # assertion 없음!
    # 실행은 되지만 검증 안 함
```

**좋은 예 (80% 커버리지, 좋은 테스트):**
```python
def test_register_success():
    result = register("test@example.com")
    assert result["status"] == "success"
    assert db.exists("test@example.com")

def test_register_invalid_email():
    result = register("invalid")
    assert result["error"] == "잘못된 형식"
    assert not db.exists("invalid")
```

#### 실전 팁

1. **점진적 개선**
   ```bash
   # 현재 커버리지 확인
   pytest --cov

   # 누락된 라인 확인
   pytest --cov-report=term-missing

   # HTML로 시각화
   pytest --cov-report=html
   open htmlcov/index.html
   ```

2. **Critical path 우선**
   - 결제, 인증, 데이터 손실 가능 코드 → 95%+
   - 유틸리티, 헬퍼 함수 → 70%+도 OK

3. **커버리지 예외 처리**
   ```python
   def debug_only_function():  # pragma: no cover
       """개발용 함수, 테스트 불필요"""
       print("Debug info")
   ```

4. **리포트 활용**
   ```bash
   # 특정 모듈만
   pytest --cov=backend.api

   # 이전 측정에 추가
   pytest tests/unit --cov=backend
   pytest tests/integration --cov=backend --cov-append

   # JSON 출력 (자동화용)
   pytest --cov=backend --cov-report=json
   ```

---

## 3. 전체 프로젝트 구조

```
practice-landing-page/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── email_service.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── registration.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   └── firebase.json
│
├── tests/
│   ├── conftest.py                    # 전역 설정
│   ├── pytest.ini                     # pytest 설정
│   │
│   ├── fixtures/                      # 공통 fixture & 헬퍼
│   │   ├── __init__.py
│   │   ├── factories.py               # Factory 패턴 (데이터 생성)
│   │   ├── builders.py                # Builder 패턴
│   │   └── helpers.py                 # 헬퍼 함수
│   │
│   ├── data/                          # 테스트 데이터 파일
│   │   ├── valid_emails.json
│   │   ├── invalid_emails.json
│   │   └── sample_registrations.json
│   │
│   ├── unit/                          # Unit tests
│   │   ├── conftest.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── test_routes.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── test_email_service.py
│   │   └── models/
│   │       ├── __init__.py
│   │       └── test_registration.py
│   │
│   ├── integration/                   # Integration tests
│   │   ├── conftest.py
│   │   ├── test_database.py
│   │   └── test_api_with_db.py
│   │
│   └── e2e/                           # E2E tests
│       ├── conftest.py
│       ├── test_walking_skeleton.py
│       └── test_user_registration_flow.py
│
├── docker-compose.yml
├── pyproject.toml                     # 프로젝트 메타데이터
└── README.md
```

### 각 디렉토리 역할

**backend/**
- 실제 애플리케이션 코드
- API, 비즈니스 로직, DB 연결 등

**tests/**
- 모든 테스트 코드
- unit/integration/e2e로 명확히 분리

**tests/fixtures/**
- 재사용 가능한 테스트 데이터 생성 로직
- Factory, Builder 패턴 구현

**tests/data/**
- 정적 테스트 데이터 파일 (JSON, CSV 등)
- 외부 API 응답 mock 데이터

---

## 4. tests/ 디렉토리 상세 구조

### 4.1 conftest.py 계층 구조

```
tests/
├── conftest.py              ← 전역: 모든 테스트에서 사용
│   ├── pytest 옵션 설정
│   ├── 공통 fixture (base_url, test_client)
│   └── 테스트 데이터 로더
│
├── unit/
│   └── conftest.py          ← unit 전용: DB mock, 의존성 mock
│       ├── mock_db
│       └── mock_services
│
├── integration/
│   └── conftest.py          ← integration 전용: 실제 DB, 트랜잭션
│       ├── test_db_connection
│       └── db_transaction
│
└── e2e/
    └── conftest.py          ← e2e 전용: 브라우저, 배포 URL
        ├── playwright_page
        └── deployed_app_url
```

**Fixture 탐색 순서 (pytest가 자동으로):**
```
tests/e2e/test_walking_skeleton.py 실행 시:

1. tests/e2e/conftest.py         (가장 가까운)
2. tests/conftest.py             (상위)
3. pytest 내장 fixture           (최종)
```

### 4.2 Fixture 조직화

**레벨별 fixture 분리:**

```python
# tests/conftest.py - 전역
@pytest.fixture(scope="session")
def base_url():
    """전체 테스트에서 사용하는 기본 URL"""
    return os.getenv("TEST_BASE_URL", "http://localhost:8000")

@pytest.fixture(scope="module")
def test_client():
    """FastAPI TestClient"""
    from fastapi.testclient import TestClient
    from backend.main import app
    return TestClient(app)

# tests/unit/conftest.py - unit 전용
@pytest.fixture
def mock_db():
    """Mock DB (실제 DB 사용 안 함)"""
    return MagicMock()

# tests/integration/conftest.py - integration 전용
@pytest.fixture(scope="module")
def test_db():
    """실제 테스트 DB"""
    db = create_test_database()
    yield db
    db.drop_all()

# tests/e2e/conftest.py - e2e 전용
@pytest.fixture(scope="session")
def browser():
    """Playwright 브라우저"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()
```

### 4.3 테스트 데이터 관리

**Factory 패턴 (tests/fixtures/factories.py):**
```python
from datetime import datetime
from typing import Dict, Any

class RegistrationFactory:
    """등록 데이터 생성 Factory"""

    @staticmethod
    def create(
        email: str = "test@example.com",
        created_at: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """기본 등록 데이터 생성"""
        if created_at is None:
            created_at = datetime.now().isoformat()

        return {
            "email": email,
            "created_at": created_at,
            **kwargs
        }

    @staticmethod
    def create_batch(count: int = 3) -> list:
        """여러 개 생성"""
        return [
            RegistrationFactory.create(email=f"test{i}@example.com")
            for i in range(count)
        ]

    @staticmethod
    def create_invalid():
        """잘못된 이메일"""
        return {"email": "invalid-email"}
```

**Builder 패턴 (tests/fixtures/builders.py):**
```python
class RegistrationBuilder:
    """등록 데이터 Builder (복잡한 객체용)"""

    def __init__(self):
        self.data = {
            "email": "default@example.com",
            "created_at": datetime.now().isoformat(),
        }

    def with_email(self, email: str):
        self.data["email"] = email
        return self

    def with_timestamp(self, timestamp: str):
        self.data["created_at"] = timestamp
        return self

    def build(self) -> Dict[str, Any]:
        return self.data.copy()

# 사용
registration = (RegistrationBuilder()
    .with_email("specific@example.com")
    .with_timestamp("2025-01-01T00:00:00")
    .build())
```

**정적 데이터 (tests/data/):**
```json
// tests/data/valid_emails.json
[
  "simple@example.com",
  "with.dot@example.com",
  "with+plus@example.com",
  "subdomain@mail.example.com"
]

// tests/data/invalid_emails.json
[
  "no-at-sign",
  "@no-local-part.com",
  "no-domain@.com",
  "spaces in@email.com"
]
```

### 4.4 unit/integration/e2e 분리

**Unit Tests (tests/unit/)**
- **목적**: 개별 함수/클래스의 로직 검증
- **특징**:
  - 외부 의존성 없음 (DB, API, 파일시스템 등)
  - 모든 의존성은 mock
  - 매우 빠름 (밀리초 단위)
- **예시**:
  ```python
  # tests/unit/services/test_email_service.py
  @pytest.mark.unit
  def test_validate_email_format():
      service = EmailService()
      assert service.is_valid("test@example.com") == True
      assert service.is_valid("invalid") == False
  ```

**Integration Tests (tests/integration/)**
- **목적**: 컴포넌트 간 상호작용 검증
- **특징**:
  - 실제 DB 사용 (테스트 DB)
  - 실제 파일시스템 사용
  - 외부 API는 mock (또는 테스트 서버)
  - 중간 속도 (초 단위)
- **예시**:
  ```python
  # tests/integration/test_api_with_db.py
  @pytest.mark.integration
  def test_register_saves_to_database(test_client, test_db):
      response = test_client.post("/api/register",
          json={"email": "test@example.com"})

      assert response.status_code == 200
      # 실제 DB에 저장됐는지 확인
      saved = test_db.get_registration("test@example.com")
      assert saved is not None
  ```

**E2E Tests (tests/e2e/)**
- **목적**: 사용자 시나리오 전체 검증
- **특징**:
  - 실제 브라우저 사용
  - 실제 배포된 환경 (또는 로컬 전체 스택)
  - UI → API → DB 전체 흐름
  - 느림 (초~분 단위)
- **예시**:
  ```python
  # tests/e2e/test_user_registration_flow.py
  @pytest.mark.e2e
  def test_user_can_register_and_see_confirmation(page, base_url):
      # 사용자 관점의 전체 플로우
      page.goto(base_url)
      page.fill("#email-input", "user@example.com")
      page.click("#submit-button")
      expect(page.locator("#success-message")).to_be_visible()
  ```

---

## 5. pytest 설정 파일들

### 5.1 pytest.ini (또는 pyproject.toml)

**pytest.ini:**
```ini
[pytest]
# 테스트 탐색 경로
testpaths = tests

# Python 경로 설정
pythonpath = . backend

# 마커 정의
markers =
    unit: Unit tests (fast, no external dependencies)
    integration: Integration tests (database, external services)
    e2e: End-to-end tests (full stack, slowest)
    slow: Tests that take more than 1 second
    smoke: Smoke tests for production

# 출력 설정
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=backend
    --cov-report=term-missing
    --cov-report=html

# 경고 필터
filterwarnings =
    error
    ignore::DeprecationWarning

# Timeout (전체 테스트)
timeout = 300

# 병렬 실행 (선택)
# addopts = -n auto
```

**또는 pyproject.toml:**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = [".", "backend"]

markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "e2e: End-to-end tests",
    "slow: Slow tests",
    "smoke: Smoke tests",
]

addopts = [
    "-v",
    "--strict-markers",
    "--tb=short",
    "--cov=backend",
    "--cov-report=term-missing",
]

[tool.coverage.run]
source = ["backend"]
omit = [
    "*/tests/*",
    "*/conftest.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

### 5.2 각 레벨 conftest.py의 역할

**tests/conftest.py (전역):**
```python
"""전역 pytest 설정 및 공통 fixture"""
import os
import pytest
from pathlib import Path

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent

# 테스트 데이터 로더
@pytest.fixture(scope="session")
def test_data_dir():
    """테스트 데이터 디렉토리"""
    return PROJECT_ROOT / "tests" / "data"

@pytest.fixture(scope="session")
def load_json_data(test_data_dir):
    """JSON 데이터 로더"""
    import json
    def _load(filename: str):
        with open(test_data_dir / filename) as f:
            return json.load(f)
    return _load

# 공통 환경 설정
@pytest.fixture(scope="session")
def base_url():
    """기본 URL (환경변수 또는 기본값)"""
    return os.getenv("TEST_BASE_URL", "http://localhost:8000")

# FastAPI TestClient
@pytest.fixture(scope="module")
def test_client():
    """FastAPI 테스트 클라이언트"""
    from fastapi.testclient import TestClient
    from backend.main import app

    with TestClient(app) as client:
        yield client

# Cleanup hook
@pytest.fixture(autouse=True, scope="session")
def cleanup_test_artifacts():
    """테스트 후 정리 (자동 실행)"""
    yield
    # 테스트 세션 종료 후 실행
    test_db_path = PROJECT_ROOT / "test.db"
    if test_db_path.exists():
        test_db_path.unlink()
```

**tests/unit/conftest.py (unit 전용):**
```python
"""Unit test 전용 fixture"""
import pytest
from unittest.mock import MagicMock, Mock

@pytest.fixture
def mock_db():
    """Mock DB 연결"""
    db = MagicMock()
    db.save.return_value = True
    db.get.return_value = None
    return db

@pytest.fixture
def mock_email_service():
    """Mock 이메일 서비스"""
    service = Mock()
    service.send.return_value = True
    return service

# Unit test에서는 실제 DB 사용 금지
@pytest.fixture(autouse=True)
def disable_real_db(monkeypatch):
    """실제 DB 연결 차단"""
    def mock_connect(*args, **kwargs):
        raise RuntimeError("Unit test에서 실제 DB 사용 불가!")

    monkeypatch.setattr("sqlite3.connect", mock_connect)
```

**tests/integration/conftest.py (integration 전용):**
```python
"""Integration test 전용 fixture"""
import pytest
import sqlite3
from pathlib import Path

@pytest.fixture(scope="module")
def test_db_path(tmp_path_factory):
    """임시 테스트 DB 경로"""
    return tmp_path_factory.mktemp("data") / "test.db"

@pytest.fixture(scope="module")
def test_db(test_db_path):
    """실제 테스트 DB"""
    # DB 생성 및 스키마 초기화
    conn = sqlite3.connect(test_db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE registrations (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()

    yield conn

    # 테스트 후 정리
    conn.close()
    test_db_path.unlink()

@pytest.fixture
def db_transaction(test_db):
    """각 테스트마다 트랜잭션 격리"""
    test_db.execute("BEGIN")
    yield test_db
    test_db.rollback()
```

**tests/e2e/conftest.py (e2e 전용):**
```python
"""E2E test 전용 fixture"""
import pytest
import os
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    """Playwright 브라우저 (세션당 1번 생성)"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,  # CI에서는 headless
            slow_mo=50 if os.getenv("DEBUG") else 0,
        )
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    """각 테스트마다 새 페이지"""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        locale="ko-KR",
    )
    page = context.new_page()

    yield page

    # 실패 시 스크린샷
    if hasattr(pytest, "current_test_failed"):
        page.screenshot(path=f"screenshots/{pytest.current_test_name}.png")

    context.close()

@pytest.fixture
def deployed_url(base_url):
    """배포된 URL (프로덕션 또는 스테이징)"""
    # CI에서 실제 배포 URL 주입
    return os.getenv("DEPLOYED_URL", base_url)
```

---

## 6. 구체적인 파일별 구현 예시

### 6.1 tests/fixtures/factories.py

```python
"""테스트 데이터 Factory"""
from datetime import datetime, timedelta
from typing import Dict, Any, List
import random
import string

class EmailFactory:
    """이메일 생성 Factory"""

    @staticmethod
    def create_valid(domain: str = "example.com") -> str:
        """유효한 이메일 생성"""
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"{username}@{domain}"

    @staticmethod
    def create_invalid() -> str:
        """잘못된 이메일 생성"""
        invalid_patterns = [
            "no-at-sign",
            "@no-local.com",
            "no-domain@",
            "spaces in@email.com",
        ]
        return random.choice(invalid_patterns)

class RegistrationFactory:
    """등록 데이터 Factory"""

    @staticmethod
    def create(
        email: str = None,
        created_at: datetime = None,
        **kwargs
    ) -> Dict[str, Any]:
        """기본 등록 데이터"""
        if email is None:
            email = EmailFactory.create_valid()
        if created_at is None:
            created_at = datetime.now()

        return {
            "email": email,
            "created_at": created_at.isoformat(),
            **kwargs
        }

    @staticmethod
    def create_batch(count: int = 5) -> List[Dict[str, Any]]:
        """여러 개 생성"""
        base_time = datetime.now()
        return [
            RegistrationFactory.create(
                created_at=base_time - timedelta(minutes=i)
            )
            for i in range(count)
        ]
```

### 6.2 테스트 예시들

**tests/unit/services/test_email_service.py:**
```python
"""이메일 서비스 Unit Test"""
import pytest
from backend.services.email_service import EmailService
from tests.fixtures.factories import EmailFactory

@pytest.mark.unit
class TestEmailValidation:
    """이메일 검증 로직 테스트"""

    def setup_method(self):
        self.service = EmailService()

    def test_validates_correct_email_format(self):
        """올바른 이메일 형식을 검증한다"""
        valid_email = EmailFactory.create_valid()
        assert self.service.is_valid(valid_email) is True

    def test_rejects_invalid_email_format(self):
        """잘못된 이메일 형식을 거부한다"""
        invalid_email = EmailFactory.create_invalid()
        assert self.service.is_valid(invalid_email) is False

    @pytest.mark.parametrize("email,expected", [
        ("simple@example.com", True),
        ("with.dot@example.com", True),
        ("with+plus@example.com", True),
        ("no-at-sign", False),
        ("@no-local.com", False),
    ])
    def test_validates_various_email_formats(self, email, expected):
        """다양한 이메일 형식을 검증한다"""
        assert self.service.is_valid(email) == expected
```

**tests/integration/test_api_with_db.py:**
```python
"""API + DB Integration Test"""
import pytest
from tests.fixtures.factories import RegistrationFactory

@pytest.mark.integration
class TestRegistrationAPI:
    """등록 API 통합 테스트"""

    def test_registers_new_email_to_database(
        self,
        test_client,
        db_transaction
    ):
        """새 이메일을 DB에 저장한다"""
        # Given
        registration = RegistrationFactory.create()

        # When
        response = test_client.post(
            "/api/register",
            json={"email": registration["email"]}
        )

        # Then
        assert response.status_code == 200
        assert response.json()["status"] == "success"

        # DB 확인
        cursor = db_transaction.cursor()
        cursor.execute(
            "SELECT email FROM registrations WHERE email = ?",
            (registration["email"],)
        )
        saved = cursor.fetchone()
        assert saved is not None
        assert saved[0] == registration["email"]

    def test_rejects_duplicate_email(self, test_client, db_transaction):
        """중복 이메일을 거부한다"""
        # Given: 이미 등록된 이메일
        email = "duplicate@example.com"
        test_client.post("/api/register", json={"email": email})

        # When: 같은 이메일로 재등록 시도
        response = test_client.post("/api/register", json={"email": email})

        # Then
        assert response.status_code == 400
        assert "이미 등록" in response.json()["message"]
```

**tests/e2e/test_walking_skeleton.py:**
```python
"""Walking Skeleton E2E Test"""
import pytest
from playwright.sync_api import expect

@pytest.mark.e2e
@pytest.mark.smoke
class TestWalkingSkeleton:
    """Walking Skeleton: 가장 얇은 조각"""

    def test_user_can_register_interest(self, page, base_url):
        """사용자가 이메일로 관심 등록을 할 수 있다

        Given: 랜딩페이지가 배포되어 있고
        When: 이메일을 입력하고 등록하면
        Then: 성공 메시지가 표시된다
        """
        # Given
        page.goto(base_url)

        # When
        email_input = page.locator("#email-input")
        submit_button = page.locator("#submit-button")

        email_input.fill("test@example.com")
        submit_button.click()

        # Then
        success_message = page.locator("#success-message")
        expect(success_message).to_be_visible(timeout=5000)
        expect(success_message).to_contain_text("등록 완료")
```

---

## 7. 요약: 핵심 베스트 프랙티스

### 7가지 핵심 원칙

1. **명확한 분리**: unit/integration/e2e 각각 독립 실행 가능
2. **계층적 conftest.py**: 공통 → 특화 fixture 상속
3. **재사용 가능한 데이터**: Factory/Builder 패턴 활용
4. **명확한 마킹**: pytest 마커로 선택적 실행
5. **스코프 최적화**: session/module/function 적절히 사용
6. **격리된 테스트**: 각 테스트는 독립적으로 실행 가능
7. **미러링 구조**: 소스 코드와 테스트 구조 일치

### 빠른 실행 가이드

```bash
# 개발 중 (빠른 피드백)
pytest -m unit

# PR 전 (전체 검증)
pytest -m "unit or integration"

# 배포 전 (전체 + E2E)
pytest

# 특정 레벨만
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# 커버리지 포함
pytest --cov=backend --cov-report=html
```

### 디렉토리 생성 명령어

```bash
# 전체 구조 한 번에 생성
mkdir -p tests/{unit/{api,services,models},integration,e2e,fixtures,data}
touch tests/{conftest.py,pytest.ini}
touch tests/unit/conftest.py
touch tests/integration/conftest.py
touch tests/e2e/conftest.py
touch tests/fixtures/{__init__.py,factories.py,builders.py,helpers.py}
```

---

**참고 문서:**
- [pytest 공식 문서](https://docs.pytest.org/)
- [pytest-cov 문서](https://pytest-cov.readthedocs.io/)
- [Playwright for Python](https://playwright.dev/python/)
- Growing Object-Oriented Software, Guided by Tests (GOOS)

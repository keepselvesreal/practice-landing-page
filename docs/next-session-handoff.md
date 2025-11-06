# 다음 세션 인계 문서

**작성일:** 2025-11-06
**목적:** 다음 세션에서 Walking Skeleton 구축 작업 계속 진행

---

## 1. 프로젝트 개요

### 프로젝트 정보
- **프로젝트명:** practice-landing-page
- **브랜치:** mvp/v1
- **프로젝트 경로:** `/home/nadle/para/projects/practice-landing-page`

### 목적
구매 기능이 있는 랜딩페이지 MVP 개발

### 현재 상태
- Walking Skeleton 구축 준비 완료
- 설계 및 계획 단계 완료
- 실제 코드 작성 대기 중

### 개발 방식
**Outside-In TDD (GOOS 방식)**
- CI/CD First 접근
- E2E 테스트 먼저 작성 (실패)
- CI/CD 파이프라인 구축
- 최소 구현으로 테스트 통과
- 점진적 기능 추가

---

## 2. 기술 스택 결정사항

### Frontend
- HTML5, Vanilla JavaScript
- Firebase Hosting (배포)
- 최소한의 구현

### Backend
- **FastAPI** (웹 프레임워크)
- **SQLite3** (데이터베이스)
- **Cloud Run** (배포 환경)
- **Python 3.11+**

### 테스트
- **pytest** (테스트 프레임워크)
- **pytest-cov** (커버리지)
- **pytest-playwright** (E2E 테스트)

### 개발 도구 (현대화)
- **uv** (의존성 관리 - pip 대체)
- **ruff** (linter + formatter)
- **mypy** (타입 체커)
- **pyproject.toml** (통합 설정)

### CI/CD
- **GitHub Actions**
- Firebase CLI
- gcloud CLI

### 외부 서비스 (나중에)
- PayPal (결제 - Phase 3)
- Google Places API (주소 - Phase 4)
- Google Cloud Storage (SQLite 백업)

---

## 3. Walking Skeleton 설계

### 가장 얇은 조각 정의

**구매 플로우 (결제 제외)**
```
사용자 정보 입력 → 구매 버튼 클릭 → DB 저장 → 구매 완료 페이지
```

**입력 필드:**
- 이름 (name)
- 핸드폰 번호 (phone)
- 이메일 (email)
- 집주소 (address)

### E2E 테스트 시나리오

```python
@pytest.mark.e2e
@pytest.mark.smoke
def test_user_can_complete_purchase(page, base_url):
    """사용자가 구매를 완료할 수 있다 (결제 제외)"""

    # Given: 랜딩페이지 접속
    page.goto(base_url)

    # When: 사용자 정보 입력
    page.fill("#name", "홍길동")
    page.fill("#phone", "010-1234-5678")
    page.fill("#email", "hong@example.com")
    page.fill("#address", "서울시 강남구 테헤란로 123")

    # And: 구매 버튼 클릭
    page.click("#purchase-button")

    # Then: 구매 완료 페이지로 이동
    expect(page).to_have_url(f"{base_url}/purchase-complete")
    expect(page.locator("#confirmation-message")).to_be_visible()
    expect(page.locator("#confirmation-message")).to_contain_text("구매가 완료되었습니다")
```

### 최소 구현 범위

**포함:**
- ✅ 사용자 정보 입력 폼
- ✅ POST /api/purchase 엔드포인트
- ✅ SQLite DB 저장
- ✅ 구매 완료 페이지
- ✅ CI/CD 파이프라인
- ✅ Firebase + Cloud Run 자동 배포

**제외 (나중에 추가):**
- ❌ PayPal 결제 (Phase 3)
- ❌ Google Places API (Phase 4)
- ❌ 폼 검증 세부 로직 (Phase 2)
- ❌ 에러 처리 세부 (Phase 2)

### 단계별 확장 계획

```
Phase 1 (Walking Skeleton): 정보 저장 + 완료 페이지 [1-2일]
↓
Phase 2: 폼 검증 강화 [1일]
↓
Phase 3: PayPal 결제 통합 [2-3일]
↓
Phase 4: Google Places API [1일]
```

---

## 4. 프로젝트 구조

### 전체 디렉토리 구조

```
practice-landing-page/
├── .github/
│   └── workflows/
│       └── ci-cd.yml                # CI/CD 파이프라인
│
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py                # API 엔드포인트
│   ├── models/
│   │   ├── __init__.py
│   │   └── purchase.py              # Purchase 모델 (Pydantic)
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py              # SQLite 연결
│   ├── main.py                      # FastAPI 앱
│   ├── config.py                    # 설정
│   └── Dockerfile                   # 멀티스테이지
│
├── frontend/
│   ├── index.html                   # 랜딩페이지
│   ├── purchase-complete.html      # 구매 완료 페이지
│   ├── app.js                       # API 호출 로직
│   ├── style.css                    # 스타일
│   └── firebase.json                # Firebase 설정
│
├── tests/
│   ├── conftest.py                  # 전역 fixture
│   ├── fixtures/
│   │   ├── __init__.py
│   │   ├── factories.py             # 테스트 데이터 Factory
│   │   └── helpers.py               # 헬퍼 함수
│   ├── data/
│   │   └── sample_purchases.json    # 정적 테스트 데이터
│   ├── unit/
│   │   ├── conftest.py
│   │   └── (미래 테스트들)
│   ├── integration/
│   │   ├── conftest.py
│   │   └── (미래 테스트들)
│   └── e2e/
│       ├── conftest.py              # E2E fixture
│       └── test_walking_skeleton.py # 첫 테스트
│
├── docs/
│   ├── pytest-project-structure-best-practices.md
│   └── next-session-handoff.md      # 이 문서
│
├── records/
│   ├── notes/
│   │   └── walking-skeleton-and-cicd-first.md
│   └── sources/
│       └── test-coverage-understanding.md
│
├── pyproject.toml                   # 통합 설정 (pytest, 의존성)
├── uv.lock                          # 의존성 락파일
├── .python-version                  # Python 버전
├── docker-compose.yml               # 로컬 테스트용
└── README.md
```

### tests/ 구조 상세

```
tests/
├── conftest.py              # 전역 fixture (base_url, test_client)
├── fixtures/
│   ├── factories.py         # PurchaseFactory 등
│   └── helpers.py           # 헬퍼 함수
├── data/
│   └── sample_purchases.json
├── unit/
│   └── conftest.py          # Mock DB, Mock services
├── integration/
│   └── conftest.py          # 실제 테스트 DB
└── e2e/
    └── conftest.py          # Playwright browser, page
```

---

## 5. 개발 계획 (30개 항목)

### Phase 1: 기반 구조 (5개)
1. [ ] 프로젝트 디렉토리 구조 생성
2. [ ] pyproject.toml 작성 (pytest, coverage, 의존성 통합)
3. [ ] .python-version 파일 생성
4. [ ] uv로 프로젝트 초기화
5. [ ] 테스트 fixture 및 헬퍼 설정 (conftest.py)

### Phase 2: E2E 테스트 작성 (2개)
6. [ ] E2E 테스트 작성 - 구매 완료 플로우
7. [ ] Playwright 설정 및 fixture (e2e/conftest.py)

### Phase 3: CI/CD 파이프라인 (4개)
8. [ ] GitHub Actions workflow 파일 작성
9. [ ] 빌드 단계 설정
10. [ ] 테스트 실행 단계 설정
11. [ ] 배포 단계 설정 (Firebase + Cloud Run)

### Phase 4: Backend 더미 구현 (7개)
12. [ ] FastAPI 앱 구조 생성 (main.py)
13. [ ] Purchase 모델 정의 (Pydantic)
14. [ ] SQLite 스키마 생성 (database.py)
15. [ ] POST /api/purchase 엔드포인트 구현
16. [ ] CORS 설정
17. [ ] 멀티스테이지 Dockerfile 작성
18. [ ] backend 디렉토리 구조 정리

### Phase 5: Frontend 더미 구현 (5개)
19. [ ] 랜딩페이지 HTML (index.html)
20. [ ] 구매 폼 구현 (name, phone, email, address)
21. [ ] API 호출 로직 (app.js)
22. [ ] 기본 스타일 (style.css)
23. [ ] 구매 완료 페이지 (purchase-complete.html)

### Phase 6: 배포 설정 (4개)
24. [ ] Firebase Hosting 설정 (firebase.json)
25. [ ] Cloud Run 배포 설정
26. [ ] 환경변수 및 Secret 설정
27. [ ] GitHub Secrets 등록

### Phase 7: 통합 및 검증 (3개)
28. [ ] 로컬에서 전체 스택 테스트 (docker-compose)
29. [ ] CI/CD 파이프라인 첫 실행 및 디버깅
30. [ ] 배포된 환경에서 E2E 테스트 통과 확인

### 현재 진행 상태
- **완료:** 설계 및 계획 (이번 세션)
- **다음 시작:** Phase 1, 항목 1번부터

---

## 6. 설정 파일 템플릿

### pyproject.toml (루트)

```toml
[project]
name = "practice-landing-page"
version = "0.1.0"
description = "Landing page MVP with purchase flow"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "pydantic>=2.5.0",
]

[project.optional-dependencies]
test = [
    "pytest>=7.4.3",
    "pytest-cov>=4.1.0",
    "pytest-playwright>=0.4.3",
    "pytest-asyncio>=0.21.0",
]
dev = [
    "ruff>=0.1.0",
    "mypy>=1.7.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# pytest 설정
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
    "--cov-report=html",
]

# coverage 설정
[tool.coverage.run]
source = ["backend"]
omit = [
    "*/tests/*",
    "*/conftest.py",
    "*/__init__.py",
]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if __name__ == .__main__.:",
    "raise AssertionError",
    "raise NotImplementedError",
]
precision = 2

# ruff 설정
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I"]

# mypy 설정
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
```

### Dockerfile (멀티스테이지)

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# uv 설치
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 의존성 복사 및 설치
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# 빌더에서 가상환경 복사
COPY --from=builder /app/.venv /app/.venv

# 애플리케이션 코드 복사
COPY backend/ ./backend/

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### .python-version

```
3.11
```

### GitHub Actions 구조

```yaml
name: Walking Skeleton CI/CD

on:
  push:
    branches: [main, mvp/v1]
  pull_request:
    branches: [main, mvp/v1]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v1
      - name: Install dependencies
        run: uv sync
      - name: Run E2E tests
        run: uv run pytest tests/e2e/

  deploy:
    needs: build-and-test
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Firebase
        run: firebase deploy
      - name: Deploy to Cloud Run
        run: gcloud run deploy ...
```

---

## 7. 현재 세션 컨텍스트

### 주요 결정사항

1. **Walking Skeleton 기능 확정**
   - 당초 계획: 이메일 관심 등록
   - 변경: 구매 플로우 (name, phone, email, address)
   - 이유: 실제 비즈니스 플로우에 맞춤

2. **결제 제외 결정**
   - PayPal 통합은 Phase 3로 연기
   - Walking Skeleton에서는 정보 저장까지만
   - 이유: 외부 의존성 분리, 빠른 인프라 검증

3. **완전 현대화 방식 선택**
   - pytest.ini → pyproject.toml 통합
   - requirements.txt → pyproject.toml 의존성
   - pip → uv 사용
   - 단순 Dockerfile → 멀티스테이지
   - 이유: 현업 베스트 프랙티스 반영

4. **테스트 커버리지 목표**
   - Walking Skeleton: 60%+
   - MVP: 75%+
   - Production: 80%+

### 이해한 핵심 개념

1. **CI/CD First 접근**
   - 로컬에서 개발 후 배포 ❌
   - CI/CD 환경 먼저 구축 → 그 위에서 개발 ✅

2. **Walking Skeleton = 인프라 검증**
   - 기능 완성도보다 전체 스택 관통이 중요
   - 배포 프로세스 자체를 먼저 검증

3. **테스트 커버리지 = 코드 실행 비율**
   - 테스트 케이스 실행 비율 ❌
   - 애플리케이션 코드 실행 비율 ✅

---

## 8. 알려진 이슈 및 주의사항

### Cloud Run + SQLite 영속성 문제
- **문제:** Cloud Run은 stateless, 재배포 시 데이터 손실
- **임시 해결:** Walking Skeleton 단계에서는 무시
- **장기 해결:** Cloud SQL 또는 Firestore로 전환 필요

### CORS 설정
- **문제:** Firebase Hosting → Cloud Run API 호출 시 CORS 에러 가능
- **해결:** FastAPI에 CORS middleware 추가
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],  # 나중에 실제 도메인으로 제한
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```

### 환경변수 관리
- **로컬:** .env 파일
- **CI/CD:** GitHub Secrets
- **Cloud Run:** Secret Manager
- **주의:** .env 파일은 .gitignore에 추가

### 외부 API 설정
- **PayPal:** 도메인 검증 필요 (나중에)
- **Google Places:** API 키 및 도메인 등록 (나중에)
- **Walking Skeleton에서는 제외**

---

## 9. 즉시 실행 가능한 첫 명령어들

### 1. uv 설치 확인

```bash
# uv가 설치되어 있는지 확인
uv --version

# 없으면 설치
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 디렉토리 생성

```bash
# 프로젝트 루트에서
cd /home/nadle/para/projects/practice-landing-page

# 전체 구조 한 번에 생성
mkdir -p .github/workflows
mkdir -p backend/{api,models,db}
mkdir -p frontend
mkdir -p tests/{fixtures,data,unit,integration,e2e}

# __init__.py 생성
touch backend/__init__.py
touch backend/api/__init__.py
touch backend/models/__init__.py
touch backend/db/__init__.py
touch tests/__init__.py
touch tests/fixtures/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
touch tests/e2e/__init__.py
```

### 3. Python 버전 설정

```bash
echo "3.11" > .python-version
```

### 4. uv 프로젝트 초기화

```bash
# pyproject.toml 생성 (uv가 자동 생성)
uv init --name practice-landing-page

# 의존성 추가
uv add fastapi uvicorn[standard] pydantic

# 개발 의존성 추가
uv add --dev pytest pytest-cov pytest-playwright ruff mypy
```

### 5. pyproject.toml 수정

```bash
# 위의 "설정 파일 템플릿" 섹션의 pyproject.toml 내용을 복사
# 파일을 열어서 pytest, coverage, ruff, mypy 설정 추가
```

### 6. Playwright 설치

```bash
# Playwright 브라우저 설치
uv run playwright install chromium
```

### 7. 첫 파일 생성 순서

```bash
# 1. 테스트부터 (TDD)
touch tests/e2e/test_walking_skeleton.py

# 2. conftest.py
touch tests/conftest.py
touch tests/e2e/conftest.py

# 3. Backend
touch backend/main.py
touch backend/models/purchase.py
touch backend/db/database.py

# 4. Frontend
touch frontend/index.html
touch frontend/purchase-complete.html
touch frontend/app.js
touch frontend/style.css

# 5. Docker
touch backend/Dockerfile
touch docker-compose.yml

# 6. CI/CD
touch .github/workflows/ci-cd.yml
```

### 8. Git 상태 확인

```bash
git status
git branch  # mvp/v1인지 확인
```

---

## 10. 다음 세션 시작 체크리스트

### 환경 확인
- [ ] Python 3.11+ 설치 확인
- [ ] uv 설치 확인 (`uv --version`)
- [ ] Git 브랜치 확인 (`git branch`)
- [ ] 프로젝트 경로 확인

### 첫 작업 순서
1. [ ] 디렉토리 구조 생성 (위의 명령어 실행)
2. [ ] pyproject.toml 작성
3. [ ] .python-version 생성
4. [ ] uv로 의존성 설치
5. [ ] tests/e2e/test_walking_skeleton.py 작성
6. [ ] pytest 실행하여 테스트 실패 확인
7. [ ] CI/CD 파이프라인 작성
8. [ ] 더미 구현 시작

### 참고 문서
- `docs/pytest-project-structure-best-practices.md` - 테스트 구조 상세
- `records/notes/walking-skeleton-and-cicd-first.md` - Walking Skeleton 개념
- `records/sources/test-coverage-understanding.md` - 커버리지 이해

---

**다음 세션에서 볼게! 🚀**

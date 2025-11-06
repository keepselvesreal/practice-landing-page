# pytest conftest와 fixture 이해하기

**작성일:** 2025-11-06

---

## 1. conftest 계층별 작성 이유와 동작 원리

### 맥락
conftest를 계층별로 작성하는 이유가 "불필요한 픽스처 로딩 방지"인데, 동시에 "모든 계층의 conftest가 병합된다"는 설명이 모순처럼 느껴짐. 또한 테스트 실행 시 conftest가 어떻게 준비되고 동작하는지 정확한 프로세스가 궁금함.

### 질문
- conftest를 계층별로 작성하는 이유는?
- 테스트 파일에서 가장 가까운 conftest의 설정과 픽스처가 사용되는가?
- conftest, fixture란 이름의 의미 또는 유래는?
- unit test, integration, e2e 마커별로 conftest가 어떻게 준비되고 동작하는가?

### 답변

#### conftest 계층별 작성 이유
**범위와 재사용성을 분리하기 위해:**
- **전역 conftest** (`tests/conftest.py`): 모든 테스트에서 공통으로 사용 (base_url, test_client 등)
- **레벨별 conftest**: 각 테스트 레벨에만 필요한 픽스처
  - `unit/conftest.py`: mock_db, mock_services (실제 DB 사용 안 함)
  - `integration/conftest.py`: 실제 test_db, transaction 관리
  - `e2e/conftest.py`: playwright 브라우저, 배포 URL

**핵심:** "병합"의 의미는 "모든 픽스처가 사용 가능"하다는 뜻이지, "자동으로 실행"된다는 게 아님!

```
등록(registration) ≠ 실행(execution)

pytest 동작:
1. conftest 읽기 → 픽스처 "목록만" 등록 (실행 X)
2. 테스트 실행 → 요청된 픽스처만 실제 실행

비유:
- 메뉴판에 100개 있어도 (등록)
- 주문한 것만 조리함 (실행)
```

**장점:**
- 불필요한 픽스처를 scope에서 숨김 (개념적 분리)
- 관심사 분리, 유지보수 편함
- 실수 방지 (unit에서 실수로 playwright 픽스처 못 봄)

#### 가장 가까운 conftest만 사용되는가?

**아니다. 모든 계층의 conftest가 병합됨:**

```
tests/e2e/test_walking_skeleton.py 실행 시:
1. tests/e2e/conftest.py (가장 가까운)
2. tests/conftest.py (상위)
3. pytest 내장 fixture

→ 모두 사용 가능! (상위 픽스처도 하위에서 쓸 수 있음)
```

만약 **같은 이름의 픽스처**가 있으면 가장 가까운 것이 우선.

#### 이름의 의미와 유래

**conftest.py:**
- "**conf**iguration for **test**" 의미
- pytest가 자동으로 찾는 특수 파일명 (규약)
- 테스트 설정과 공통 픽스처를 모아두는 곳

**fixture:**
- 원래 뜻: "고정 장치", "부착물"
- 테스트에 필요한 **고정된 테스트 환경/데이터**를 제공한다는 의미
- xUnit 계열 테스트 프레임워크에서 유래 (setUp/tearDown과 유사한 개념)

#### 테스트 실행 시 conftest 준비/동작 과정

**케이스 1: unit 테스트**
```bash
pytest tests/unit/services/test_email_service.py::test_validates_email
```

**Step 1: conftest 탐색 (테스트 수집 단계)**
```
1. tests/unit/services/test_email_service.py 위치 파악
2. 상위로 올라가며 conftest.py 탐색:
   - tests/unit/conftest.py (발견!) → 읽음
   - tests/conftest.py (발견!) → 읽음
```

**Step 2: 사용 가능한 픽스처 등록 (아직 실행 안 함)**
```python
# tests/conftest.py
- base_url (session)
- test_client (module)
- load_json_data (session)

# tests/unit/conftest.py
- mock_db (function)
- mock_email_service (function)
- disable_real_db (autouse=True)  ← 특별! 자동 실행
```

**Step 3: 테스트 함수 실행**
```python
@pytest.mark.unit
def test_validates_email(mock_email_service):  # 이 픽스처만 요청
    # pytest 동작:
    # 1. mock_email_service 찾음 (unit/conftest.py)
    # 2. 의존성 확인 (없음)
    # 3. mock_email_service 실행 → 반환값을 인자로 전달

    service = EmailService(mock_email_service)
    assert service.is_valid("test@example.com")
```

**실제 실행된 픽스처:**
- `mock_email_service` (명시적 요청)
- `disable_real_db` (autouse=True라서 자동 실행)

**실행 안 된 픽스처:**
- `base_url`, `test_client`, `load_json_data`, `mock_db` (요청 안 함)

**케이스 2: integration 테스트**
```bash
pytest tests/integration/test_api_with_db.py::test_registers_new_email
```

```python
@pytest.mark.integration
def test_registers_new_email(test_client, db_transaction):
    # pytest 동작:
    # 1. test_client 찾음 (tests/conftest.py, module scope)
    # 2. db_transaction 찾음 (integration/conftest.py)
    #    → db_transaction이 test_db에 의존 → test_db도 실행
    #    → test_db가 test_db_path에 의존 → test_db_path도 실행

    response = test_client.post("/api/register", json={"email": "test@ex.com"})
    assert response.status_code == 200
```

**실제 실행된 픽스처 (의존성 순서):**
1. `test_db_path` (module, 의존성 체인)
2. `test_db` (module, db_transaction이 의존)
3. `test_client` (module, 명시적 요청)
4. `db_transaction` (function, 명시적 요청)

**케이스 3: e2e 테스트**
```bash
pytest tests/e2e/test_walking_skeleton.py::test_user_can_register
```

```python
@pytest.mark.e2e
def test_user_can_register(page, base_url):
    # pytest 동작:
    # 1. page 찾음 (e2e/conftest.py, function scope)
    #    → page가 browser에 의존 → browser도 실행
    # 2. base_url 찾음 (tests/conftest.py, session scope)

    page.goto(base_url)
    page.fill("#email", "test@ex.com")
```

**실제 실행된 픽스처:**
1. `browser` (session, 처음이면 생성, 아니면 재사용)
2. `base_url` (session, 처음이면 생성)
3. `page` (function, 매 테스트마다 새로 생성)

---

## 2. fixture scope의 의미

### 맥락
conftest에서 `@pytest.fixture(scope="function")`, `scope="module"`, `scope="session"` 같은 파라미터를 보았는데 정확한 의미와 동작 방식이 불명확함.

### 질문
- function과 module의 의미는?
- session의 의미는? pytest 명령 실행부터 종료까지를 의미하는가?

### 답변

#### scope = 픽스처의 생명주기/재사용 범위

```python
@pytest.fixture(scope="function")  # 기본값
def db_transaction():
    # 각 테스트 함수마다 새로 생성/파괴
    pass

@pytest.fixture(scope="module")
def test_db():
    # 모듈(.py 파일)당 1번만 생성
    pass

@pytest.fixture(scope="session")
def browser():
    # 전체 테스트 세션당 1번만 생성
    pass
```

#### 실제 동작 예시

```python
# tests/integration/test_api_with_db.py

@pytest.mark.integration
def test_register_email(test_db, db_transaction):  # 테스트 1
    pass

@pytest.mark.integration
def test_duplicate_email(test_db, db_transaction):  # 테스트 2
    pass

@pytest.mark.integration
def test_invalid_email(test_db, db_transaction):  # 테스트 3
    pass
```

**실행 순서:**
```
pytest tests/integration/test_api_with_db.py 실행

1. 모듈 시작 (test_api_with_db.py)
   → test_db 생성 (module scope) ───┐
                                    │
2. test_register_email 실행         │
   → db_transaction 생성 (function) │← test_db 재사용
   → 테스트 실행                     │
   → db_transaction 파괴            │
                                    │
3. test_duplicate_email 실행        │
   → db_transaction 생성 (새로!)    │← test_db 재사용
   → 테스트 실행                     │
   → db_transaction 파괴            │
                                    │
4. test_invalid_email 실행          │
   → db_transaction 생성 (새로!)    │← test_db 재사용
   → 테스트 실행                     │
   → db_transaction 파괴            │
                                    │
5. 모듈 종료                         │
   → test_db 파괴 ──────────────────┘
```

**왜 이렇게 나눠?**
- `test_db` (module): DB 연결 생성은 **느림** → 모듈당 1번만
- `db_transaction` (function): 각 테스트는 **격리**되어야 함 → 매번 새로운 트랜잭션

#### session의 정확한 의미

**session = pytest 실행 시작 ~ 종료까지**

```bash
# 이게 하나의 "세션"
pytest tests/e2e/
```

**실행 과정:**
```
1. pytest 프로세스 시작 ──────────┐
                                │
2. 테스트 수집                   │
   - test_walking_skeleton.py   │ session scope
   - test_user_flow.py          │ 픽스처는 이 전체 동안
                                │ 1번만 생성/파괴
3. 테스트 실행                   │
   - browser 픽스처 생성 ←───┐   │
   - test1 실행              │   │
   - test2 실행 (browser 재사용) │
   - test3 실행 (browser 재사용) │
                             │   │
4. pytest 프로세스 종료       │   │
   - browser 픽스처 파괴 ────┘   │
─────────────────────────────────┘
```

#### 실제 예시: Playwright Browser

```python
@pytest.fixture(scope="session")
def browser():
    """브라우저는 무거우니까 session당 1번만"""
    print("🚀 브라우저 실행 (3초 걸림)")
    browser = sync_playwright().start().chromium.launch()
    yield browser
    print("🛑 브라우저 종료")
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    """페이지는 테스트마다 새로 (격리)"""
    print("  📄 새 페이지 열기")
    page = browser.new_page()
    yield page
    print("  ❌ 페이지 닫기")
    page.close()
```

**실행 출력:**
```bash
pytest tests/e2e/test_*.py

🚀 브라우저 실행 (3초 걸림)  ← session scope, 1번만!

test_walking_skeleton.py::test_user_can_register
  📄 새 페이지 열기           ← function scope
  PASSED
  ❌ 페이지 닫기

test_walking_skeleton.py::test_shows_error
  📄 새 페이지 열기           ← function scope, 새로
  PASSED
  ❌ 페이지 닫기

🛑 브라우저 종료              ← session 끝, 1번만!
```

#### scope 종류 전체

```python
scope="function"  # 각 테스트 함수마다 (기본값)
scope="class"     # 테스트 클래스마다
scope="module"    # .py 파일마다
scope="package"   # 패키지마다
scope="session"   # pytest 실행 전체
```

---

## 3. conftest 탐색 경로

### 맥락
unit/conftest.py는 integration 테스트에서 읽히지 않는다는 설명을 들었는데, 같은 tests/ 폴더 아래에 있는데도 왜 안 읽히는지 궁금함.

### 질문
- unit/conftest.py는 integration 테스트에서 읽히지 않는가?
- 그 이유는 별도 경로이고, integration 상위 폴더가 아니기 때문인가?

### 답변

#### pytest의 conftest 탐색 규칙

**"현재 위치에서 상위로만 올라감" (옆 폴더는 절대 안 봄!)**

```
tests/
├── conftest.py              # ← 모든 테스트가 읽음
├── unit/
│   ├── conftest.py          # ← unit 폴더 테스트만 읽음
│   └── test_foo.py
└── integration/
    ├── conftest.py          # ← integration 폴더 테스트만 읽음
    └── test_bar.py
```

#### 탐색 경로 예시

```python
# tests/integration/test_bar.py 실행 시

pytest가 탐색하는 경로:
tests/integration/test_bar.py
  ↓ (상위)
tests/integration/conftest.py  ✅ 읽음
  ↓ (상위)
tests/conftest.py              ✅ 읽음
  ↓ (상위)
/home/nadle/para/projects/...  ❌ 프로젝트 루트 넘어가면 중단

절대 가지 않는 경로:
tests/unit/conftest.py         ❌❌❌ (옆 폴더, 상위 아님!)
tests/e2e/conftest.py          ❌❌❌ (옆 폴더)
```

#### 시각적 이해

```
tests/unit/test_foo.py 실행:
    test_foo.py
        ↑
    unit/conftest.py  ✅
        ↑
    tests/conftest.py ✅

tests/integration/test_bar.py 실행:
    test_bar.py
        ↑
    integration/conftest.py ✅
        ↑
    tests/conftest.py       ✅

❌ integration은 unit/conftest.py를 절대 못 봄!
   (옆 폴더니까)
```

**결론:** 네 이해가 정확함. unit/conftest.py와 integration/conftest.py는 서로의 상위 경로가 아니므로 서로 읽히지 않음.

---

## 4. 픽스처 접근 제한

### 맥락
"unit에서 real_db를 못 쓴다"는 설명과 "모든 상위 conftest의 픽스처가 사용 가능"하다는 설명이 충돌하는 것처럼 보임.

### 질문
- unit에서 real_db를 못 쓰는 이유는?
- 픽스처가 모두 등록되면 사용할 수 있는 것 아닌가?

### 답변

#### 실제로는 기술적으로 사용 가능함!

```
tests/
├── conftest.py
│   └── real_db 픽스처 정의
└── unit/
    └── test_foo.py
```

```python
# tests/unit/test_foo.py
def test_something(real_db):  # ← 기술적으로 가능! (상위 conftest에 있으니까)
    pass
```

**pytest는 실행해줌! 막지 않음!**

#### "못 쓴다"의 진짜 의미

**"관례와 설계로 막는 것"이지, pytest가 막는 게 아님.**

#### 방법 1: conftest 위치로 암묵적 제한

```
tests/
├── conftest.py              # 진짜 공통만 (base_url 등)
├── unit/
│   └── conftest.py          # mock_db만 여기
└── integration/
    └── conftest.py          # real_db는 여기만!
```

- `real_db`를 integration/conftest.py에만 정의
- unit/test_foo.py에서 `real_db` 요청하면?
  → pytest 에러: `fixture 'real_db' not found`

#### 방법 2: autouse로 강제 차단 (더 확실함)

```python
# tests/unit/conftest.py

@pytest.fixture(autouse=True)
def disable_real_db(monkeypatch):
    """unit에서 실수로 실제 DB 쓰는 거 방지"""
    def raise_error(*args, **kwargs):
        raise RuntimeError(
            "❌ Unit 테스트에서 실제 DB 사용 금지!\n"
            "mock_db를 사용하세요."
        )

    # 실제 DB 연결 함수를 에러 발생으로 대체
    monkeypatch.setattr("sqlite3.connect", raise_error)
```

**이제 unit에서 실수로 실제 DB 쓰면:**
```python
# tests/unit/test_foo.py
def test_something():
    import sqlite3
    conn = sqlite3.connect("test.db")  # 💥 RuntimeError!
```

#### 정리: "못 쓴다"의 진짜 의미

| 방식 | 의미 | 강제성 |
|------|------|--------|
| **계층별 conftest 분리** | real_db를 integration/conftest.py에만 정의 | ⭐⭐ (픽스처가 scope에 없음) |
| **autouse로 차단** | 실제 DB 연결 자체를 막음 | ⭐⭐⭐ (실행 시 에러) |
| **코드 리뷰** | "왜 unit에서 real_db 써?" | ⭐ (사람이 막음) |

**핵심:**
```
기술적 제약 ❌
설계적 제약 ✅ (conftest 위치 + autouse)
```

---

## 5. pytest 설정 파일

### 맥락
pytest 설정을 pyproject.toml과 pytest.ini 둘 다 사용할 수 있다는 것을 알게 됨. 또한 pythonpath, addopts 같은 설정 옵션들의 의미를 정확히 알고 싶음.

### 질문
- pyproject.toml과 pytest.ini 사용의 차이는?
- pythonpath의 의미는?
- addopts 출력 설정의 의미와 각 인자 의미는?

### 답변

#### pyproject.toml vs pytest.ini

**기능적으로는 거의 동일:**

```ini
# pytest.ini
[pytest]
testpaths = tests
pythonpath = . backend
markers =
    unit: Unit tests
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = [".", "backend"]
markers = [
    "unit: Unit tests",
]
```

**차이점:**

| 항목 | pytest.ini | pyproject.toml |
|------|-----------|----------------|
| **용도** | pytest 전용 | 프로젝트 전체 설정 통합 |
| **포함 내용** | pytest 설정만 | pytest + ruff + mypy + coverage + ... |
| **우선순위** | ⭐⭐⭐ 높음 | ⭐⭐ 중간 |
| **현대적** | 구식 (과거 방식) | ✅ 최신 권장 (PEP 518) |

**실무 권장:** pyproject.toml
- 한 파일에 모든 도구 설정
- Python 공식 표준 (PEP 518)
- uv, poetry 같은 최신 도구들이 선호

**우선순위 (충돌 시):**
```
pytest 실행 시 설정 파일 탐색 순서:
1. pytest.ini          (최우선)
2. pyproject.toml
3. setup.cfg           (구식)
4. tox.ini

→ pytest.ini가 있으면 나머지 무시!
```

#### pythonpath의 의미

**문제 상황:**
```
practice-landing-page/
├── backend/
│   └── api/routes.py
└── tests/
    └── unit/test_routes.py
```

```python
# tests/unit/test_routes.py
from backend.api.routes import register_email  # ❌ ModuleNotFoundError!
```

**왜 에러?**
- pytest는 `tests/` 에서 실행됨
- Python은 `backend/` 를 모름 (import 경로에 없음)

**pythonpath가 해결:**
```ini
[pytest]
pythonpath = . backend
```

**의미:**
```
pytest 실행 시 Python import 경로에 추가:
- . (프로젝트 루트)
- backend (backend 폴더)

이제 import 가능:
- from backend.api.routes import ...  ✅
- from tests.fixtures.factories import ... ✅
```

**실무 권장:**
- 간단한 프로젝트: `pythonpath = .`
- 복잡한 프로젝트: `pip install -e .` (editable install)

#### addopts의 의미

**addopts = "add options"**

```ini
[pytest]
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=backend
    --cov-report=term-missing
```

**의미:** pytest 실행할 때 항상 이 옵션들 자동 추가

```bash
# 이렇게 실행해도
pytest

# 실제로는 이렇게 실행됨
pytest -v --strict-markers --tb=short --cov=backend --cov-report=term-missing
```

#### 각 옵션 의미

**`-v` (verbose, 상세 출력):**
```bash
# -v 없으면
tests/unit/test_routes.py .....  [100%]

# -v 있으면
tests/unit/test_routes.py::test_register_success PASSED  [ 20%]
tests/unit/test_routes.py::test_register_invalid PASSED  [ 40%]
```

**`--strict-markers` (정의 안 된 마커 에러):**
```python
@pytest.mark.unit  # pytest.ini에 정의됨 ✅
def test_foo():
    pass

@pytest.mark.typo_here  # 오타! ❌
def test_bar():
    pass
```

- `--strict-markers` 없으면 → 경고만
- `--strict-markers` 있으면 → 에러 발생, 실행 중단

**`--tb=short` (traceback 길이):**
```bash
# --tb=long (기본값, 너무 김)
... 수십 줄 에러 메시지 ...

# --tb=short (핵심만)
tests/test_foo.py:42: AssertionError

# --tb=line (한 줄만)
tests/test_foo.py:42: assert 5 == 10

# --tb=no (안 보임)
```

**`--cov=backend` (커버리지 측정 대상):**
```bash
--cov=backend  # backend 폴더만 측정
```

**`--cov-report=term-missing` (터미널에 누락 라인 표시):**
```bash
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
backend/main.py      25      3    88%   20-22      ← 누락된 라인!
backend/db.py        15      2    86%   14-15
```

**`--cov-report=html` (HTML 리포트):**
```bash
pytest --cov=backend --cov-report=html

# htmlcov/ 폴더 생성
# htmlcov/index.html 브라우저로 열기
# - 초록색: 실행된 코드
# - 빨간색: 실행 안 된 코드
```

---

## 6. Mock 객체 관리

### 맥락
테스트에서 외부 의존성을 mock으로 대체해야 하는데, mock 객체를 어디서 정의하고 관리해야 하는지 궁금함.

### 질문
- 모킹 객체는 각 conftest에서 관리하는가?

### 답변

#### 각 레벨 conftest에서 관리함

```
tests/
├── conftest.py              # 공통 픽스처만
│   └── base_url, test_client
│
├── unit/
│   └── conftest.py          # ✅ Mock 객체들 여기
│       ├── mock_db
│       ├── mock_email_service
│       └── mock_external_api
│
├── integration/
│   └── conftest.py          # ✅ 실제 객체들 여기
│       ├── test_db (실제 DB)
│       └── real_email_service
│
└── e2e/
    └── conftest.py          # ✅ 브라우저 등 E2E 도구
        ├── browser
        └── page
```

#### 이유

**1. 관심사 분리**
```python
# tests/unit/conftest.py - unit은 mock만
from unittest.mock import MagicMock, Mock

@pytest.fixture
def mock_db():
    """Mock DB - 빠르고 가짜"""
    db = MagicMock()
    db.save.return_value = True
    db.get.return_value = {"id": 1, "email": "test@ex.com"}
    return db

@pytest.fixture
def mock_email_service():
    """Mock 이메일 - 실제 메일 안 보냄"""
    service = Mock()
    service.send_email.return_value = True
    return service
```

```python
# tests/integration/conftest.py - integration은 실제
import sqlite3

@pytest.fixture(scope="module")
def test_db():
    """실제 DB - 느리지만 진짜"""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE
        )
    """)
    conn.commit()
    yield conn
    conn.close()
```

**2. 이름 충돌 방지**
```
unit/conftest.py:  mock_db
integration/conftest.py: test_db  ← 다른 이름 사용

❌ 같은 이름 쓰면 헷갈림:
unit/conftest.py: db
integration/conftest.py: db
```

**3. 실수 방지**
```python
# tests/unit/conftest.py
@pytest.fixture(autouse=True)
def prevent_real_db(monkeypatch):
    """unit에서 실수로 실제 DB 쓰는 거 차단"""
    def mock_connect(*args, **kwargs):
        raise RuntimeError("Unit 테스트에서 실제 DB 금지!")

    monkeypatch.setattr("sqlite3.connect", mock_connect)
```

#### Mock 종류별 위치

```python
# tests/unit/conftest.py - Unit test용 mock
@pytest.fixture
def mock_db():
    from unittest.mock import MagicMock
    return MagicMock()

@pytest.fixture
def mock_external_api():
    """외부 API mock"""
    from unittest.mock import patch
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"status": "ok"}
        yield mock_get

@pytest.fixture
def mock_datetime():
    """시간 고정"""
    from unittest.mock import patch
    from datetime import datetime
    fixed_time = datetime(2025, 1, 1, 12, 0, 0)
    with patch('datetime.datetime') as mock_dt:
        mock_dt.now.return_value = fixed_time
        yield mock_dt

# tests/integration/conftest.py - 실제 객체
# (mock 거의 안 씀, 외부 API만 가끔 mock)
@pytest.fixture
def mock_payment_api():
    """결제 API만 mock (실제 결제 안 하려고)"""
    from unittest.mock import patch
    with patch('stripe.Charge.create') as mock_charge:
        mock_charge.return_value = {"id": "ch_123", "status": "succeeded"}
        yield mock_charge
```

#### 핵심 원칙

```
Unit test: 모든 외부 의존성을 mock
Integration test: DB는 실제, 외부 API만 mock
E2E test: 전부 실제 (또는 테스트 환경)
```

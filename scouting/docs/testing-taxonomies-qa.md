# Software Testing Taxonomies - Q&A

**작성일**: 2025-11-04
**작성자**: Claude & 태수

---

## 목차

- [테스트 구조화 패턴](#test-structuring-patterns)
  - [AAA 패턴과 Given-When-Then 패턴](#aaa-pattern-given-when-then)
- [테스트 명명 규칙](#test-naming-conventions)
- [테스트 프로젝트 구조](#test-project-structure)
  - [디렉터리 조직화](#directory-organization)
  - [테스트 설정 파일](#test-config-files)
  - [테스트 데이터 관리](#test-data-management)
    - [Factory 패턴](#factory-pattern)
    - [Builder 패턴](#builder-pattern)
    - [Object Mother 패턴](#object-mother-pattern)
    - [Fixture 패턴](#fixture-pattern)
  - [모킹 전략](#mocking-strategy)
- [테스트 커버리지](#test-coverage)
  - [커버리지 측정 지표](#coverage-metrics)
  - [커버리지 도구](#coverage-tools)
  - [커버리지 관리 전략](#coverage-management)

---

<a id="test-structuring-patterns"></a>
## 테스트 구조화 패턴

<a id="aaa-pattern-given-when-then"></a>
### AAA 패턴과 Given-When-Then 패턴

**질문**: aaa 패턴과 given when then 패턴의 차이는?

**응답**:
본질적으로 같은 개념. 둘 다 테스트를 3단계로 구조화.

- **AAA (Arrange-Act-Assert)**
  - Arrange: 테스트 준비 (데이터, 객체 설정)
  - Act: 실제 동작 실행
  - Assert: 결과 검증

- **Given-When-Then**
  - Given: 초기 상황/전제조건
  - When: 특정 동작/이벤트 발생
  - Then: 예상 결과/상태

**차이점**:
- AAA는 **단위 테스트**에서 주로 사용 (xUnit 계열)
- Given-When-Then은 **BDD**(Behavior-Driven Development)에서 유래, 비개발자도 읽을 수 있게 비즈니스 언어로 작성
- Given-When-Then이 좀 더 시나리오/스토리 중심

---

<a id="test-naming-conventions"></a>
## 테스트 명명 규칙

**질문**: 테스트 케이스에 이름을 붙이는 규칙은?

**응답**:
테스트 이름은 무엇을 테스트하는지 명확히 전달하는 게 핵심.

**주요 패턴**:
```python
# MethodName_StateUnderTest_ExpectedBehavior
test_calculateTotal_withDiscountCode_returnsReducedPrice()

# Should_ExpectedBehavior_When_StateUnderTest
test_should_returnReducedPrice_when_discountCodeApplied()

# Given_When_Then (BDD 스타일)
test_given_validUser_when_login_then_redirectToDashboard()
```

**일반 원칙**:
- 테스트 대상 명확히: 메서드/기능 이름
- 테스트 조건: 어떤 상황에서
- 기대 결과: 무엇이 일어나야 하는지
- 언더스코어(`_`)로 가독성 확보
- `test_` 접두사 (프레임워크 관례)

---

<a id="test-project-structure"></a>
## 테스트 프로젝트 구조

<a id="directory-organization"></a>
### 디렉터리 조직화

**질문**: 테스트 코드 관련 디렉터리와 파일 조직화 방법은? 테스트 설정 파일, 테스트 데이터, 모킹 객체 등 포함해서

**응답**:

**일반적인 구조**:
```
project/
├── src/
│   ├── auth/
│   └── payment/
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # pytest 설정, fixture 정의
│   ├── unit/                    # 단위 테스트
│   │   ├── auth/
│   │   └── payment/
│   ├── integration/             # 통합 테스트
│   ├── e2e/                     # E2E 테스트
│   ├── fixtures/                # 테스트 데이터
│   │   ├── users.json
│   │   └── products.csv
│   ├── mocks/                   # 모킹 객체
│   │   ├── __init__.py
│   │   ├── api_responses.py
│   │   └── database.py
│   └── helpers/                 # 테스트 유틸리티
├── pytest.ini                   # pytest 전역 설정
└── .coveragerc                  # 커버리지 설정
```

**핵심 원칙**:
1. **미러링 구조**: `tests/` 내부가 `src/` 구조 반영
2. **테스트 레벨 분리**: unit/integration/e2e로 구분
3. **공유 리소스 중앙화**: fixtures, mocks, helpers 별도 디렉터리
4. **설정 파일 루트 배치**: pytest.ini, jest.config.js 등

---

<a id="test-config-files"></a>
### 테스트 설정 파일

**관련 질문**: tests/mocks/__init__.py의 용도는? 왜 필요한 거고 어떻게 활용해?

**응답**:

`__init__.py`의 3가지 역할:

1. **디렉터리를 Python 패키지로 만들기**
2. **공개 API 정의** (편의성)
   ```python
   # tests/mocks/__init__.py
   from .api_responses import mock_user_api
   from .database import mock_db_session

   # 다른 테스트 파일에서
   from tests.mocks import mock_user_api  # 간결함
   ```
3. **초기화 코드 실행** (공통 설정)

**실전 예시**:
```python
# tests/mocks/__init__.py
"""테스트용 모킹 객체 모음"""

from .api_responses import mock_user_api, MockAPIResponse
from .database import mock_db_session, InMemoryDB

__all__ = [
    'mock_user_api',
    'MockAPIResponse',
    'mock_db_session',
    'InMemoryDB'
]
```

---

<a id="test-data-management"></a>
### 테스트 데이터 관리

<a id="factory-pattern"></a>
#### Factory 패턴

**질문**: Factory 패턴 도입 시 이점은?

**응답**:

**비교 예시**:
```python
# ❌ Factory 없을 때 - 반복, 유지보수 지옥
def test_adult_user():
    user = User(id=1, name="Test", age=25, email="test@example.com",
                role="user", created_at=datetime.now(), is_active=True)

# ✅ Factory 있을 때 - 간결, 의도 명확
def test_adult_user():
    user = UserFactory.create(age=25)
```

**이점**:
1. **중복 제거**: 기본값 한 곳에서 관리
2. **변경 용이**: User 모델 바뀌면 Factory만 수정
3. **가독성**: 테스트 의도만 보임
4. **일관성**: 모든 테스트가 같은 기본 데이터 사용

---

<a id="builder-pattern"></a>
#### Builder 패턴

**질문**: 테스트 데이터 유지보수 도와주는 다른 패턴은?

**응답**:

복잡한 객체 단계별 구성:
```python
user = (UserBuilder()
    .with_name("태수")
    .with_age(25)
    .with_role("admin")
    .with_verified_email()
    .build())
```

**특징**: 체이닝으로 가독성 UP, 선택적 설정

---

<a id="object-mother-pattern"></a>
#### Object Mother 패턴

**응답**:

사전 정의된 시나리오:
```python
class UserMother:
    @staticmethod
    def typical_user():
        return User(name="일반유저", age=25, role="user")

    @staticmethod
    def admin_user():
        return User(name="관리자", age=30, role="admin")

    @staticmethod
    def suspended_user():
        return User(name="정지유저", age=20, is_active=False)
```

**특징**: 비즈니스 시나리오 중심

---

<a id="fixture-pattern"></a>
#### Fixture 패턴

**응답**:

pytest/unittest의 자동 의존성 주입:
```python
@pytest.fixture
def valid_user():
    return User(name="테스트", age=25)

@pytest.fixture
def db_session():
    session = create_session()
    yield session
    session.rollback()  # 테스트 후 정리

def test_save_user(valid_user, db_session):
    db_session.add(valid_user)
    # fixture가 자동 주입
```

**패턴 비교**:

| 패턴 | 적합한 상황 | 장점 |
|------|------------|------|
| Factory | 단순 객체, 다양한 변형 | 간결, 유연 |
| Builder | 복잡한 객체, 많은 옵션 | 가독성, 단계별 구성 |
| Object Mother | 고정 시나리오, 비즈니스 맥락 | 의미 명확, 재사용 |
| Fixture | 셋업/클린업 필요 | 자동 관리, 의존성 주입 |

---

<a id="mocking-strategy"></a>
### 모킹 전략

**관련 내용**: 테스트 프로젝트 구조의 일부로 언급됨

**핵심 개념**:
- `tests/mocks/` 디렉터리에 모킹 객체 중앙화
- API 응답, 데이터베이스, 외부 서비스 모킹
- `__init__.py`로 공개 API 관리

---

<a id="test-coverage"></a>
## 테스트 커버리지

<a id="coverage-metrics"></a>
### 커버리지 측정 지표

**질문**: 테스트 커버리지란? 보통 어떤 용도로 어떻게 활용되고 관리되는지?

**응답**:

테스트 커버리지는 테스트가 실제 코드의 얼마나 많은 부분을 실행했는지 측정하는 지표.

**주요 커버리지 유형**:

1. **Line Coverage** (라인 커버리지) - 가장 기본
   - 전체 코드 라인 중 실행된 라인 비율

2. **Branch Coverage** (분기 커버리지)
   - 모든 if/else 경로 실행했는지

3. **Function Coverage** - 함수가 호출되었는지

4. **Statement Coverage** - 실행 가능한 모든 구문

---

<a id="coverage-tools"></a>
### 커버리지 도구

**응답**:

```bash
# Python - coverage.py / pytest-cov
pytest --cov=src --cov-report=html

# JavaScript - Jest
jest --coverage

# Java - JaCoCo
mvn test jacoco:report
```

**리포트 예시**:
```
Name                 Stmts   Miss  Cover
----------------------------------------
src/auth/login.py       45      3    93%
src/payment.py          32     15    53%
----------------------------------------
TOTAL                   77     18    77%
```

---

<a id="coverage-management"></a>
### 커버리지 관리 전략

**응답**:

**1. CI/CD 통합**:
```yaml
# .github/workflows/test.yml
- name: Run tests with coverage
  run: pytest --cov=src --cov-fail-under=80
```

**2. 목표 설정**:
- 일반적 목표: 80-90%
- 핵심 비즈니스 로직: 95%+
- 단순 getter/setter: 무시해도 됨

**3. 제외 패턴**:
```python
# .coveragerc
[run]
omit =
    */tests/*
    */migrations/*
    */settings.py
    */__init__.py
```

**4. 실용 팁**:
- 커버리지 ≠ 품질 (100%여도 버그 있을 수 있음)
- 트렌드 관리: 커버리지 떨어지는 걸 방지
- 핫스팟 집중: 자주 변경되는 코드 우선 커버
- 레거시 점진 개선: 기존 코드는 천천히, 새 코드는 엄격하게

**5. 테스트 속도 최적화**:
- 변경된 파일만 체크
- 병렬 실행 (pytest-xdist, Jest maxWorkers)
- 커버되지 않은 라인 표시로 타겟팅

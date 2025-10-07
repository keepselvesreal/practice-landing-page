# 6장: 동적 및 매개변수화 테스트와 픽스처 - 추출된 정보

## 핵심 내용
- PyTest의 고급 기능과 동적 동작 지원
- 테스트 스위트 설정과 구성 파일 관리
- 동적 픽스처 생성과 관리
- 매개변수화를 통한 테스트 생성과 확장

## 상세 핵심 내용

### PyTest 설정 시스템
- **pytest.ini**: 테스트 러너와 발견 메커니즘 설정
- **conftest.py**: 테스트와 테스트 스위트 구성
- **명령행 옵션**: 실행 시 동적 옵션 제공
- **계층적 설정**: 프로젝트, 디렉토리, 파일 레벨 설정

### 동적 픽스처
- **팩토리 패턴**: 매개변수에 따른 픽스처 생성
- **조건부 픽스처**: 환경에 따른 픽스처 선택
- **픽스처 체인**: 픽스처 간 의존성 관리
- **스코프 관리**: function, class, module, session 레벨

### 매개변수화 테스트
- **@pytest.mark.parametrize**: 테스트 케이스 자동 생성
- **데이터 기반 테스트**: 외부 데이터로 테스트 확장
- **조합 테스트**: 다중 매개변수 조합
- **ID 커스터마이징**: 테스트 케이스 식별자 관리

## 상세 내용

### pytest.ini 설정 예제
```ini
[pytest]
addopts = -v -s --tb=short
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test* *Tests
python_functions = test_*
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
```

### conftest.py 픽스처 정의
```python
import pytest
import tempfile
import shutil

@pytest.fixture(scope="session")
def test_database():
    # 테스트 데이터베이스 설정
    db = create_test_database()
    yield db
    # 정리
    db.cleanup()

@pytest.fixture
def temp_directory():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture(params=['sqlite', 'mysql', 'postgres'])
def database_connection(request):
    db_type = request.param
    conn = create_connection(db_type)
    yield conn
    conn.close()
```

### 동적 픽스처 팩토리
```python
@pytest.fixture
def user_factory():
    created_users = []

    def _create_user(name, age=25, email=None):
        if email is None:
            email = f"{name.lower()}@example.com"
        user = User(name=name, age=age, email=email)
        created_users.append(user)
        return user

    yield _create_user

    # 정리
    for user in created_users:
        user.delete()

def test_user_creation(user_factory):
    user1 = user_factory("Alice", 30)
    user2 = user_factory("Bob", email="bob@custom.com")
    assert user1.name == "Alice"
    assert user2.email == "bob@custom.com"
```

### 매개변수화 테스트
```python
@pytest.mark.parametrize("input,expected", [
    (1, 1),
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    assert input ** 2 == expected

@pytest.mark.parametrize("username,password,expected", [
    ("admin", "secret", True),
    ("user", "password", True),
    ("invalid", "wrong", False),
    ("", "", False),
], ids=["admin_login", "user_login", "invalid_credentials", "empty_credentials"])
def test_login(username, password, expected):
    result = authenticate(username, password)
    assert result == expected
```

### 다중 매개변수 조합
```python
@pytest.mark.parametrize("browser", ["chrome", "firefox", "safari"])
@pytest.mark.parametrize("device", ["desktop", "mobile"])
@pytest.mark.parametrize("resolution", ["1920x1080", "1366x768", "375x667"])
def test_ui_compatibility(browser, device, resolution):
    driver = setup_browser(browser, device, resolution)
    page = navigate_to_homepage(driver)
    assert page.is_displayed_correctly()
```

### 조건부 테스트 실행
```python
@pytest.mark.skipif(sys.platform == "win32",
                   reason="Unix-specific test")
def test_unix_feature():
    assert run_unix_command() == "success"

@pytest.mark.xfail(reason="Known issue #123")
def test_known_failure():
    assert buggy_function() == "expected"

@pytest.fixture(autouse=True)
def setup_test_environment(request):
    if "slow" in request.keywords:
        pytest.skip("Slow tests disabled")
```

## 주요 화제

### 1. 테스트 스위트 구성
- pytest.ini를 통한 전역 설정
- conftest.py를 통한 픽스처 공유
- 계층적 설정 관리
- 명령행 옵션과 설정 파일 통합

### 2. 동적 픽스처 패턴
- 팩토리 픽스처로 객체 생성
- 매개변수화된 픽스처
- 조건부 픽스처 선택
- 픽스처 체인과 의존성

### 3. 매개변수화 전략
- 단일 매개변수 테스트
- 다중 매개변수 조합
- 외부 데이터 소스 활용
- 테스트 ID 커스터마이징

### 4. 테스트 마킹과 필터링
- 커스텀 마커 정의
- 조건부 테스트 실행
- 테스트 그룹화와 선택적 실행
- CI/CD 파이프라인 통합

### 5. 고급 픽스처 기법
- 스코프별 픽스처 관리
- 자동 사용(autouse) 픽스처
- 픽스처 파라미터화
- 리소스 관리와 정리

### 6. 성능과 확장성
- 효율적인 픽스처 재사용
- 병렬 테스트 실행 고려
- 메모리 사용 최적화
- 테스트 실행 시간 관리

## 부차 화제

### 1. 설정 파일 관리
- 환경별 설정 분리
- 버전 관리 고려사항
- 팀 협업을 위한 설정 표준화
- 로컬 개발 환경 커스터마이징

### 2. 테스트 데이터 관리
- 테스트 데이터 생성 전략
- 픽스처를 통한 데이터 준비
- 외부 데이터 소스 통합
- 데이터 격리와 정리

### 3. 마커 시스템 활용
- 빌드 파이프라인 최적화
- 테스트 분류와 조직화
- 환경별 테스트 선택
- 성능 테스트 분리

### 4. 플러그인과 확장
- 커스텀 픽스처 플러그인
- 테스트 리포트 커스터마이징
- 서드파티 도구 통합
- 프로젝트별 확장 개발

### 5. 디버깅과 진단
- 픽스처 의존성 시각화
- 테스트 실행 프로파일링
- 실패 분석과 디버깅
- 로그 수집과 분석

### 6. 모범 사례
- 픽스처 네이밍 컨벤션
- 테스트 구조화 패턴
- 코드 재사용 전략
- 유지보수 가능한 테스트 설계
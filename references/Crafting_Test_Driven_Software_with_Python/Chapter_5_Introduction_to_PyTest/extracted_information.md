# 5장: PyTest 소개 - 추출된 정보

## 핵심 내용
- PyTest 프레임워크의 기본 사용법과 unittest와의 차이점
- PyTest 픽스처(fixtures)를 통한 테스트 설정 관리
- 임시 데이터 관리와 I/O 테스트 기법
- 테스트 스위트의 부분 실행과 필터링

## 상세 핵심 내용

### PyTest의 장점
- **unittest 호환성**: 기존 unittest 테스트를 수정 없이 실행 가능
- **간단한 문법**: 함수 기반 테스트 작성 가능
- **향상된 assert**: 실패 시 상세한 정보 제공
- **풍부한 플러그인**: 다양한 확장 기능 제공

### 테스트 발견 메커니즘
- **패턴 기반**: [Tt]est* 패턴의 모듈, 클래스, 함수
- **구성 가능**: pytest.ini로 발견 규칙 커스터마이징
- **유연성**: 클래스 상속 불필요
- **상세 출력**: -v 옵션으로 진행 상황 표시

### 픽스처(Fixtures) 시스템
- **의존성 주입**: 테스트 함수에 자동으로 매개변수 제공
- **스코프 관리**: function, class, module, session 레벨
- **설정과 정리**: setup과 teardown 로직 통합
- **재사용성**: 여러 테스트에서 공통 설정 재사용

### 내장 픽스처 활용
- **tmp_path**: 임시 디렉토리 자동 생성 및 정리
- **capsys**: 표준 출력/에러 캡처
- **monkeypatch**: 런타임 객체 수정
- **request**: 테스트 메타데이터 접근

## 상세 내용

### 기본 PyTest 테스트
```python
def test_something():
    a = 5
    b = 10
    assert a + b == 15  # 단순한 assert 문 사용
```

### 픽스처 정의와 사용
```python
import pytest

@pytest.fixture
def sample_data():
    return {"name": "Test User", "age": 30}

@pytest.fixture(scope="module")
def database_connection():
    # 설정
    conn = create_connection()
    yield conn
    # 정리
    conn.close()

def test_user_data(sample_data):
    assert sample_data["name"] == "Test User"
    assert sample_data["age"] == 30
```

### 임시 경로 사용
```python
def test_file_operations(tmp_path):
    # 임시 파일 생성
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello World")

    # 파일 내용 확인
    content = test_file.read_text()
    assert content == "Hello World"
    # tmp_path는 자동으로 정리됨
```

### 표준 출력 캡처
```python
def print_hello():
    print("Hello World")

def test_print_output(capsys):
    print_hello()
    captured = capsys.readouterr()
    assert captured.out == "Hello World\n"
    assert captured.err == ""
```

### 매개변수화된 테스트
```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert input * 2 == expected
```

### 테스트 실행 옵션
```bash
# 모든 테스트 실행
pytest

# 상세 출력
pytest -v

# 특정 패턴만 실행
pytest -k "test_client"

# 특정 마커만 실행
pytest -m "unit"

# 실패 시 즉시 중단
pytest -x

# 최대 실패 개수 제한
pytest --maxfail=3
```

### 마커 사용
```python
import pytest

@pytest.mark.unit
def test_fast_operation():
    assert True

@pytest.mark.integration
def test_database_operation():
    assert True

@pytest.mark.slow
def test_time_consuming_operation():
    assert True
```

## 주요 화제

### 1. PyTest 기본 사용법
- unittest에서 PyTest로의 마이그레이션
- 함수 기반 테스트 작성
- 향상된 assert 기능 활용
- 테스트 발견과 실행 메커니즘

### 2. 픽스처 시스템
- 테스트 설정과 정리 로직
- 스코프별 픽스처 관리
- 의존성 주입 패턴
- 픽스처 조합과 재사용

### 3. 내장 픽스처 활용
- tmp_path로 임시 파일/디렉토리 관리
- capsys로 출력 검증
- monkeypatch로 모킹
- 테스트 환경 격리

### 4. 테스트 조직화
- 마커를 통한 테스트 분류
- 매개변수화를 통한 테스트 케이스 확장
- 조건부 테스트 실행
- 테스트 스위트 필터링

### 5. 고급 기능
- 플러그인 시스템
- 커스텀 픽스처 작성
- 테스트 설정 파일 관리
- 병렬 테스트 실행

### 6. 성능과 효율성
- 빠른 테스트 실행
- 효율적인 픽스처 관리
- 선택적 테스트 실행
- 리소스 최적화

## 부차 화제

### 1. 설치와 설정
- pip install pytest
- pytest.ini 설정 파일
- tox.ini와 통합
- IDE 통합 설정

### 2. 호환성 고려사항
- unittest와의 차이점
- Python 버전 호환성
- 서드파티 라이브러리 통합
- 기존 테스트 마이그레이션

### 3. 플러그인 생태계
- pytest-cov (커버리지)
- pytest-mock (모킹)
- pytest-xdist (병렬 실행)
- pytest-html (HTML 리포트)

### 4. 디버깅과 진단
- 상세한 오류 메시지
- 테스트 실패 분석
- 성능 프로파일링
- 로그 캡처

### 5. CI/CD 통합
- JUnit XML 출력
- 테스트 리포트 생성
- 병렬 실행 최적화
- 실패 알림 설정

### 6. 모범 사례
- 픽스처 네이밍 컨벤션
- 테스트 구조화 패턴
- 코드 재사용 전략
- 유지보수 가능한 테스트
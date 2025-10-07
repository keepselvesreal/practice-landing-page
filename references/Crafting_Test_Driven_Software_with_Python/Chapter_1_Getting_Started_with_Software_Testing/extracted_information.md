# 1장: 소프트웨어 테스팅 시작하기 - 추출된 정보

## 핵심 내용
- 소프트웨어 품질 관리와 테스팅의 기본 개념
- 수동 테스트에서 자동화 테스트로의 전환
- 테스트 주도 개발(TDD)과 단위 테스트의 기초
- 통합 테스트와 기능 테스트의 이해
- 테스팅 피라미드와 트로피 모델

## 상세 핵심 내용

### 소프트웨어 테스팅의 필요성
- **품질 관리**: 제조업에서 영감을 받은 소프트웨어 품질 보증 프로세스
- **테스트 플랜**: 전제조건(Preconditions), 단계(Steps), 후제조건(Postconditions)으로 구성
- **자동화의 필요성**: 빠른 릴리스 주기와 복잡한 소프트웨어 요구사항 충족

### 자동화 테스트와 테스트 스위트
- **unittest 모듈**: Python 표준 라이브러리의 테스트 프레임워크
- **테스트 케이스**: `unittest.TestCase`를 상속하고 `test_`로 시작하는 메서드
- **테스트 러너**: 테스트 발견(discovery)과 실행(execution) 담당
- **테스트 조직**: 여러 모듈과 디렉토리로 테스트 구조화

### 테스트 주도 개발(TDD)
- **Arrange, Act, Assert 패턴**: 상태 준비 → 동작 실행 → 결과 검증
- **TDD 사이클**: 실패하는 테스트 작성 → 통과시키는 코드 작성 → 리팩터링
- **화이트박스 테스트**: 코드 내부 구조를 알고 작성하는 테스트
- **테스트와 코드의 상호 작용**: 지속적인 테스트-코드 작성 순환

### 단위 테스트의 분류
- **솔리터리 단위**: 다른 의존성 없이 독립적으로 테스트 가능한 단위
- **소셜 단위**: 다른 단위들을 사용하는 단위 (컴포넌트 테스트라고도 함)
- **테스트 더블**: 의존성을 대체하여 솔리터리 단위로 변환하는 기법

## 상세 내용

### unittest 모듈 사용법
```python
import unittest

class MyTestCase(unittest.TestCase):
    def test_one(self):
        # Arrange phase
        # Act phase
        result = do_something()
        # Assert phase
        assert result == "expected_value"

if __name__ == '__main__':
    unittest.main()
```

### 테스트 발견과 실행
```bash
# 단일 모듈 실행
python test_module.py -v

# 디렉토리 내 모든 테스트 발견 및 실행
python -m unittest discover tests -v

# 특정 패턴으로 필터링
python -m unittest discover tests -k sum -v
```

### TDD 예제: addition 함수
```python
def addition(*args):
    total = 0
    for a in args:
        total += a
    return total

class AdditionTestCase(unittest.TestCase):
    def test_main(self):
        result = addition(3, 2)
        assert result == 5

    def test_threeargs(self):
        result = addition(3, 2, 1)
        assert result == 6

    def test_noargs(self):
        result = addition()
        assert result == 0
```

### 통합 테스트 예제
```python
class TestAuthorizeAuthenticatedUser(unittest.TestCase):
    def test_auth(self):
        auth = Authentication()
        authz = Authorization()
        auth.USERS = [{"username": "testuser", "password": "testpass"}]
        authz.PERMISSIONS = [{"user": "testuser", "permissions": {"create"}}]

        u = auth.login("testuser", "testpass")
        resp = authz.can(u, "create")
        assert resp is True
```

## 주요 화제

### 1. 소프트웨어 품질 관리
- 제조업에서 영감을 받은 품질 보증 프로세스
- 테스트 플랜과 체크리스트 기반 검증
- 수동 테스트의 한계와 자동화의 필요성
- 빠른 릴리스 주기 요구사항

### 2. 자동화 테스트 구축
- unittest 모듈을 이용한 테스트 케이스 작성
- 테스트 러너의 발견과 실행 메커니즘
- 여러 테스트 케이스와 개별 테스트 관리
- 테스트 조직화와 디렉토리 구조

### 3. 테스트 주도 개발
- Arrange, Act, Assert 패턴의 적용
- 실패하는 테스트 우선 작성의 중요성
- 리팩터링을 통한 코드 품질 향상
- 요구사항의 명시적 표현

### 4. 단위 테스트 전략
- 솔리터리 vs 소셜 단위 테스트
- 테스트 가능한 최소 단위의 정의
- 컴포넌트 테스트와의 경계
- 테스트 더블을 통한 격리

### 5. 통합 및 기능 테스트
- 모듈 간 통합 검증의 필요성
- 아키텍처 컴포넌트 간 테스트
- 기능 테스트, E2E 테스트, 시스템 테스트, 승인 테스트의 구분
- 구현 vs 동작 테스트의 차이점

### 6. 테스팅 전략 모델
- 테스팅 피라미드: 단위 테스트 중심의 계층적 구조
- 테스팅 트로피: 통합 테스트 중심의 균형잡힌 접근
- 정적 분석의 가치와 ROI 고려사항

## 부차 화제

### 1. Python 환경 요구사항
- Python 3.7 이상 권장
- unittest 모듈은 표준 라이브러리에 포함
- GitHub 저장소: PacktPublishing/Crafting-Test-Driven-Software-with-Python

### 2. 테스트 실행 옵션
- `-v` 플래그로 상세 출력
- `-k` 패턴으로 테스트 필터링
- 알파벳 순서로 테스트 실행
- 테스트 간 독립성과 병렬 실행 고려

### 3. 코드 커버리지
- 80% 코드 커버리지가 일반적 목표
- Python의 경우 90% 권장
- 100% 커버리지가 필요한 특수 상황 (Python 2→3 포팅)
- getter/setter 등 단순 코드의 테스트 제외

### 4. 테스트 유형의 다양성
- 기능 테스트: 사용자 기능 검증 (블랙박스)
- E2E 테스트: 수직적 통합, Selenium 등 활용
- 시스템 테스트: 전체 사용자 여정 시뮬레이션
- 승인 테스트: 명세 기반 주요 플로우 검증
- 컴포넌트 테스트, 계약 테스트 등 추가 분류

### 5. 프로덕션 환경 테스트
- 스테이징 환경의 중요성
- 실제 동시 사용자와 대용량 데이터 테스트
- 카오스 엔지니어링과 연속적 문제 주입
- 프로덕션 모니터링과 사고 재현 시스템

### 6. 개발 프로세스 통합
- 지속적 통합(CI)과 지속적 배포(CD) 지원
- 개발 중 단위 테스트 연속 실행
- 안정 단계에서 통합 테스트 실행
- 테스트 스위트의 점진적 감소 수익률 관리
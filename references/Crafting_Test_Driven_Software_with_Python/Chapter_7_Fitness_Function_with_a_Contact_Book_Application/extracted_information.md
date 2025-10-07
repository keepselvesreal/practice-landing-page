# 7장: 연락처 북 애플리케이션을 통한 피트니스 함수 - 추출된 정보

## 핵심 내용
- 피트니스 함수(Fitness Function) 개념과 소프트웨어 품질 측정
- 승인 테스트를 통한 전체 소프트웨어 검증
- 행동 주도 개발(BDD)과 pytest-bdd 활용
- 예제를 통한 명세(Specifications by Example) 작성

## 상세 핵심 내용

### 피트니스 함수 개념
- **품질 측정**: 소프트웨어가 얼마나 요구사항을 만족하는지 측정
- **전체적 검증**: 개별 단위가 아닌 전체 시스템의 동작 검증
- **비즈니스 정렬**: 기술적 정확성이 아닌 비즈니스 요구사항 충족도 측정
- **지속적 피드백**: 개발 과정에서 지속적인 품질 모니터링

### 승인 테스트의 중요성
- **최종 검증**: 단위 테스트로는 보장할 수 없는 전체 기능 검증
- **비즈니스 가치**: 개발자의 의도가 아닌 비즈니스 요구사항 검증
- **사용자 관점**: 실제 사용자가 경험할 기능과 동작 검증
- **회귀 방지**: 전체 시스템 레벨에서의 회귀 버그 감지

### 행동 주도 개발(BDD)
- **자연어 명세**: Given-When-Then 구조로 명확한 시나리오 정의
- **협업 도구**: 개발자, 테스터, 비즈니스 관계자 간 공통 언어
- **실행 가능한 명세**: 문서이면서 동시에 실행 가능한 테스트
- **pytest-bdd 통합**: Python 환경에서의 BDD 구현

### 명세서로서의 테스트
- **Living Documentation**: 항상 최신 상태를 유지하는 문서
- **예제 기반**: 구체적인 예제를 통한 요구사항 명시
- **비모호성**: 추상적 설명 대신 구체적인 동작 정의
- **검증 가능성**: 명세가 곧 테스트로 동작

## 상세 내용

### 연락처 북 애플리케이션 구조
```
.
├── src
│   ├── contacts
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── app.py
│   │   └── storage.py
│   └── setup.py
└── tests
    ├── acceptance
    │   ├── test_contact_management.py
    │   └── features
    │       └── contact_book.feature
    ├── unit
    │   ├── test_contact.py
    │   └── test_storage.py
    └── conftest.py
```

### Gherkin 피처 파일 예제
```gherkin
Feature: Contact Book Management
  As a user
  I want to manage my contacts
  So that I can keep track of people's information

  Scenario: Adding a new contact
    Given I have an empty contact book
    When I add a contact "John Doe" with phone "123-456-7890"
    Then the contact book should contain 1 contact
    And the contact "John Doe" should have phone "123-456-7890"

  Scenario: Searching for contacts
    Given I have contacts in my contact book:
      | name     | phone        | email              |
      | John Doe | 123-456-7890 | john@example.com   |
      | Jane Doe | 098-765-4321 | jane@example.com   |
    When I search for "Doe"
    Then I should see 2 contacts in the results
    And the results should include "John Doe" and "Jane Doe"
```

### pytest-bdd 스텝 정의
```python
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from contacts.app import ContactBook

scenarios('features/contact_book.feature')

@pytest.fixture
def contact_book():
    return ContactBook()

@given('I have an empty contact book')
def empty_contact_book(contact_book):
    contact_book.clear()

@given(parsers.parse('I add a contact "{name}" with phone "{phone}"'))
def add_contact(contact_book, name, phone):
    contact_book.add_contact(name=name, phone=phone)

@when(parsers.parse('I search for "{query}"'))
def search_contacts(contact_book, query):
    contact_book.search_results = contact_book.search(query)

@then(parsers.parse('the contact book should contain {count:d} contact'))
def verify_contact_count(contact_book, count):
    assert len(contact_book.contacts) == count

@then(parsers.parse('I should see {count:d} contacts in the results'))
def verify_search_results(contact_book, count):
    assert len(contact_book.search_results) == count
```

### 승인 테스트 예제
```python
class TestContactBookAcceptance:
    def test_complete_contact_workflow(self):
        # Given: 새로운 연락처 북
        app = ContactBookApp()

        # When: 연락처 추가
        app.execute_command("add John Doe 123-456-7890 john@example.com")
        app.execute_command("add Jane Smith 098-765-4321 jane@example.com")

        # Then: 연락처가 올바르게 저장됨
        contacts = app.execute_command("list")
        assert "John Doe" in contacts
        assert "Jane Smith" in contacts

        # When: 연락처 검색
        search_results = app.execute_command("search Doe")

        # Then: 올바른 결과 반환
        assert "John Doe" in search_results
        assert "Jane Smith" not in search_results
```

## 주요 화제

### 1. 피트니스 함수 설계
- 전체 시스템 품질 측정 방법
- 비즈니스 가치 중심의 검증
- 정량적 품질 지표 정의
- 지속적 품질 모니터링

### 2. 승인 테스트 전략
- 사용자 시나리오 기반 테스트
- 엔드투엔드 기능 검증
- 비즈니스 요구사항 추적성
- 회귀 방지 메커니즘

### 3. BDD 구현
- Gherkin 언어를 통한 명세 작성
- pytest-bdd를 통한 자동화
- 자연어와 코드의 연결
- 협업 도구로서의 활용

### 4. 테스트 계층 구조
- 단위 테스트와 승인 테스트의 역할 분담
- 통합 테스트의 위치와 범위
- 각 계층별 피드백 속도와 신뢰성
- 테스트 피라미드 최적화

### 5. 명세 문서화
- 실행 가능한 문서 작성
- 예제를 통한 요구사항 명시
- 비기술자와의 협업 도구
- 지속적인 문서 최신화

### 6. 품질 보증 프로세스
- 개발 프로세스와 테스트 통합
- 지속적 통합에서의 승인 테스트
- 배포 전 품질 검증
- 모니터링과 피드백 루프

## 부차 화제

### 1. 도구와 프레임워크
- pytest-bdd 설치와 설정
- Gherkin 언어 문법
- 스텝 정의 패턴
- 테스트 실행과 리포팅

### 2. 협업과 커뮤니케이션
- 비즈니스 관계자와의 협업
- 요구사항 명세 작성 프로세스
- 테스트 케이스 리뷰
- 피드백 수집과 반영

### 3. 유지보수성
- 테스트 시나리오 관리
- 변경 사항 추적과 업데이트
- 테스트 데이터 관리
- 환경별 설정 분리

### 4. 성능 고려사항
- 승인 테스트 실행 시간
- 테스트 환경 최적화
- 병렬 실행 전략
- 리소스 사용량 관리

### 5. 실제 적용
- 프로젝트별 적용 전략
- 기존 시스템에 BDD 도입
- 팀 교육과 문화 변화
- 점진적 도입 방법

### 6. 품질 메트릭
- 테스트 커버리지 측정
- 결함 발견율 추적
- 사용자 만족도 지표
- 비즈니스 가치 측정
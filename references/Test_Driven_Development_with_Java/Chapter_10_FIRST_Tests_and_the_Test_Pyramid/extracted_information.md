# Test_Driven_Development_with_Java_Chapter_10_FIRST_Tests_and_the_Test_Pyramid

## 압축 내용

**Test Pyramid**은 **Unit Tests(FIRST)**를 기반으로 하고 그 위에 **Integration Tests**, 최상단에 **End-to-End/Acceptance Tests**를 계층화하여, 빠르고 반복 가능한 테스트를 최대화하고 느리고 불안정한 테스트를 최소화하며, **CI/CD 파이프라인**과 **테스트 환경**을 통해 전체 시스템을 통합하고 배포한다.

---

## 핵심 내용

### 핵심 개념
1. **Test Pyramid 구조** → 상세 내용 1
2. **Unit Tests (FIRST)** → 상세 내용 2
3. **Integration Tests** → 상세 내용 3
4. **End-to-End/Acceptance Tests** → 상세 내용 4
5. **CI/CD 파이프라인** → 상세 내용 5
6. **테스트 환경** → 상세 내용 6

### 핵심 개념 간 관계
**Unit Tests (FIRST)** 기반 → **Integration Tests** 추가 → **E2E/Acceptance Tests** 완성 → **Test Pyramid** 구조 → **테스트 환경**에서 실행 → **CI/CD 파이프라인**으로 자동화

---

## 상세 내용

### 목차
1. Test Pyramid 개요
2. Unit Tests - FIRST 테스트
3. Integration Tests
4. End-to-End와 User Acceptance Tests
5. CI/CD 파이프라인과 테스트 환경
6. Wordz - 데이터베이스 통합 테스트

---

### 1. Test Pyramid 개요 → [핵심 개념 1]

**출처**: Lines 40-92

**4개 계층** (Lines 50-69):
1. **Unit Tests**: 외부 시스템 불필요, FIRST 테스트
2. **Integration Tests**: 외부 시스템과의 통합 검증, 느리고 환경 의존적
3. **End-to-End Tests**: 실제 컴포넌트로 사용자 경험에 가까운 테스트
4. **User Acceptance Tests**: 실제 시스템을 사용자가 사용하는 대로 테스트

**피라미드 형태 이유** (Lines 74-80):
- Unit Tests가 가장 많고, Integration Tests, E2E Tests 순으로 감소
- 상위로 갈수록 내부 컴포넌트→외부 시스템→최종 사용자로 이동
- Unit Tests는 빠르고 반복 가능하지만 외부 연결 테스트 불가
- 외부 시스템/사용자와의 상호작용 테스트 필요

**목표** (Lines 81-89):
- 가능한 빠른 실행
- 최대한 많은 코드 커버
- 최대한 많은 결함 방지
- 테스트 노력 중복 최소화

---

### 2. Unit Tests - FIRST 테스트 → [핵심 개념 2]

**출처**: Lines 93-149

**장점** (Lines 110-123):
- 가장 빠른 테스트, 가장 빠른 피드백 루프
- 안정적이고 반복 가능, 외부 의존성 없음
- 특정 로직 상세 커버, 결함 정확히 위치

**한계** (Lines 112-123):
- 작은 범위 → 모든 테스트 통과해도 전체 시스템 작동 보장 안 됨
- 구현 세부사항과 강한 결합 가능 → 리팩토링 어려움
- 외부 시스템 상호작용 테스트에 도움 안 됨

**Hexagonal Architecture와의 시너지** (Lines 131-147):
- 도메인 모델 대부분을 Unit Tests로 커버
- 빠른 Unit Tests로 넓은 영역 커버, 높은 신뢰도
- 외부 시스템이 예상대로 동작하면 도메인 레이어가 모든 use case 처리 가능
- 테스트 더블로 외부 시스템 시뮬레이션
- **한계**: Adapter 레이어는 Unit Test 레벨에서 테스트 안 됨

---

### 3. Integration Tests → [핵심 개념 3]

**출처**: Lines 150-315

#### 3.1 목적과 특징 (Lines 154-191)

**목적**: 코드가 외부 시스템과 성공적으로 통합되는지 테스트

**장단점** (Lines 163-174):

장점:
- 연결된 소프트웨어 컴포넌트의 올바른 상호작용 테스트
- 실제 사용 시스템의 더 가까운 시뮬레이션

단점:
- 테스트 환경 설정 및 유지보수 필요
- Unit Tests보다 느린 실행
- 테스트 환경 문제(잘못된 데이터, 네트워크 연결 실패)에 취약

**Flaky Tests** (Lines 183-191):
- 가끔 통과, 가끔 실패하는 테스트
- 외부 시스템 문제로 실패 (코드 결함 아님)
- False negative 결과
- 개발자가 테스트 무시하도록 학습 → 좋지 않은 상황

#### 3.2 커버 범위 (Lines 192-220)

**Thin Adapter** (Lines 197-204):
- 외부 시스템과 상호작용하는 최소한의 코드만 포함
- 애플리케이션 로직 없음 (도메인 레이어에 있어야 함)
- Integration Test 범위가 제한됨

**테스트 환경** (Lines 215-220):
- Integration Tests에 사용되는 외부 시스템 배열
- 테스트용 웹 서비스와 데이터 소스 실행
- 프로덕션 서비스가 아닌 테스트 버전 사용
- Integration Test 통과 전에는 실제 서비스 접근 안 함

#### 3.3 데이터베이스 어댑터 테스트 (Lines 221-258)

**기본 접근** (Lines 222-225):
- 테스트 환경에 데이터베이스 서버 설정
- Arrange: 알려진 데이터셋 미리 로드
- Act: 데이터베이스 상호작용 코드 실행
- Assert: 예상 데이터베이스 변경 검사

**문제: 데이터 기억** (Lines 226-234):
- 데이터베이스는 데이터를 기억 → 격리되고 반복 가능한 테스트와 충돌
- 예: `testuser1` 생성 후 재실행 시 "이미 존재" 에러

**해결 방법** (Lines 235-256):

1. **각 테스트 전후 모든 데이터 삭제** (Lines 236-238):
   - 테스트 격리 보존
   - 느림 (매 테스트마다 스키마 재생성)

2. **전체 테스트 세트 전후 데이터 삭제** (Lines 239-243):
   - 덜 자주 삭제
   - 테스트 격리 상실 (다음 테스트 시작 시 예상 상태 아님)
   - 특정 순서로 실행 필요, 모두 통과해야 함
   - 좋지 않은 접근

3. **무작위 데이터 사용** (Lines 244-249):
   - `testuser1` 대신 `testuser-cfee-0a9b-931f` 같은 무작위 이름
   - 테스트 격리 보존
   - 테스트 가독성 저하
   - 주기적 테스트 DB 정리 필요

4. **트랜잭션 롤백** (Lines 250-252):
   - 데이터베이스 트랜잭션 내에서 테스트 데이터 추가
   - 테스트 끝에 롤백

5. **문제 무시** (Lines 253-256):
   - 읽기 전용 데이터베이스
   - 프로덕션 코드가 접근하지 않을 테스트 데이터 추가
   - 가능하면 매력적 (추가 노력 불필요)

**도구**: database-rider (https://database-rider.github.io/getting-started/)

#### 3.4 웹 서비스 테스트 (Lines 259-315)

**Sandbox API** (Lines 270-277):
- 타사 벤더가 호스팅하는 테스트 버전 서비스
- 프로덕션 시스템과 분리
- 테스트 계정/데이터 생성 가능
- 프로덕션 응답과 동일하게 응답하지만 실제 동작(결제 등) 안 함

**Consumer-Driven Contract Testing** (Lines 278-315):
- 외부 서비스와의 계약(contract) 개념
- 우리 코드: 특정 API 함수 호출, 요구 형식 데이터 제공
- 외부 서비스: 예측 가능하게 응답, 알려진 포맷 데이터, 잘 이해된 상태 코드

**2가지 컴포넌트** (Lines 298-313):

1. **외부 서비스 스텁** (Lines 299-304):
   - 외부 서비스를 로컬로 시뮬레이션
   - 어댑터 코드 작성 시 테스트 더블로 사용
   - 외부 시스템 접근 없이 어댑터 로직 테스트
   - 올바른 API 호출 전송 및 예상 응답 처리 검증

2. **실제 외부 서비스 호출 재생** (Lines 305-313):
   - 실제 외부 서비스(sandbox 모드 가능)에 대한 테스트 실행
   - 외부 서비스 기능 테스트 아님 (제공자가 수행 가정)
   - API에 대한 우리 믿음이 맞는지 검증
   - 어댑터가 특정 순서로 특정 API 호출하도록 코딩됨 검증
   - 이전에 작동했으나 지금 실패 → 외부 서비스 API 변경 조기 경고

**도구**: Pact (https://docs.pact.io)

---

### 4. End-to-End와 User Acceptance Tests → [핵심 개념 4]

**출처**: Lines 318-414

#### 4.1 정의 (Lines 321-329)

**기술적으로 동일한 테스트**:
- 가장 실제 환경에 가까운 테스트 환경 또는 프로덕션에서 소프트웨어 완전 구성 시작
- 시스템 전체를 처음부터 끝까지 테스트

**User Acceptance Testing (UAT)** (Lines 325-329):
- 여러 주요 E2E 테스트 시나리오 실행
- 모두 통과 → 소프트웨어가 목적에 적합하다고 선언, 사용자가 수락
- 상업적 개발에서 계약 단계인 경우 많음
- 소프트웨어 구매자가 개발 계약 만족 공식 동의

#### 4.2 장단점 (Lines 330-358)

**장점**:
- 가장 포괄적인 기능 테스트
- 사용자(사람 또는 기계) 경험과 동일한 수준에서 테스트
- 순수 행동 관심 (외부에서 관찰)
- 시스템 대부분 리팩토링/재설계해도 이 테스트들이 보호
- 계약적으로 중요 (최종 사용자가 관심 있는 본질)

**단점**:
- 가장 느린 테스트
- 신뢰성 문제 - 환경 설정 문제로 false negative 발생
- "Brittleness" (취약성): 환경에 크게 의존, 우리 통제 밖 상황으로 환경 손상 가능
- 작성이 가장 도전적 (광범위한 환경 설정 요구사항)

#### 4.3 커버 범위와 목적 (Lines 359-390)

**위치**: 피라미드 최상단 (Lines 359-361)
- 많이 필요 없음 반영
- 대부분 코드는 Unit/Integration Tests로 커버됨

**남은 테스트 대상** (Lines 362-385):
- Unit/Integration 레벨에서 이미 수행한 테스트 중복 원하지 않음
- 전체 소프트웨어가 예상대로 작동하는지 검증 필요
- 실제 데이터베이스와 실제 외부 서비스에 연결
- 테스트 더블로 Unit Tests 통과 → 실제 외부 서비스 연결 시 작동할 것으로 예상
- "should"는 소프트웨어 개발의 멋진 회피 단어
- E2E 테스트로 실제로 작동하는지 검증 시점

**주요 기술적 측면** (Lines 377-385):
- 소프트웨어가 올바르게 구성되고 연결되었는지 테스트
- Dependency Inversion과 Injection으로 외부 시스템 격리
- 테스트 더블 생성 및 주입
- 실제 어댑터 레이어 컴포넌트 생성 (프로덕션 시스템 연결)
- 초기화 및 구성 중 주입 → 실제 작동 설정

**Happy Path 중복** (Lines 382-385):
- Unit/Integration으로 이미 커버된 소량의 happy path 중복
- 목적: 이미 테스트한 행동 검증 아님
- 목적: 올바른 프로덕션 객체 주입했는지 검증 (프로덕션 서비스 연결 시 전체 시스템이 올바르게 작동함을 확인)

**UAT의 더 넓은 목적** (Lines 386-390):
- 기술적 수준에서는 E2E 테스트
- 기술적 목표(시스템이 올바르게 구성됨) 이상
- 법적/계약적 성격: 요청한 것을 구축했는가?
- 이 책의 반복적 접근과 기술 관행으로 더 높은 확률

#### 4.4 도구 (Lines 391-410)

**주요 차별점**: 소프트웨어와 상호작용하는 방식

**인기 도구**:
- **RestEasy** (https://resteasy.dev/): REST API 테스트
- **RestAssured** (https://rest-assured.io/): REST API 테스트, Fluent 접근으로 JSON 응답 검사
- **Selenium** (https://www.selenium.dev/): 브라우저를 통한 웹 UI 테스트
- **Cucumber** (https://cucumber.io/): 영어 같은 테스트 설명, 도메인 전문가가 작성 (이론상, 실제로는 개발자가 작성)

---

### 5. CI/CD 파이프라인과 테스트 환경 → [핵심 개념 5]

**출처**: Lines 418-651

#### 5.1 CI/CD 정의 (Lines 423-434)

**CI (Continuous Integration)** (Lines 425-427):
- Integration: 개별 소프트웨어 컴포넌트를 결합하여 전체 생성
- Continuous: 새 코드 작성 시 항상 수행

**CD (Continuous Delivery/Deployment)** (Lines 428-432):
- Continuous Delivery 또는 Continuous Deployment
- 통합된 소프트웨어의 최신 버전을 이해관계자에게 전달
- 목표: 모든 코드 변경을 버튼 클릭 하나로 프로덕션 배포 가능

**본질** (Lines 433-434):
- CI/CD는 엔지니어링 규율, 도구 세트 아님
- 목표: 항상 사용 가능한 상태의 단일 시스템 성장

#### 5.2 CI 필요성 (Lines 435-471)

**Test Pyramid 관점** (Lines 436-442):
- 모든 테스트를 함께 가져오는 메커니즘
- 최신 코드로 전체 소프트웨어 빌드
- 모든 테스트 실행, 모두 통과 확인 후 패키징/배포
- 테스트 실패 → 배포 부적합 코드
- 빠른 피드백 → 가장 빠른 것부터 느린 순서로 테스트 실행
- Unit → Integration → E2E/Acceptance 순서
- 실패 시 빌드 중지 및 실패 리포트

**일반적 필요성** (Lines 443-464):
- 혼자 작업 시에도 중요
- 여러 빌딩 블록 통합 필요 (자체 제작, 라이브러리, 어댑터)
- 팀 작업 시 더욱 중요
- 다른 팀원이 작성한 모든 조각 통합
- 진행 중인 작업을 동료로부터 통합하는 것이 긴급
- 다른 사람이 작성한 것 위에 구축
- 메인 통합 코드베이스 외부 작업 → 최신 설계 결정 및 재사용 가능 코드 미포함 위험

**Waterfall 함정 회피** (Lines 460-464):
- 팀이 계획을 따르며 개별적으로 코드 작성, 마지막에만 통합
- 통합 실패로 작동하는 소프트웨어 미생성
- 오해 또는 누락 → 컴포넌트가 맞지 않음
- Waterfall 프로젝트 후반 → 실수 수정 비용 큼

**개인 경험 사례** (Lines 465-470):
- RAF Red Arrows 비행 시뮬레이터 게임
- 2명이 공통 API로 작업
- 첫 통합 시도: 새벽 3시, 이사 앞에서
- 3프레임 실행 후 크래시
- CI 부족으로 인한 교훈

#### 5.3 CD 필요성 (Lines 475-511)

**목표** (Lines 476-478):
- CI가 컴포넌트를 함께 유지 → CD는 관심 있는 사람들 손에 전달

**3가지 이점** (Lines 481-494):

1. **사용자가 원하는 가치 획득** (Lines 482-486):
   - 최종 사용자는 개발 프로세스 관심 없음
   - 문제 해결만 관심 (Uber 대기 중 오락, 다국적 기업 급여 지급)
   - 가치 있는 기능을 사용자에게 전달 → 경쟁 우위

2. **귀중한 사용자 피드백** (Lines 487-490):
   - "요청한 것이지만 의도한 것은 아님!"
   - 최종 사용자가 구현된 기능 보면 → 문제 해결 아님 명확해짐
   - 빠른 수정 가능

3. **코드베이스와 개발 팀 정렬** (Lines 491-494):
   - 이를 성공시키려면 팀과 워크플로우가 함께해야 함
   - 작동하는 소프트웨어가 단일 전체로 지속적으로 사용 가능한 워크플로우 필요

**Continuous Delivery vs Deployment** (Lines 500-511):

**Continuous Delivery** (Lines 501-502):
- 내부 이해관계자(제품 소유자, QA 엔지니어)에게 소프트웨어 전달

**Continuous Deployment** (Lines 503-511):
- 프로덕션과 최종 사용자에게 소프트웨어 전달
- 훨씬 높은 기준
- 파이프라인에 코드 통합 → 실제 사용자에게 배포 준비 완료
- 어려움
- 최고급 테스트 자동화 필요 (배포 준비 확신)
- 프로덕션에서 빠른 롤백 시스템 필요 (테스트 미커버 결함 발견 시 빠른 배포 되돌림)
- 궁극적 워크플로우
- 성취 시: 금요일 늦게 새 코드 배포해도 두려움 없음 (적어도 덜 두려움)

#### 5.4 실용적 CI/CD 파이프라인 (Lines 512-551)

**도구** (Lines 513-517):
- Jenkins, GitLab, CircleCI, Travis CI, Azure DevOps
- 유사하게 작동: 개별 빌드 단계를 순차적으로 실행
- "파이프라인" 이름: 한쪽 끝에서 다음 빌드 단계 로드, 다른 끝에서 나옴

**7단계** (Lines 519-548):

1. **Source Control** (Lines 521-524):
   - 코드 저장 공통 위치 필수
   - 코드 통합 장소
   - 최신 소스 코드 버전 가져오기, 클린 빌드 수행
   - 오래된 코드 버전으로 인한 에러 방지

2. **Build** (Lines 526-528):
   - 빌드 스크립트 실행: 라이브러리 다운로드, 코드 컴파일, 링크
   - 출력: 실행 가능한 것 (일반적으로 단일 Java archive .jar 파일)

3. **Static Code Analysis** (Lines 534-536):
   - Linters 및 분석 도구로 소스 코드 검사
   - 스타일 위반 (변수 길이, 명명 규칙 등)
   - 팀이 특정 코드 문제 발견 시 빌드 실패 선택 가능

4. **Unit Tests** (Lines 538-539):
   - 빌드된 코드에 대해 모든 Unit Tests 실행
   - 실패 시 파이프라인 중지, 테스트 실패 메시지 리포트

5. **Integration Tests** (Lines 541-542):
   - 빌드된 코드에 대해 모든 Integration Tests 실행
   - 실패 시 파이프라인 중지, 에러 메시지 리포트

6. **Acceptance Tests** (Lines 544-545):
   - 빌드된 코드에 대해 모든 Acceptance Tests 실행
   - 모든 테스트 통과 → 코드 작동, 전달/배포 준비

7. **Delivery Packaging** (Lines 547-548):
   - 코드를 전달에 적합한 형태로 패키징
   - Java 웹 서비스: 임베디드 웹 서버 포함 단일 .jar 파일

**이후 단계** (Lines 549-551):
- 프로덕션에 자동 배포 또는
- 내부 저장소에 배치 (제품 소유자와 QA 엔지니어 접근)
- 공식 배포는 품질 게이트키핑 후 나중에

#### 5.5 테스트 환경 (Lines 552-606)

**필요성** (Lines 553-563):
- CI 파이프라인에서 Integration Tests 실행 위치 문제
- 프로덕션: 데이터베이스, 결제 제공자와 통합
- CI 파이프라인: 결제 처리나 프로덕션 DB 쓰기 원하지 않음
- 하지만 실제 시스템 연결 시 통합 테스트 필요
- **해결책**: 테스트 환경 생성
  - 우리 통제 하 데이터베이스와 시뮬레이션 외부 시스템 모음
  - 코드가 우리 통제 하 실제 외부 시스템 테스트 버전 연결
  - 사용자 세부 데이터베이스 필요 → 로컬로 복사본 실행
  - 테스트 중 이 로컬 DB 연결 (프로덕션 버전 대신)
  - 외부 결제 제공자: sandbox API 제공

**Live-like/Staging 환경** (Lines 564-566):
- 더 현실적인 통합 테스트
- Unit Tests: stubs와 mocks 사용
- Integration Tests: 더 풍부한 테스트 환경 사용

**장단점** (Lines 567-606):

**장점**:
- **자체 포함** (Lines 575-577): 생성/파괴 자유, 프로덕션 시스템 영향 없음
- **Stubs보다 현실적** (Lines 586-589): 프로덕션 부하/조건에 가까운 테스트
- **외부 시스템 가정 확인** (Lines 594-597): 타사 sandbox 환경으로 최신 올바른 API 사용 확인

**단점**:
- **프로덕션 환경 아님** (Lines 578-585):
  - 아무리 실제 같아도 시뮬레이션
  - 위험: 가짜 환경이 false positive 제공 (가짜 데이터로만 통과)
  - 잘못된 자신감 → 프로덕션 실패 코드 배포
  - **실제 테스트는 항상 코드 배포 시**

- **생성/유지보수 추가 노력** (Lines 590-593): 환경 설정 및 테스트 코드와 동기화 유지 개발 작업 필요

- **개인정보 문제** (Lines 598-605):
  - 프로덕션 데이터 덩어리를 단순히 복사 불충분
  - PII (개인 식별 정보, GDPR/HIPAA 정의) 포함 시 법적으로 직접 사용 불가
  - 데이터 익명화 또는 유사 현실적 무작위 테스트 데이터 생성 추가 단계 필요
  - 둘 다 쉽지 않음

#### 5.6 프로덕션에서 테스트 (Lines 607-647)

**일반적으로 끔찍한 아이디어** (Lines 608-612):
- 가짜 주문 도입 → 프로덕션이 실제로 처리
- 테스트 사용자 계정 추가 → 보안 위험
- 테스트 단계 → 코드 아직 작동 안 할 가능성 높음 → 온갖 문제 (프로덕션 시스템 연결 중)

**필요한 경우** (Lines 613-616):
- Google, Meta 같은 빅데이터 회사
- 데이터 규모로 인해 실제만 테스트 가능
- 의미 있는 실제 같은 테스트 환경 생성 불가 (너무 작음)

**위험 완화 기술** (Lines 617-647):

**1. Blue-Green Deployment** (Lines 623-634):
- 실패 배포의 빠른 롤백 위한 배포 기술
- 프로덕션 서버를 2그룹으로 분할 (Blue, Green - 중립 성공 색상)
- 프로덕션 코드가 한 번에 한 그룹에서 실행
- 현재 Blue 실행 중 → 다음 배포는 Green으로
- Green 배포 후 프로덕션 구성을 Green으로 전환
- 이전 작동 프로덕션 코드는 Blue에 유지
- Green 테스트 성공 → 완료 (프로덕션이 최신 Green 코드로 작동)
- 테스트 실패 → 구성을 Blue로 되돌림
- 빠른 롤백 시스템으로 실험 가능

**2. Traffic Partitioning** (Lines 635-647):
- Blue-green에 추가하여 테스트 서버로 보내는 트래픽 양 제한
- 프로덕션을 새 테스트 코드로 완전 전환하지 않고, 소량 사용자 트래픽만 전송
- 99% 사용자 → Blue (작동 확인)
- 1% → Green (새 테스트 코드)
- 결함 발견 → 100% Blue로 되돌리기 전 1% 사용자만 영향
- 빠른 롤백으로 프로덕션 실패 배포 문제 완화

---

### 6. Wordz - 데이터베이스 통합 테스트 → [핵심 개념 3, 6]

**출처**: Lines 651-750

#### 6.1 WordRepository 인터페이스 (Lines 655-661)

**이전 설계** (Lines 656-658):
- Wordz가 추측 대상 단어 저장 장소 필요
- `WordRepository` 인터페이스로 저장 세부사항 격리

```java
public interface WordRepository {
    String fetchWordByNumber(int wordNumber);
}
```

```python
# Python 버전
from typing import Protocol

class WordRepository(Protocol):
    def fetch_word_by_number(self, word_number: int) -> str:
        """단어 번호로 단어 가져오기"""
        ...
```

#### 6.2 통합 테스트 코드 (Lines 666-750)

**구현 연기** (Lines 666-667):
- `WordRepository` 인터페이스 구현은 Chapter 14에서
- 지금은 Integration Test가 어떻게 생겼는지 고수준 조기 확인

**오픈소스 라이브러리** (Lines 669-672):
- **database-rider** (https://database-rider.github.io/getting-started/): 테스트 도구
- **Postgres**: 인기 오픈소스 관계형 데이터베이스

**테스트 코드** (Lines 673-709):

```java
package com.wordz.adapters.db;

import com.github.database.rider.core.api.connection.ConnectionHolder;
import com.github.database.rider.core.api.dataset.DataSet;
import com.github.database.rider.junit5.api.DBRider;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.postgresql.ds.PGSimpleDataSource;
import javax.sql.DataSource;
import static org.assertj.core.api.Assertions.assertThat;

@DBRider  // database-rider 프레임워크 활성화
public class WordRepositoryPostgresTest {
    private DataSource dataSource;

    @BeforeEach
    void beforeEachTest() {
        // Postgres 데이터 소스 설정
        var ds = new PGSimpleDataSource();
        ds.setServerNames(new String[]{"localhost"});
        ds.setDatabaseName("wordzdb");
        ds.setUser("ciuser");
        ds.setPassword("cipassword");
        this.dataSource = ds;
    }

    private final ConnectionHolder connectionHolder = () ->
        dataSource.getConnection();

    @Test
    @DataSet("adapters/data/wordTable.json")  // 테스트 데이터 파일 지정
    public void fetchesWord() {
        // Arrange: WordRepositoryPostgres 객체 생성
        var adapter = new WordRepositoryPostgres(dataSource);

        // Act: 단어 번호 27로 단어 가져오기
        String actual = adapter.fetchWordByNumber(27);

        // Assert: "ARISE" 반환 확인
        assertThat(actual).isEqualTo("ARISE");
    }
}
```

```python
# Python 버전
import pytest
from wordz.adapters.db import WordRepositoryPostgres
from database_rider import DBRider, DataSet

@pytest.fixture
def data_source():
    """Postgres 데이터 소스 설정"""
    return {
        'host': 'localhost',
        'database': 'wordzdb',
        'user': 'ciuser',
        'password': 'cipassword'
    }

@DBRider
class TestWordRepositoryPostgres:
    @DataSet("adapters/data/wordTable.json")
    def test_fetches_word(self, data_source):
        # Arrange
        adapter = WordRepositoryPostgres(data_source)

        # Act
        actual = adapter.fetch_word_by_number(27)

        # Assert
        assert actual == "ARISE"
```

**@DataSet 어노테이션** (Lines 710-726):
- database-rider 테스트 프레임워크 제공
- Arrange 단계 형성
- 테스트 실행 전 데이터베이스에 로드할 알려진 테스트 데이터 파일 지정
- 파일 위치: `src/test/resources` 루트 폴더 아래
- 경로: `src/test/resources/adapters/data/wordTable.json`

**테스트 데이터 파일** (Lines 716-724):

```json
{
  "WORD": [
    {
      "id": 1,
      "number": 27,
      "text": "ARISE"
    }
  ]
}
```

**의미**: `WORD` 테이블에 1행 삽입 (컬럼 값: 1, 27, "ARISE")

**AAA 구조** (Lines 740-749):

1. **Arrange** (Lines 742-744):
   - `WordRepositoryPostgres` 객체 생성 (데이터베이스 코드 포함)
   - `@DataSet` 어노테이션과 함께 작동하여 테스트 실행 전 알려진 데이터를 DB에 넣음

2. **Act** (Lines 746-747):
   - `fetchWordByNumber()` 메서드 호출, 테스트할 숫자 `wordNumber` 전달
   - 숫자는 `wordTable.json` 파일 내용과 일치

3. **Assert** (Lines 749):
   - 예상 단어 "ARISE"가 데이터베이스에서 반환되는지 확인

**결론** (Lines 750):
- Integration Tests는 본질적으로 Unit Tests와 크게 다르지 않음

---

## 요약 및 다음 단계

**출처**: Lines 751-763

### 이 장에서 배운 내용

1. **Test Pyramid**: 테스트 노력을 조직하는 시스템
   - FIRST Unit Tests를 모든 작업의 기초로 확고히 함
   - 다른 테스트 관심사도 무시하지 않음

2. **Integration/Acceptance Testing**: 시스템의 더 많은 부분 테스트

3. **CI/CD**: 소프트웨어 컴포넌트를 함께 가져오고 자주 릴리스 준비 유지

4. **CI 파이프라인**: 전체 빌드 프로세스를 함께 가져오기, CD로 진행 가능

5. **Wordz 진전**: `WordRepositoryPostgres` 어댑터용 Integration Test 작성 → 데이터베이스 코드 자체 작성 준비

### 다음 장 예고 (Chapter 11)

- 프로젝트에서 수동 테스트의 역할
- 가능한 많은 테스트 자동화 → 수동 테스트 역할은 더 이상 거대한 테스트 계획 따르기 아님
- 여전히 매우 가치 있는 수동 테스트
- 역할이 어떻게 변했는가?

---

## Q&A

**출처**: Lines 764-798

### Q1: Test Pyramid가 피라미드 형태로 표현되는 이유는?

**출처**: Lines 767-770

많은 Unit Tests의 넓은 기초를 묘사. 최종 통합 시스템에 더 가까운 근사치를 실행하는 테스트 레이어 표시. 더 높은 통합 수준에서 더 적은 테스트 예상.

### Q2: Unit, Integration, Acceptance Tests 간 트레이드오프는?

**출처**: Lines 772-780

- **Unit Tests**: 빠르고 반복 가능. 외부 시스템 연결 테스트 안 함.
- **Integration Tests**: 더 느림, 때로 반복 불가. 외부 시스템 연결 테스트.
- **Acceptance Tests**: 가장 느림. Flaky할 수 있지만 전체 시스템의 가장 포괄적 테스트 제공.

### Q3: Test Pyramid가 정확성을 보장하는가?

**출처**: Lines 782-784

아니오. 테스트는 결함의 존재만 드러낼 수 있고, 부재는 절대 못 드러냄. 광범위한 테스트의 가치는 프로덕션에 넣는 결함을 얼마나 많이 피하는가에 있음.

### Q4: Test Pyramid는 객체지향 프로그래밍에만 적용되는가?

**출처**: Lines 786-790

아니오. 이 테스트 커버리지 전략은 모든 프로그래밍 패러다임에 적용. 모든 패러다임(OOP, Functional, Procedural, Declarative)으로 코드 작성 가능. 다양한 종류의 테스트는 코드가 외부 시스템 접근하는지 또는 순수 내부 컴포넌트인지에만 의존.

### Q5: 전체 시스템을 테스트하는데 왜 E2E 테스트를 선호하지 않는가?

**출처**: Lines 792-798

E2E 테스트는 느리게 실행. 프로덕션 데이터베이스/웹 서비스 실행 또는 테스트 버전 포함 테스트 환경에 직접 의존. 필요한 네트워크 연결, 데이터베이스 설정 등이 false negative 결과 초래 가능 (환경 때문에 실패, 코드 오류 아님). 이런 이유로 빠르고 반복 가능한 Unit Tests를 최대한 활용하도록 시스템 엔지니어링.

---

## 추가 읽기 자료

**출처**: Lines 799-812

1. **Consumer-Driven Contract Testing 소개**:
   - Pact.io의 인기 오픈소스 계약 테스트 도구 (https://docs.pact.io)
   - 설명 비디오 및 계약 기반 테스트 장점 소개

2. **Database-rider 데이터베이스 테스트 라이브러리**:
   - JUnit5와 작동하는 오픈소스 데이터베이스 통합 테스트 라이브러리
   - https://database-rider.github.io/getting-started/

3. **Modern Software Engineering, Dave Farley, ISBN 978-0137314911**:
   - CD 배경 이유 상세 설명
   - Trunk-based development 같은 기술 관행
   - 적극 추천

4. **Minimum CD**:
   - CD에 필요한 세부사항: https://minimumcd.org/minimumcd/

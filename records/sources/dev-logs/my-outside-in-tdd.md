Outside-In TDD 실행 가이드 (목차 제안)

  1. 개요

  - 1.1 Outside-In TDD란?
  - 1.2 테스트 레벨 (E2E → Integration → Unit)
  - 1.3 진행 원칙

  2. 전체 진행 단계

  2.1 Phase 단위 진행 흐름

  Phase (예: E2E 레벨 확장)
  ├─ Step 1: 사용자 스토리 & 환경 설정 제안
  ├─ Step 2: 통합 단위 분리 및 조율
  ├─ Step 3: 개별 테스트 상세 제안
  └─ Step 4: TDD 사이클 (RED → GREEN → REFACTOR)

  2.2 Step별 상세 설명

  ---
  3. Step 1: 사용자 스토리 & 환경 설정 제안

  3.1 목적

  - 전체 기능 범위 파악
  - 공통 환경 설정 사전 합의
  - 테스트 케이스 전체 목록 가시화

  3.2 제안 형식

  ## [Phase X] 레벨 - 사용자 스토리 & 환경 설정

  ### 사용자 스토리
  - Story 1: [스토리 설명]
  - Story 2: [스토리 설명]

  ### 공통 환경 설정

  **환경변수**:
    - (필요한 환경변수 목록)

  **각 테스트 전 (Setup)**:
    - (Setup 작업 목록)

  **각 테스트 후 (Teardown)**:
    - (Teardown 작업 목록)

  ### 테스트 케이스 전체 목록
  1. [케이스명] 🟢/🟡/🔴 Happy/Edge/Error 🟣/🟠/🔵 E2E/Int/Unit
  2. [케이스명] 🟢/🟡/🔴 Happy/Edge/Error 🟣/🟠/🔵 E2E/Int/Unit

  3.3 조율 포인트

  - 환경 설정 확인/수정
  - 테스트 케이스 추가/삭제/수정
  - 우선순위 조정

  ---
  4. Step 2: 통합 단위 분리 및 조율

  4.1 목적

  - 불필요한 Setup 제거
  - 테스트 독립성 확보
  - 테스트 실행 속도 최적화

  4.2 분리 기준

  - 환경 설정 기준: 필요한 fixture/의존성
  - 외부 시스템 기준: DB, SMTP, API 등
  - 도메인 경계 기준: 비즈니스 로직 단위

  4.3 분리 예시

  Integration 테스트 (6개)
  ├─ test_shipment_db.py (4개) - DB만 필요
  │   ├─ Fixture: db_session, test_data
  │   └─ 불필요: smtp_mock
  └─ test_shipment_email.py (3개) - SMTP만 필요
      ├─ Fixture: smtp_mock
      └─ 불필요: db_session (또는 최소 사용)

  4.4 제안 형식

  ## 통합 단위 분리

  ### 단위 1: [이름] (예: DB Integration)
  - **테스트 파일**: `test_xxx_db.py`
  - **필요 Fixture**: db_session, test_data
  - **테스트 개수**: N개
  - **테스트 목록**: [간단한 목록]

  ### 단위 2: [이름] (예: SMTP Integration)
  - **테스트 파일**: `test_xxx_email.py`
  - **필요 Fixture**: smtp_mock
  - **테스트 개수**: N개
  - **테스트 목록**: [간단한 목록]

  4.5 조율 포인트

  - 분리 단위 확인/수정
  - 각 단위별 진행 순서 결정

  ---
  5. Step 3: 개별 테스트 상세 제안

  5.1 목적

  - 구체적인 Given/When/Then 명시
  - 구현 방향 사전 합의
  - 예상 코드 위치 파악

  5.2 제안 형식

  ### 테스트: [테스트명] 🟢 Happy 🟠 Integration

  **파일**: `tests/integration/test_xxx.py`
  **구현 위치**: `backend/services/xxx.py`

  **Given**:
    - [초기 상태/데이터]
    - [Mock 설정] (필요 시)

  **When**:
    - [실행할 함수/API 호출]
    - [파라미터]

  **Then**:
    - [예상 결과 1]
    - [예상 결과 2]
    - [검증할 부작용] (DB 저장, 이메일 발송 등)

  5.3 조율 포인트

  - Given/When/Then 확인/수정
  - 구현 위치 합의
  - 동의 후 TDD 사이클 시작

  ---
  6. Step 4: TDD 사이클 (RED → GREEN → REFACTOR)

  6.1 RED: 실패하는 테스트 작성

  - 테스트 코드 작성
  - 테스트 실행 → 실패 확인
  - 실패 이유 확인 (예상한 이유인지 검증)

  6.2 GREEN: 최소 구현

  - 테스트만 통과하도록 최소 구현
  - 과도한 일반화 금지
  - 하드코딩 허용 (다음 테스트가 강제함)

  6.3 REFACTOR: 리팩터링 (선택)

  - 중복 제거
  - 가독성 개선
  - 테스트는 여전히 GREEN 유지

  6.4 완료 확인

  - 모든 테스트 통과
  - 다음 테스트로 이동

  ---
  7. 테스트 명명 규칙

  7.1 테스트 함수명: When-Then 패턴

  test_when_[조건/행위]_then_[결과]

  예시:
  # Integration - DB
  test_when_updating_to_shipped_then_persists_tracking_and_timestamp
  test_when_updating_to_delivered_then_records_delivered_timestamp
  test_when_querying_nonexistent_order_then_returns_none

  # Integration - SMTP
  test_when_sending_shipment_email_then_smtp_receives_message
  test_when_smtp_fails_then_retries_three_times

  # Unit
  test_when_transitioning_preparing_to_delivered_then_raises_error
  test_when_shipped_without_tracking_then_raises_validation_error

  7.2 테스트 케이스 이모지 표기

  - 🟢 Happy Path: 정상 시나리오
  - 🟡 Edge Case: 경계값, 특수 상황
  - 🔴 Error Case: 오류 시나리오
  - 🟣 E2E: End-to-End 테스트
  - 🟠 Integration: 통합 테스트
  - 🔵 Unit: 단위 테스트

  7.3 파일명 규칙

  tests/
  ├─ e2e/
  │   └─ test_[feature]_flow.py
  ├─ integration/
  │   ├─ test_[feature]_db.py
  │   ├─ test_[feature]_email.py
  │   └─ test_[feature]_api.py
  └─ unit/
      └─ test_[model/service]_logic.py

  ---
  8. Fixture 설계 원칙

  8.1 Scope 결정

  - session: 전체 테스트 세션 동안 1회 (DB 연결)
  - module: 모듈 단위 1회
  - function: 각 테스트마다 (기본값, 독립성 보장)

  8.2 의존성 최소화

  - 각 테스트는 필요한 fixture만 사용
  - 불필요한 fixture 의존 금지

  8.3 Fixture 위치

  - tests/conftest.py: 전역 fixture
  - tests/e2e/conftest.py: E2E 전용
  - tests/integration/conftest.py: Integration 전용

  ---
  9. 체크리스트

  9.1 Phase 시작 전

  - 사용자 스토리 명확한가?
  - 환경 설정 합의했는가?
  - 테스트 케이스 목록 조율 완료했는가?

  9.2 통합 단위 분리 시

  - 분리 기준이 명확한가?
  - 각 단위의 fixture 의존성이 최소화되었는가?
  - 파일명이 규칙에 맞는가?

  9.3 각 테스트 진행 시

  - RED 단계를 확인했는가?
  - 예상한 이유로 실패하는가?
  - 최소 구현만 했는가? (과도한 일반화 없는가?)
  - GREEN 상태에서 리팩터링 했는가?

  9.4 Phase 완료 시

  - 모든 테스트 통과하는가?
  - 커버리지 목표 달성했는가?
  - 문서 업데이트 완료했는가?

  ---
  10. 예시: Phase 2-2 Integration 레벨

  10.1 Step 1: 사용자 스토리 & 환경 설정

  ## 사용자 스토리
  - 배송 상태 변경 시 DB에 영속화되어야 함
  - 배송 상태 변경 시 이메일이 발송되어야 함
  - 이메일 발송 실패 시에도 상태 변경은 성공해야 함

  ## 환경 설정
  - DB: TEST_DATABASE_URL
  - SMTP: Mock SMTP (localhost:1025)

  ## 테스트 케이스 목록 (6개)
  1. 배송 상태 SHIPPED 변경 시 DB 저장 🟢 Happy 🟠 Integration
  2. 배송 상태 DELIVERED 변경 시 타임스탬프 기록 🟢 Happy 🟠 Integration
  ...

  10.2 Step 2: 통합 단위 분리

  ### 단위 1: DB Integration (4개)
  - 파일: `test_shipment_db.py`
  - Fixture: db_session, test_data

  ### 단위 2: SMTP Integration (3개)
  - 파일: `test_shipment_email.py`
  - Fixture: smtp_mock

  10.3 Step 3: 개별 테스트 상세

  ### test_when_updating_to_shipped_then_persists_tracking_and_timestamp

  Given: PREPARING 상태 Shipment
  When: update_shipment_status(db_session, order_id, "SHIPPED", ...)
  Then: 
    - DB에서 조회 시 status=SHIPPED
    - tracking_number, courier 저장됨
    - shipped_at IS NOT NULL

  10.4 Step 4: TDD 사이클

  - RED: ImportError 확인
  - GREEN: update_shipment_status() 함수 구현
  - REFACTOR: (필요 시)

  ---
  부록

  A. 용어 정리

  - Walking Skeleton: 최소 기능만 동작하는 골격
  - Test Double: Mock, Stub, Spy 등 테스트 대역
  - Fixture: 테스트 사전 준비 데이터/환경

  B. 참고 자료

  - Growing Object-Oriented Software, Guided by Tests
  - Test-Driven Development: By Example (Kent Beck)
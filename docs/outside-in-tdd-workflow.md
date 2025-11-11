# Outside-In TDD 워크플로우

## 핵심 원칙

### 1. Acceptance Test First (전체 흐름 검증)
- **목표**: 하나의 사용자 시나리오를 End-to-End로 검증
- **범위**: UI → API → Service → Domain → DB (모든 계층 포함)
- **특징**: 처음에는 실패하는 것이 정상

### 2. Walking Skeleton (최소 구현으로 통과)
- **목표**: Acceptance Test를 **통과만** 하게 만들기
- **방법**:
  - 하드코딩, Fake 구현, 최소한의 코드
  - 복잡한 로직 없이 전체 연결만 확인
- **결과**: "끝에서 끝까지 동작하는" 뼈대 완성

### 3. Outside-In 순서 (바깥→안쪽, 기능별 완성)
- **핵심**: Acceptance Test 하나당 Integration → Unit까지 완성
- **순서**:
  ```
  Acceptance Test 1개 작성
    ↓ Walking Skeleton
  Integration 레벨 (해당 기능)
    ↓
  Unit 레벨 (해당 기능)
    ↓
  다음 Acceptance Test
  ```
- **가로 확장 ❌**: 모든 E2E → 모든 Integration → 모든 Unit
- **세로 완성 ✅**: 기능1 완성 → 기능2 완성 → 기능3 완성

### 4. 테스트 피라미드와 독립성

**Test Pyramid 원칙:**
```
        /\
       /E2E\      ← 적게 (느림, 비쌈, 깨지기 쉬움)
      /------\
     /  Int  \    ← 적당히 (중간 속도, 중간 비용)
    /----------\
   /   Unit    \  ← 많이 (빠름, 저렴, 안정적)
  /--------------\
```

**각 레벨의 특성과 목적:**

| 레벨 | 목적 | 속도 | 범위 | 실패 원인 파악 |
|------|------|------|------|---------------|
| **Unit** | 도메인 로직, 비즈니스 규칙 검증 | ⚡ 매우 빠름 | 함수/클래스 | 쉬움 |
| **Integration** | 외부 시스템 연동 검증 (DB, API, Email) | 🐢 느림 | 연동 계층 | 중간 |
| **E2E** | 사용자 시나리오, 전체 흐름 검증 | 🐌 매우 느림 | 전체 시스템 | 어려움 |

**독립성 원칙:**
- 각 테스트는 **독립적으로 실행 가능**해야 함
- 상위 테스트 없이도 하위 테스트만으로 동작을 이해할 수 있어야 함
- 한 레벨의 테스트가 실패해도 다른 레벨은 정상 실행되어야 함

**FIRST 원칙:**
- **Fast**: 빠르게 실행 (특히 Unit)
- **Isolated**: 독립적 (다른 테스트에 영향 없음)
- **Repeatable**: 반복 가능 (같은 결과)
- **Self-validating**: 자동 검증 (수동 확인 불필요)
- **Timely**: 적시에 작성 (구현 전 or 직후)

---

## 전체 개발 흐름 (기능별)

**한 기능당 다음 순서로 완성**:

```
Phase 1: 첫 번째 기능 (Walking Skeleton)
├─ 1. Acceptance Test 작성 (RED)
├─ 2. 최소 구현으로 통과 (GREEN)
└─ ✅ 첫 기능 뼈대 완성

Phase 2: 첫 번째 기능 확장
├─ 3. Integration 레벨 (연동 요소별로 분리)
│   ├─ DB 연동 검증 → tests/integration/test_[기능]_db.py
│   ├─ Email/메시징 연동 검증 → tests/integration/test_[기능]_email.py
│   ├─ 외부 API 연동 검증 → tests/integration/test_[기능]_api.py
│   └─ 각 테스트마다 RED → GREEN → REFACTOR
├─ 4. Unit 레벨
│   ├─ 도메인 로직, 비즈니스 규칙 검증
│   └─ 각 테스트마다 RED → GREEN → REFACTOR
└─ ✅ 첫 기능 완전 완성

Phase 3: 두 번째 기능 시작
├─ 5. 다음 Acceptance Test 작성 (E2E 확장)
├─ 6. Integration 레벨 (해당 기능)
├─ 7. Unit 레벨 (해당 기능)
└─ ✅ 두 번째 기능 완성

... 반복
```

---

## Integration 테스트 파일 구조

**연동 요소별로 파일 분리:**

Integration 테스트는 Acceptance Test 단위가 아니라 **연동 요소별**로 파일을 구성:

```
tests/integration/
├── test_[기능]_db.py          # DB 연동만 검증
├── test_[기능]_email.py       # Email/메시징 연동만 검증
├── test_[기능]_api.py         # 외부 API 연동만 검증
└── test_[기능]_cache.py       # 캐시 연동만 검증
```

**예시: 배송(shipment) 기능**

```
tests/integration/
├── test_shipment_db.py        # DB 영속성 검증
│   ├─ test_when_updating_to_shipped_then_persists_tracking_and_timestamp
│   └─ test_when_updating_to_delivered_then_records_delivered_timestamp
│
└── test_shipment_email.py     # SMTP 연동 검증
    ├─ test_when_sending_shipment_email_then_smtp_receives_message
    └─ test_when_sending_delivery_email_then_smtp_receives_completion_message
```

**장점:**
- ✅ 관심사 분리: 각 파일이 하나의 연동만 책임
- ✅ 독립적 실행: DB 테스트만 실행하거나 Email 테스트만 실행 가능
- ✅ 명확한 실패 원인: 어떤 연동이 문제인지 파일명으로 즉시 파악
- ✅ 유지보수 용이: 연동 방식 변경 시 해당 파일만 수정

---

## 각 테스트 레벨별 작업 진행 방식

각 레벨(E2E/Integration/Unit)은 다음 순서로 진행:

### Step 1: 환경 설정 & 테스트 케이스 목록 제안

**AI가 제안**:
```markdown
## [테스트 레벨 (E2E/Integration/Unit)] - 공통 환경 설정 & 테스트 케이스 목록

### 공통 환경 설정

**환경변수**:
  - (필요한 환경변수 목록)

**각 테스트 전 (Setup)**:
  - (Setup 작업 목록)

**각 테스트 후 (Teardown)**:
  - (Teardown 작업 목록)

---

### 테스트 케이스 목록

1. [케이스명] 🟢/🟡/🔴 Happy/Edge/Error 🟣/🟠/🔵 E2E/Int/Unit
2. [케이스명] 🟢/🟡/🔴 Happy/Edge/Error 🟣/🟠/🔵 E2E/Int/Unit
...
```

**사용자 조율**:
- 환경 설정 확인/수정 요청
- 테스트 케이스 추가/삭제/수정 요청
- "동의" → 다음 단계 진행

---

### Step 2: 개별 테스트 케이스 상세 제안 (순서대로)

**AI가 제안**:
```markdown
테스트 케이스명: [케이스명] 🟢 Happy 🟣 E2E

구현 코드: [파일경로]#[클래스/함수명]

Given:
  - [초기 상태/데이터]
  - [TestDouble.메서드()] ([Double 유형]) → [반환값]

When:
  - [실행 동작 + 파라미터]

Then:
  - [예상 결과] ← [Spec: 관련 요구사항]
  - [검증할 호출/상태 변경]
  - [기법: 적용 지점]
```

**사용자 조율**:
- Given/When/Then 확인/수정 요청
- "동의" → 구현 진행

---

### Step 3: 구현 (RED → GREEN → REFACTOR)

**AI가 수행**:
1. **RED**: 테스트 코드 작성 → 실행 → 실패 확인
2. **GREEN**: 최소 구현 → 테스트 통과
3. **REFACTOR**: 코드 정리 (필요시)
4. **완료 보고**: 테스트 통과 결과 제시

---

### Step 4: 다음 테스트로 이동

- 현재 테스트 완료 (GREEN 상태) 확인
- Step 2로 돌아가서 다음 테스트 진행
- 모든 테스트 완료 시 다음 Phase로 이동

## 진행 시 주의사항

1. **한 번에 하나의 테스트만**:
   - 테스트 작성 → RED 확인 → GREEN 구현 → 다음
   - 여러 테스트를 동시에 작성하지 말 것

2. **RED 단계 확인**:
   - 테스트 작성 후 반드시 실패하는지 확인
   - 예상한 이유로 실패하는지 확인 (에러 메시지 체크)

3. **최소 구현**:
   - GREEN 단계에서는 테스트만 통과하도록 최소한으로 구현
   - 과도한 일반화 금지

4. **리팩터링은 GREEN 이후**:
   - 테스트가 통과한 상태에서만 리팩터링
   - 리팩터링 중에는 기능 추가 금지

5. **커밋 타이밍**:
   - 각 테스트가 GREEN 상태에서 커밋
   - 리팩터링 완료 후 커밋
   - RED 상태에서는 커밋 금지

6. **기능별로 세로 완성**:
   - 하나의 Acceptance Test에 대해 Integration → Unit까지 완성
   - 모든 E2E를 먼저 하지 말 것
   - 기능 하나를 깊이 파고들어 완성

7. **Integration 테스트는 연동 요소별로 분리**:
   - Acceptance Test 단위로 Integration 파일을 만들지 말 것
   - DB, Email, API 등 연동 요소별로 파일 분리
   - 예: `test_shipment_db.py`, `test_shipment_email.py`
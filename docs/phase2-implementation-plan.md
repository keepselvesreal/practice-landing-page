# Phase 2: Outside-In 리팩터링 계획

**작성일**: 2025-11-11
**세션**: after-commit-3173652 이후
**선행 작업**: Phase 1 Walking Skeleton 완료 (E2E 테스트 1개 통과)

---

## 목표

Walking Skeleton을 Outside-In 방식으로 리팩터링하여 완전하고 견고한 배송 추적 시스템 구축

**핵심 원칙**:
- 바깥쪽(E2E) → 안쪽(Unit) 순서로 구현
- 각 계층마다 RED → GREEN → REFACTOR 사이클
- 한 번에 하나의 테스트에 집중

---

## 전체 진행 순서

```
Phase 2-1: E2E 레벨 확장
├─ [환경 검토 + 추가 테스트 목록] 제안 → 승인
└─ 각 테스트 순서대로: 상세 제안 → 구현 → 다음

Phase 2-2: Integration 레벨 확장
├─ [환경 검토 + 테스트 목록] 제안 → 승인
└─ 각 테스트 순서대로: 상세 제안 → 구현 → 다음

Phase 2-3: Unit 레벨 확장
├─ [환경 검토 + 테스트 목록] 제안 → 승인
└─ 각 테스트 순서대로: 상세 제안 → 구현 → 다음
```

---

## 작업 진행 방식

각 Phase는 다음 순서로 진행:

### Step 1: 환경 설정 & 테스트 케이스 목록 제안

**AI가 제안**:
```markdown
## [Phase 2-X] 레벨 - 공통 환경 설정 & 테스트 케이스 목록

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

---

## Phase 2-1: E2E 레벨 확장

### 목표
관리자 UI의 모든 사용자 시나리오 검증 (Happy/Edge/Error 케이스)

### 공통 환경 설정 (Phase 1과 동일)

**환경변수**: `.env` (이미 설정됨)
```bash
DATABASE_URL=postgresql://nadle:1089@localhost:5432/k_beauty_landing_page
TEST_DATABASE_URL=postgresql://nadle:1089@localhost:5432/test_landing_page
ENCRYPTION_KEY=2I8QsWMSdxbySW41U5d1hAxuoH2yG0pyK7HoFR0qMpM=
ADMIN_API_KEY=VjAkut2ky5hfGIrJ4TQwc_JqYc3oDBCt5MeyDC4tu74
```

**각 테스트 전 (Setup)**:
- 테스트 DB 초기화
- 테스트 데이터 생성 (Product, Order, Shipment)
- FastAPI 테스트 서버 시작

**각 테스트 후 (Teardown)**:
- DB 트랜잭션 롤백
- 테스트 서버 종료

---

### 추가 테스트 케이스 목록

**파일**: `tests/e2e/test_admin_shipment.py`

#### ✅ 완료된 테스트
1. **관리자가_배송상태를_SHIPPED로_변경하면_발송이메일이_발송된다** 🟢 Happy 🟣 E2E

#### 🔲 추가 필요한 테스트

2. **운송장_번호_없이_SHIPPED로_변경하면_에러_메시지가_표시된다** 🔴 Error 🟣 E2E
   - Given: PREPARING 상태 주문
   - When: 운송장 번호 빈칸, status=SHIPPED
   - Then: "운송장 번호를 입력하세요" 에러 메시지

3. **택배사_선택_없이_SHIPPED로_변경하면_에러_메시지가_표시된다** 🔴 Error 🟣 E2E
   - Given: PREPARING 상태 주문
   - When: 택배사 미선택, status=SHIPPED
   - Then: "택배사를 선택하세요" 에러 메시지

4. **PREPARING에서_DELIVERED로_직접_변경하면_에러_메시지가_표시된다** 🔴 Error 🟣 E2E
   - Given: PREPARING 상태 주문
   - When: status=DELIVERED (단계 건너뛰기)
   - Then: "PREPARING → SHIPPED 순서로 변경하세요" 에러 메시지

5. **SHIPPED에서_DELIVERED로_변경하면_배송완료_이메일이_발송된다** 🟢 Happy 🟣 E2E
   - Given: SHIPPED 상태 주문
   - When: status=DELIVERED
   - Then: 성공 메시지 + "배송이 완료되었습니다" 이메일 (콘솔 확인)

6. **SHIPPED_상태에서_PREPARING으로_되돌리기_시도하면_에러가_표시된다** 🔴 Error 🟣 E2E
   - Given: SHIPPED 상태 주문
   - When: status=PREPARING (역방향 전환)
   - Then: "이전 상태로 되돌릴 수 없습니다" 에러 메시지

7. **존재하지_않는_주문_ID로_접근하면_404_에러가_표시된다** 🔴 Error 🟣 E2E
   - Given: DB에 없는 주문
   - When: POST /admin/shipments/99999
   - Then: "주문을 찾을 수 없습니다" 에러 페이지

---

### 구현 순서

각 테스트를 순서대로 진행:
1. 테스트 케이스 상세 제안 (Given/When/Then) → 승인
2. 테스트 코드 작성 → RED 확인
3. 최소 구현으로 GREEN
4. 리팩터링
5. 다음 테스트로 이동

**예상 시간**: 2-3시간

---

## Phase 2-2: Integration 레벨 확장

### 목표
외부 시스템(DB, Email) 연동 검증

### 공통 환경 설정

**환경변수**: Phase 1과 동일

**각 테스트 전 (Setup)**:
- 테스트 DB 초기화
- Mock SMTP 서버 시작 (aiosmtpd)
- 테스트 데이터 생성

**각 테스트 후 (Teardown)**:
- DB 롤백
- Mock SMTP 서버 종료

---

### 테스트 케이스 목록

**파일**: `tests/integration/test_shipment_integration.py`

1. **배송_상태가_SHIPPED로_변경되면_DB에_저장된다** 🟢 Happy 🟠 Integration
   - Given: PREPARING Shipment
   - When: update_status("SHIPPED", tracking="123", courier="LBC")
   - Then: DB에서 조회 시 status=SHIPPED, tracking=123, shipped_at IS NOT NULL

2. **배송_상태가_DELIVERED로_변경되면_delivered_at이_기록된다** 🟢 Happy 🟠 Integration
   - Given: SHIPPED Shipment
   - When: update_status("DELIVERED")
   - Then: DB에서 delivered_at IS NOT NULL

3. **SHIPPED_전환_시_발송_이메일이_실제로_발송된다** 🟢 Happy 🟠 Integration
   - Given: PREPARING Shipment
   - When: update_status("SHIPPED", tracking="123", courier="LBC")
   - Then: Mock SMTP에 이메일 1개 수신됨, 운송장 번호 포함

4. **DELIVERED_전환_시_배송완료_이메일이_실제로_발송된다** 🟢 Happy 🟠 Integration
   - Given: SHIPPED Shipment
   - When: update_status("DELIVERED")
   - Then: Mock SMTP에 이메일 1개 수신됨, "배송 완료" 포함

5. **이메일_발송_실패_시_상태_변경은_성공한다** 🔴 Error 🟠 Integration
   - Given: PREPARING Shipment, Mock SMTP 장애
   - When: update_status("SHIPPED")
   - Then: DB에 SHIPPED 저장됨, 에러 로그 기록됨

6. **이메일_발송_3회_재시도_후_실패하면_CRITICAL_로그가_기록된다** 🔴 Error 🟠 Integration
   - Given: Mock SMTP 항상 실패
   - When: update_status("SHIPPED")
   - Then: 재시도 3회, CRITICAL 로그 "SMTP FAILURE" 포함

---

### 필요한 구현

#### Mock SMTP 서버 설정

**파일**: `tests/conftest.py` 추가

```python
import asyncio
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Message

class MockSMTPHandler:
    def __init__(self):
        self.messages = []

    def handle_message(self, message):
        self.messages.append({
            "from": message["from"],
            "to": message["to"],
            "subject": message["subject"],
            "body": message.get_payload()
        })

@pytest.fixture
def smtp_mock():
    handler = MockSMTPHandler()
    controller = Controller(handler, hostname="localhost", port=1025)
    controller.start()

    yield handler

    controller.stop()
```

#### 이메일 서비스 리팩터링

**파일**: `backend/services/email.py` 수정

```python
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def send_email_with_retry(to: str, subject: str, html: str):
    """3회 재시도 (2초, 4초, 8초 대기)"""
    try:
        # 실제 SMTP 발송 로직
        smtp.send(to, subject, html)
        logger.info(f"Email sent to {to}: {subject}")
    except Exception as e:
        logger.error(f"Email send failed: {e}")
        raise

def send_shipment_email(shipment):
    """배송 이메일 발송 (재시도 포함)"""
    try:
        send_email_with_retry(...)
    except Exception as e:
        logger.critical(
            f"SMTP FAILURE: Failed to send shipment email after 3 retries. "
            f"Order: {shipment.order.order_number}, Error: {e}",
            extra={"order_id": shipment.order_id}
        )
        # 상태 변경은 이미 완료됨
```

**예상 시간**: 2-3시간

---

## Phase 2-3: Unit 레벨 확장

### 목표
도메인 로직 검증 (상태 전환 규칙, 비즈니스 규칙)

### 공통 환경 설정

**환경변수**: 없음 (순수 도메인 로직)

**각 테스트 전 (Setup)**:
- Shipment 인스턴스 생성 (DB 없이)
- Mock 객체 준비

**각 테스트 후 (Teardown)**:
- 없음

---

### 테스트 케이스 목록

**파일**: `tests/unit/test_shipment_model.py`

1. **PREPARING에서_SHIPPED로_전환_가능하다** 🟢 Happy 🔵 Unit
   - Given: Shipment(status=PREPARING)
   - When: update_status("SHIPPED", tracking="123", courier="LBC")
   - Then: status=SHIPPED, tracking=123, courier="LBC", shipped_at IS NOT NULL

2. **SHIPPED에서_DELIVERED로_전환_가능하다** 🟢 Happy 🔵 Unit
   - Given: Shipment(status=SHIPPED)
   - When: update_status("DELIVERED")
   - Then: status=DELIVERED, delivered_at IS NOT NULL

3. **PREPARING에서_DELIVERED로_직접_전환_불가능하다** 🔴 Error 🔵 Unit
   - Given: Shipment(status=PREPARING)
   - When: update_status("DELIVERED")
   - Then: InvalidTransitionError 발생

4. **SHIPPED에서_PREPARING으로_역방향_전환_불가능하다** 🔴 Error 🔵 Unit
   - Given: Shipment(status=SHIPPED)
   - When: update_status("PREPARING")
   - Then: InvalidTransitionError 발생

5. **DELIVERED_상태에서는_더_이상_전환_불가능하다** 🔴 Error 🔵 Unit
   - Given: Shipment(status=DELIVERED)
   - When: update_status("SHIPPED")
   - Then: InvalidTransitionError 발생

6. **SHIPPED_전환_시_운송장_번호_필수이다** 🔴 Error 🔵 Unit
   - Given: Shipment(status=PREPARING)
   - When: update_status("SHIPPED", tracking=None)
   - Then: ValueError("운송장 번호 필수") 발생

7. **SHIPPED_전환_시_택배사_필수이다** 🔴 Error 🔵 Unit
   - Given: Shipment(status=PREPARING)
   - When: update_status("SHIPPED", courier=None)
   - Then: ValueError("택배사 필수") 발생

8. **SHIPPED_전환_시_이메일_이벤트가_발행된다** 🟢 Happy 🔵 Unit
   - Given: Shipment(status=PREPARING)
   - When: events = update_status("SHIPPED", tracking="123", courier="LBC")
   - Then: len(events) == 1, events[0].type == "shipment_sent"

9. **DELIVERED_전환_시_이메일_이벤트가_발행된다** 🟢 Happy 🔵 Unit
   - Given: Shipment(status=SHIPPED)
   - When: events = update_status("DELIVERED")
   - Then: len(events) == 1, events[0].type == "delivery_completed"

---

### 필요한 구현

#### Shipment 모델 리팩터링

**파일**: `backend/models/db/shipment.py`

```python
from enum import Enum
from datetime import datetime

class ShipmentStatus(str, Enum):
    PREPARING = "PREPARING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"

class InvalidTransitionError(Exception):
    """잘못된 상태 전환 예외"""
    pass

class ShipmentDB(Base):
    __tablename__ = "shipments"

    # ... (기존 필드)

    # 상태 전환 규칙
    VALID_TRANSITIONS = {
        ShipmentStatus.PREPARING: [ShipmentStatus.SHIPPED],
        ShipmentStatus.SHIPPED: [ShipmentStatus.DELIVERED],
        ShipmentStatus.DELIVERED: []
    }

    def update_status(
        self,
        new_status: str,
        tracking_number: str | None = None,
        courier: str | None = None
    ) -> list:
        """
        배송 상태 업데이트

        Returns:
            list: 발생한 이벤트 목록
        """
        new_status_enum = ShipmentStatus(new_status)

        # 1. 상태 전환 규칙 검증
        if new_status_enum not in self.VALID_TRANSITIONS[self.shipping_status]:
            raise InvalidTransitionError(
                f"{self.shipping_status} → {new_status} 전환은 불가능합니다. "
                f"허용: {[s.value for s in self.VALID_TRANSITIONS[self.shipping_status]]}"
            )

        # 2. SHIPPED 필수 필드 검증
        if new_status_enum == ShipmentStatus.SHIPPED:
            if not tracking_number:
                raise ValueError("운송장 번호를 입력하세요")
            if not courier:
                raise ValueError("택배사를 선택하세요")

        # 3. 상태 업데이트
        self.shipping_status = new_status_enum

        if tracking_number:
            self.tracking_number = tracking_number
        if courier:
            self.courier = courier

        # 4. 타임스탬프 기록
        events = []
        if new_status_enum == ShipmentStatus.SHIPPED:
            self.shipped_at = datetime.now()
            events.append(ShipmentEvent("shipment_sent", self))
        elif new_status_enum == ShipmentStatus.DELIVERED:
            self.delivered_at = datetime.now()
            events.append(ShipmentEvent("delivery_completed", self))

        return events

class ShipmentEvent:
    """이벤트 객체 (이메일 발송 트리거)"""
    def __init__(self, event_type: str, shipment: ShipmentDB):
        self.type = event_type
        self.shipment = shipment
```

**예상 시간**: 2-3시간

---

## 리팩터링 작업 (선택)

Phase 2 테스트 통과 후 추가 개선 고려

### 1. Service 계층 분리

**파일**: `backend/services/shipment_service.py` (신규)

```python
class ShipmentService:
    def __init__(
        self,
        shipment_repo: ShipmentRepository,
        email_service: EmailService
    ):
        self.repo = shipment_repo
        self.email_service = email_service

    def update_shipment_status(
        self,
        order_id: int,
        new_status: str,
        tracking_number: str | None = None,
        courier: str | None = None
    ):
        # 1. Shipment 조회
        shipment = self.repo.get_by_order_id(order_id)
        if not shipment:
            raise HTTPException(404, "배송 정보를 찾을 수 없습니다")

        # 2. 상태 업데이트 (도메인 로직)
        events = shipment.update_status(new_status, tracking_number, courier)

        # 3. 이메일 발송 (이벤트 기반)
        for event in events:
            if event.type == "shipment_sent":
                self.email_service.send_shipment_email(shipment)
            elif event.type == "delivery_completed":
                self.email_service.send_delivery_email(shipment)

        # 4. 저장
        self.repo.save(shipment)

        return shipment
```

### 2. Repository 패턴

**파일**: `backend/repositories/shipment_repository.py` (신규)

```python
class ShipmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_order_id(self, order_id: int) -> ShipmentDB | None:
        return self.db.query(ShipmentDB).filter_by(order_id=order_id).first()

    def save(self, shipment: ShipmentDB):
        self.db.add(shipment)
        self.db.commit()
        self.db.refresh(shipment)
        return shipment
```

### 3. Admin 라우터 간소화

**파일**: `backend/api/admin.py` 수정

```python
@router.post("/shipments/{order_id}")
def update_shipment(
    order_id: int,
    request: UpdateShipmentRequest,
    service: ShipmentService = Depends(get_shipment_service)
):
    """배송 상태 업데이트 (Service 계층 위임)"""
    try:
        shipment = service.update_shipment_status(
            order_id,
            request.status,
            request.tracking_number,
            request.courier
        )
        return RedirectResponse(
            url="/admin/shipments?success=저장되었습니다",
            status_code=303
        )
    except InvalidTransitionError as e:
        return RedirectResponse(
            url=f"/admin/shipments?error={str(e)}",
            status_code=303
        )
    except ValueError as e:
        return RedirectResponse(
            url=f"/admin/shipments?error={str(e)}",
            status_code=303
        )
```

**예상 시간**: 2-3시간

---

## 전체 예상 시간

- Phase 2-1 (E2E 확장): 2-3시간
- Phase 2-2 (Integration 확장): 2-3시간
- Phase 2-3 (Unit 확장): 2-3시간
- 리팩터링 (선택): 2-3시간

**총 예상 시간**: 6-12시간

---

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

---

## 다음 세션 시작 시

### 1. Phase 1 완료 확인

```bash
uv run pytest tests/e2e/test_admin_shipment.py::test_관리자가_배송상태를_SHIPPED로_변경하면_발송이메일이_발송된다 -v
```

**통과 확인**: `PASSED ✅`

---

### 2. Phase 2-1 시작 (권장 프롬프트)

```
Phase 2-1 E2E 레벨 확장을 시작하려고 해.

`docs/phase2-implementation-plan.md`의 "작업 진행 방식"과 "Phase 2-1: E2E 레벨 확장" 섹션을 참고해서 진행해줘.

Step 1부터 시작:
- 공통 환경 설정 검토 (Phase 1과 동일한지 확인)
- 추가 테스트 케이스 목록 제안 (문서에 있는 6개)

제안 후 내가 확인하고 동의하면, 첫 번째 테스트부터 순서대로 Given/When/Then 제안해줘.
```

---

### 3. 진행 흐름 (요약)

```
Step 1: [환경 + 테스트 목록] 제안
        ↓ (사용자 조율)
Step 2: 첫 번째 테스트 [Given/When/Then] 상세 제안
        ↓ (사용자 동의)
Step 3: 구현 (RED → GREEN → REFACTOR)
        ↓ (테스트 통과)
Step 4: 다음 테스트로 이동
        ↓
      반복 (모든 테스트 완료까지)
        ↓
      Phase 2-2로 이동
```

---

### 4. 진행 중 참고 문서

- **TDD 방법론**: `docs/outside-in-tdd-guide.md`
- **DB 스키마**: `docs/02-database-schema.md`
- **상태 관리**: `docs/04-state-management.md`
- **Phase 2 계획**: `docs/phase2-implementation-plan.md` (이 문서)

---

### 5. 각 Phase 시작 시 프롬프트 템플릿

**Phase 2-2 시작 시**:
```
Phase 2-2 Integration 레벨 확장을 시작해.
`docs/phase2-implementation-plan.md`의 "Phase 2-2" 섹션 참고해서
Step 1부터 진행해줘 (환경 설정 + 테스트 목록 제안).
```

**Phase 2-3 시작 시**:
```
Phase 2-3 Unit 레벨 확장을 시작해.
`docs/phase2-implementation-plan.md`의 "Phase 2-3" 섹션 참고해서
Step 1부터 진행해줘 (환경 설정 + 테스트 목록 제안).
```

---

## 체크리스트

Phase 2 완료 조건:
- [ ] E2E 테스트 7개 통과
- [ ] Integration 테스트 6개 통과
- [ ] Unit 테스트 9개 통과
- [ ] 모든 테스트 GREEN 상태
- [ ] 코드 커버리지 80% 이상
- [ ] 문서 업데이트 완료

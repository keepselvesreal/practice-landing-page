---
created_at: 2025-10-11
links:
   - ./index.md
   - ./concept_tdd.md
   - ./concept_tdd_part2.md
   - ./guide_tdd_application_v4.md
---

# TDD 모범 사례

TDD를 효과적으로 적용하기 위한 실전 모범 사례 모음

---

## 1. 테스트 명명 및 구조 일관성 (GOOS 21장)

### 1.1 TestDox 스타일 명명

**행동 중심 명명**: 테스트 이름이 그 자체로 문서가 되도록 작성

```python
# ❌ 기술 중심 이름
def test_commission_calculates_20_percent():
    pass

# ✅ 행동 중심 이름 (TestDox)
def test_affiliate_earns_20_percent_commission_on_sale():
    """어필리에이트는 판매 금액의 20% 커미션을 받는다"""
    pass
```

**원칙**:
- 도메인 용어 사용
- "무엇을" 테스트하는지 명확히
- docstring으로 한국어 설명 추가

---

### 1.2 Given/When/Then 구조 일관성

**3단계 구조**: 모든 테스트를 동일한 패턴으로 작성

```python
def test_place_order_validates_address():
    """주문 생성 시 주소를 검증한다"""
    # Given: 테스트 전제 조건
    invalid_address = "Invalid Address"
    service = build_place_order_service(
        validate_address=always_reject_address()
    )

    # When: 테스트 실행
    command = PlaceOrderCommand(..., customer_address=invalid_address)

    # Then: 예상 결과 검증
    with pytest.raises(ValueError, match="Invalid address"):
        service.place_order(command)
```

**장점**:
- 가독성 향상
- 테스트 의도 명확화
- 리뷰어가 이해하기 쉬움

---

### 1.3 Test Data Builder 패턴

**복잡한 테스트 데이터 생성 단순화**

```python
# ❌ 원시 값 하드코딩 (반복적)
def test_affiliate_records_sale():
    commission = Money.of(Decimal("5.00"))

# ✅ 빌더 활용 (재사용)
def test_affiliate_records_sale():
    commission = MoneyBuilder.commission_for(sale_amount=Decimal("25.00"))
```

**서비스 헬퍼 패턴**:

```python
class TestPlaceOrderService:
    def create_service(
        self,
        save_order=None,
        process_payment=None,
        validate_address=None
    ):
        """테스트용 서비스 생성 헬퍼"""
        return PlaceOrderService(
            save_order_port=save_order or Mock(),
            process_payment_port=process_payment or Mock(),
            validate_address_port=validate_address or Mock()
        )
```

---

## 2. 자기 설명적 테스트 (GOOS 23-24장)

### 2.1 명명된 상수

**매직 넘버 제거**

```python
# ❌ 매직 넘버/문자열
def test_sends_email():
    result = send_email("test@example.com", "support@example.com")

# ✅ 명명된 상수
CUSTOMER_EMAIL = "customer@example.com"
SUPPORT_EMAIL = "support@cosmetics.com"

def test_sends_email():
    result = send_email(CUSTOMER_EMAIL, SUPPORT_EMAIL)
```

---

### 2.2 커스텀 단언 헬퍼

**도메인 검증 로직 캡슐화**

```python
def assert_affiliate_has_sales(
    affiliate: Affiliate,
    expected_sales: int,
    expected_commission: Decimal
):
    """어필리에이트 판매 및 커미션 검증"""
    assert affiliate.total_sales == expected_sales, \
        f"Expected {expected_sales} sales, but got {affiliate.total_sales}"
    assert affiliate.total_commission.amount == expected_commission, \
        f"Expected commission {expected_commission}"
```

**장점**:
- 도메인 의도 명확화
- 실패 메시지 개선
- 재사용 가능

---

### 2.3 유연한 단언 (GOOS 24장)

**중요한 부분만 검증**

```python
def assert_email_sent_with(
    mock_sender,
    from_email: str,
    to_email: str,
    containing: str  # 전체 본문 검증 대신 키워드만
):
    """이메일 전송 내용 검증"""
    sent_email = mock_sender.send.call_args[0][0]

    assert sent_email.from_address == from_email
    assert sent_email.to_address == to_email
    assert containing in sent_email.body  # 유연한 검증
```

---

## 3. 계층별 테스트 전략

### 3.1 테스트 계층 분류

| 계층 | 테스트 타입 | 마커 | Mock 사용 | 검증 대상 |
|------|------------|------|-----------|-----------|
| **Domain** | 단위 테스트 | - | ❌ 없음 | 비즈니스 규칙 |
| **Application** | 단위 테스트 | - | ✅ 포트 Mock | Use Case 로직 |
| **Adapter (Learning)** | Learning Test | `@pytest.mark.learning` | ❌ 실제 API | API 계약 학습 |
| **Adapter (Contract)** | Contract Test | - | ❌ 없음 | Fake↔Real 계약 일치 |
| **Adapter (Integration)** | 통합 테스트 | `@pytest.mark.integration` | ❌ Sandbox/Fake | 외부 연동 |
| **End-to-End** | E2E 테스트 | `@pytest.mark.e2e` | ❌ 실제 환경 | 전체 흐름 |

---

### 3.2 테스트 실행 명령어

```bash
# 마커별 실행
pytest -m learning      # Learning Test만 실행
pytest -m integration   # Integration Test만 실행
pytest -m e2e           # E2E Test만 실행

# 빠른 단위 테스트만 (외부 의존성 제외)
pytest -m "not (learning or integration or e2e)"

# 특정 계층만 실행
pytest tests/unit/domain -v      # 도메인 계층만
pytest tests/unit/application -v # 애플리케이션 계층만
```

---

## 4. Mock 사용 원칙 (GOOS 7-8장)

### 4.1 명시적 협력 검증

**Mock 내부 파고들기 대신 프로토콜 검증**

```python
# ✅ 명시적 협력 검증
def test_place_order_records_affiliate_sale(self):
    # Given
    load_affiliate = Mock()
    save_affiliate = Mock()

    # When
    service.place_order(command)

    # Then: 협력 프로토콜 검증
    load_affiliate.load_by_code.assert_called_once_with("INFLUENCER123")
    save_affiliate.save.assert_called_once()

    # 저장된 상태 검증 (커스텀 헬퍼 활용)
    saved_affiliate = save_affiliate.save.call_args[0][0]
    assert_affiliate_has_sales(saved_affiliate, expected_sales=1)
```

---

### 4.2 테스트가 알려주는 설계 피드백

**다중 Mock 의존 → 설계 냄새**

```python
# ❌ 5개 Mock 의존 (설계 문제)
service = PlaceOrderService(
    save_order=mock1,
    process_payment=mock2,
    validate_address=mock3,
    load_affiliate=mock4,
    save_affiliate=mock5  # 너무 많은 책임!
)

# ✅ 역할 분리 (3개 포트 + 1개 도메인 서비스)
service = PlaceOrderService(
    save_order=mock1,
    process_payment=mock2,
    validate_address=mock3,
    affiliate_tracker=AffiliateTracker(...)  # 책임 분리
)
```

---

## 5. Fake와 Contract Test (GOOS 22장)

### 5.1 Fake 구현 원칙

**빠른 피드백 + Real과 동일한 계약**

```python
class FakePaymentAdapter(ProcessPaymentPort):
    def __init__(self, always_succeed=True):
        self.always_succeed = always_succeed  # 테스트 제어

    def process_payment(self, order: Order) -> PaymentResult:
        if self.always_succeed:
            return PaymentResult(
                success=True,
                transaction_id="fake_txn_123",  # 예측 가능
                error_message=None
            )
        else:
            return PaymentResult(success=False, ...)
```

---

### 5.2 Contract Test 필수

**Fake와 Real이 동일한 계약 보장**

```python
class TestFakePaymentAdapterContract:
    def test_implements_process_payment_port(self):
        """ProcessPaymentPort 인터페이스 구현 확인"""
        fake_gateway = FakePaymentAdapter()
        assert isinstance(fake_gateway, ProcessPaymentPort)

    def test_same_interface_as_paypal_adapter(self):
        """PayPalAdapter와 동일한 인터페이스"""
        fake_gateway = FakePaymentAdapter()
        result = fake_gateway.process_payment(sample_order)
        assert isinstance(result, PaymentResult)
```

---

## 6. TDD 사이클 유지 (GOOS 전반)

### 6.1 Red-Green-Refactor 리듬

```
1. ❌ Red: 실패하는 테스트 작성
   → 새로운 기능에 대한 테스트 먼저

2. ✅ Green: 최소 구현으로 통과
   → 하드코딩도 OK, 일단 통과시키기

3. 🔄 Refactor: 코드 개선
   → 중복 제거, 추상화, 설계 개선
```

---

### 6.2 Outside-in 흐름 유지

```
인수 테스트(E2E) 작성
  ↓
UI/API 계층 스텁 구현
  ↓
애플리케이션 계층 테스트 작성
  ↓
도메인 계층 테스트 작성
  ↓
어댑터 계층 테스트 작성
  ↓
인수 테스트 통과
```

---

## 7. Learning Test 전략 (GOOS 22장)

### 7.1 외부 API 계약 학습

**실제 API 호출로 계약 확인**

```python
@pytest.mark.learning
class TestPayPalPaymentCreation:
    def test_payment_creation_returns_payment_id(self, paypal_config):
        """학습 목표: 결제 생성 시 payment_id를 반환한다"""
        # Given: PayPal SDK 직접 호출
        payment = paypalrestsdk.Payment({...})

        # When
        result = payment.create()

        # Then: API 계약 검증
        assert payment.id.startswith("PAYID-")
        assert payment.state == "created"
```

**목적**:
- 외부 API 동작 방식 학습
- 응답 구조 파악
- 에러 패턴 이해
- Real Adapter 구현 근거

---

## 8. CI/CD 친화적 테스트

### 8.1 테스트 격리

```python
# ✅ In-Memory DB 사용
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = SessionLocal()
    yield session
    session.close()
```

---

### 8.2 빠른 피드백 우선

```bash
# 1단계: 빠른 단위 테스트 (1-5초)
pytest -m "not (learning or integration or e2e)"

# 2단계: 통합 테스트 (10-30초)
pytest -m integration

# 3단계: E2E 테스트 (1-3분)
pytest -m e2e

# 4단계: Learning Test (수동/선택적)
pytest -m learning
```

---

## 9. 핵심 원칙 요약

### 9.1 GOOS 원칙 준수 체크리스트

- ✅ **Outside-in**: 모든 기능이 인수 테스트로 시작
- ✅ **Learning Test**: 외부 API 계약 학습 후 구현
- ✅ **Contract Test**: Fake↔Real 동일 계약 보장
- ✅ **명시적 협력**: Mock 내부 대신 프로토콜 검증
- ✅ **자기 설명적 진단**: 커스텀 헬퍼, 명명된 상수
- ✅ **설계 피드백**: 테스트 어려움 → 설계 개선 신호
- ✅ **통제 가능한 테스트**: Fake, In-Memory DB로 안정성

---

### 9.2 안티패턴 회피

❌ **피해야 할 것**:
- 구현 세부사항 테스트 (내부 메서드 직접 호출)
- 과도한 Mock 사용 (5개 이상 → 설계 문제)
- 실제 외부 서비스 의존 (CI 불안정)
- 테스트 간 의존성 (실행 순서 중요)
- 매직 넘버/문자열 (의도 불명확)

✅ **지향해야 할 것**:
- 행동 검증 (공개 인터페이스)
- 적절한 Mock 사용 (2-3개)
- Fake/In-Memory 활용
- 테스트 격리 (독립 실행 가능)
- 명명된 상수, 커스텀 헬퍼

---

## 참고문헌

- **GOOS** (Growing Object-Oriented Software, Guided by Tests)
  - Chapter 7-8: Mock 사용
  - Chapter 21: 테스트 가독성
  - Chapter 22: Learning Tests, Contract Tests
  - Chapter 23-24: 자기 설명적 테스트

- **관련 문서**:
  - [concept_tdd.md](./concept_tdd.md): TDD 기본 개념
  - [concept_tdd_part2.md](./concept_tdd_part2.md): Learning Test, Contract Test
  - [guide_tdd_application_v4.md](./guide_tdd_application_v4.md): 실전 적용 가이드

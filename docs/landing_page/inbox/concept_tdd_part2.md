---
created_at: 2025-10-10 20:55:47
links:
   - ./concept_tdd.md
   - ./guide_tdd_application_v1.md
   - ./guide_tdd_application_v2.md
---

# TDD 고급 패턴 (Part 2)

**개요**: TDD의 고급 테스트 패턴과 외부 의존성 관리 전략

**출처**: GOOS (Growing Object-Oriented Software, Guided by Tests) Chapter 22

**관련 문서**:
- [TDD 핵심 개념 (Part 1)](./concept_tdd.md)
- [TDD 적용 가이드 v1](./guide_tdd_application_v1.md)
- [TDD 적용 가이드 v2](./guide_tdd_application_v2.md)

---

## 1. Learning Test 패턴

### 1.1 개념

**정의**: 외부 라이브러리나 API의 동작을 학습하고 검증하기 위한 테스트

**목적**:
1. **API 계약 이해**: 외부 서비스의 실제 동작과 응답 구조 파악
2. **문서화**: API 사용법을 테스트 코드로 문서화
3. **변경 감지**: API 버전 업그레이드 시 동작 변경 감지
4. **구현 근거**: Mock/Fake 어댑터 구현의 신뢰성 확보

**출처**: GOOS Chapter 22 "Maintaining the TDD Cycle" (p.277-290)

### 1.2 특징

**Learning Test vs Unit Test**:

| 구분 | Learning Test | Unit Test |
|------|---------------|-----------|
| **대상** | 외부 라이브러리/API | 내부 코드 |
| **목적** | 이해와 학습 | 정확성 검증 |
| **실행 환경** | 실제 외부 서비스 (Sandbox) | 격리된 환경 (Mock) |
| **실패 의미** | API 계약 변경 감지 | 코드 결함 발견 |
| **실행 빈도** | 낮음 (API 변경 시) | 높음 (매 커밋마다) |

**마커 시스템**:
```python
@pytest.mark.learning
class TestPayPalPaymentCreation:
    """PayPal 결제 생성 API 계약 학습"""

    def test_payment_creation_returns_payment_id(self, paypal_config):
        """
        학습 목표: 결제 생성 시 payment_id를 반환한다

        API 계약 검증:
        - 성공 시 payment.create() == True
        - payment.id가 "PAYID-"로 시작
        - payment.state == "created"
        """
        ...
```

**실행 명령어**:
```bash
# Learning Test만 실행
pytest -m learning -v

# Learning Test 제외하고 실행
pytest -m "not learning"
```

### 1.3 작성 전략

#### Step 1: 기본 계약 검증

**목표**: API의 정상 동작 시나리오 학습

```python
@pytest.mark.learning
class TestPayPalPaymentCreation:
    """PayPal 결제 생성 API 계약 학습"""

    def test_payment_creation_returns_payment_id(self, paypal_config):
        """결제 생성 시 payment_id를 반환한다"""
        # Given: 최소 결제 정보
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [{
                "amount": {"total": "10.00", "currency": "USD"}
            }],
            "redirect_urls": {
                "return_url": "http://localhost:8000/payment/success",
                "cancel_url": "http://localhost:8000/payment/cancel"
            }
        })

        # When: 결제 생성
        result = payment.create()

        # Then: 성공 응답 검증
        assert result is True, f"Payment failed: {payment.error}"
        assert payment.id is not None
        assert payment.id.startswith("PAYID-")
        assert payment.state == "created"

        print(f"\n✅ Payment created: {payment.id}")
```

**검증 항목**:
- ✅ API 호출 성공 여부
- ✅ 응답 필드 존재 확인
- ✅ 응답 값 타입 검증
- ✅ 응답 값 패턴 검증 (예: ID 접두사)

#### Step 2: 응답 구조 상세 분석

**목표**: API 응답의 모든 필드와 데이터 타입 파악

```python
@pytest.mark.learning
class TestPayPalResponseStructure:
    """PayPal 응답 구조 상세 학습"""

    def test_payment_response_contains_expected_fields(self, paypal_config):
        """결제 응답의 모든 필드 구조 파악"""
        # Given & When
        payment = paypalrestsdk.Payment({...})
        payment.create()

        # Then: 응답 구조 분석
        print("\n📋 Payment Response Structure:")
        print(f"   ID: {payment.id}")
        print(f"   Intent: {payment.intent}")
        print(f"   State: {payment.state}")

        # Payer 정보
        assert hasattr(payment, 'payer')
        print(f"   Payer Method: {payment.payer.payment_method}")

        # Transactions 정보
        assert hasattr(payment, 'transactions')
        tx = payment.transactions[0]
        print(f"   Amount: {tx.amount.total} {tx.amount.currency}")

        # Links 정보 (HATEOAS)
        assert hasattr(payment, 'links')
        for link in payment.links:
            print(f"      - {link.rel}: {link.method} {link.href[:50]}...")
```

**검증 항목**:
- ✅ 응답 객체의 모든 필드 목록
- ✅ 중첩 객체 구조 파악
- ✅ HATEOAS 링크 구조 (rel, method, href)

#### Step 3: 에러 케이스 학습

**목표**: API 에러 처리 방식과 에러 응답 구조 이해

```python
@pytest.mark.learning
class TestPayPalErrorHandling:
    """PayPal 에러 처리 계약 학습"""

    def test_invalid_amount_returns_error(self, paypal_config):
        """잘못된 금액으로 결제 생성 시 에러를 반환한다"""
        # Given: 음수 금액
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [{
                "amount": {"total": "-10.00", "currency": "USD"}
            }],
            "redirect_urls": {...}
        })

        # When
        result = payment.create()

        # Then: 실패 응답 검증
        assert result is False
        assert hasattr(payment, 'error')
        assert payment.error is not None
        assert 'name' in payment.error

        print(f"\n✅ Error caught: {payment.error.get('name')}")
        print(f"   Message: {payment.error.get('message')}")
```

**검증 항목**:
- ✅ 에러 시 반환 값 (False, None, 예외 등)
- ✅ 에러 객체 구조 (error.name, error.message)
- ✅ 다양한 에러 케이스 (음수 금액, 필수 필드 누락, 잘못된 credentials)

#### Step 4: Mock/Fake 어댑터 구현 근거 마련

**Learning Test 결과 → Fake 어댑터 설계**:

```python
# Learning Test에서 학습한 내용
"""
PayPal API 계약:
- 성공 시: payment.id (str), payment.state ("created")
- 실패 시: payment.error (dict)
- transaction_id 패턴: "PAYID-" 접두사
"""

# Fake 어댑터 구현
class FakePaymentAdapter(ProcessPaymentPort):
    def __init__(self, always_succeed=True):
        self.always_succeed = always_succeed

    def process_payment(self, order: Order) -> PaymentResult:
        if self.always_succeed:
            # Learning Test에서 학습한 ID 패턴 적용
            return PaymentResult(
                success=True,
                transaction_id=f"fake_txn_{order.id.value}",  # 예측 가능한 ID
                error_message=None
            )
        else:
            # Learning Test에서 학습한 에러 응답 구조 적용
            return PaymentResult(
                success=False,
                transaction_id=None,
                error_message="Payment processing failed"
            )
```

**Learning Test의 가치**:
- ✅ Fake 어댑터가 Real 어댑터와 동일한 계약 준수
- ✅ 테스트 편의성 (성공/실패 모드 전환, 예측 가능한 ID)
- ✅ 실제 API 동작에 대한 신뢰성 확보

### 1.4 Learning Test 실행 전략

**CI/CD 파이프라인 통합**:

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Run Unit Tests
        run: pytest -m "not (learning or integration or e2e)" -v

  learning-tests:
    runs-on: ubuntu-latest
    # Learning Test는 주기적으로만 실행 (매일 또는 주말)
    if: github.event_name == 'schedule'
    steps:
      - name: Run Learning Tests
        run: pytest -m learning -v
        env:
          PAYPAL_SANDBOX_CLIENT_ID: ${{ secrets.PAYPAL_SANDBOX_CLIENT_ID }}
          PAYPAL_SANDBOX_CLIENT_SECRET: ${{ secrets.PAYPAL_SANDBOX_CLIENT_SECRET }}
```

**로컬 개발 실행**:
```bash
# 개발 중에는 Learning Test 스킵
pytest -m "not learning"

# API 업그레이드 전후로만 실행
pytest -m learning -v
```

---

## 2. Contract Test 패턴

### 2.1 개념

**정의**: Fake 구현체와 Real 구현체가 동일한 포트 인터페이스를 준수하는지 검증하는 테스트

**목적**:
1. **계약 일치 검증**: Fake와 Real이 동일한 입출력 타입과 동작 보장
2. **테스트 신뢰성**: Fake를 사용한 단위 테스트가 실제 환경에서도 동작함을 보장
3. **리팩토링 안전성**: 포트 인터페이스 변경 시 모든 어댑터가 동기화됨을 확인

**출처**: GOOS Chapter 22 "Learning Tests"

### 2.2 특징

**Contract Test vs Integration Test**:

| 구분 | Contract Test | Integration Test |
|------|---------------|------------------|
| **대상** | Fake↔Real 계약 일치 | Real 어댑터 동작 |
| **목적** | 인터페이스 준수 검증 | 실제 외부 서비스 연동 |
| **실행 환경** | 격리된 환경 | 실제 외부 서비스 (Sandbox) |
| **실행 속도** | 빠름 | 느림 |
| **실행 빈도** | 높음 (매 커밋) | 중간 (배포 전) |

### 2.3 작성 전략

#### Step 1: 포트 인터페이스 구현 검증

```python
# tests/unit/adapter/test_fake_payment_contract.py
"""
Fake Payment Adapter Contract Test

목적:
- FakePaymentAdapter가 PayPalAdapter와 동일한 계약 준수 확인
- 포트 인터페이스(ProcessPaymentPort) 구현 검증
"""
import pytest
from cosmetics_landing.adapter.out.payment.fake_payment_adapter import FakePaymentAdapter
from cosmetics_landing.application.port.out.payment_gateway import ProcessPaymentPort


class TestFakePaymentAdapterContract:
    """FakePaymentAdapter 계약 검증"""

    def test_implements_process_payment_port(self):
        """ProcessPaymentPort 인터페이스 구현 확인"""
        fake_gateway = FakePaymentAdapter()

        assert isinstance(fake_gateway, ProcessPaymentPort)

    def test_same_interface_as_paypal_adapter(self, sample_order):
        """PayPalAdapter와 동일한 인터페이스"""
        fake_gateway = FakePaymentAdapter()

        # 두 어댑터 모두 동일한 포트 구현
        assert isinstance(fake_gateway, ProcessPaymentPort)

        # 동일한 메서드 시그니처
        assert hasattr(fake_gateway, 'process_payment')

        # 동일한 입출력 타입
        result = fake_gateway.process_payment(sample_order)
        assert isinstance(result, PaymentResult)
```

#### Step 2: 입출력 타입 검증

```python
class TestFakePaymentAdapterContract:
    def test_process_payment_returns_payment_result(self, sample_order):
        """process_payment가 PaymentResult 반환"""
        fake_gateway = FakePaymentAdapter()

        result = fake_gateway.process_payment(sample_order)

        # PaymentResult 타입 검증
        assert isinstance(result, PaymentResult)
        assert hasattr(result, 'success')
        assert hasattr(result, 'transaction_id')
        assert hasattr(result, 'error_message')

    def test_successful_payment_returns_transaction_id(self, sample_order):
        """성공 시 transaction_id 반환"""
        fake_gateway = FakePaymentAdapter()

        result = fake_gateway.process_payment(sample_order)

        # Fake는 항상 성공 (Real은 실제 API 호출 결과에 따라 결정)
        assert result.success is True
        assert result.transaction_id is not None
        assert isinstance(result.transaction_id, str)
        assert result.error_message is None
```

#### Step 3: Fake 특화 동작 검증

**Fake와 Real의 차이점 명시**:

```python
class TestFakePaymentAdapterBehavior:
    """FakePaymentAdapter 동작 검증 (Real과 다를 수 있는 부분)"""

    def test_fake_allows_success_mode_toggle(self, sample_order):
        """Fake는 성공/실패 모드 전환 가능 (테스트 편의성)"""
        # 성공 모드
        fake_gateway = FakePaymentAdapter(always_succeed=True)
        result = fake_gateway.process_payment(sample_order)
        assert result.success is True

        # 실패 모드
        fake_gateway = FakePaymentAdapter(always_succeed=False)
        result = fake_gateway.process_payment(sample_order)
        assert result.success is False

    def test_fake_generates_predictable_transaction_ids(self, sample_order):
        """Fake는 예측 가능한 transaction_id 생성 (테스트 편의성)"""
        fake_gateway = FakePaymentAdapter()

        result = fake_gateway.process_payment(sample_order)

        # Fake는 "fake_txn_" 접두사 (Real PayPal은 "PAYID-")
        assert result.transaction_id.startswith("fake_txn_")
```

**Fake의 테스트 편의성**:
- ✅ **성공/실패 모드 전환**: `FakePaymentAdapter(always_succeed=False)`
- ✅ **예측 가능한 ID**: `fake_txn_{order_id}` (테스트 검증 용이)
- ✅ **빠른 실행**: 실제 네트워크 호출 없음

### 2.4 Real 어댑터 포트 준수 검증

**Integration Test에 포트 준수 검증 추가**:

```python
# tests/integration/adapter/test_paypal_adapter.py
@pytest.mark.integration
class TestPayPalAdapterPortCompliance:
    """PayPal 어댑터의 포트 인터페이스 준수 검증"""

    def test_implements_process_payment_port(self, paypal_adapter):
        """ProcessPaymentPort 인터페이스 구현 확인"""
        from cosmetics_landing.application.port.out.payment_gateway import ProcessPaymentPort

        assert isinstance(paypal_adapter, ProcessPaymentPort)

    def test_returns_payment_result_type(self, paypal_adapter, sample_order):
        """PaymentResult 타입 반환 확인"""
        from cosmetics_landing.application.port.out.payment_gateway import PaymentResult

        result = paypal_adapter.process_payment(sample_order)

        assert isinstance(result, PaymentResult)
        assert hasattr(result, 'success')
        assert hasattr(result, 'transaction_id')
        assert hasattr(result, 'error_message')
```

**포트 준수 검증의 가치**:
- ✅ Fake와 Real이 동일한 포트 인터페이스 구현 확인
- ✅ 포트 변경 시 모든 어댑터가 동기화됨을 보장
- ✅ 리팩토링 안전성 확보

---

## 3. 테스트 마커 시스템

### 3.1 마커 정의

**pytest 마커 설정** (`conftest.py`):

```python
def pytest_configure(config):
    """pytest 마커 설정"""
    config.addinivalue_line(
        "markers", "learning: 외부 API 계약 검증을 위한 Learning Test"
    )
    config.addinivalue_line(
        "markers", "integration: 실제 외부 서비스를 사용하는 통합 테스트"
    )
    config.addinivalue_line(
        "markers", "e2e: UI + API 전체 흐름을 검증하는 End-to-End 테스트"
    )
```

### 3.2 마커 사용 패턴

**테스트 파일별 마커 적용**:

```python
# tests/learning/test_paypal_contract.py
@pytest.mark.learning
class TestPayPalPaymentCreation:
    """PayPal 결제 생성 API 계약 학습"""
    ...

# tests/integration/adapter/test_paypal_adapter.py
@pytest.mark.integration
class TestPayPalAdapterIntegration:
    """PayPal 어댑터 통합 테스트"""
    ...

# tests/integration/end_to_end/test_order_form_ui.py
@pytest.mark.e2e
class TestOrderFormUI:
    """브라우저 레벨 인수 테스트"""
    ...
```

### 3.3 테스트 실행 전략

**로컬 개발**:
```bash
# 빠른 단위 테스트만 실행 (Learning, Integration, E2E 제외)
pytest -m "not (learning or integration or e2e)" -v

# 특정 마커만 실행
pytest -m learning -v
pytest -m integration -v
pytest -m e2e -v
```

**CI/CD 파이프라인**:
```yaml
# Pull Request 시: 빠른 단위 테스트만
- name: Run Unit Tests
  run: pytest -m "not (learning or integration or e2e)" -v

# Merge 전: Integration Test 추가
- name: Run Integration Tests
  run: pytest -m integration -v

# 배포 전: E2E Test 추가
- name: Run E2E Tests
  run: pytest -m e2e -v

# 주기적으로: Learning Test 실행 (매일 또는 주말)
- name: Run Learning Tests
  run: pytest -m learning -v
```

---

## 4. 테스트 계층별 전략 (확장)

### 4.1 테스트 피라미드와 마커

```
           /\
          /E2\      ← @pytest.mark.e2e
         /    \       (느림, 적은 수)
        /------\
       /  Intg \    ← @pytest.mark.integration
      /        \     (중간 속도, 중간 수)
     /----------\
    /   Learn   \  ← @pytest.mark.learning
   /            \   (API 계약 학습)
  /--------------\
 /      Unit      \ ← 마커 없음
/                  \  (빠름, 많은 수)
--------------------
```

### 4.2 계층별 테스트 전략 (최종)

| 계층 | 테스트 타입 | 마커 | Mock 사용 | 검증 대상 | 실행 빈도 |
|------|------------|------|-----------|-----------|-----------|
| **Domain** | 단위 테스트 | - | ❌ 없음 | 비즈니스 규칙 | 매 커밋 |
| **Application** | 단위 테스트 | - | ✅ 포트 Mock | Use Case 로직 | 매 커밋 |
| **Adapter (Learning)** | Learning Test | `@pytest.mark.learning` | ❌ 실제 API | API 계약 학습 | 주기적 (일/주) |
| **Adapter (Contract)** | Contract Test | - | ❌ 없음 | Fake↔Real 계약 일치 | 매 커밋 |
| **Adapter (Integration)** | 통합 테스트 | `@pytest.mark.integration` | ❌ Sandbox 환경 | 외부 연동 | 배포 전 |
| **End-to-End** | E2E 테스트 | `@pytest.mark.e2e` | ❌ 실제 환경 | 전체 흐름 | 배포 전 |

**실행 명령어**:
```bash
# 개발 중 (빠른 피드백)
pytest -m "not (learning or integration or e2e)" -v

# Pull Request (통합 검증)
pytest -m "not learning" -v

# 배포 전 (전체 검증)
pytest -v

# API 업그레이드 시 (계약 검증)
pytest -m learning -v
```

---

## 5. 테스트 작성 워크플로우 (확장)

### 5.1 Outside-in TDD with Learning Test

```
1. Learning Test: 외부 API 계약 학습
   ↓
2. Contract Test: Fake 어댑터 계약 검증
   ↓
3. E2E Test: 전체 흐름 실패 테스트 작성
   ↓
4. Unit Test (Application): Use Case 로직 구현
   ↓
5. Unit Test (Domain): 비즈니스 규칙 구현
   ↓
6. Integration Test: Real 어댑터 통합 검증
   ↓
7. E2E Test: 전체 흐름 통과 확인
```

**각 단계별 TDD 사이클**:
- 🔴 **Red**: 실패하는 테스트 작성
- 🟢 **Green**: 최소 구현으로 테스트 통과
- 🔵 **Refactor**: 코드 개선

### 5.2 예시: PayPal 결제 기능 구현

**Step 1: Learning Test** (🔴 Red)
```python
@pytest.mark.learning
def test_paypal_payment_creation():
    """PayPal API 계약 학습"""
    payment = paypalrestsdk.Payment({...})
    result = payment.create()

    assert result is True  # ← 실제 API 동작 확인
    assert payment.id.startswith("PAYID-")
```

**Step 2: Contract Test** (🔴 Red → 🟢 Green)
```python
def test_fake_implements_same_contract():
    """Fake가 Real과 동일한 계약 준수"""
    fake = FakePaymentAdapter()

    assert isinstance(fake, ProcessPaymentPort)  # ← 인터페이스 검증
```

**Step 3: E2E Test** (🔴 Red)
```python
@pytest.mark.e2e
def test_user_can_place_order(client):
    """사용자가 주문할 수 있다"""
    response = client.post("/api/orders", json={...})

    assert response.status_code == 201  # ← 전체 흐름 실패
```

**Step 4-6: 내부 계층 구현** (🟢 Green)
- Application Layer (PlaceOrderService)
- Domain Layer (Order, Money)
- Adapter Layer (PayPalAdapter)

**Step 7: E2E Test** (🟢 Green)
```python
@pytest.mark.e2e
def test_user_can_place_order(client):
    """사용자가 주문할 수 있다"""
    response = client.post("/api/orders", json={...})

    assert response.status_code == 201  # ← 통과!
```

---

## 6. 모범 사례 정리

### 6.1 Learning Test 작성 시

✅ **Do**:
- 실제 외부 서비스 (Sandbox) 사용
- API 계약을 명시적으로 문서화
- 에러 케이스 학습
- 응답 구조 상세 분석

❌ **Don't**:
- Production 환경에서 실행
- Learning Test에 비즈니스 로직 포함
- Mock/Stub 사용 (실제 API 호출 필수)

### 6.2 Contract Test 작성 시

✅ **Do**:
- Fake와 Real 모두에 대해 동일한 테스트 작성
- 포트 인터페이스 준수 명시적 검증
- 입출력 타입 검증

❌ **Don't**:
- Fake와 Real의 내부 구현 세부사항 테스트
- Fake에만 있는 테스트 편의 기능 Contract Test에 포함

### 6.3 테스트 마커 사용 시

✅ **Do**:
- 테스트 목적에 맞는 마커 사용
- CI/CD 파이프라인에서 마커별 실행 전략 수립
- 느린 테스트는 별도 마커로 분리

❌ **Don't**:
- 마커 없이 모든 테스트를 항상 실행
- 마커 의미를 모호하게 정의

---

## 참조

**GOOS (Growing Object-Oriented Software, Guided by Tests)**:
- Chapter 22: "Maintaining the TDD Cycle" (p.277-290)
  - Learning Tests
  - Contract Tests
  - Test Diagnostics

**관련 문서**:
- [TDD 핵심 개념](./concept_tdd.md)
- [TDD 적용 가이드 v1](./guide_tdd_application_v1.md)
- [TDD 적용 가이드 v2](./guide_tdd_application_v2.md)

# 화장품 랜딩페이지 구현 가이드
## Hexagonal Architecture 기반 프로젝트 설계

---

## 📋 목차
1. [프로젝트 개요](#1-프로젝트-개요)
2. [프로젝트 폴더 구조](#2-프로젝트-폴더-구조)
3. [모듈별 상세 설계](#3-모듈별-상세-설계)
4. [TDD 적용 가이드](#4-tdd-적용-가이드)
5. [참조 및 근거](#5-참조-및-근거)
6. [추가 고려사항](#6-추가-고려사항)

---

## 1. 프로젝트 개요

### 1.1 프로젝트 목표
- **비즈니스 목표**: MVP 10개 판매, 인플루언서 5명 확보
- **학습 목표**: TDD 적용, Hexagonal Architecture 패턴 학습
- **기술 스택**: FastAPI + SQLite/PostgreSQL + PayPal

### 1.2 핵심 기능
**Epic 1: 고객 구매 여정**
- 주소 입력 (Google Places API)
- PayPal 결제
- 주문 확인

**Epic 2: 인플루언서 파트너십**
- 어필리에이트 링크 생성
- 실시간 성과 추적
- 자동 수수료 지급 (20%)

**Epic 3: 고객 지원**
- 제품 문의 (Gmail SMTP)

---

## 2. 프로젝트 폴더 구조

### 2.1 전체 폴더 구조 개요

```
cosmetics_landing/
├── src/
│   └── cosmetics_landing/
│       ├── domain/                    # 도메인 계층 (가장 안쪽)
│       │   ├── __init__.py
│       │   ├── order.py               # Order 엔티티
│       │   ├── affiliate.py           # Affiliate 엔티티
│       │   └── commission.py          # Commission 값 객체
│       │
│       ├── application/               # 애플리케이션 계층
│       │   ├── __init__.py
│       │   ├── port/
│       │   │   ├── __init__.py
│       │   │   ├── in_/               # Incoming ports (Use Cases)
│       │   │   │   ├── __init__.py
│       │   │   │   ├── place_order_use_case.py
│       │   │   │   ├── track_affiliate_use_case.py
│       │   │   │   ├── calculate_commission_use_case.py
│       │   │   │   └── send_inquiry_use_case.py
│       │   │   │
│       │   │   └── out/               # Outgoing ports
│       │   │       ├── __init__.py
│       │   │       ├── order_repository.py
│       │   │       ├── affiliate_repository.py
│       │   │       ├── payment_gateway.py
│       │   │       ├── email_sender.py
│       │   │       └── address_validator.py
│       │   │
│       │   └── service/               # Use Case 구현
│       │       ├── __init__.py
│       │       ├── place_order_service.py
│       │       ├── track_affiliate_service.py
│       │       ├── calculate_commission_service.py
│       │       └── send_inquiry_service.py
│       │
│       ├── adapter/                   # 어댑터 계층
│       │   ├── __init__.py
│       │   ├── in_/                   # Incoming adapters
│       │   │   ├── __init__.py
│       │   │   └── web/               # FastAPI 웹 어댑터
│       │   │       ├── __init__.py
│       │   │       ├── order_controller.py
│       │   │       ├── affiliate_controller.py
│       │   │       ├── inquiry_controller.py
│       │   │       └── dto/           # 웹 전용 DTO
│       │   │           ├── __init__.py
│       │   │           ├── order_request.py
│       │   │           ├── affiliate_response.py
│       │   │           └── inquiry_request.py
│       │   │
│       │   └── out/                   # Outgoing adapters
│       │       ├── __init__.py
│       │       ├── persistence/       # 영속성 어댑터
│       │       │   ├── __init__.py
│       │       │   ├── order_persistence_adapter.py
│       │       │   ├── affiliate_persistence_adapter.py
│       │       │   └── model/         # DB 모델
│       │       │       ├── __init__.py
│       │       │       ├── order_model.py
│       │       │       └── affiliate_model.py
│       │       │
│       │       ├── payment/           # 결제 어댑터
│       │       │   ├── __init__.py
│       │       │   └── paypal_adapter.py
│       │       │
│       │       ├── email/             # 이메일 어댑터
│       │       │   ├── __init__.py
│       │       │   └── gmail_smtp_adapter.py
│       │       │
│       │       └── geocoding/         # 주소 검증 어댑터
│       │           ├── __init__.py
│       │           └── google_places_adapter.py
│       │
│       └── config/                    # 설정 계층 (가장 바깥)
│           ├── __init__.py
│           ├── settings.py            # 환경 설정
│           ├── dependencies.py        # 의존성 주입 설정
│           └── main.py                # FastAPI 앱 초기화
│
├── tests/                             # 테스트
│   ├── unit/                          # 단위 테스트
│   │   ├── domain/
│   │   │
│   │   └── application/
│   │
│   ├── integration/                   # 통합 테스트
│   │   ├── adapter/
│   │   │
│   │   └── end_to_end/                # 시스템 테스트
│   │
│   └── conftest.py                    # pytest 설정
│
├── migrations/                        # 데이터베이스 마이그레이션 (Alembic)
│   └── versions/
│
├── static/                            # 정적 파일
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/                         # HTML 템플릿
│   ├── landing.html
│   └── affiliate_stats.html
│
├── pyproject.toml                     # 프로젝트 메타데이터 (uv)
├── README.md
└── .env.example                       # 환경변수 예시
```

### 2.2 폴더 구조 설계 근거

**출처**: Chapter 3 "Organizing Code", Lines 114-171

**계층별 패키지 설명**:

1. **domain 패키지** (public entities)
   - **근거**: Chapter 3, Lines 179-180
   - **역할**: 도메인 모델 포함, 비즈니스 규칙 캡슐화
   - **가시성**: public (다른 계층에서 접근 필요)
   - **의존성**: 다른 계층에 의존하지 않음

2. **application 패키지**
   - **근거**: Chapter 3, Lines 180-186
   - **역할**: 유스케이스 구현, 포트 정의
   - **하위 구조**:
     - `port/in_`: Incoming ports (Use Case 인터페이스) - public
     - `port/out`: Outgoing ports (Repository, Gateway 인터페이스) - public
     - `service`: Use Case 구현 - package-private 가능

3. **adapter 패키지**
   - **근거**: Chapter 3, Lines 183-186
   - **역할**: 외부 세계와의 통신 담당
   - **하위 구조**:
     - `in_/web`: HTTP 요청 처리 (Incoming adapter)
     - `out/persistence`: 데이터베이스 통신 (Outgoing adapter)
     - `out/payment`: 결제 서비스 통신 (Outgoing adapter)
     - `out/email`: 이메일 발송 (Outgoing adapter)
     - `out/geocoding`: 주소 검증 서비스 통신 (Outgoing adapter)
   - **가시성**: package-private (포트를 통해서만 접근)

4. **config 패키지** (Configuration Layer)
   - **근거**: Chapter 9, Lines 23-49
   - **역할**: 의존성 주입, 애플리케이션 조립
   - **책임**: 모든 객체 인스턴스화 및 연결

---

## 3. 모듈별 상세 설계

### 3.1 도메인 계층 (Domain Layer)

**출처**: Chapter 4 "Implementing a Use Case", Lines 12-129

#### 3.1.1 Order 엔티티 (domain/order.py)

**설계 근거**: Chapter 4, Lines 109-225 (Account 엔티티 패턴 적용)

```python
# domain/order.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal

@dataclass(frozen=True)  # 불변성 보장
class OrderId:
    value: int

@dataclass(frozen=True)
class Money:
    amount: Decimal

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount must be positive")

    @classmethod
    def of(cls, amount: Decimal) -> 'Money':
        return cls(amount=amount)

@dataclass
class Order:
    """주문 엔티티 - 비즈니스 규칙 캡슐화"""
    id: Optional[OrderId]
    customer_email: str
    customer_address: str
    product_price: Money
    affiliate_code: Optional[str]
    created_at: datetime
    payment_status: str  # 'pending', 'completed', 'failed'

    @classmethod
    def create_new(cls, customer_email: str, customer_address: str,
                   product_price: Money, affiliate_code: Optional[str] = None) -> 'Order':
        """새 주문 생성 (ID 없음)"""
        return cls(
            id=None,
            customer_email=customer_email,
            customer_address=customer_address,
            product_price=product_price,
            affiliate_code=affiliate_code,
            created_at=datetime.now(),
            payment_status='pending'
        )

    def mark_as_paid(self) -> 'Order':
        """결제 완료 처리 (불변 객체이므로 새 인스턴스 반환)"""
        return Order(
            id=self.id,
            customer_email=self.customer_email,
            customer_address=self.customer_address,
            product_price=self.product_price,
            affiliate_code=self.affiliate_code,
            created_at=self.created_at,
            payment_status='completed'
        )

    def is_paid(self) -> bool:
        """결제 완료 여부 확인"""
        return self.payment_status == 'completed'
```

**핵심 포인트**:
- **불변성**: `@dataclass(frozen=True)` (Chapter 4, Lines 364-402)
- **팩토리 메서드**: `create_new()` (Chapter 4, Lines 212-224)
- **비즈니스 규칙**: `mark_as_paid()`, `is_paid()` (Chapter 4, Lines 130-165)

#### 3.1.2 Affiliate 엔티티 (domain/affiliate.py)

```python
# domain/affiliate.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class AffiliateId:
    value: int

@dataclass
class Affiliate:
    """어필리에이트 엔티티"""
    id: Optional[AffiliateId]
    code: str  # 고유 추천 코드
    total_clicks: int
    total_sales: int
    total_commission: Money
    pending_commission: Money
    created_at: datetime

    @classmethod
    def create_new(cls, code: str) -> 'Affiliate':
        """새 어필리에이트 생성"""
        return cls(
            id=None,
            code=code,
            total_clicks=0,
            total_sales=0,
            total_commission=Money.of(Decimal('0')),
            pending_commission=Money.of(Decimal('0')),
            created_at=datetime.now()
        )

    def record_click(self) -> 'Affiliate':
        """클릭 기록"""
        return Affiliate(
            id=self.id,
            code=self.code,
            total_clicks=self.total_clicks + 1,
            total_sales=self.total_sales,
            total_commission=self.total_commission,
            pending_commission=self.pending_commission,
            created_at=self.created_at
        )

    def record_sale(self, commission: Money) -> 'Affiliate':
        """판매 및 수수료 기록"""
        return Affiliate(
            id=self.id,
            code=self.code,
            total_clicks=self.total_clicks,
            total_sales=self.total_sales + 1,
            total_commission=Money.of(self.total_commission.amount + commission.amount),
            pending_commission=Money.of(self.pending_commission.amount + commission.amount),
            created_at=self.created_at
        )
```

#### 3.1.3 Commission 값 객체 (domain/commission.py)

```python
# domain/commission.py
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Commission:
    """수수료 계산 로직을 캡슐화한 값 객체"""
    rate: Decimal = Decimal('0.20')  # 20%

    def calculate(self, order_amount: Money) -> Money:
        """주문 금액에서 수수료 계산"""
        commission_amount = order_amount.amount * self.rate
        return Money.of(commission_amount)

    def __post_init__(self):
        if not (Decimal('0') <= self.rate <= Decimal('1')):
            raise ValueError("Commission rate must be between 0 and 1")
```

**설계 근거**:
- **값 객체**: Chapter 4, Lines 522-547 (Rich Domain Model)
- 비즈니스 규칙(20% 수수료)을 도메인에 캡슐화

---

### 3.2 애플리케이션 계층 (Application Layer)

**출처**: Chapter 4 "Implementing a Use Case", Lines 130-196

#### 3.2.1 Incoming Ports (Use Case 인터페이스)

**설계 근거**: Chapter 4, Lines 159-188

**application/port/in_/place_order_use_case.py**:

```python
# application/port/in_/place_order_use_case.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class PlaceOrderCommand:
    """주문 생성 명령 - Self-Validating Command"""
    customer_email: str
    customer_address: str
    product_price: Decimal
    affiliate_code: Optional[str]

    def __post_init__(self):
        # Input Validation (Chapter 4, Lines 200-363)
        if not self.customer_email:
            raise ValueError("customer_email is required")
        if not self.customer_address:
            raise ValueError("customer_address is required")
        if self.product_price <= 0:
            raise ValueError("product_price must be positive")

class PlaceOrderUseCase(ABC):
    """주문 생성 Use Case 인터페이스"""

    @abstractmethod
    def place_order(self, command: PlaceOrderCommand) -> OrderId:
        """주문 생성 및 결제 처리"""
        pass
```

**핵심 포인트**:
- **Self-Validating Command**: Chapter 4, Lines 274-363
- **Use Case별 전용 Input Model**: Chapter 4, Lines 403-427
- **생성자 기반 검증**: Chapter 4, Lines 364-402

**application/port/in_/track_affiliate_use_case.py**:

```python
# application/port/in_/track_affiliate_use_case.py
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class TrackAffiliateCommand:
    """어필리에이트 추적 명령"""
    affiliate_code: str

    def __post_init__(self):
        if not self.affiliate_code:
            raise ValueError("affiliate_code is required")

@dataclass(frozen=True)
class AffiliateStats:
    """어필리에이트 통계 - Use Case 전용 Output Model"""
    code: str
    total_clicks: int
    total_sales: int
    total_commission: Decimal
    pending_commission: Decimal

class TrackAffiliateUseCase(ABC):
    """어필리에이트 추적 Use Case 인터페이스"""

    @abstractmethod
    def track_click(self, command: TrackAffiliateCommand) -> None:
        """클릭 추적"""
        pass

    @abstractmethod
    def get_stats(self, affiliate_code: str) -> AffiliateStats:
        """통계 조회 (Query)"""
        pass
```

**설계 근거**:
- **Use Case별 Output Model**: Chapter 4, Lines 548-575
- **Query Service 패턴**: Chapter 4, Lines 576-625

#### 3.2.2 Outgoing Ports (Repository, Gateway 인터페이스)

**설계 근거**: Chapter 6, Lines 67-104 (포트 인터페이스 슬라이싱)

**application/port/out/order_repository.py**:

```python
# application/port/out/order_repository.py
from abc import ABC, abstractmethod

class SaveOrderPort(ABC):
    """주문 저장 포트 - 단일 책임"""

    @abstractmethod
    def save(self, order: Order) -> OrderId:
        pass

class LoadOrderPort(ABC):
    """주문 조회 포트 - 단일 책임"""

    @abstractmethod
    def load_by_id(self, order_id: OrderId) -> Optional[Order]:
        pass

    @abstractmethod
    def load_by_affiliate_code(self, affiliate_code: str) -> list[Order]:
        pass
```

**핵심 포인트**:
- **Interface Segregation Principle**: Chapter 6, Lines 146-159
- **"포트당 하나의 메서드" 접근**: Chapter 6, Lines 152-157

**application/port/out/payment_gateway.py**:

```python
# application/port/out/payment_gateway.py
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class PaymentResult:
    success: bool
    transaction_id: Optional[str]
    error_message: Optional[str]

class ProcessPaymentPort(ABC):
    """결제 처리 포트"""

    @abstractmethod
    def process_payment(self, order: Order) -> PaymentResult:
        pass

class PayoutCommissionPort(ABC):
    """수수료 지급 포트"""

    @abstractmethod
    def payout(self, affiliate: Affiliate, amount: Money) -> bool:
        pass
```

#### 3.2.3 Use Case 서비스 구현

**설계 근거**: Chapter 4, Lines 230-299

**application/service/place_order_service.py**:

```python
# application/service/place_order_service.py
from ..port.in_.place_order_use_case import PlaceOrderUseCase, PlaceOrderCommand
from ..port.out.order_repository import SaveOrderPort
from ..port.out.payment_gateway import ProcessPaymentPort
from ..port.out.address_validator import ValidateAddressPort
from ..port.out.affiliate_repository import LoadAffiliatePort, SaveAffiliatePort
from ...domain.order import Order, OrderId, Money
from ...domain.commission import Commission

class PlaceOrderService(PlaceOrderUseCase):
    """주문 생성 Use Case 구현"""

    def __init__(
        self,
        save_order_port: SaveOrderPort,
        process_payment_port: ProcessPaymentPort,
        validate_address_port: ValidateAddressPort,
        load_affiliate_port: LoadAffiliatePort,
        save_affiliate_port: SaveAffiliatePort
    ):
        self.save_order = save_order_port
        self.process_payment = process_payment_port
        self.validate_address = validate_address_port
        self.load_affiliate = load_affiliate_port
        self.save_affiliate = save_affiliate_port

    def place_order(self, command: PlaceOrderCommand) -> OrderId:
        """
        주문 생성 4단계 (Chapter 4, Lines 237-243):
        1. Input 받기 (Command 객체)
        2. 비즈니스 규칙 검증
        3. 모델 상태 조작
        4. Output 반환
        """
        # 1. Business Rule Validation (Chapter 4, Lines 428-521)
        if not self.validate_address.is_valid(command.customer_address):
            raise ValueError("Invalid address")

        # 2. 도메인 엔티티 생성
        order = Order.create_new(
            customer_email=command.customer_email,
            customer_address=command.customer_address,
            product_price=Money.of(command.product_price),
            affiliate_code=command.affiliate_code
        )

        # 3. 주문 저장 (결제 전)
        order_id = self.save_order.save(order)
        order_with_id = Order(
            id=order_id,
            customer_email=order.customer_email,
            customer_address=order.customer_address,
            product_price=order.product_price,
            affiliate_code=order.affiliate_code,
            created_at=order.created_at,
            payment_status=order.payment_status
        )

        # 4. 결제 처리
        payment_result = self.process_payment.process_payment(order_with_id)
        if not payment_result.success:
            raise PaymentFailedError(payment_result.error_message)

        # 5. 주문 상태 업데이트
        paid_order = order_with_id.mark_as_paid()
        self.save_order.save(paid_order)

        # 6. 어필리에이트 수수료 처리
        if command.affiliate_code:
            affiliate = self.load_affiliate.load_by_code(command.affiliate_code)
            if affiliate:
                commission = Commission().calculate(order.product_price)
                updated_affiliate = affiliate.record_sale(commission)
                self.save_affiliate.save(updated_affiliate)

        # 7. Output 반환
        return order_id
```

**핵심 포인트**:
- **Use Case 4단계 구조**: Chapter 4, Lines 237-243
- **Business Rule Validation**: Chapter 4, Lines 428-521
- **의존성 주입**: Chapter 9, Lines 11-22

---

### 3.3 어댑터 계층 (Adapter Layer)

#### 3.3.1 Incoming Adapter - Web Controller

**출처**: Chapter 5 "Implementing a Web Adapter", Lines 48-91

**adapter/in_/web/order_controller.py**:

```python
# adapter/in_/web/order_controller.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, condecimal
from typing import Optional

from .dto.order_request import OrderRequest
from ....application.port.in_.place_order_use_case import (
    PlaceOrderUseCase,
    PlaceOrderCommand
)

router = APIRouter(prefix="/api", tags=["orders"])

class OrderController:
    """주문 웹 어댑터 - 단일 유스케이스 담당"""

    def __init__(self, place_order_use_case: PlaceOrderUseCase):
        self.place_order = place_order_use_case

@router.post("/order")
def create_order(
    request: OrderRequest,
    controller: OrderController = Depends()
) -> dict:
    """
    웹 어댑터 책임 7단계 (Chapter 5, Lines 91-120):
    1. HTTP 요청을 객체로 매핑
    2. 인증/인가 검사
    3. 입력 검증
    4. 유스케이스 입력 모델로 변환
    5. 유스케이스 호출
    6. 유스케이스 출력을 HTTP로 매핑
    7. HTTP 응답 반환
    """
    try:
        # 4. 유스케이스 입력 모델로 변환
        command = PlaceOrderCommand(
            customer_email=request.customer_email,
            customer_address=request.customer_address,
            product_price=request.product_price,
            affiliate_code=request.affiliate_code
        )

        # 5. 유스케이스 호출
        order_id = controller.place_order.place_order(command)

        # 6-7. HTTP 응답 반환
        return {"order_id": order_id.value, "status": "success"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
```

**adapter/in_/web/dto/order_request.py**:

```python
# adapter/in_/web/dto/order_request.py
from pydantic import BaseModel, EmailStr, condecimal
from typing import Optional

class OrderRequest(BaseModel):
    """웹 어댑터 전용 입력 모델 - Pydantic으로 HTTP 검증"""
    customer_email: EmailStr
    customer_address: str
    product_price: condecimal(gt=0, decimal_places=2)
    affiliate_code: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "customer_email": "customer@example.com",
                "customer_address": "123 Main St, Manila, Philippines",
                "product_price": 29.99,
                "affiliate_code": "INFLUENCER123"
            }
        }
```

**설계 근거**:
- **컨트롤러 슬라이싱**: Chapter 5, Lines 268-343
- **유스케이스별 컨트롤러**: Chapter 5, Lines 272-299
- **전용 Input Model**: Chapter 5, Lines 335-343

#### 3.3.2 Outgoing Adapter - Persistence

**출처**: Chapter 6 "Implementing a Persistence Adapter", Lines 138-483

**adapter/out/persistence/order_persistence_adapter.py**:

```python
# adapter/out/persistence/order_persistence_adapter.py
from sqlalchemy.orm import Session
from typing import Optional

from ....application.port.out.order_repository import SaveOrderPort, LoadOrderPort
from ....domain.order import Order, OrderId, Money
from .model.order_model import OrderModel

class OrderPersistenceAdapter(SaveOrderPort, LoadOrderPort):
    """주문 영속성 어댑터 - 여러 포트 구현"""

    def __init__(self, db_session: Session):
        self.db = db_session

    def save(self, order: Order) -> OrderId:
        """
        영속성 어댑터 책임 5단계 (Chapter 6, Lines 92-116):
        1. 입력 받기
        2. 입력을 데이터베이스 형식으로 매핑
        3. 데이터베이스로 입력 전송
        4. 데이터베이스 출력을 애플리케이션 형식으로 매핑
        5. 출력 반환
        """
        # 2. 도메인 → DB 모델 매핑
        if order.id:
            # 기존 주문 업데이트
            order_model = self.db.query(OrderModel).filter(
                OrderModel.id == order.id.value
            ).first()
            order_model.payment_status = order.payment_status
        else:
            # 새 주문 생성
            order_model = OrderModel(
                customer_email=order.customer_email,
                customer_address=order.customer_address,
                product_price=float(order.product_price.amount),
                affiliate_code=order.affiliate_code,
                created_at=order.created_at,
                payment_status=order.payment_status
            )
            self.db.add(order_model)

        # 3. 데이터베이스에 저장
        self.db.commit()
        self.db.refresh(order_model)

        # 5. Output 반환
        return OrderId(value=order_model.id)

    def load_by_id(self, order_id: OrderId) -> Optional[Order]:
        """주문 ID로 조회"""
        order_model = self.db.query(OrderModel).filter(
            OrderModel.id == order_id.value
        ).first()

        if not order_model:
            return None

        # 4. DB 모델 → 도메인 엔티티 매핑
        return Order(
            id=OrderId(value=order_model.id),
            customer_email=order_model.customer_email,
            customer_address=order_model.customer_address,
            product_price=Money.of(Decimal(str(order_model.product_price))),
            affiliate_code=order_model.affiliate_code,
            created_at=order_model.created_at,
            payment_status=order_model.payment_status
        )
```

**adapter/out/persistence/model/order_model.py**:

```python
# adapter/out/persistence/model/order_model.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OrderModel(Base):
    """주문 DB 모델 - JPA 엔티티 패턴"""
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_email = Column(String, nullable=False)
    customer_address = Column(String, nullable=False)
    product_price = Column(Float, nullable=False)
    affiliate_code = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
    payment_status = Column(String, nullable=False)  # 'pending', 'completed', 'failed'
```

**설계 근거**:
- **도메인-영속성 모델 분리**: Chapter 6, Lines 584-591
- **매핑의 필요성**: Chapter 6, Lines 584-591
- **영속성 어댑터 슬라이싱**: Chapter 6, Lines 105-137

#### 3.3.3 Outgoing Adapter - Payment

**adapter/out/payment/paypal_adapter.py**:

```python
# adapter/out/payment/paypal_adapter.py
from paypalrestsdk import Payment as PayPalPayment
import paypalrestsdk

from ....application.port.out.payment_gateway import (
    ProcessPaymentPort,
    PaymentResult
)
from ....domain.order import Order

class PayPalAdapter(ProcessPaymentPort):
    """PayPal 결제 어댑터"""

    def __init__(self, client_id: str, client_secret: str, mode: str = 'sandbox'):
        paypalrestsdk.configure({
            "mode": mode,
            "client_id": client_id,
            "client_secret": client_secret
        })

    def process_payment(self, order: Order) -> PaymentResult:
        """PayPal로 결제 처리"""
        payment = PayPalPayment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": str(order.product_price.amount),
                    "currency": "USD"
                },
                "description": f"Order for {order.customer_email}"
            }],
            "redirect_urls": {
                "return_url": "http://localhost:8000/payment/success",
                "cancel_url": "http://localhost:8000/payment/cancel"
            }
        })

        if payment.create():
            return PaymentResult(
                success=True,
                transaction_id=payment.id,
                error_message=None
            )
        else:
            return PaymentResult(
                success=False,
                transaction_id=None,
                error_message=payment.error.get('message', 'Unknown error')
            )
```

**핵심 포인트**:
- **교체 가능성**: Stripe로 전환 시 이 어댑터만 교체
- **포트 인터페이스 준수**: ProcessPaymentPort 구현

---

### 3.4 설정 계층 (Configuration Layer)

**출처**: Chapter 9 "Assembling the Application", Lines 231-317

**config/dependencies.py**:

```python
# config/dependencies.py
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from ..application.service.place_order_service import PlaceOrderService
from ..adapter.out.persistence.order_persistence_adapter import OrderPersistenceAdapter
from ..adapter.out.payment.paypal_adapter import PayPalAdapter
from ..adapter.out.email.gmail_smtp_adapter import GmailSmtpAdapter
from ..adapter.out.geocoding.google_places_adapter import GooglePlacesAdapter
from .settings import get_settings

# Java Config 방식 (Chapter 9, Lines 239-317)

def get_db_session() -> Session:
    """데이터베이스 세션 팩토리"""
    settings = get_settings()
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()

@lru_cache()
def get_order_persistence_adapter() -> OrderPersistenceAdapter:
    """Order Persistence Adapter Bean"""
    return OrderPersistenceAdapter(db_session=get_db_session())

@lru_cache()
def get_paypal_adapter() -> PayPalAdapter:
    """PayPal Adapter Bean"""
    settings = get_settings()
    return PayPalAdapter(
        client_id=settings.paypal_client_id,
        client_secret=settings.paypal_client_secret,
        mode=settings.paypal_mode
    )

@lru_cache()
def get_place_order_service() -> PlaceOrderService:
    """Place Order Service Bean"""
    return PlaceOrderService(
        save_order_port=get_order_persistence_adapter(),
        process_payment_port=get_paypal_adapter(),
        validate_address_port=get_google_places_adapter(),
        load_affiliate_port=get_affiliate_persistence_adapter(),
        save_affiliate_port=get_affiliate_persistence_adapter()
    )
```

**설계 근거**:
- **Java Config 방식**: Chapter 9, Lines 231-317
- **명시적 의존성 제어**: Chapter 9, Lines 301-312
- **Configuration Component의 책임**: Chapter 9, Lines 35-49

---

## 4. TDD 적용 가이드

### 4.1 Walking Skeleton 구축 (Epic 1)

**목표**: 주문 생성부터 결제까지 전체 흐름을 관통하는 최소 기능 구현

#### 4.1.1 Phase 1: End-to-End 테스트 작성

```python
# tests/integration/end_to_end/test_place_order_e2e.py
import pytest
from fastapi.testclient import TestClient

def test_customer_can_place_order(client: TestClient):
    """
    E2E 테스트: 고객이 주문을 생성하고 결제할 수 있다
    (Chapter 4, 5: Walking Skeleton)
    """
    # Given: 주문 요청 데이터
    order_request = {
        "customer_email": "customer@example.com",
        "customer_address": "123 Main St, Manila",
        "product_price": 29.99
    }

    # When: 주문 생성 API 호출
    response = client.post("/api/order", json=order_request)

    # Then: 주문이 성공적으로 생성됨
    assert response.status_code == 200
    data = response.json()
    assert "order_id" in data
    assert data["status"] == "success"
```

**핵심**: 실패하는 E2E 테스트부터 시작 → 계층별 구현 → 테스트 통과

#### 4.1.2 Phase 2: 도메인 계층 TDD

```python
# tests/unit/domain/test_order.py
import pytest
from decimal import Decimal
from domain.order import Order, Money

def test_creates_new_order_with_pending_status():
    """새 주문은 pending 상태로 생성된다"""
    # Given
    order = Order.create_new(
        customer_email="test@example.com",
        customer_address="123 Main St",
        product_price=Money.of(Decimal("29.99"))
    )

    # Then
    assert order.payment_status == "pending"
    assert order.id is None

def test_marks_order_as_paid():
    """주문을 결제 완료 상태로 변경할 수 있다"""
    # Given
    order = Order.create_new(
        customer_email="test@example.com",
        customer_address="123 Main St",
        product_price=Money.of(Decimal("29.99"))
    )

    # When
    paid_order = order.mark_as_paid()

    # Then
    assert paid_order.payment_status == "completed"
    assert paid_order.is_paid()
```

**TDD 사이클**:
1. ❌ 실패: `Order` 클래스 없음
2. ✅ 통과: 최소 구현 (dataclass + 메서드)
3. 🔄 리팩토링: 불변성 추가 (`frozen=True`)

#### 4.1.3 Phase 3: 애플리케이션 계층 TDD

```python
# tests/unit/application/test_place_order_service.py
import pytest
from unittest.mock import Mock
from decimal import Decimal

from application.service.place_order_service import PlaceOrderService
from application.port.in_.place_order_use_case import PlaceOrderCommand
from domain.order import Order, OrderId, Money

def test_place_order_validates_address():
    """주문 생성 시 주소를 검증한다 (Chapter 4: Business Rule Validation)"""
    # Given: Mock 의존성
    save_order = Mock()
    process_payment = Mock()
    validate_address = Mock()
    validate_address.is_valid.return_value = False  # 잘못된 주소

    service = PlaceOrderService(
        save_order_port=save_order,
        process_payment_port=process_payment,
        validate_address_port=validate_address,
        load_affiliate_port=Mock(),
        save_affiliate_port=Mock()
    )

    command = PlaceOrderCommand(
        customer_email="test@example.com",
        customer_address="Invalid Address",
        product_price=Decimal("29.99"),
        affiliate_code=None
    )

    # When/Then: 잘못된 주소로 예외 발생
    with pytest.raises(ValueError, match="Invalid address"):
        service.place_order(command)

def test_place_order_processes_payment():
    """주문 생성 시 결제를 처리한다"""
    # Given
    save_order = Mock()
    save_order.save.return_value = OrderId(value=1)

    process_payment = Mock()
    process_payment.process_payment.return_value = PaymentResult(
        success=True,
        transaction_id="txn_123",
        error_message=None
    )

    validate_address = Mock()
    validate_address.is_valid.return_value = True

    service = PlaceOrderService(
        save_order_port=save_order,
        process_payment_port=process_payment,
        validate_address_port=validate_address,
        load_affiliate_port=Mock(),
        save_affiliate_port=Mock()
    )

    command = PlaceOrderCommand(
        customer_email="test@example.com",
        customer_address="123 Main St",
        product_price=Decimal("29.99"),
        affiliate_code=None
    )

    # When
    order_id = service.place_order(command)

    # Then
    assert order_id.value == 1
    process_payment.process_payment.assert_called_once()
```

**Mock 사용 원칙** (Chapter 8):
- **외부 의존성은 Mock 처리**: PayPal, Google Places API
- **도메인 로직은 실제 객체 사용**: `Order`, `Money`

#### 4.1.4 Phase 4: 어댑터 계층 통합 테스트

```python
# tests/integration/adapter/test_paypal_adapter.py
import pytest
from adapter.out.payment.paypal_adapter import PayPalAdapter
from domain.order import Order, Money, OrderId

@pytest.mark.integration
def test_paypal_adapter_processes_payment(paypal_sandbox_credentials):
    """PayPal 어댑터가 실제 결제를 처리할 수 있다 (Chapter 8: Third-Party Integration)"""
    # Given
    adapter = PayPalAdapter(
        client_id=paypal_sandbox_credentials["client_id"],
        client_secret=paypal_sandbox_credentials["client_secret"],
        mode="sandbox"
    )

    order = Order(
        id=OrderId(value=1),
        customer_email="test@example.com",
        customer_address="123 Main St",
        product_price=Money.of(Decimal("29.99")),
        affiliate_code=None,
        created_at=datetime.now(),
        payment_status="pending"
    )

    # When
    result = adapter.process_payment(order)

    # Then
    assert result.success
    assert result.transaction_id is not None
```

**통합 테스트 전략** (Chapter 7):
- **단위 테스트**: Mock 사용, 빠른 피드백
- **통합 테스트**: 실제 외부 서비스 (Sandbox), 느리지만 신뢰성 확보

---

### 4.2 Epic 2: 어필리에이트 기능 TDD

#### 4.2.1 도메인 계층: Affiliate 엔티티

```python
# tests/unit/domain/test_affiliate.py
from domain.affiliate import Affiliate
from domain.commission import Commission
from domain.order import Money
from decimal import Decimal

def test_affiliate_records_click():
    """어필리에이트 클릭을 기록한다"""
    # Given
    affiliate = Affiliate.create_new(code="INFLUENCER123")

    # When
    updated = affiliate.record_click()

    # Then
    assert updated.total_clicks == 1

def test_affiliate_records_sale_with_commission():
    """판매와 수수료를 함께 기록한다"""
    # Given
    affiliate = Affiliate.create_new(code="INFLUENCER123")
    commission = Money.of(Decimal("5.00"))

    # When
    updated = affiliate.record_sale(commission)

    # Then
    assert updated.total_sales == 1
    assert updated.total_commission.amount == Decimal("5.00")
    assert updated.pending_commission.amount == Decimal("5.00")

def test_commission_calculates_20_percent():
    """수수료는 주문 금액의 20%이다"""
    # Given
    commission = Commission()
    order_amount = Money.of(Decimal("100.00"))

    # When
    result = commission.calculate(order_amount)

    # Then
    assert result.amount == Decimal("20.00")
```

#### 4.2.2 애플리케이션 계층: 어필리에이트 추적

```python
# tests/unit/application/test_track_affiliate_service.py
from application.service.track_affiliate_service import TrackAffiliateService
from application.port.in_.track_affiliate_use_case import TrackAffiliateCommand

def test_track_click_increments_counter():
    """클릭 추적 시 카운터가 증가한다"""
    # Given
    load_affiliate = Mock()
    load_affiliate.load_by_code.return_value = Affiliate.create_new("INFLUENCER123")

    save_affiliate = Mock()

    service = TrackAffiliateService(
        load_affiliate_port=load_affiliate,
        save_affiliate_port=save_affiliate
    )

    command = TrackAffiliateCommand(affiliate_code="INFLUENCER123")

    # When
    service.track_click(command)

    # Then
    saved_affiliate = save_affiliate.save.call_args[0][0]
    assert saved_affiliate.total_clicks == 1

def test_place_order_records_affiliate_sale():
    """어필리에이트 코드가 있는 주문은 판매를 기록한다 (Chapter 4: Use Case Composition)"""
    # Given
    affiliate = Affiliate.create_new("INFLUENCER123")

    load_affiliate = Mock()
    load_affiliate.load_by_code.return_value = affiliate

    save_affiliate = Mock()

    service = PlaceOrderService(
        save_order_port=Mock(save=Mock(return_value=OrderId(1))),
        process_payment_port=Mock(process_payment=Mock(return_value=PaymentResult(True, "txn", None))),
        validate_address_port=Mock(is_valid=Mock(return_value=True)),
        load_affiliate_port=load_affiliate,
        save_affiliate_port=save_affiliate
    )

    command = PlaceOrderCommand(
        customer_email="test@example.com",
        customer_address="123 Main St",
        product_price=Decimal("100.00"),
        affiliate_code="INFLUENCER123"
    )

    # When
    service.place_order(command)

    # Then
    saved_affiliate = save_affiliate.save.call_args[0][0]
    assert saved_affiliate.total_sales == 1
    assert saved_affiliate.total_commission.amount == Decimal("20.00")  # 20%
```

---

### 4.3 Epic 3: 고객 문의 기능 TDD

#### 4.3.1 애플리케이션 계층: 문의 전송

```python
# tests/unit/application/test_send_inquiry_service.py
from application.service.send_inquiry_service import SendInquiryService
from application.port.in_.send_inquiry_use_case import SendInquiryCommand

def test_sends_inquiry_email():
    """문의 내용을 이메일로 전송한다"""
    # Given
    email_sender = Mock()
    email_sender.send.return_value = True

    service = SendInquiryService(email_sender_port=email_sender)

    command = SendInquiryCommand(
        customer_email="customer@example.com",
        message="When will my order arrive?"
    )

    # When
    result = service.send_inquiry(command)

    # Then
    assert result is True
    email_sender.send.assert_called_once()
    sent_email = email_sender.send.call_args[0][0]
    assert "customer@example.com" in sent_email.from_address
    assert "When will my order arrive?" in sent_email.body
```

#### 4.3.2 어댑터 계층: Gmail SMTP

```python
# tests/integration/adapter/test_gmail_smtp_adapter.py
@pytest.mark.integration
def test_gmail_smtp_sends_email(gmail_credentials):
    """Gmail SMTP 어댑터가 실제 이메일을 전송한다 (Chapter 8)"""
    # Given
    adapter = GmailSmtpAdapter(
        smtp_server="smtp.gmail.com",
        port=587,
        username=gmail_credentials["username"],
        password=gmail_credentials["password"]
    )

    email = Email(
        from_address="customer@example.com",
        to_address="support@cosmetics.com",
        subject="Product Inquiry",
        body="When will my order arrive?"
    )

    # When
    result = adapter.send(email)

    # Then
    assert result is True
```

---

### 4.4 TDD 모범 사례 정리

#### 4.4.1 Test Data Builder 패턴 활용

```python
# tests/builders.py
class OrderBuilder:
    """주문 테스트 데이터 빌더 (Chapter 22: Test Data Builder)"""

    def __init__(self):
        self.id = None
        self.customer_email = "test@example.com"
        self.customer_address = "123 Main St"
        self.product_price = Money.of(Decimal("29.99"))
        self.affiliate_code = None
        self.created_at = datetime.now()
        self.payment_status = "pending"

    @classmethod
    def an_order(cls):
        return cls()

    def with_id(self, order_id: int):
        self.id = OrderId(value=order_id)
        return self

    def with_affiliate_code(self, code: str):
        self.affiliate_code = code
        return self

    def paid(self):
        self.payment_status = "completed"
        return self

    def build(self) -> Order:
        return Order(
            id=self.id,
            customer_email=self.customer_email,
            customer_address=self.customer_address,
            product_price=self.product_price,
            affiliate_code=self.affiliate_code,
            created_at=self.created_at,
            payment_status=self.payment_status
        )

# 사용 예
def test_paid_order():
    order = OrderBuilder.an_order() \
        .with_id(1) \
        .with_affiliate_code("INFLUENCER123") \
        .paid() \
        .build()

    assert order.is_paid()
```

#### 4.4.2 테스트 진단성 향상

```python
# tests/helpers.py
class NamedMoney(Money):
    """자가 설명 Money 값 객체 (Chapter 23: Self-Describing Values)"""

    def __init__(self, amount: Decimal, name: str):
        super().__init__(amount)
        self._name = name

    def __repr__(self):
        return f"{self._name}({self.amount})"

# 사용
STANDARD_PRICE = NamedMoney(Decimal("29.99"), "STANDARD_PRICE")
VIP_DISCOUNT = NamedMoney(Decimal("5.00"), "VIP_DISCOUNT")

def test_calculates_total():
    order = OrderBuilder.an_order() \
        .with_price(STANDARD_PRICE) \
        .build()

    # 실패 시: "Expected STANDARD_PRICE(29.99), got VIP_DISCOUNT(5.00)"
```

#### 4.4.3 포트 슬라이싱으로 테스트 단순화

```python
# Chapter 6: 포트 인터페이스 슬라이싱
# ❌ 나쁜 예: 거대한 Repository
class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> OrderId: pass

    @abstractmethod
    def find_by_id(self, id: OrderId) -> Order: pass

    @abstractmethod
    def find_by_email(self, email: str) -> List[Order]: pass

    @abstractmethod
    def find_by_affiliate(self, code: str) -> List[Order]: pass

# ✅ 좋은 예: 슬라이싱된 포트
class SaveOrderPort(ABC):
    @abstractmethod
    def save(self, order: Order) -> OrderId: pass

class LoadOrderPort(ABC):
    @abstractmethod
    def load_by_id(self, id: OrderId) -> Order: pass

# 테스트에서는 필요한 포트만 Mock
def test_place_order():
    service = PlaceOrderService(
        save_order_port=Mock(),  # SaveOrderPort만 필요
        # ... 다른 포트들
    )
```

#### 4.4.4 계층별 테스트 전략

| 계층 | 테스트 타입 | Mock 사용 | 검증 대상 |
|------|------------|-----------|-----------|
| **Domain** | 단위 테스트 | ❌ 없음 | 비즈니스 규칙 |
| **Application** | 단위 테스트 | ✅ 포트 Mock | Use Case 로직 |
| **Adapter (Web)** | 통합 테스트 | ✅ Use Case Mock | HTTP 매핑 |
| **Adapter (Persistence)** | 통합 테스트 | ❌ 실제 DB (TestContainer) | 영속성 로직 |
| **Adapter (External)** | 통합 테스트 | ❌ Sandbox 환경 | 외부 연동 |
| **End-to-End** | 시스템 테스트 | ❌ 실제 환경 (Staging) | 전체 흐름 |

---

## 5. 참조 및 근거

### 5.1 주요 참조 문서

| 챕터 | 주요 내용 | 적용 위치 |
|------|----------|-----------|
| Chapter 3 | 패키지 구조 설계 | 전체 폴더 구조 |
| Chapter 4 | Use Case 구현 | 애플리케이션 계층 |
| Chapter 5 | Web Adapter 구현 | 웹 어댑터 |
| Chapter 6 | Persistence Adapter 구현 | 영속성 어댑터 |
| Chapter 7 | 테스트 전략 | 전체 테스트 |
| Chapter 8 | 외부 라이브러리 통합 | 어댑터 계층 |
| Chapter 9 | 의존성 주입 | 설정 계층 |
| Chapter 10 | 아키텍처 경계 강제 | 패키지 가시성 |
| Chapter 20 | 테스트가 주는 신호 | TDD 프로세스 |
| Chapter 21 | 테스트 가독성 | 테스트 작성 |
| Chapter 22 | 복잡한 테스트 데이터 | Test Data Builder |
| Chapter 23 | 테스트 진단성 | 실패 메시지 개선 |
| Chapter 24 | 테스트 유연성 | Brittle Test 방지 |

### 5.2 핵심 설계 결정 및 근거

1. **포트-어댑터 패턴**
   - **근거**: Chapter 3, Lines 180-186
   - **적용**: application/port, adapter 분리

2. **도메인 중심 설계**
   - **근거**: Chapter 4, Lines 12-129
   - **적용**: domain 패키지

3. **Use Case별 Input/Output 분리**
   - **근거**: Chapter 4, Lines 403-427, 548-575
   - **적용**: 각 Use Case마다 전용 Command/Result

4. **컨트롤러 슬라이싱**
   - **근거**: Chapter 5, Lines 268-343
   - **적용**: 유스케이스별 컨트롤러

5. **도메인-영속성 모델 분리**
   - **근거**: Chapter 6, Lines 584-591
   - **적용**: domain/order.py ≠ model/order_model.py

6. **Java Config 방식 의존성 주입**
   - **근거**: Chapter 9, Lines 231-317
   - **적용**: config/dependencies.py

7. **Walking Skeleton 우선**
   - **근거**: Chapter 4, 5
   - **적용**: E2E 테스트부터 시작

8. **Test Data Builder 패턴**
   - **근거**: Chapter 22
   - **적용**: tests/builders.py

---

## 6. 추가 고려사항

### 6.1 프로덕션 준비

1. **환경 분리**
   - 개발/스테이징/프로덕션 설정 분리
   - `.env` 파일 관리

2. **로깅 및 모니터링**
   - 구조화된 로깅 (JSON)
   - Cloud Logging 통합

3. **보안**
   - API 키 보안
   - HTTPS 강제
   - CORS 설정

### 6.2 확장 가능성

1. **어댑터 교체**
   - PayPal → Stripe 전환 시 `PayPalAdapter`만 교체
   - SQLite → PostgreSQL 전환 시 설정만 변경

2. **새 기능 추가**
   - SMS 알림: `adapter/out/sms/` 추가
   - 소셜 로그인: `adapter/in_/web/auth_controller.py` 추가

---

## 결론

이 문서는 **Hexagonal Architecture**와 **TDD** 원칙에 따라 화장품 랜딩페이지 프로젝트의 폴더 구조, 모듈 설계, 테스트 전략을 제공합니다.

**핵심 원칙**:
1. **도메인 중심**: 비즈니스 로직을 중앙에 배치
2. **의존성 역전**: 모든 의존성이 내부를 향함
3. **포트-어댑터**: 외부 세계와의 통신을 격리
4. **교체 가능성**: 어댑터를 쉽게 교체 가능
5. **TDD 사이클**: Red → Green → Refactor
6. **Walking Skeleton**: E2E 테스트부터 시작

이 문서를 참고하여 실제 프로젝트 폴더와 파일을 생성하고, 각 모듈의 역할과 책임을 이해하며, TDD를 통해 안정적인 코드를 작성할 수 있습니다.

---

## 🔍 비판적 검토 (추가 섹션)
- Chapter 20의 "테스트가 주는 설계 신호"에 따라 Mock 난이도를 설계 개선으로 해석하도록 안내하고 있으며, 본 가이드는 도메인 객체는 실제 구현을 사용하고 외부 의존성만 Mock 처리하도록 제안해 일관성을 유지합니다.
- Chapter 21과 23이 강조하는 읽기 쉬운, 자기 진단적 테스트 원칙과도 부합합니다. 예시 테스트는 명확한 이름과 의미 있는 Assertion을 사용하고 Self-Describing Value (`NamedMoney`) 패턴을 채택해 실패 메시지를 풍부하게 만듭니다.
- Chapter 22의 Test Data Builder 활용과 Chapter 24의 "정보 vs 표현" 및 "Allow Queries, Expect Commands" 원칙이 그대로 반영되어 과도한 명세나 취약한 테스트를 유발할 만한 지점이 발견되지 않았습니다.
- 제공된 참조 범위(Ch.20~24) 기준에서 잘못된 내용이나 보완해야 할 사항은 확인되지 않았습니다.

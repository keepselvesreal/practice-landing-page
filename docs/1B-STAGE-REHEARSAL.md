---
version: 1
created_date: 25-11-04
note: 1-b 단계 Outside-In TDD 구현 리허설 및 비판적 검토 요청
---

# 1-b 단계 구현 리허설 - 비판적 검토 요청

## 목차

1. [1-b 단계 개요](#1-1b-단계-개요)
2. [Outside-In TDD 구현 리허설](#2-outside-in-tdd-구현-리허설)
3. [테스트 전략 및 인프라](#3-테스트-전략-및-인프라)
4. [검토 요청 사항](#검토-요청-사항)

---

## 1. 1-b 단계 개요

### 1.1 목적 및 범위

**목표**: 주문번호를 입력하면 주문 정보를 조회할 수 있다

**구현 범위**:
- GET `/orders/{order_number}` API
- 주문 정보 응답 (구매자 정보, 주문 상태, 금액 등)
- 404 에러 처리 (주문번호 없을 시)
- 주문 조회 페이지 (`/order-check`)

**제외 사항**:
- 실제 주문 생성 (Mock 데이터로 테스트)
- PayPal 통합
- 배송/환불 정보 (추후 단계에서 추가)

---

### 1.2 기능 요구사항

| 시나리오 | 입력 | 출력 |
|---------|------|------|
| 정상 조회 | `ORD-12345678` | 200, 주문 정보 (10개 필드) |
| 주문 없음 | `ORD-NOTFOUND` | 404, `ORDER_NOT_FOUND` 에러 |

---

### 1.3 기술 스택 및 제약사항

- **백엔드**: FastAPI (Python 3.11+)
- **데이터베이스**: SQLite3 (동기 방식)
- **테스트**: pytest, pytest-mock, httpx
- **패키지 관리**: uv
- **아키텍처**: 3-Layer (API → Service → Repository)

**제약사항**:
- 동기 방식 SQLite (비동기 X)
- 단일 상품만 존재
- 주문 생성 기능 없음 (Mock 데이터 사용)

---

### 1.4 API 명세

#### GET `/orders/{order_number}`

**요청**:
```
GET /orders/ORD-12345678
```

**성공 응답** (200):
```json
{
  "order_number": "ORD-12345678",
  "customer_name": "홍길동",
  "customer_email": "hong@example.com",
  "customer_phone": "01012345678",
  "shipping_address": "서울시 강남구 테헤란로 123",
  "product_name": "조선미녀 맑은쌀 선크림 50ml",
  "quantity": 2,
  "unit_price": 57500,
  "total_amount": 115000,
  "order_status": "PAID",
  "created_at": "2025-11-04T10:30:00"
}
```

**실패 응답** (404):
```json
{
  "error": "주문을 찾을 수 없습니다",
  "code": "ORDER_NOT_FOUND"
}
```

---

### 1.5 데이터베이스 스키마

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,              -- 센타보(centavo) 단위
    stock INTEGER NOT NULL DEFAULT 10
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT UNIQUE NOT NULL,
    customer_name TEXT NOT NULL,
    customer_email TEXT NOT NULL,
    customer_phone TEXT NOT NULL,
    shipping_address TEXT NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price INTEGER NOT NULL,
    total_amount INTEGER NOT NULL,
    paypal_order_id TEXT UNIQUE,
    paypal_transaction_id TEXT,
    order_status TEXT DEFAULT 'PAYMENT_PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

**테스트 데이터**:
```sql
INSERT INTO products (id, name, price, stock)
VALUES (1, '조선미녀 맑은쌀 선크림 50ml', 57500, 10);

INSERT INTO orders (
  order_number, customer_name, customer_email, customer_phone,
  shipping_address, product_id, quantity, unit_price, total_amount,
  order_status
) VALUES (
  'ORD-12345678', '홍길동', 'hong@example.com', '01012345678',
  '서울시 강남구 테헤란로 123', 1, 2, 57500, 115000, 'PAID'
);
```

---

### 1.6 아키텍처 레이어 구조

```
브라우저
  ↓
FastAPI Endpoint (main.py)
  ↓ OrderResponse (Pydantic)
Service Layer (services.py)
  ↓ dict
Repository Layer (repository.py)
  ↓ SQL
SQLite Database
```

**레이어 책임**:
- **Endpoint**: HTTP 요청/응답 처리, 에러 핸들링
- **Service**: 비즈니스 로직 (현재는 단순 위임)
- **Repository**: DB 조회, 데이터 변환 (Row → dict)

---

## 2. Outside-In TDD 구현 리허설

### 2.1 Outside-In TDD 방법론 개요

**핵심 원칙**:
1. **바깥(E2E)에서 안쪽(DB)으로** 테스트 작성
2. **테스트 먼저, 구현은 나중에** (Red-Green-Refactor)
3. **Mock으로 시작, 실제 구현으로 교체**

**장점**:
- 사용자 관점에서 시작 (E2E 테스트)
- 필요한 인터페이스가 자연스럽게 도출됨
- 과도한 구현 방지 (YAGNI)

---

### 2.2 Red-Green-Refactor 사이클

```
🔴 RED: 테스트 작성 → 실패 확인
  ↓
🟢 GREEN: 최소한의 코드로 테스트 통과
  ↓
🔵 REFACTOR: 코드 개선 (테스트는 그대로)
  ↓
(반복)
```

---

### 2.3 구현 단계별 흐름

#### Step 1: E2E 테스트 작성 (RED)

```python
# tests/test_orders.py
def test_user_can_check_order_by_order_number(test_client, sample_order):
    """
    사용자가 주문번호를 입력하면 주문 정보를 조회할 수 있다

    Given: 결제 완료된 주문이 존재함
    When: GET /orders/ORD-12345678 요청
    Then: 200 응답, 주문 정보 반환 (구매자 정보, 주문 상태, 금액)
    """
    response = test_client.get("/orders/ORD-12345678")

    assert response.status_code == 200
    data = response.json()

    assert data["order_number"] == "ORD-12345678"
    assert data["customer_name"] == "홍길동"
    assert data["customer_email"] == "hong@example.com"
    assert data["product_name"] == "조선미녀 맑은쌀 선크림 50ml"
    assert data["quantity"] == 2
    assert data["total_amount"] == 115000
    assert data["order_status"] == "PAID"
```

**실행 결과**:
```
FAILED - 404 Not Found (엔드포인트가 아직 없음)
```

---

#### Step 2: FastAPI 앱 생성 및 엔드포인트 추가 (GREEN)

```python
# app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/orders/{order_number}")
def get_order(order_number: str):
    """주문 조회 API - 일단 빈 응답"""
    return {}
```

**실행 결과**:
```
FAILED - KeyError: 'order_number' (응답에 필수 필드 없음)
```

✅ 404 에러는 해결됨!

---

#### Step 3: API 레벨 테스트 작성 (RED)

```python
# tests/integration/test_api_orders.py
class TestGetOrderAPI:
    """GET /orders/{order_number} 통합 테스트"""

    def test_returns_order_info(self, test_client, sample_order):
        """주문 조회 성공"""
        response = test_client.get("/orders/ORD-12345678")

        assert response.status_code == 200
        data = response.json()
        assert data["order_number"] == "ORD-12345678"
        assert data["customer_name"] == "홍길동"

    def test_not_found(self, test_client):
        """존재하지 않는 주문번호 → 404"""
        response = test_client.get("/orders/ORD-NOTFOUND")

        assert response.status_code == 404
        data = response.json()
        assert data["code"] == "ORDER_NOT_FOUND"
        assert "error" in data

    def test_response_format(self, test_client, sample_order):
        """응답 형식 검증 (필수 필드 포함 여부)"""
        response = test_client.get("/orders/ORD-12345678")
        data = response.json()

        required_fields = [
            "order_number", "customer_name", "customer_email",
            "customer_phone", "shipping_address", "product_name",
            "quantity", "unit_price", "total_amount", "order_status"
        ]

        for field in required_fields:
            assert field in data, f"{field} 필드가 응답에 없음"
```

**실행 결과**:
```
FAILED - 모든 테스트 실패 (빈 dict 반환 중)
```

---

#### Step 4: Service 레이어 추가 (Mock Repository 사용)

```python
# app/models.py
from pydantic import BaseModel

class OrderResponse(BaseModel):
    order_number: str
    customer_name: str
    customer_email: str
    customer_phone: str
    shipping_address: str
    product_name: str
    quantity: int
    unit_price: int
    total_amount: int
    order_status: str
    created_at: str
```

```python
# app/services.py
from app.models import OrderResponse
from typing import Optional

class OrderService:
    def __init__(self, repository):
        self.repository = repository

    def get_order(self, order_number: str) -> Optional[OrderResponse]:
        """주문 조회 - Repository에 위임"""
        order_data = self.repository.find_by_order_number(order_number)

        if not order_data:
            return None

        return OrderResponse(**order_data)
```

```python
# app/main.py
from fastapi import FastAPI, HTTPException
from app.services import OrderService
from app.models import OrderResponse

app = FastAPI()

# Mock Repository (나중에 실제 구현으로 교체)
class MockOrderRepository:
    def find_by_order_number(self, order_number: str):
        """Mock 데이터 반환"""
        if order_number == "ORD-12345678":
            return {
                "order_number": "ORD-12345678",
                "customer_name": "홍길동",
                "customer_email": "hong@example.com",
                "customer_phone": "01012345678",
                "shipping_address": "서울시 강남구 테헤란로 123",
                "product_name": "조선미녀 맑은쌀 선크림 50ml",
                "quantity": 2,
                "unit_price": 57500,
                "total_amount": 115000,
                "order_status": "PAID",
                "created_at": "2025-11-04T10:30:00"
            }
        return None

order_service = OrderService(repository=MockOrderRepository())

@app.get("/orders/{order_number}", response_model=OrderResponse)
def get_order(order_number: str):
    """주문 조회 API"""
    order = order_service.get_order(order_number)

    if not order:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "주문을 찾을 수 없습니다",
                "code": "ORDER_NOT_FOUND"
            }
        )

    return order
```

**실행 결과**:
```
PASSED test_returns_order_info
PASSED test_not_found
PASSED test_response_format
```

🎉 **모든 테스트 통과!** (Mock으로)

---

#### Step 5: Service 테스트 작성 (Unit Test)

```python
# tests/unit/test_services.py
from app.services import OrderService
from unittest.mock import Mock
import pytest

@pytest.mark.unit
class TestOrderService:
    """OrderService 단위 테스트"""

    def test_returns_order_when_found(self):
        """Repository가 데이터를 반환하면 OrderResponse 반환"""
        # Mock Repository 설정
        mock_repo = Mock()
        mock_repo.find_by_order_number.return_value = {
            "order_number": "ORD-TEST",
            "customer_name": "테스트",
            "customer_email": "test@example.com",
            "customer_phone": "01011111111",
            "shipping_address": "테스트 주소",
            "product_name": "테스트 상품",
            "quantity": 1,
            "unit_price": 10000,
            "total_amount": 10000,
            "order_status": "PAID",
            "created_at": "2025-11-04T10:00:00"
        }

        service = OrderService(repository=mock_repo)
        result = service.get_order("ORD-TEST")

        # 검증
        assert result is not None
        assert result.order_number == "ORD-TEST"
        assert result.customer_name == "테스트"
        mock_repo.find_by_order_number.assert_called_once_with("ORD-TEST")

    def test_returns_none_when_not_found(self):
        """Repository가 None 반환하면 Service도 None 반환"""
        mock_repo = Mock()
        mock_repo.find_by_order_number.return_value = None

        service = OrderService(repository=mock_repo)
        result = service.get_order("ORD-NOTFOUND")

        assert result is None
        mock_repo.find_by_order_number.assert_called_once_with("ORD-NOTFOUND")
```

**실행 결과**:
```
PASSED test_returns_order_when_found
PASSED test_returns_none_when_not_found
```

✅ Service 레이어 테스트 통과!

---

#### Step 6: Repository 레이어 추가 (실제 DB 연결)

```python
# app/database.py
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "database.db"

def get_connection():
    """DB 연결 반환"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # dict 형태로 반환
    return conn

def execute_update(cursor, table: str, set_clause: dict, where_clause: dict):
    """자동으로 updated_at을 추가하는 UPDATE 헬퍼"""
    set_clause["updated_at"] = datetime.now().isoformat()

    set_parts = ", ".join([f"{k}=?" for k in set_clause.keys()])
    where_parts = " AND ".join([f"{k}=?" for k in where_clause.keys()])

    sql = f"UPDATE {table} SET {set_parts} WHERE {where_parts}"
    params = list(set_clause.values()) + list(where_clause.values())

    cursor.execute(sql, params)
```

```python
# app/repository.py
import sqlite3
from typing import Optional, Dict
from app.database import get_connection

class OrderRepository:
    def find_by_order_number(self, order_number: str) -> Optional[Dict]:
        """주문번호로 주문 조회 (상품명 포함)"""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                o.order_number,
                o.customer_name,
                o.customer_email,
                o.customer_phone,
                o.shipping_address,
                p.name AS product_name,
                o.quantity,
                o.unit_price,
                o.total_amount,
                o.order_status,
                o.created_at
            FROM orders o
            JOIN products p ON o.product_id = p.id
            WHERE o.order_number = ?
        """, (order_number,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None
```

---

#### Step 7: Repository 테스트 작성

```python
# tests/integration/test_repository.py
from app.repository import OrderRepository
import pytest

@pytest.mark.integration
class TestOrderRepository:
    """OrderRepository 통합 테스트 (실제 DB 사용)"""

    def test_finds_order_by_number(self, db_connection, sample_order_in_db):
        """DB에서 주문번호로 조회 성공"""
        repo = OrderRepository()
        result = repo.find_by_order_number("ORD-12345678")

        assert result is not None
        assert result["order_number"] == "ORD-12345678"
        assert result["customer_name"] == "홍길동"
        assert result["product_name"] == "조선미녀 맑은쌀 선크림 50ml"

    def test_returns_none_when_not_found(self, db_connection):
        """주문번호 없으면 None 반환"""
        repo = OrderRepository()
        result = repo.find_by_order_number("ORD-NOTFOUND")

        assert result is None
```

**실행 결과**:
```
PASSED test_finds_order_by_number
PASSED test_returns_none_when_not_found
```

✅ Repository 테스트 통과!

---

#### Step 8: Mock 제거 및 통합 테스트

```python
# app/main.py (수정)
from app.repository import OrderRepository  # 실제 Repository import

# MockOrderRepository 제거

# 실제 Repository 사용
order_repository = OrderRepository()
order_service = OrderService(repository=order_repository)

@app.get("/orders/{order_number}", response_model=OrderResponse)
def get_order(order_number: str):
    """주문 조회 API"""
    order = order_service.get_order(order_number)

    if not order:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "주문을 찾을 수 없습니다",
                "code": "ORDER_NOT_FOUND"
            }
        )

    return order
```

**통합 테스트 실행**:
```bash
pytest tests/integration/test_api_orders.py -v
```

**결과**:
```
PASSED test_returns_order_info
PASSED test_not_found
PASSED test_response_format
```

🎉 **모든 테스트 통과!** (실제 DB 사용)

---

#### Step 9: 404 에러 처리 확인

이미 Step 4에서 구현됨:

```python
if not order:
    raise HTTPException(
        status_code=404,
        detail={
            "error": "주문을 찾을 수 없습니다",
            "code": "ORDER_NOT_FOUND"
        }
    )
```

**테스트 확인**:
```bash
pytest tests/integration/test_api_orders.py::TestGetOrderAPI::test_not_found -v
```

**결과**:
```
PASSED
```

✅ 404 에러 처리 완료!

---

#### Step 10: UI 구현 (주문 조회 페이지)

```html
<!-- templates/order_check.html -->
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>주문 조회 - Scout Landing Page</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="container">
        <h1>주문 조회</h1>

        <div class="search-section">
            <input
                type="text"
                id="order-number-input"
                placeholder="주문번호 입력 (예: ORD-12345678)"
            >
            <button id="search-button">조회</button>
        </div>

        <div id="message" class="message" style="display:none;"></div>

        <div id="order-info" style="display:none;">
            <h2>주문 정보</h2>
            <div class="info-row">
                <span class="label">주문번호:</span>
                <span id="order-number"></span>
            </div>
            <div class="info-row">
                <span class="label">구매자:</span>
                <span id="customer-name"></span>
            </div>
            <div class="info-row">
                <span class="label">총 금액:</span>
                <span id="total-amount" class="highlight"></span>
            </div>
            <!-- 나머지 필드들... -->
        </div>
    </div>

    <script src="/static/js/order_check.js"></script>
</body>
</html>
```

```javascript
// static/js/order_check.js
document.addEventListener('DOMContentLoaded', () => {
    const searchButton = document.getElementById('search-button');
    const orderNumberInput = document.getElementById('order-number-input');

    searchButton.addEventListener('click', async () => {
        const orderNumber = orderNumberInput.value.trim();

        if (!orderNumber) {
            showMessage('주문번호를 입력해주세요', 'error');
            return;
        }

        try {
            const response = await fetch(`/orders/${orderNumber}`);

            if (response.ok) {
                const data = await response.json();
                displayOrder(data);
            } else if (response.status === 404) {
                const error = await response.json();
                showMessage(error.detail.error, 'error');
            }
        } catch (error) {
            showMessage('서버 연결에 실패했습니다', 'error');
        }
    });

    function displayOrder(order) {
        document.getElementById('order-number').textContent = order.order_number;
        document.getElementById('customer-name').textContent = order.customer_name;
        document.getElementById('total-amount').textContent =
            `₱${(order.total_amount / 100).toFixed(2)}`;

        document.getElementById('order-info').style.display = 'block';
    }

    function showMessage(text, type) {
        const messageDiv = document.getElementById('message');
        messageDiv.textContent = text;
        messageDiv.className = `message ${type}`;
        messageDiv.style.display = 'block';
    }
});
```

**FastAPI 라우트 추가**:
```python
# app/main.py
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/order-check")
def order_check_page(request: Request):
    """주문 조회 페이지"""
    return templates.TemplateResponse("order_check.html", {"request": request})
```

**수동 테스트**:
1. `uvicorn app.main:app --reload`
2. http://localhost:8000/order-check 접속
3. `ORD-12345678` 입력 → ✅ 주문 정보 표시
4. `ORD-NOTFOUND` 입력 → ✅ 에러 메시지 표시

---

### 2.4 최종 코드 구조

```
scouting/
├── app/
│   ├── main.py              # FastAPI 앱, 엔드포인트
│   ├── models.py            # Pydantic 모델 (OrderResponse)
│   ├── services.py          # OrderService
│   ├── repository.py        # OrderRepository
│   └── database.py          # DB 연결, execute_update 헬퍼
├── tests/
│   ├── conftest.py          # 전역 fixture
│   ├── unit/
│   │   ├── conftest.py
│   │   └── test_services.py
│   ├── integration/
│   │   ├── conftest.py
│   │   ├── test_api_orders.py
│   │   └── test_repository.py
│   └── fixtures/
│       ├── order_fixtures.py
│       └── mock_objects.py
├── static/
│   ├── css/style.css
│   └── js/order_check.js
├── templates/
│   └── order_check.html
└── database.db
```

---

### 2.5 핵심 학습 포인트

#### ✅ Outside-In TDD 흐름

```
E2E 테스트 작성
  ↓ (실패)
API 테스트 작성
  ↓ (실패)
Service 테스트 작성 (Mock Repository)
  ↓ (실패)
Repository 테스트 작성
  ↓ (실패)
Repository 구현 → 테스트 통과
  ↓
Service에서 Mock 제거 → 테스트 통과
  ↓
모든 테스트 통과 확인
```

#### ✅ Mock 사용 전략

- **초기**: Mock Repository로 Service 레이어 빠르게 구현
- **중간**: Repository 단위 테스트로 DB 로직 검증
- **최종**: Mock 제거하고 실제 통합 테스트

#### ✅ 테스트 레벨 구분

| 레벨 | 대상 | Mock 사용 | 속도 |
|------|------|-----------|------|
| Unit | Service | ✅ | 빠름 |
| Integration | Repository, API | ❌ | 중간 |
| E2E | 전체 플로우 | ❌ | 느림 |

---

## 3. 테스트 전략 및 인프라

### 3.1 테스트 디렉토리 구조

#### 3.1.1 Unit / Integration / E2E 분리 전략

```
tests/
├── conftest.py                      # 전역 설정 (pytest marker 등록)
├── fixtures/                        # 재사용 가능한 fixture 모듈
│   ├── __init__.py
│   ├── order_fixtures.py           # 주문 관련 fixture
│   ├── product_fixtures.py         # 상품 관련 fixture
│   └── mock_objects.py             # Mock 클래스들
│
├── unit/                            # 단위 테스트 (빠름, Mock 사용)
│   ├── conftest.py                 # unit 전용 fixture
│   ├── test_services.py            # Service 레이어
│   └── test_validators.py          # 입력 검증 로직
│
├── integration/                     # 통합 테스트 (실제 DB 사용)
│   ├── conftest.py                 # integration 전용 fixture
│   ├── test_repository.py          # Repository + DB
│   └── test_api_orders.py          # API + Service + Repository
│
└── e2e/                             # E2E 테스트 (전체 플로우)
    ├── conftest.py                 # e2e 전용 fixture (서버 실행 등)
    └── test_order_flow.py          # 주문 조회 플로우
```

**분리 기준**:

| 타입 | 목적 | DB 사용 | Mock 사용 | 속도 | 비율 |
|------|------|---------|-----------|------|------|
| **Unit** | 로직 검증 | ❌ | ✅ | 빠름 | 70% |
| **Integration** | 레이어 통합 | ✅ | ❌ | 중간 | 20% |
| **E2E** | 전체 플로우 | ✅ | ❌ | 느림 | 10% |

---

#### 3.1.2 파일 조직화 원칙

**원칙 1: 테스트 대상과 1:1 매핑**
```
app/services.py         → tests/unit/test_services.py
app/repository.py       → tests/integration/test_repository.py
app/routers/orders.py   → tests/integration/test_api_orders.py
```

**원칙 2: 클래스 기반 그룹화**
```python
# tests/integration/test_api_orders.py

class TestGetOrderAPI:
    """GET /orders/{order_number} 테스트 그룹"""
    def test_returns_order_info(self, test_client, sample_order_in_db):
        ...
    def test_not_found(self, test_client):
        ...
    def test_response_format(self, test_client, sample_order_in_db):
        ...

class TestCreateOrderAPI:  # 1-a 단계에서 추가
    """POST /orders 테스트 그룹"""
    ...
```

**원칙 3: 네이밍 컨벤션**
```python
# 클래스명: Test + 대상
class TestOrderService: ...
class TestGetOrderAPI: ...

# 메서드명: test_<조건>_<결과>
def test_returns_order_when_found(): ...
def test_raises_error_when_stock_insufficient(): ...
```

---

### 3.2 Fixture 관리

#### 3.2.1 전역 conftest.py

```python
# tests/conftest.py
import pytest

def pytest_configure(config):
    """pytest marker 등록"""
    config.addinivalue_line("markers", "unit: Unit tests (fast, mocked)")
    config.addinivalue_line("markers", "integration: Integration tests (real DB)")
    config.addinivalue_line("markers", "e2e: End-to-end tests (slow)")
    config.addinivalue_line("markers", "slow: Slow running tests")
```

---

#### 3.2.2 레벨별 conftest.py

**Unit 테스트 conftest.py**:
```python
# tests/unit/conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_order_repository():
    """Mock Repository (unit 테스트용)"""
    from tests.fixtures.mock_objects import MockOrderRepository
    return MockOrderRepository()

@pytest.fixture
def mock_paypal_client():
    """Mock PayPal Client"""
    mock = Mock()
    mock.create_order.return_value = {"id": "PAYPAL-123", "status": "CREATED"}
    mock.capture_order.return_value = {"status": "COMPLETED"}
    return mock
```

**Integration 테스트 conftest.py**:
```python
# tests/integration/conftest.py
import pytest
import sqlite3
from pathlib import Path

TEST_DB_PATH = Path(__file__).parent / "test_database.db"

@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    """매 integration 테스트마다 DB 초기화"""
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()

    # 테이블 초기화
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS products")

    # 테이블 생성
    cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            stock INTEGER NOT NULL DEFAULT 10
        )
    """)

    cursor.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            shipping_address TEXT NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price INTEGER NOT NULL,
            total_amount INTEGER NOT NULL,
            paypal_order_id TEXT UNIQUE,
            paypal_transaction_id TEXT,
            order_status TEXT DEFAULT 'PAYMENT_PENDING',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    # 기본 상품 삽입
    cursor.execute("""
        INSERT INTO products (id, name, price, stock)
        VALUES (1, '조선미녀 맑은쌀 선크림 50ml', 57500, 10)
    """)

    conn.commit()
    conn.close()

    yield

    # 테스트 후 정리
    TEST_DB_PATH.unlink(missing_ok=True)


@pytest.fixture
def db_connection():
    """테스트 DB 연결"""
    conn = sqlite3.connect(TEST_DB_PATH)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


@pytest.fixture
def test_client():
    """FastAPI TestClient (실제 DB 사용)"""
    from fastapi.testclient import TestClient
    from app.main import app

    # 테스트 DB 경로로 변경
    import app.database as db
    db.DB_PATH = TEST_DB_PATH

    return TestClient(app)
```

**E2E 테스트 conftest.py**:
```python
# tests/e2e/conftest.py
import pytest
import subprocess
import time
import signal

_server_process = None

@pytest.fixture(scope="session", autouse=True)
def start_test_server():
    """E2E 테스트용 서버 실행"""
    global _server_process

    _server_process = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    time.sleep(2)  # 서버 시작 대기

    yield

    _server_process.send_signal(signal.SIGTERM)
    _server_process.wait()
```

---

#### 3.2.3 재사용 가능한 fixture 설계

**Fixture 조합 패턴**:
```python
# tests/fixtures/order_fixtures.py
import pytest

@pytest.fixture
def sample_order_data():
    """샘플 주문 데이터 (dict)"""
    return {
        "order_number": "ORD-12345678",
        "customer_name": "홍길동",
        "customer_email": "hong@example.com",
        "customer_phone": "01012345678",
        "shipping_address": "서울시 강남구 테헤란로 123",
        "product_id": 1,
        "quantity": 2,
        "unit_price": 57500,
        "total_amount": 115000,
        "order_status": "PAID",
        "created_at": "2025-11-04T10:30:00"
    }


@pytest.fixture
def sample_order_in_db(db_connection, sample_order_data):
    """DB에 샘플 주문 삽입 (integration 테스트용)"""
    cursor = db_connection.cursor()
    cursor.execute("""
        INSERT INTO orders (
            order_number, customer_name, customer_email, customer_phone,
            shipping_address, product_id, quantity, unit_price, total_amount,
            order_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        sample_order_data["order_number"],
        sample_order_data["customer_name"],
        sample_order_data["customer_email"],
        sample_order_data["customer_phone"],
        sample_order_data["shipping_address"],
        sample_order_data["product_id"],
        sample_order_data["quantity"],
        sample_order_data["unit_price"],
        sample_order_data["total_amount"],
        sample_order_data["order_status"]
    ))
    db_connection.commit()

    return sample_order_data


@pytest.fixture
def multiple_orders_in_db(db_connection):
    """여러 주문 삽입 (목록 조회 테스트용)"""
    orders = [
        ("ORD-11111111", "김철수", "kim@example.com", "PAID"),
        ("ORD-22222222", "이영희", "lee@example.com", "PAYMENT_PENDING"),
        ("ORD-33333333", "박민수", "park@example.com", "REFUNDED"),
    ]

    cursor = db_connection.cursor()
    for order_number, name, email, status in orders:
        cursor.execute("""
            INSERT INTO orders (
                order_number, customer_name, customer_email, customer_phone,
                shipping_address, product_id, quantity, unit_price, total_amount,
                order_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (order_number, name, email, "01011111111", "주소", 1, 1, 57500, 57500, status))

    db_connection.commit()

    return orders
```

**사용 예시**:
```python
# tests/integration/test_api_orders.py
def test_returns_order_info(test_client, sample_order_in_db):
    """sample_order_in_db가 자동으로 DB 초기화 + 데이터 삽입"""
    response = test_client.get("/orders/ORD-12345678")
    assert response.status_code == 200
```

---

### 3.3 테스트 데이터 관리

#### 3.3.1 Fixture 모듈 분리

```python
# tests/fixtures/product_fixtures.py
import pytest

@pytest.fixture
def sample_product_data():
    return {
        "id": 1,
        "name": "조선미녀 맑은쌀 선크림 50ml",
        "price": 57500,
        "stock": 10
    }

@pytest.fixture
def low_stock_product(db_connection):
    """재고 부족 상품"""
    cursor = db_connection.cursor()
    cursor.execute("""
        INSERT INTO products (id, name, price, stock)
        VALUES (2, '재고부족 상품', 10000, 1)
    """)
    db_connection.commit()
    return {"id": 2, "stock": 1}
```

---

#### 3.3.2 Mock 객체 관리

```python
# tests/fixtures/mock_objects.py
from typing import Optional, Dict

class MockOrderRepository:
    """Mock Repository (unit 테스트용)"""

    def __init__(self):
        self._orders = {
            "ORD-12345678": {
                "order_number": "ORD-12345678",
                "customer_name": "홍길동",
                "customer_email": "hong@example.com",
                "customer_phone": "01012345678",
                "shipping_address": "서울시 강남구 테헤란로 123",
                "product_name": "조선미녀 맑은쌀 선크림 50ml",
                "quantity": 2,
                "unit_price": 57500,
                "total_amount": 115000,
                "order_status": "PAID",
                "created_at": "2025-11-04T10:30:00"
            }
        }

    def find_by_order_number(self, order_number: str) -> Optional[Dict]:
        return self._orders.get(order_number)

    def add_order(self, order_data: Dict):
        """테스트 중 동적으로 주문 추가"""
        self._orders[order_data["order_number"]] = order_data


class MockPayPalClient:
    """Mock PayPal Client (1-a 단계에서 사용)"""

    def create_order(self, amount: int):
        return {
            "id": "MOCK-PAYPAL-ORDER-123",
            "status": "CREATED"
        }

    def capture_order(self, order_id: str):
        return {
            "id": order_id,
            "status": "COMPLETED",
            "purchase_units": [{
                "payments": {
                    "captures": [{"id": "MOCK-TXN-123"}]
                }
            }]
        }
```

---

#### 3.3.3 샘플 데이터 생성 전략

**Factory 패턴 (선택사항)**:
```python
# tests/fixtures/factories.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class OrderFactory:
    """주문 데이터 팩토리"""
    order_number: str = "ORD-TEST"
    customer_name: str = "테스트"
    customer_email: str = "test@example.com"
    customer_phone: str = "01011111111"
    shipping_address: str = "테스트 주소"
    product_id: int = 1
    quantity: int = 1
    unit_price: int = 57500
    total_amount: int = 57500
    order_status: str = "PAID"

    def build(self) -> dict:
        """dict로 변환"""
        return {
            "order_number": self.order_number,
            "customer_name": self.customer_name,
            "customer_email": self.customer_email,
            "customer_phone": self.customer_phone,
            "shipping_address": self.shipping_address,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_amount": self.total_amount,
            "order_status": self.order_status
        }

# 사용 예시
def test_example():
    order = OrderFactory(
        order_number="ORD-CUSTOM",
        customer_name="커스텀"
    ).build()
```

---

### 3.4 테스트 실행 전략

#### 3.4.1 pytest.ini 설정

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

markers =
    unit: Unit tests (fast, mocked)
    integration: Integration tests (real DB)
    e2e: End-to-end tests (slow)
    slow: Slow running tests

# 기본은 unit + integration만 실행
addopts = -v -m "not e2e"

# 경고 무시 (선택)
filterwarnings =
    ignore::DeprecationWarning
```

---

#### 3.4.2 Marker 기반 선택적 실행

```bash
# Unit 테스트만 (빠름, 개발 중 자주 실행)
pytest -m unit

# Integration 테스트만
pytest -m integration

# E2E 테스트만 (느림, PR 전에만 실행)
pytest -m e2e

# 느린 테스트 제외
pytest -m "not slow"

# 전체 테스트
pytest

# 특정 파일만
pytest tests/unit/test_services.py

# 특정 클래스만
pytest tests/integration/test_api_orders.py::TestGetOrderAPI

# 특정 테스트만
pytest tests/integration/test_api_orders.py::TestGetOrderAPI::test_returns_order_info

# 코드 커버리지 포함
pytest --cov=app --cov-report=html
```

---

#### 3.4.3 성능 최적화 (scope, autouse)

**Scope 전략**:

| Scope | 생명주기 | 사용 예시 |
|-------|---------|----------|
| `function` | 테스트 함수마다 | DB 초기화 (기본값) |
| `class` | 테스트 클래스마다 | 공통 설정 |
| `module` | 파일마다 | 무거운 fixture |
| `session` | 전체 세션 | 서버 실행 |

**예시**:
```python
# 느림: 매 테스트마다 서버 재시작
@pytest.fixture(scope="function")
def start_server():
    ...

# 빠름: 전체 세션에서 서버 한 번만 시작
@pytest.fixture(scope="session")
def start_server():
    ...
```

**autouse 전략**:
```python
# 명시적 사용 (권장)
@pytest.fixture
def setup_db():
    ...

def test_example(setup_db):  # fixture 명시
    ...

# 자동 적용 (주의해서 사용)
@pytest.fixture(autouse=True)
def setup_db():
    """모든 테스트에 자동 적용"""
    ...

def test_example():  # fixture 명시 불필요
    ...
```

---

### 3.5 테스트 격리 및 DB 관리

#### 3.5.1 테스트 DB 초기화 전략

**방법 1: 매 테스트마다 전체 재생성** (현재 사용)
```python
@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    """매번 DROP → CREATE"""
    conn = sqlite3.connect(TEST_DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("CREATE TABLE ...")

    conn.commit()
    conn.close()

    yield

    TEST_DB_PATH.unlink(missing_ok=True)
```

**장점**: 완전한 격리, 간단
**단점**: 느림

---

**방법 2: 트랜잭션 롤백** (더 빠름)
```python
@pytest.fixture(scope="function")
def db_connection():
    """트랜잭션 롤백으로 격리"""
    conn = sqlite3.connect(TEST_DB_PATH)

    # 트랜잭션 시작
    conn.execute("BEGIN")

    yield conn

    # 테스트 후 롤백 (변경사항 취소)
    conn.rollback()
    conn.close()
```

**장점**: 빠름
**단점**: 복잡함, DDL 문은 롤백 불가

---

#### 3.5.2 트랜잭션 롤백 vs 전체 재생성

| 기준 | 전체 재생성 | 트랜잭션 롤백 |
|------|------------|--------------|
| **속도** | 느림 | 빠름 |
| **격리** | 완벽 | 완벽 |
| **복잡도** | 낮음 | 높음 |
| **DDL 지원** | ✅ | ❌ |
| **권장** | MVP, 학습 | 프로덕션 |

**1-b 단계 권장**: **전체 재생성** (간단하고 이해하기 쉬움)

---

#### 3.5.3 테스트 간 독립성 보장

**원칙**:
- 각 테스트는 다른 테스트에 영향받지 않아야 함
- 실행 순서에 무관하게 통과해야 함

**검증 방법**:
```bash
# 랜덤 순서로 실행 (pytest-randomly)
pip install pytest-randomly
pytest --randomly-seed=12345

# 역순으로 실행
pytest --reverse
```

**안티패턴**:
```python
# ❌ 나쁜 예: 전역 상태 의존
test_data = None

def test_create():
    global test_data
    test_data = create_order()

def test_read():
    # test_create가 먼저 실행되지 않으면 실패
    assert test_data is not None
```

**올바른 패턴**:
```python
# ✅ 좋은 예: fixture 사용
def test_create(db_connection):
    order = create_order(db_connection)
    assert order is not None

def test_read(db_connection, sample_order_in_db):
    # 독립적으로 실행 가능
    order = get_order(db_connection, "ORD-12345678")
    assert order is not None
```

---

### 3.6 UI 테스트 (선택사항)

#### 3.6.1 Playwright를 사용한 UI E2E 테스트

**설치**:
```bash
uv pip install playwright pytest-playwright
playwright install
```

**테스트 예시**:
```python
# tests/e2e/test_ui_order_check.py
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
@pytest.mark.slow
class TestOrderCheckUI:
    """주문 조회 UI 테스트"""

    def test_user_can_search_order(self, page: Page, sample_order_in_db):
        """사용자가 UI에서 주문번호를 입력하면 주문 정보 표시"""
        # Given: 주문 조회 페이지 접속
        page.goto("http://localhost:8000/order-check")

        # When: 주문번호 입력
        page.fill("#order-number-input", "ORD-12345678")
        page.click("#search-button")

        # Then: 주문 정보 표시 확인
        expect(page.locator("#order-info")).to_be_visible()
        expect(page.locator("#order-number")).to_have_text("ORD-12345678")
        expect(page.locator("#customer-name")).to_have_text("홍길동")

    def test_user_sees_error_when_order_not_found(self, page: Page):
        """존재하지 않는 주문번호 조회 시 에러 메시지"""
        page.goto("http://localhost:8000/order-check")

        page.fill("#order-number-input", "ORD-NOTFOUND")
        page.click("#search-button")

        expect(page.locator("#message")).to_be_visible()
        expect(page.locator("#message")).to_have_class("message error")
        expect(page.locator("#order-info")).to_be_hidden()

    def test_user_can_search_by_pressing_enter(self, page: Page, sample_order_in_db):
        """Enter 키로 검색"""
        page.goto("http://localhost:8000/order-check")

        page.fill("#order-number-input", "ORD-12345678")
        page.press("#order-number-input", "Enter")

        expect(page.locator("#order-info")).to_be_visible()
```

**실행**:
```bash
# 헤드리스 모드 (브라우저 안 보임)
pytest tests/e2e/test_ui_order_check.py -v

# 브라우저 보면서 실행 (디버깅)
pytest tests/e2e/test_ui_order_check.py -v --headed --slowmo=500
```

---

#### 3.6.2 UI TDD의 장단점

**장점**:
- ✅ 실제 사용자 시나리오 검증
- ✅ UI 동작 자동 검증 (회귀 테스트)
- ✅ 리팩토링 시 안전성

**단점**:
- ❌ 느림 (브라우저 실행 오버헤드)
- ❌ 깨지기 쉬움 (CSS 선택자 변경 시)
- ❌ 작성/유지보수 비용 높음
- ❌ MVP에서는 과도함

---

#### 3.6.3 비용 대비 효과 분석

| 테스트 타입 | 작성 시간 | 유지보수 | 실행 속도 | ROI | 권장 |
|------------|----------|---------|----------|-----|------|
| **Unit** | 낮음 | 낮음 | 빠름 | 높음 | ✅ 많이 |
| **Integration** | 중간 | 중간 | 중간 | 높음 | ✅ 적당히 |
| **UI E2E** | 높음 | 높음 | 느림 | 낮음 | ⚠️ 최소한 |

**1-b 단계 권장**:
- Unit + Integration 테스트로 충분
- UI는 **수동 테스트**로 확인
- 핵심 플로우만 UI 테스트 (선택)

---

## 검토 요청 사항

### 1. Outside-In TDD 흐름
- ✅ E2E → API → Service → Repository 순서가 올바른지
- ✅ Mock 사용 시점 (Service 테스트)과 제거 시점 (통합 테스트)이 적절한지
- ⚠️ Step을 더 세분화하거나 병합해야 하는지

### 2. 테스트 조직화
- ✅ Unit / Integration / E2E 분리 기준이 적절한지
- ✅ Fixture 관리 전략 (전역 vs 레벨별 conftest)
- ⚠️ 테스트 데이터 관리 방식 (fixtures/ 모듈 분리)이 과도한지

### 3. 아키텍처
- ✅ 3-Layer 구조 (API → Service → Repository)가 MVP에 적절한지
- ⚠️ Service 레이어가 현재 단순 위임만 하는데 필요한지
- ⚠️ Pydantic 모델(OrderResponse)을 별도 파일로 분리해야 하는지

### 4. 누락된 테스트 케이스
- ⚠️ 주문번호 형식 검증 (예: `ORD-` 접두사 없으면?)
- ⚠️ SQL Injection 방어 테스트
- ⚠️ 동시성 테스트 (여러 요청 동시 처리)

### 5. 더 나은 패턴
- ⚠️ Repository에서 Connection을 매번 열고 닫는데, Connection Pool 사용해야 하는지
- ⚠️ `execute_update` 헬퍼가 실제로 유용한지 (1-b 단계에서는 UPDATE 사용 안 함)
- ⚠️ 비동기 SQLite(aiosqlite)로 전환해야 하는지

### 6. 테스트 성능
- ⚠️ DB 초기화를 매 테스트마다 하는 것이 너무 느린지
- ⚠️ 트랜잭션 롤백 방식으로 전환해야 하는지

### 7. 기타
- ⚠️ UI 테스트를 1-b 단계에서 구현해야 하는지, 아니면 전체 완성 후 추가해야 하는지
- ⚠️ 테스트 커버리지 목표 (현재 약 80-90% 예상)

---

**검토자께 드리는 질문**:
1. Outside-In TDD 방식이 올바르게 적용되었나요?
2. 테스트 조직화 전략(unit/integration/e2e)이 실무적으로 적절한가요?
3. 과도하거나 부족한 부분이 있나요?
4. 1-a 단계(주문 생성 + PayPal 결제)를 진행하기 전에 리팩토링해야 할 부분이 있나요?

---

**문서 작성일**: 2025-11-04
**작성자**: 태수
**목적**: 1-b 단계 구현 리허설에 대한 비판적 피드백 수집

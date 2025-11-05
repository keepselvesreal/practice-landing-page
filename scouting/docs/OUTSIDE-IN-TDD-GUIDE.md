---
version: 1
created_date: 25-11-04
note: 1-b단계 시작 전 필수 TDD 학습 자료
---

# Outside-In TDD 최소 학습 가이드

> **목표**: 1-b단계 시작 전 필수 개념 이해하기
> **소요 시간**: 30분 읽기 + 30분 실습

---

## 1. Outside-In TDD란?

### 핵심 아이디어

**"사용자가 보는 것부터 테스트하고, 점점 안쪽으로 들어간다"**

```
Outside (사용자 관점)
  ↓
API/Controller (인터페이스)
  ↓
Service/Business Logic (비즈니스 로직)
  ↓
Repository/Database (데이터 접근)
  ↓
Inside (구현 세부사항)
```

### 왜 Outside-In인가?

**전통적 TDD (Inside-Out)**:
```
1. DB 함수 작성 (get_order_from_db)
2. Service 함수 작성 (get_order_service)
3. API 엔드포인트 작성 (GET /orders/{id})
4. "어? 사용자가 원하는 게 이게 아니었네?"
```

**Outside-In TDD**:
```
1. 사용자 시나리오 테스트 작성 ("주문번호 입력하면 정보 보여줘")
2. API 테스트 작성 (GET /orders/{order_number} → 200)
3. Service 로직 작성 (필요한 것만)
4. DB 함수 작성 (필요한 것만)
→ 사용자가 원하는 것만 정확히 구현
```

---

## 2. Red-Green-Refactor 사이클

### 기본 순서

```
┌─────────────────────────────────────┐
│ Red: 실패하는 테스트 작성            │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ Green: 최소한의 코드로 테스트 통과   │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ Refactor: 코드 개선 (테스트 그대로)  │
└─────────────────────────────────────┘
         ↓ (다음 테스트로)
       (반복)
```

### 구체적 예시: 주문 조회 API

#### Red (실패하는 테스트)
```python
# tests/test_orders.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_order_by_number():
    """주문번호로 주문 조회 가능"""
    response = client.get("/orders/ORD-12345678")
    assert response.status_code == 200

# 실행: pytest
# 결과: FAILED (404 Not Found - 엔드포인트 없음)
```

#### Green (최소 코드로 통과)
```python
# app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/orders/{order_number}")
def get_order(order_number: str):
    return {}  # 일단 빈 딕셔너리

# 실행: pytest
# 결과: PASSED (200 반환)
```

#### Refactor (개선)
```python
# 다음 테스트 추가: 응답에 order_number 포함되어야 함
def test_get_order_returns_order_number():
    response = client.get("/orders/ORD-12345678")
    assert response.json()["order_number"] == "ORD-12345678"

# 실행: pytest
# 결과: FAILED (KeyError: 'order_number')

# 코드 수정
@app.get("/orders/{order_number}")
def get_order(order_number: str):
    return {"order_number": order_number}

# 실행: pytest
# 결과: PASSED
```

---

## 3. Mock과 Stub

### Stub: 가짜 응답 제공

**언제 사용?**: DB나 외부 API 없이 빠르게 테스트하고 싶을 때

```python
# 실제 DB 함수
def get_order_from_db(order_number: str):
    conn = sqlite3.connect("database.db")
    # ... DB 조회 로직
    return order

# Stub (가짜 함수)
def fake_get_order(order_number: str):
    return {
        "order_number": "ORD-12345678",
        "customer_name": "홍길동",
        "total_amount": 57500
    }

# 테스트에서 Stub 사용
def test_get_order_api(monkeypatch):
    # 실제 DB 함수를 Stub으로 교체
    monkeypatch.setattr("app.database.get_order_from_db", fake_get_order)

    response = client.get("/orders/ORD-12345678")
    assert response.json()["customer_name"] == "홍길동"

# DB 없이도 API 테스트 가능!
```

### Mock: 호출 검증

**언제 사용?**: "이 함수가 제대로 호출됐는지" 확인하고 싶을 때

```python
from unittest.mock import Mock

def test_verify_payment_calls_paypal_api():
    # Mock 객체 생성
    mock_paypal = Mock()
    mock_paypal.capture_order.return_value = {"status": "COMPLETED"}

    # 테스트 대상 함수
    service = PaymentService(paypal_client=mock_paypal)
    service.verify_payment("PAYPAL-ORDER-123")

    # 검증: capture_order가 정확한 인자로 호출됐는지
    mock_paypal.capture_order.assert_called_once_with("PAYPAL-ORDER-123")
```

### Stub vs Mock 비교

| 특징 | Stub | Mock |
|-----|------|------|
| 목적 | 가짜 응답 제공 | 호출 검증 |
| 사용 예 | DB 대신 고정 데이터 반환 | "PayPal API가 호출됐나?" 확인 |
| 검증 | 반환값 검증 (`assert result == ...`) | 호출 여부 검증 (`assert_called_with`) |

---

## 4. Outside-In TDD 진행 순서 (1-b 예시)

### 전체 레이어 구조
```
E2E (End-to-End)
  ↓
API (FastAPI 엔드포인트)
  ↓
Service (비즈니스 로직)
  ↓
Repository (DB 접근)
```

### Step-by-Step 진행

---

#### Step 1: E2E 테스트 (가장 바깥)

**목표**: 사용자 시나리오 검증

```python
# tests/test_e2e_orders.py
def test_user_can_check_order():
    """
    사용자가 주문번호를 입력하면 주문 정보를 볼 수 있다
    """
    # Given: DB에 주문 데이터 준비
    setup_test_order("ORD-12345678", customer_name="홍길동")

    # When: API 호출
    response = client.get("/orders/ORD-12345678")

    # Then: 성공 응답 + 주문 정보 포함
    assert response.status_code == 200
    assert response.json()["customer_name"] == "홍길동"

# 실행: pytest
# 결과: FAILED (404 - 엔드포인트 없음)
```

**해결**: 엔드포인트만 추가 (빈 응답)

```python
# app/main.py
@app.get("/orders/{order_number}")
def get_order(order_number: str):
    return {}

# 실행: pytest
# 결과: 여전히 FAILED (customer_name 없음)
```

---

#### Step 2: API 응답 형식 테스트

**목표**: 응답에 필요한 필드 포함

```python
# tests/test_api_orders.py
def test_get_order_returns_customer_info(monkeypatch):
    """응답에 고객 정보 포함"""
    # Stub으로 Service 함수 대체
    def fake_service(order_number):
        return {
            "order_number": order_number,
            "customer_name": "홍길동",
            "total_amount": 57500
        }

    monkeypatch.setattr("app.routers.orders.get_order_service", fake_service)

    response = client.get("/orders/ORD-12345678")
    data = response.json()

    assert data["order_number"] == "ORD-12345678"
    assert data["customer_name"] == "홍길동"
    assert data["total_amount"] == 57500

# 실행: pytest
# 결과: FAILED (get_order_service 없음)
```

**해결**: Service 함수 호출 추가 (아직 Mock)

```python
# app/routers/orders.py
from app.services.orders import get_order_service

@app.get("/orders/{order_number}")
def get_order(order_number: str):
    order = get_order_service(order_number)
    return order

# app/services/orders.py
def get_order_service(order_number: str):
    # 아직 구현 안 함, 나중에 Repository 호출할 예정
    pass

# 실행: pytest (with Stub)
# 결과: PASSED
```

---

#### Step 3: Service 로직 테스트

**목표**: Service가 Repository를 제대로 호출하는지 검증

```python
# tests/test_service_orders.py
def test_get_order_service_calls_repository():
    """get_order_service가 Repository를 호출"""
    from unittest.mock import Mock

    mock_repo = Mock()
    mock_repo.get_order_by_number.return_value = {
        "order_number": "ORD-12345678",
        "customer_name": "홍길동"
    }

    # Service에 Mock Repository 주입
    service = OrderService(repository=mock_repo)
    result = service.get_order("ORD-12345678")

    # 검증
    mock_repo.get_order_by_number.assert_called_once_with("ORD-12345678")
    assert result["customer_name"] == "홍길동"

# 실행: pytest
# 결과: FAILED (OrderService 클래스 없음)
```

**해결**: Service 클래스 작성

```python
# app/services/orders.py
class OrderService:
    def __init__(self, repository):
        self.repository = repository

    def get_order(self, order_number: str):
        return self.repository.get_order_by_number(order_number)

# 실행: pytest
# 결과: PASSED
```

---

#### Step 4: Repository/DB 테스트

**목표**: 실제 DB 조회 로직 구현

```python
# tests/test_repository_orders.py
def test_get_order_by_number_from_db():
    """DB에서 주문번호로 조회"""
    # Given: 테스트 DB 준비
    conn = sqlite3.connect(":memory:")  # 메모리 DB
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE orders (
            order_number TEXT,
            customer_name TEXT,
            total_amount INTEGER
        )
    """)
    cursor.execute("""
        INSERT INTO orders VALUES ('ORD-12345678', '홍길동', 57500)
    """)
    conn.commit()

    # When: Repository 호출
    repo = OrderRepository(conn)
    order = repo.get_order_by_number("ORD-12345678")

    # Then: 올바른 데이터 반환
    assert order["customer_name"] == "홍길동"
    assert order["total_amount"] == 57500

# 실행: pytest
# 결과: FAILED (OrderRepository 없음)
```

**해결**: Repository 클래스 작성

```python
# app/repositories/orders.py
class OrderRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_order_by_number(self, order_number: str):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT order_number, customer_name, total_amount
            FROM orders
            WHERE order_number = ?
        """, (order_number,))

        row = cursor.fetchone()
        if not row:
            return None

        return {
            "order_number": row[0],
            "customer_name": row[1],
            "total_amount": row[2]
        }

# 실행: pytest
# 결과: PASSED
```

---

#### Step 5: 통합 테스트 (Mock 제거)

**목표**: 모든 레이어 연결해서 E2E 테스트 통과

```python
# tests/test_e2e_orders.py (다시)
def test_user_can_check_order():
    """이번엔 Mock 없이 전체 플로우 테스트"""
    # Given: 실제 DB에 데이터 삽입
    conn = get_test_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (order_number, customer_name, total_amount)
        VALUES ('ORD-12345678', '홍길동', 57500)
    """)
    conn.commit()

    # When: API 호출 (Mock 없음, 실제 DB 사용)
    response = client.get("/orders/ORD-12345678")

    # Then: 성공
    assert response.status_code == 200
    assert response.json()["customer_name"] == "홍길동"

# 실행: pytest
# 결과: PASSED ✅
```

---

## 5. pytest 기본 사용법

### 설치
```bash
uv add pytest pytest-mock
```

### 테스트 파일 구조
```
tests/
├── test_e2e_orders.py      # E2E 테스트
├── test_api_orders.py      # API 테스트
├── test_service_orders.py  # Service 테스트
└── test_repository_orders.py  # Repository 테스트
```

### 테스트 실행
```bash
# 모든 테스트 실행
pytest

# 특정 파일만
pytest tests/test_api_orders.py

# 특정 테스트만
pytest tests/test_api_orders.py::test_get_order_returns_customer_info

# 상세 출력
pytest -v

# 실패한 것만 재실행
pytest --lf
```

### Fixture 사용 (테스트 데이터 준비)

```python
# tests/conftest.py (모든 테스트에서 공유)
import pytest
import sqlite3

@pytest.fixture
def test_db():
    """테스트용 DB 생성"""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE orders (
            order_number TEXT,
            customer_name TEXT,
            total_amount INTEGER
        )
    """)
    conn.commit()
    yield conn  # 테스트에 전달
    conn.close()  # 테스트 후 정리

# 사용
def test_something(test_db):
    cursor = test_db.cursor()
    cursor.execute("INSERT INTO orders ...")
    # ...
```

---

## 6. FastAPI TestClient 사용법

### 기본 사용
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_order():
    response = client.get("/orders/ORD-12345678")
    assert response.status_code == 200
    assert response.json()["order_number"] == "ORD-12345678"
```

### POST 요청
```python
def test_create_order():
    response = client.post("/orders", json={
        "customer_name": "홍길동",
        "quantity": 2
    })
    assert response.status_code == 201
    assert "order_number" in response.json()
```

### 헤더 추가 (관리자 인증)
```python
def test_admin_endpoint():
    response = client.patch(
        "/admin/shipments/1",
        headers={"X-Admin-Key": "secret-key"},
        json={"status": "SHIPPED"}
    )
    assert response.status_code == 200
```

---

## 7. pytest-mock 사용법

### monkeypatch (함수 교체)
```python
def test_with_stub(monkeypatch):
    def fake_db_query(order_number):
        return {"customer_name": "홍길동"}

    monkeypatch.setattr("app.database.get_order", fake_db_query)

    # 이제 get_order 호출 시 fake_db_query가 대신 실행됨
    result = app.database.get_order("ORD-12345678")
    assert result["customer_name"] == "홍길동"
```

### Mock 객체 (호출 검증)
```python
from unittest.mock import Mock

def test_service_calls_paypal():
    mock_paypal = Mock()
    mock_paypal.create_order.return_value = {"id": "PAYPAL-123"}

    service = PaymentService(paypal=mock_paypal)
    service.create_payment(amount=57500)

    # 검증: create_order가 호출됐는지
    mock_paypal.create_order.assert_called_once()

    # 검증: 정확한 인자로 호출됐는지
    mock_paypal.create_order.assert_called_with(amount=57500)
```

---

## 8. 최소 학습 체크리스트

### ✅ 개념 이해 (5분)
- [ ] "Outside-In이 뭔지" 한 문장으로 설명할 수 있다
  - **답**: 사용자 관점(E2E)부터 테스트하고 점점 내부(DB)로 들어간다
- [ ] Red-Green-Refactor 순서를 말할 수 있다
  - **답**: 실패 테스트 → 최소 코드로 통과 → 개선
- [ ] Stub과 Mock의 차이를 설명할 수 있다
  - **답**: Stub은 가짜 응답, Mock은 호출 검증

### ✅ 도구 사용법 (10분)
- [ ] pytest 실행 명령어 (`pytest`, `pytest -v`)
- [ ] TestClient로 GET 요청 테스트
  ```python
  response = client.get("/orders/ORD-12345678")
  assert response.status_code == 200
  ```
- [ ] monkeypatch로 함수 교체 (Stub)
- [ ] Mock으로 호출 검증

### ✅ 실습 (15분)
**간단한 연습 문제**:
```python
# 목표: 이 테스트를 통과시키기

def test_hello_endpoint():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "hello"}

# 1. app/main.py에 엔드포인트 추가
# 2. pytest 실행해서 통과 확인
```

**정답**:
```python
# app/main.py
@app.get("/hello")
def hello():
    return {"message": "hello"}
```

---

## 9. 1-b단계 시작 전 준비

### 환경 설정
```bash
# 프로젝트 디렉토리로 이동
cd /home/nadle/para/projects/practice-landing-page/scouting

# uv 프로젝트 초기화
uv init

# 의존성 추가
uv add fastapi uvicorn pytest pytest-mock
```

### 첫 테스트 작성
```python
# tests/test_hello.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
```

### 테스트 실행
```bash
pytest tests/test_hello.py -v
```

**실패하면 정상!** (Red 단계)
→ `app/main.py`에 엔드포인트 추가
→ 다시 실행 → 통과 (Green 단계)

---

## 10. 학습 자료 추천

### 최소한만 보려면 (30분)
1. **5분 영상**: "TDD in Python with pytest" (YouTube)
2. **10분 읽기**: pytest 공식 문서 "Getting Started"
3. **15분 실습**: 위의 연습 문제 풀기

### 제대로 배우려면 (3시간)
1. **책**: "Test Driven Development: By Example" (Kent Beck) - Chapter 1-3
2. **영상**: "Outside-In TDD" (Sandro Mancuso, 1시간)
3. **실습**: Todo API를 Outside-In TDD로 만들어보기

### 추가 자료
- [pytest 공식 문서](https://docs.pytest.org/)
- [FastAPI Testing 문서](https://fastapi.tiangolo.com/tutorial/testing/)
- [Martin Fowler - Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)

---

## 11. FAQ

### Q1: 모든 기능을 TDD로 개발해야 하나?
**A**: 핵심 비즈니스 로직만. HTML/CSS는 TDD 안 해도 됨.

### Q2: 테스트 작성이 너무 느린데?
**A**: 처음엔 느림. 5-10개 테스트 작성하면 익숙해짐.

### Q3: Mock을 남발하면 테스트가 깨지기 쉬운데?
**A**: 맞음. Mock은 외부 의존성(DB, API)에만 사용. 내부 함수는 실제로 호출.

### Q4: E2E 테스트가 너무 느린데?
**A**: 메모리 DB(`:memory:`) 사용하면 빠름. 또는 E2E는 핵심 시나리오만.

### Q5: 테스트 없이 먼저 구현하고 나중에 테스트 작성하면?
**A**: 그건 TDD가 아님. 테스트를 먼저 작성해야 "필요한 것만" 구현함.

---

## 12. 다음 단계

### 준비 완료 체크
- [ ] Outside-In 개념 이해
- [ ] pytest 설치 및 실행 확인
- [ ] TestClient 사용법 확인
- [ ] 간단한 테스트 작성 및 통과 경험

### 1-b단계 시작
1. `IMPLEMENTATION-PLAN.md`의 "1-b단계" 섹션 읽기
2. 첫 E2E 테스트 작성:
   ```python
   def test_user_can_check_order_by_order_number():
       # ...
   ```
3. Red-Green-Refactor 사이클 시작

---

**행운을 빌어! 막히는 부분 있으면 언제든 물어봐.**

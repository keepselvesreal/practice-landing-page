# 개발 환경 가이드

## 초기 설정

### 1. DB 마이그레이션 적용
```bash
uv run alembic upgrade head
```

### 2. 초기 데이터 생성
```bash
uv run python -m backend.db.seed
```

### 3. 개발 서버 실행
```bash
./scripts/dev.sh
```

또는 직접:
```bash
uv run uvicorn backend.main:app --reload
```

## 주요 엔드포인트

- **메인 페이지**: http://localhost:8000/
- **주문 조회 페이지**: http://localhost:8000/order-check.html
- **API 문서**: http://localhost:8000/docs

## DB 관리

### 마이그레이션 생성
```bash
uv run alembic revision --autogenerate -m "변경 내용"
```

### 마이그레이션 적용
```bash
uv run alembic upgrade head
```

### 마이그레이션 롤백
```bash
uv run alembic downgrade -1
```

### 현재 마이그레이션 버전 확인
```bash
uv run alembic current
```

### DB 초기화 (개발용)
```bash
# 1. 모든 마이그레이션 롤백
uv run alembic downgrade base

# 2. 다시 적용
uv run alembic upgrade head

# 3. Seed 데이터 생성
uv run python -m backend.db.seed
```

## 테스트 실행

### 전체 테스트
```bash
uv run pytest
```

### 특정 테스트만
```bash
uv run pytest tests/e2e/test_order_creation_flow.py
```

### Coverage 확인
```bash
uv run pytest --cov=backend --cov-report=html
open htmlcov/index.html
```

## DB 직접 접속

```bash
psql -U nadle -d k_beauty_landing_page
```

유용한 쿼리:
```sql
-- 모든 주문 조회
SELECT order_number, order_status, created_at FROM orders;

-- 상품 재고 확인
SELECT name, stock FROM products;

-- 배송 정보 조회
SELECT o.order_number, s.shipping_status, s.tracking_number
FROM orders o
LEFT JOIN shipments s ON o.id = s.order_id;
```

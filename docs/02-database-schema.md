---
version: 1
created_date: 25-11-07 15:38
note:
---

## 메모

### products
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,              -- 센타보(centavo) 단위 (페소 × 100)
    stock INTEGER NOT NULL DEFAULT 10
);
```

---

### orders
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_number TEXT UNIQUE NOT NULL,  -- ORD-XXXXXXXX (8자리 랜덤)

    -- 구매자 정보 (암호화 저장)
    customer_name TEXT NOT NULL,        -- Fernet 암호화
    customer_email TEXT NOT NULL,       -- Fernet 암호화
    customer_phone TEXT NOT NULL,       -- Fernet 암호화
    shipping_address TEXT NOT NULL,     -- Fernet 암호화

    -- 주문 정보
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price INTEGER NOT NULL,        -- 센타보 단위
    shipping_fee INTEGER NOT NULL DEFAULT 10000,  -- 100페소 (10000센타보)
    total_amount INTEGER NOT NULL,      -- 센타보 단위

    -- 어필리에이트 정보
    affiliate_code TEXT,                -- NULL 가능 (어필리에이트 없으면)

    -- PayPal 결제 정보
    paypal_order_id TEXT UNIQUE,
    paypal_transaction_id TEXT,

    -- 주문 상태 (단일 상태로 통합)
    order_status TEXT DEFAULT 'PAYMENT_PENDING',

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (affiliate_code) REFERENCES affiliates(affiliate_code),
    CHECK (total_amount = (unit_price * quantity) + shipping_fee)
);

-- 인덱스
CREATE INDEX idx_orders_order_number ON orders(order_number);
CREATE INDEX idx_orders_paypal_order_id ON orders(paypal_order_id);
CREATE INDEX idx_orders_status ON orders(order_status);
CREATE INDEX idx_orders_affiliate_code ON orders(affiliate_code);
```

---

### shipments
```sql
CREATE TABLE shipments (
    id SERIAL PRIMARY KEY,
    order_id INTEGER UNIQUE NOT NULL,

    -- 배송 정보
    shipping_status TEXT DEFAULT 'PREPARING',

    tracking_number TEXT,
    courier TEXT,

    shipped_at TIMESTAMP WITH TIME ZONE,
    delivered_at TIMESTAMP WITH TIME ZONE,
    returned_at TIMESTAMP WITH TIME ZONE,              -- 환불 시 물품 반송 확인

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

---

### refunds
```sql
CREATE TABLE refunds (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    paypal_refund_id TEXT,
    refund_amount INTEGER NOT NULL,     -- 센타보 단위
    refund_reason TEXT,
    refund_status TEXT DEFAULT 'PENDING',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

---

### affiliates (신규)
```sql
CREATE TABLE affiliates (
    id SERIAL PRIMARY KEY,
    affiliate_code TEXT UNIQUE NOT NULL,
    influencer_name TEXT NOT NULL,
    commission_rate INTEGER NOT NULL DEFAULT 20,  -- 20% (기본값)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스
CREATE INDEX idx_affiliates_code ON affiliates(affiliate_code);
```

---

### affiliate_stats (신규)
```sql
CREATE TABLE affiliate_stats (
    id SERIAL PRIMARY KEY,
    affiliate_code TEXT UNIQUE NOT NULL,

    click_count INTEGER DEFAULT 0,
    sale_count INTEGER DEFAULT 0,
    total_commission INTEGER DEFAULT 0,    -- 센타보 단위
    pending_commission INTEGER DEFAULT 0,   -- 센타보 단위

    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (affiliate_code) REFERENCES affiliates(affiliate_code)
);
```

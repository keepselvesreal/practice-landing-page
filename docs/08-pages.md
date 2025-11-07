---
version: 1
created_date: 25-11-07 15:38
note:
---

## 메모

### 사용자 페이지

#### 1. 메인 랜딩페이지 (`/`)
- 제품 이미지 갤러리 (신규)
- 제품 상세 설명 (신규)
- **언어 토글 (영어 ⇄ Tagalog)** (신규)
- 상품 정보 표시
- 구매자 정보 입력 폼 (이름, 이메일, 전화번호, 배송지)
- 수량 선택
- 배송비 표시: "배송비: ₱100"
- 최종 금액 표시: "총 금액: ₱675"
- PayPal 결제 버튼
- **문의 버튼** (신규)

#### 2. 주문 조회 페이지 (`/order-check`)
- 주문번호 입력
- 주문 정보 표시 (구매자 정보, 주문 상품, 수량, 금액)
- **배송비 표시** (신규)
- 배송 상태 표시 (2단계 이후)
- **주문 취소 버튼 (배송 전)** (신규)
- 환불 요청 버튼 (3단계 이후, 조건부 활성화)
- 환불 상태 표시 (3단계 이후)

#### 3. 인플루언서 대시보드 (`/affiliate/stats/{code}`) (신규)
- 총 클릭 수 표시
- 판매 건수 표시
- 누적 수익 표시
- 대기 중 수수료 표시
- **인증 불필요** (public 페이지)

---

### 관리자 페이지

#### 1. 배송 상태 변경 (`/admin/shipments`)
- 주문 목록 표시
- 배송 상태 변경 (PREPARING → SHIPPED → DELIVERED)
- 송장번호, 택배사 입력
- **인증**: API 키 (헤더: `X-Admin-Key`)

#### 2. 환불 처리 (`/admin/refunds`)
- 환불 요청 목록 표시 (주문번호, 환불 사유, 배송 상태 포함)
- 환불 사유 확인
- 승인 버튼 (confirm 후 PayPal 환불 처리)
- **물품 반송 확인 버튼** (`DELIVERED` 상태 환불 시만 표시)
  - API: `POST /admin/shipments/{order_id}/return-confirm`
  - 반송 확인 시: `shipments.returned_at` 기록 → 재고 자동 복구
  - UI: 배송 상태가 `DELIVERED`이고 환불 승인된 경우에만 활성화
- **인증**: API 키 (헤더: `X-Admin-Key`)

#### 3. 어필리에이트 관리 (`/admin/affiliates`) (신규)
- 어필리에이트 목록 조회
- 새 어필리에이트 코드 생성
- 커미션 비율 설정

#### 4. 재고 관리 (`/admin/inventory`) (신규)
- 재고 수량 조회
- 재고 수량 수동 조정

#### 5. 판매 리포트 (`/admin/reports/sales`) (신규)
- 총 판매 건수
- 총 매출액
- 어필리에이트별 판매 현황

---

### API 엔드포인트

#### 사용자 API
```
POST   /api/orders                      # 주문 생성
GET    /api/orders/{order_number}       # 주문 조회
POST   /api/orders/{order_id}/cancel    # 주문 취소 (신규)
POST   /api/refunds                     # 환불 요청
POST   /api/payment/verify              # PayPal 결제 검증
GET    /api/products/{product_id}       # 제품 정보 조회 (신규)
POST   /api/contact                     # 문의 (신규)
GET    /api/affiliate/track?code={code} # 어필리에이트 클릭 추적 (신규)
```

#### 어필리에이트 API
```
GET    /affiliate/stats/{code}          # 인플루언서 대시보드 (신규)
```

#### 관리자 API (X-Admin-Key 헤더 필수)
```
GET    /admin/orders                             # 주문 목록 조회
PATCH  /admin/shipments/{order_id}              # 배송 상태 변경
GET    /admin/refunds                           # 환불 요청 목록
POST   /admin/refunds/{refund_id}/approve       # 환불 승인
POST   /admin/shipments/{order_id}/return-confirm  # 반송 확인
POST   /admin/affiliates                        # 어필리에이트 생성 (신규)
GET    /admin/affiliates                        # 어필리에이트 목록 (신규)
PATCH  /admin/inventory/{product_id}            # 재고 수동 조정 (신규)
GET    /admin/reports/sales                     # 판매 리포트 (신규)
```

---

### 미반영 요구사항
- REQ-F13: 문의 기능 (UI만 추가, API 구현 필요)

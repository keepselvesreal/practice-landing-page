---
version: 1
created_date: 25-11-07 15:38
note:
---

## 메모

### Gmail SMTP 발송
- **발송 서비스**: Gmail SMTP
- **일일 한도**: 500통 (무료 Gmail 계정)
- **제한 초과 시**: Google Workspace 계정 또는 SendGrid 등 전환 고려

---

### 템플릿 종류

#### 1. 주문 확인 이메일
**발송 시점**: 결제 완료 시 (`PAID` 상태 전환)

**내용:**
- 주문번호
- 구매 상품명, 수량, 금액
- 배송비
- 총 결제 금액
- 배송 예정 안내

**미반영 사항**: 자동 발송 로직 구현 필요

---

#### 2. 배송 완료 이메일
**발송 시점**: 배송 완료 시 (`DELIVERED` 상태 전환)

**내용:**
- 주문번호
- 배송 완료 안내
- 운송장 번호
- 택배사 정보
- 문의 연락처

**미반영 사항**: 자동 발송 로직 구현 필요

---

#### 3. 재구매 확인 이메일
**발송 시점**: 배송 완료 후 N일 경과 (예: 30일 후)

**내용:**
- 재구매 할인 쿠폰 (선택사항)
- 제품 리뷰 요청
- 재구매 링크

**미반영 사항**: 자동 발송 로직 및 발송 시점 결정 필요

---

#### 4. 취소 확인 이메일
**발송 시점**: 주문 취소 시 (`CANCELLED` 상태 전환)

**내용:**
- 주문번호
- 취소 완료 안내
- 환불 금액 (전액: 상품가 + 배송비)
- 환불 처리 기간 안내

**미반영 사항**: 자동 발송 로직 구현 필요

---

### HTML 템플릿 예시
```html
<!-- 주문 확인 이메일 -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: Arial, sans-serif; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { background-color: #4CAF50; color: white; padding: 20px; text-align: center; }
    .content { padding: 20px; }
    .footer { text-align: center; color: #888; font-size: 12px; margin-top: 20px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>주문이 완료되었습니다!</h1>
    </div>
    <div class="content">
      <p>안녕하세요, {{ customer_name }}님</p>
      <p>주문번호: <strong>{{ order_number }}</strong></p>

      <h3>주문 상품</h3>
      <ul>
        <li>{{ product_name }} x {{ quantity }}</li>
        <li>상품가: ₱{{ unit_price }}</li>
        <li>배송비: ₱100</li>
        <li><strong>총 금액: ₱{{ total_amount }}</strong></li>
      </ul>

      <p>배송 주소: {{ shipping_address }}</p>
      <p>곧 배송 준비를 시작하겠습니다.</p>
    </div>
    <div class="footer">
      <p>문의사항이 있으시면 {{ contact_email }}로 연락주세요.</p>
    </div>
  </div>
</body>
</html>
```

---

### 미반영 요구사항
- REQ-F09~F11, F28: 이메일 자동 발송 로직 구현 필요
  - 각 상태 전환 시 트리거 설정
  - 템플릿 엔진 통합 (Jinja2 등)
  - 발송 실패 시 재시도 로직

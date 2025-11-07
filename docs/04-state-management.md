---
version: 1
created_date: 25-11-07 15:38
note:
---

## 메모

### 주문 상태 (order_status) - 단일 상태로 통합
- `PAYMENT_PENDING`: 결제 대기 (주문 생성 직후)
- `VERIFICATION_PENDING`: 결제 검증 중 (PayPal API 타임아웃 시)
- `PAID`: 결제 완료 (재고 차감됨)
- `PAYMENT_FAILED`: 결제 실패
- `CANCELLED`: 주문 취소
- `REFUNDED`: 환불 완료

---

### 배송 상태 (shipping_status)
- `PREPARING`: 배송 준비 중
- `SHIPPED`: 배송 중
- `DELIVERED`: 배송 완료

---

### 환불 상태 (refund_status)
- `PENDING`: 환불 대기
- `COMPLETED`: 환불 완료
- `FAILED`: 환불 실패

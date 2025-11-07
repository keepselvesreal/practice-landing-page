---
version: 1
created_date: 25-11-07 15:38
note:
---

## 메모

### HTTP 상태 코드
```
200: 성공
201: 생성 성공 (주문 생성)
400: 입력 오류 (이메일 형식, 수량 등)
401: 인증 실패 (관리자 API)
404: 리소스 없음 (주문번호 조회 실패)
409: 재고 부족
500: 서버 오류
```

---

### 에러 응답 형식
```json
{
  "error": "재고가 부족합니다",
  "code": "STOCK_INSUFFICIENT",
  "details": {
    "requested": 5,
    "available": 3
  }
}
```

---

### PayPal API 타임아웃 처리

**1. 타임아웃 발생 시:**
- `order_status` → `VERIFICATION_PENDING`
- 재고는 차감하지 않음
- 사용자에게: "결제 확인 중입니다. 주문번호: ORD-XXX"

**2. 백그라운드 재시도 (Cloud Scheduler, 5분마다 실행):**
- 성공 시: `PAID` + 재고 차감
- 실패 시: `PAYMENT_FAILED`

**3. 3회 재시도 실패 시:**
- 관리자 대시보드에 "수동 확인 필요" 플래그
- 관리자가 PayPal 대시보드에서 직접 확인 후 처리

---

### 결제 중복 방지 (Idempotency)
- `paypal_order_id`를 UNIQUE 제약으로 중복 방지
- 재시도 전 DB 조회로 이미 처리된 주문 확인
- 동일 PayPal Order ID로 재요청 시 기존 주문 정보 반환

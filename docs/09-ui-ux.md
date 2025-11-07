---
version: 1
created_date: 25-11-07 15:38
note:
---

## 메모

### 에러/성공 메시지
- 인라인 메시지 영역 사용
- 성공: 초록색 배경 (`#4CAF50`)
- 에러: 빨간색 배경 (`#f44336`)
- 3-5초 후 자동 사라짐 (선택 사항)

```html
<div id="message" class="message success" style="display:none;">
  주문이 생성되었습니다. 주문번호: ORD-12345678
</div>
```

---

### 버튼 활성화/비활성화 규칙

**환불 요청 버튼:**
- 활성화: `order_status = PAID` AND 환불 미요청
- 비활성화: 환불 요청 중(`PENDING`) 또는 환불 완료(`COMPLETED`)
- 비활성화 시 상태 텍스트 표시 ("환불 진행 중", "환불 완료")

**주문 취소 버튼 (신규):**
- 활성화: `order_status = PAID` AND `shipping_status = PREPARING`
- 비활성화: 배송 시작 후 (`SHIPPED`, `DELIVERED`)

---

### 주문번호 형식
- `ORD-XXXXXXXX` (ORD- 접두사 + 8자리 랜덤 영숫자, 대문자)
- 충돌 시 최대 3회 재시도

---

### 다국어 UI (신규)
- 언어 토글 버튼: 우측 상단 고정
- 영어 ⇄ Tagalog 전환
- 로컬 스토리지에 선택 언어 저장
- 페이지 새로고침 시에도 유지

---
version: 1
created_date: 25-11-07 15:38
note:
---

## 메모

### [Outside-In TDD](outside-in-tdd-guide)
- 모든 핵심 기능은 TDD로 개발
- E2E 테스트부터 시작하여 내부 구현으로 진행
- Red-Green-Refactor 사이클 준수

---

### 단계별 구현 순서
1. **1-b단계**: 주문 조회 API (Mock 데이터)
2. **1-a단계**: 주문 생성 + PayPal 결제 + 재고 차감
3. **2단계**: 배송 추적 시스템
4. **3단계**: 환불 시스템
5. **추가 기능**: 어필리에이트, 다국어, 이메일 자동 발송

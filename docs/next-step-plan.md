📋 다음 단계 상세 계획

  1-c 단계: PayPal Webhook 기반 결제 완료 플로우

  스토리: "고객이 PayPal에서 결제를 완료하면 주문이 확정되고 확인 이메일을 받는다"

  구현 항목

  1. PayPal Webhook 엔드포인트
    - POST /webhooks/paypal
    - Webhook 서명 검증
    - 이벤트 타입 처리:
        - PAYMENT.CAPTURE.COMPLETED → 주문 상태 PAID
      - PAYMENT.CAPTURE.DENIED → 재고 복원
  2. 재고 차감 로직 리팩터링 ⭐
    - 현재: 주문 생성 시 차감 (orders.py:92)
    - 수정: Webhook 수신 시 차감
    - 주문 생성 시에는 재고 예약만 (옵션)
  3. Gmail SMTP 이메일 발송
    - 환경 설정: GMAIL_ADDRESS, GMAIL_APP_PASSWORD
    - 주문 확인 이메일 템플릿
    - 결제 완료 시 자동 발송
  4. 테스트
    - Webhook Mock으로 결제 완료/실패 시뮬레이션
    - 재고 차감 검증
    - 이메일 발송 확인 (테스트 환경)

  예상 작업 시간: 3-4시간

  ---
  2단계: 배송 추적 시스템

  스토리: "관리자가 배송 상태를 업데이트하고 고객이 배송 정보를 확인할 수 있다"

  구현 항목

  1. shipments 테이블 및 모델
    - shipment_status: PREPARING → SHIPPED → DELIVERED
    - tracking_number, carrier 필드
  2. 관리자 배송 관리 API
    - PATCH /admin/shipments/{id} - 배송 상태 업데이트
    - POST /admin/shipments/{id}/tracking - 운송장 등록
  3. 배송 완료 이메일
    - DELIVERED 상태 전환 시 자동 발송
    - 운송장 번호 포함
  4. 테스트
    - 배송 상태 전환 플로우
    - 배송 완료 이메일 발송

  예상 작업 시간: 2-3시간

  ---
  3단계: 주문 조회 페이지 (UI)

  스토리: "고객이 웹페이지에서 주문 번호로 주문 상태와 배송 정보를 확인한다"

  구현 항목

  1. 주문 조회 페이지 (/order-check)
    - 주문 번호 입력 폼
    - 주문 정보 표시 (상품, 금액, 상태)
    - 배송 정보 표시 (운송장, 배송 상태)
  2. E2E 테스트
    - 주문 번호 입력 → 정보 표시
    - 배송 상태별 UI 변화

  예상 작업 시간: 1-2시간

  ---
  4단계: 취소/환불

  4-a: 주문 취소

  스토리: "고객이 배송 전 주문을 취소하고 전액 환불받는다"

  구현 항목

  1. 주문 취소 API
    - POST /api/orders/{order_number}/cancel
    - 조건 검증: PAID + PREPARING
    - 전액 환불 + 재고 복원
  2. UI
    - 주문 조회 페이지에 "취소" 버튼 (PREPARING일 때만)
  3. 테스트
    - 취소 가능/불가 조건 검증
    - 재고 복원 확인

  예상 작업 시간: 1.5-2시간

  ---
  4-b: 환불 시스템

  스토리: "고객이 배송 후 환불을 요청하고 관리자가 승인하면 환불받는다"

  구현 항목

  1. refunds 테이블 및 모델
    - refund_status: PENDING → APPROVED → COMPLETED
    - refund_reason, refund_amount
  2. 환불 요청 API
    - POST /api/orders/{order_number}/refunds
    - 조건: PAID + (SHIPPED or DELIVERED)
    - refunds 레코드 생성
  3. 관리자 환불 승인 API
    - POST /admin/refunds/{id}/approve
    - PayPal API 환불 처리
    - 배송 상태별 재고 복원
  4. UI
    - 환불 요청 폼 (사유 입력)
    - 환불 상태 표시
  5. 테스트
    - 환불 가능/불가 조건
    - 배송 상태별 환불 금액
    - 재고 복원 (조건부)

  예상 작업 시간: 3-4시간

  ---
  5단계: 어필리에이트

  스토리: "어필리에이터가 링크로 판매하고 커미션을 받는다"

  구현 항목

  1. affiliates, affiliate_stats 테이블
    - affiliate_code, commission_rate
    - sale_count, pending_commission
  2. 어필리에이트 추적
    - 주문 생성 시 affiliate_code 저장
    - 커미션 계산 (상품가의 20%)
  3. 어필리에이트 대시보드 API
    - GET /api/affiliates/{code}/stats
    - 판매 건수, 커미션 조회
  4. 테스트
    - 어필리에이트 코드 추적
    - 커미션 계산 (배송비 제외)

  예상 작업 시간: 2-3시간

  ---
  📊 전체 타임라인

  | 단계     | 작업                  | 예상 시간  | 누적 시간    |
  |--------|---------------------|--------|----------|
  | ✅ 1-a  | 주문 생성 + PayPal + 재고 | 완료     | -        |
  | ✅ 1-b  | 주문 조회 API           | 완료     | -        |
  | 🔄 1-c | Webhook + 이메일       | 3-4h   | 3-4h     |
  | 📦 2   | 배송 추적               | 2-3h   | 5-7h     |
  | 🖥️ 3  | 주문 조회 페이지           | 1-2h   | 6-9h     |
  | 🔙 4-a | 주문 취소               | 1.5-2h | 7.5-11h  |
  | 🔙 4-b | 환불 시스템              | 3-4h   | 10.5-15h |
  | 🤝 5   | 어필리에이트              | 2-3h   | 12.5-18h |

  총 예상 시간: 12.5 ~ 18시간

  ---
  🎯 우선순위 및 권장 진행 순서

  즉시 진행 (필수)

  1. 1-c 단계 - Webhook이 모든 것의 기반
  2. CI 설정 - 자동 테스트 환경 구축

  그 다음 (중요)

  3. 2단계 - 배송 추적 (환불 기능의 전제조건)
  4. 3단계 - 주문 조회 페이지 (사용자 경험)

  마지막 (부가 기능)

  5. 4단계 - 취소/환불
  6. 5단계 - 어필리에이트

  ---
  ❓ 선택 사항

  지금 결정 필요:
  1. CI/CD 언제 설정?
    - 제안: 1-c 전에 (Webhook 테스트 자동화 필요)
  2. DB 연결 언제?
    - 현재: Mock 데이터
    - 제안: 2단계 전에 (배송 추적부터는 DB 필요)
  3. 관리자 페이지?
    - 현재 계획: API만
    - 제안: 4-b(환불) 시점에 간단한 관리자 UI

  ---
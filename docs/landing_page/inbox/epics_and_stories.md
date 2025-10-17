# 화장품 랜딩페이지 Epic & User Story

## Epic 1: 고객이 온라인으로 제품을 구매할 수 있다

**비즈니스 가치:**
고객이 웹사이트를 통해 화장품을 직접 주문하고 결제할 수 있도록 하여, 오프라인 의존도를 낮추고 24시간 판매 채널을 확보한다. MVP 목표인 10개 판매 달성의 핵심 기능이다.

**수용 기준:**
- 고객이 브라우저에서 주문 폼을 작성하고 제출할 수 있다
- PayPal을 통한 안전한 결제가 완료된다
- 필리핀 주소가 Google Places API로 검증된다
- 주문 완료 후 고객에게 확인 메시지가 표시된다
- 전체 주문 데이터가 데이터베이스에 저장된다

### US-1.1: 고객이 주문 폼을 제출할 수 있다 (High, 5pt)

**Story:**
As a 고객, I want 랜딩페이지에서 주문 정보를 입력하고 제출, so that 제품을 구매할 수 있다.

**수용 기준:**
- Given 고객이 랜딩페이지를 방문했을 때
- When 이메일, 주소, 가격 정보를 입력하고 '주문하기' 버튼을 클릭하면
- Then 주문이 서버로 전송되고 성공 메시지가 표시된다

**구현 노트:**
- Walking Skeleton 방식으로 UI → API → Domain 전체 흐름 구축
- Selenium을 이용한 E2E 테스트 작성
- FastAPI 엔드포인트 `/api/orders` 구현

**의존성:** 없음 (첫 번째 구현)

---

### US-1.2: 주소가 Google Places API로 검증된다 (High, 8pt)

**Story:**
As a 고객, I want 입력한 주소가 자동으로 검증, so that 배송 가능한 정확한 주소를 입력할 수 있다.

**수용 기준:**
- Given 고객이 주문 폼에서 주소를 입력할 때
- When Google Places API가 주소 유효성을 검증하면
- Then 유효한 주소는 통과하고, 잘못된 주소는 에러 메시지를 표시한다

**구현 노트:**
- Google Places API Learning Test 작성
- `GooglePlacesAdapter` 구현 (Hexagonal Architecture)
- ROOFTOP 정확도 모드 지원
- 한글 주소 지원

**의존성:** US-1.1 (주문 폼 제출 기능)

---

### US-1.3: PayPal로 안전하게 결제할 수 있다 (High, 8pt)

**Story:**
As a 고객, I want PayPal로 안전하게 결제, so that 신용카드 정보 노출 없이 구매할 수 있다.

**수용 기준:**
- Given 고객이 주문 정보를 입력하고 결제를 진행할 때
- When PayPal Sandbox API를 통해 결제를 처리하면
- Then 결제가 성공하고 transaction_id가 반환된다

**구현 노트:**
- PayPal SDK Learning Test 작성
- `PayPalPaymentAdapter` 구현
- Sandbox 환경에서 테스트
- 에러 처리 (결제 실패, 네트워크 오류)

**의존성:** US-1.1, US-1.2

---

### US-1.4: 주문 확인 정보가 표시된다 (Medium, 3pt)

**Story:**
As a 고객, I want 주문 완료 후 확인 정보를 확인, so that 내가 주문한 내용이 정확한지 알 수 있다.

**수용 기준:**
- Given 고객이 주문을 완료했을 때
- When 주문 데이터가 저장되면
- Then 주문 번호, 이메일, 주소, 결제 금액이 확인 메시지에 표시된다

**구현 노트:**
- UI 성공 메시지 컴포넌트
- 주문 ID 생성 로직

**의존성:** US-1.3

## Epic 2: 인플루언서가 판매 성과를 추적하고 수수료를 받을 수 있다

**비즈니스 가치:**
인플루언서가 자신의 고유 링크를 통해 발생한 판매를 추적하고 수수료(20%)를 받을 수 있도록 하여, MVP 목표인 인플루언서 5명 확보를 지원한다. 자동화된 추적과 정산으로 운영 부담을 최소화한다.

**수용 기준:**
- 인플루언서별 고유 어필리에이트 코드가 생성된다
- URL 파라미터(`?ref=code`)를 통한 클릭 추적이 동작한다
- 어필리에이트 링크로 유입된 고객의 주문 시 커미션(20%)이 자동 계산된다
- 인플루언서가 코드만으로 성과(클릭, 판매, 수수료)를 조회할 수 있다
- 수수료가 자동으로 지급된다 (PayPal Payouts API)

### US-2.1: 어필리에이트 링크로 클릭을 추적할 수 있다 (High, 5pt)

**Story:**
As an 인플루언서, I want 내 고유 링크로 유입된 방문자를 추적, so that 내가 얼마나 많은 트래픽을 발생시켰는지 알 수 있다.

**수용 기준:**
- Given 인플루언서가 `?ref=INFLUENCER123` 링크를 공유했을 때
- When 고객이 해당 링크를 클릭하면
- Then 클릭이 기록되고 쿠키가 30일간 저장된다

**구현 노트:**
- `Affiliate` 도메인 엔티티 구현
- `record_click()` 메서드 (불변성 유지)
- 쿠키 기반 추적 (30일 만료)
- E2E 테스트: 링크 클릭 → 클릭 카운트 증가

**의존성:** 없음

---

### US-2.2: 판매 발생 시 커미션이 자동 계산된다 (High, 8pt)

**Story:**
As an 인플루언서, I want 내 링크로 유입된 고객이 구매하면 커미션이 자동 계산, so that 내 수익을 실시간으로 파악할 수 있다.

**수용 기준:**
- Given 어필리에이트 코드를 가진 고객이 주문을 완료했을 때
- When 주문 금액의 20%를 커미션으로 계산하면
- Then 인플루언서의 `total_commission`과 `pending_commission`이 업데이트된다

**구현 노트:**
- `Commission` 값 객체 구현
- 20% 계산 로직 (소수점 둘째 자리 반올림)
- `PlaceOrderService`에 어필리에이트 추적 통합
- 단위 테스트: 커미션 계산 정확성
- 통합 테스트: 주문 → 커미션 기록 흐름

**의존성:** US-2.1, Epic 1 (주문 기능)

---

### US-2.3: 인플루언서가 성과를 조회할 수 있다 (Medium, 5pt)

**Story:**
As an 인플루언서, I want 내 코드로 성과(클릭, 판매, 수수료)를 조회, so that 별도 로그인 없이 간편하게 실적을 확인할 수 있다.

**수용 기준:**
- Given 인플루언서가 자신의 코드를 알고 있을 때
- When `/api/affiliates/{code}/stats` 엔드포인트를 호출하면
- Then 총 클릭 수, 총 판매 건수, 누적 수익, 대기 중 수수료가 JSON으로 반환된다

**구현 노트:**
- `GET /api/affiliates/{code}/stats` API 구현
- `LoadAffiliatePort` 인터페이스
- `InMemoryAffiliateAdapter` 구현
- E2E 테스트: 클릭 → 주문 → 통계 조회 전체 흐름

**의존성:** US-2.2

---

### US-2.4: 수수료가 자동으로 지급된다 (Low, 8pt)

**Story:**
As an 인플루언서, I want 수수료가 PayPal로 자동 지급, so that 정산 지연 없이 즉시 수익을 받을 수 있다.

**수용 기준:**
- Given 판매가 완료되고 커미션이 계산되었을 때
- When PayPal Payouts API를 통해 수수료를 송금하면
- Then 인플루언서의 PayPal 계정으로 금액이 입금되고 `pending_commission`이 0으로 업데이트된다

**구현 노트:**
- PayPal Payouts API Learning Test
- `PayPalPayoutAdapter` 구현
- 자동 지급 스케줄러 (또는 수동 트리거)
- 에러 처리 (송금 실패, 잘못된 계정)

**의존성:** US-2.2

## Epic 3: 고객이 제품에 대해 문의할 수 있다

**비즈니스 가치:**
고객이 구매 전 궁금한 점을 이메일로 문의할 수 있도록 하여, 구매 결정을 돕고 고객 신뢰를 구축한다. 간단한 Gmail SMTP 연동으로 별도 고객 지원 시스템 없이 초기 운영을 지원한다.

**수용 기준:**
- 고객이 랜딩페이지에서 문의 폼을 작성하고 제출할 수 있다
- 문의 내용이 판매자 이메일로 전송된다
- 이메일 형식이 검증된다
- 전송 실패 시 에러 메시지가 표시된다

### US-3.1: 고객이 문의 폼을 제출할 수 있다 (Medium, 5pt)

**Story:**
As a 고객, I want 랜딩페이지에서 제품에 대해 문의, so that 구매 전 궁금한 점을 해결할 수 있다.

**수용 기준:**
- Given 고객이 랜딩페이지를 방문했을 때
- When 이메일과 문의 내용을 입력하고 '문의하기' 버튼을 클릭하면
- Then 문의가 서버로 전송되고 "문의가 접수되었습니다" 메시지가 표시된다

**구현 노트:**
- UI 문의 폼 컴포넌트
- `POST /api/inquiries` API 엔드포인트
- Selenium E2E 테스트
- 이메일 형식 검증 (프론트엔드 + 백엔드)

**의존성:** 없음

---

### US-3.2: 문의 내용이 판매자에게 이메일로 전송된다 (High, 8pt)

**Story:**
As a 판매자, I want 고객 문의가 내 이메일로 자동 전송, so that 신속하게 답변할 수 있다.

**수용 기준:**
- Given 고객이 문의를 제출했을 때
- When Gmail SMTP를 통해 이메일을 전송하면
- Then 판매자 이메일(`support@cosmetics.com`)로 고객 이메일과 문의 내용이 포함된 메일이 도착한다

**구현 노트:**
- `SendInquiryService` 애플리케이션 서비스
- `EmailSenderPort` 인터페이스
- `GmailSmtpAdapter` 구현
- Fake SMTP 서버를 이용한 통합 테스트
- 에러 처리 (전송 실패, 네트워크 오류)

**의존성:** US-3.1

---

### US-3.3: 잘못된 이메일 형식은 거부된다 (Medium, 3pt)

**Story:**
As a 시스템, I want 잘못된 이메일 형식을 거부, so that 유효한 문의만 처리한다.

**수용 기준:**
- Given 고객이 문의 폼에 이메일을 입력할 때
- When 이메일 형식이 잘못되었으면 (`invalid-email`)
- Then "유효한 이메일을 입력하세요" 에러 메시지가 표시되고 제출이 차단된다

**구현 노트:**
- Pydantic `EmailStr` 타입 사용
- 프론트엔드 HTML5 `type="email"` 검증
- API 레벨 422 Unprocessable Entity 응답

**의존성:** US-3.1

## 기술 부채 & NFR

### TD-1: 데이터베이스 마이그레이션 (Low, 5pt)

**Story:**
As a 개발자, I want SQLite에서 PostgreSQL로 마이그레이션, so that 프로덕션 환경에서 안정적으로 운영할 수 있다.

**수용 기준:**
- Given 프로덕션 배포 전
- When PostgreSQL 연결 설정을 완료하면
- Then 모든 기능이 PostgreSQL에서 동작한다

**의존성:** Epic 1, 2, 3 완료 후

### NFR-1: E2E 테스트 커버리지 80% 이상 (Medium, 3pt)

**Story:**
As a 개발팀, I want 주요 사용자 여정에 대한 E2E 테스트 커버리지 80% 이상, so that 배포 전 회귀 버그를 자동으로 감지할 수 있다.

**수용 기준:**
- 주문 흐름 E2E 테스트 ✅
- 어필리에이트 흐름 E2E 테스트 ✅
- 문의 흐름 E2E 테스트 ✅

### NFR-2: API 응답 시간 < 500ms (Low, 5pt)

**Story:**
As a 고객, I want API 응답이 500ms 이내, so that 빠르게 페이지를 로드하고 주문할 수 있다.

**수용 기준:**
- 모든 API 엔드포인트 평균 응답 시간 < 500ms
- PayPal API 호출 제외 (외부 의존성)

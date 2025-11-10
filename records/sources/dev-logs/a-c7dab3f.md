---
session-id: 4364d2dc-e7d2-4cd8-9d37-62ca95f88bc0
created-date: 25-11-10 09:49
---

# 나
- 작성해야할 테스트, 특히 리팩터링 진행 시 필요하거나 유용한 테스트 뭔가 정리할 필요 있다고 느꼈으나, 지금 작업 진행하는데는 적어도 필요 없고 ai가 코드 구현해서 그 조금 더 걸리는 시간은 충분히 감내할 만하다 생각. 그래서 그냥 일단 계획대로 tdd로 진행
- 핵심 초점은 필요한 내용 식별, 선별, 그리고 이해에, 이게 최우선의, 그리고 현재의 거의 유일한, 다른 것을 제한하는 기준이 되어야 함
- smtp 같은 그 안의 구성 기능 구현도 outside in tdd 방식으로 해야 할 텐데? 그냥 개발 후 테스트 통과하는, 심지어 tdd도 아닌 방식으로 진행하려고 함. 

# ai

## 작업 내용

### 문제 발생 (요구사항)
- **목표**: PayPal 결제 완료 시 고객에게 주문 확인 이메일 자동 발송
- **선행 과제**: Gmail SMTP 설정 및 이메일 발송 기능 구현
- **개발 방식**: Outside-in TDD (스모크 테스트 → E2E 테스트 → 구현)

### 원인 분석 (설계 및 접근 방식)
- **Phase 1 필요성**: SMTP 연결 파라미터와 동작 확인 (통합 테스트/스모크 테스트)
  - Gmail SMTP 호스트, 포트, 인증 방식 검증 필요
  - 응답 코드 및 지원 기능 파악 필요
- **Phase 2 설계**: Outside-in TDD로 이메일 발송 서비스 구현
  - Red: E2E 테스트 작성 (함수 미구현 상태)
  - Green: 최소 구현으로 테스트 통과
  - Refactor: HTML 템플릿 분리, 에러 핸들링, 로깅 추가

### 해결 방법 (구현 내용)

**1) Phase 1: SMTP 스모크 테스트**

**파일**: `tests/integration/test_smtp_connection.py`
```python
# 구현한 테스트
- test_smtp_connection(): SMTP 서버 연결 및 인증 테스트
- test_send_simple_email(): 텍스트 이메일 발송 테스트
- test_send_html_email(): HTML 이메일 발송 테스트

핵심: Gmail SMTP 파라미터 확인 (smtp.gmail.com:587, STARTTLS, AUTH PLAIN)
```

**확인된 SMTP 응답 코드 및 기능**:
- `250` - EHLO 성공, `220` - STARTTLS 준비, `235` - 인증 승인
- 지원 기능: SIZE (34MB), 8BITMIME (UTF-8), SMTPUTF8 (국제화 이메일)

**2) Phase 2: 이메일 발송 서비스 구현**

**파일**: `tests/integration/test_email_service.py`
```python
# Red: E2E 테스트 작성
- test_send_order_confirmation_email(): 주문 확인 이메일 발송 성공 검증
- test_send_order_confirmation_email_with_invalid_email(): 잘못된 이메일 에러 처리

핵심: 실제 이메일 발송 및 수신 확인 (통합 테스트)
```

**파일**: `backend/services/email.py`
```python
# Green: 최소 구현
def send_order_confirmation_email(order: OrderResponse) -> bool:
    # SMTP 연결 → 텍스트 이메일 발송

핵심: 테스트 통과를 위한 최소 기능만 구현
```

```python
# Refactor: 코드 개선
1. _load_template(): HTML 템플릿 파일 로드 (backend/templates/email/)
2. _render_order_confirmation_template(): 텍스트 + HTML 본문 생성
3. MIMEMultipart로 텍스트/HTML 멀티파트 메시지 구성
4. 에러 핸들링: FileNotFoundError, SMTPException, 일반 Exception
5. 로깅: logger.info/error로 발송 성공/실패 기록

핵심: 템플릿 분리로 유지보수성 향상, 구체적 에러 처리
```

**파일**: `backend/templates/email/order_confirmation.html`
```html
# HTML 이메일 템플릿
- 반응형 테이블 레이아웃 (이메일 클라이언트 호환)
- 그라데이션 헤더 (#667eea → #764ba2)
- 주문 정보, 배송지 정보 테이블
- 안내 사항 박스

핵심: 인라인 CSS로 모든 이메일 클라이언트 호환
```

---

## 이해 요소

### 통합 테스트 vs 스모크 테스트

**핵심**: 스모크 테스트는 외부 시스템 연결 및 핵심 기능 동작을 빠르게 확인하는 통합 테스트의 일종

**동작 원리**:
- 통합 테스트: 여러 모듈/외부 시스템 연동 동작 검증
- 스모크 테스트: 핵심 기능만 빠르게 테스트 (빌드 검증용)
- 이 프로젝트: SMTP 서버 연결 및 이메일 발송 가능 여부 확인 → 스모크 테스트 역할

**폴더 구조**:
```
tests/integration/  # 통합 테스트 (스모크 테스트 포함)
  ├── test_smtp_connection.py
  └── test_email_service.py
```

---

### Outside-in TDD

**핵심**: 외부(사용자 관점)에서 내부(구현)로 들어가며 테스트 작성 → 구현하는 방식

**동작 원리**:
1. **Red**: E2E 테스트 작성 (사용자 시나리오 기반) → 실패
2. **Green**: 최소 구현으로 테스트 통과
3. **Refactor**: 코드 개선 (테스트는 여전히 통과)

**적용 사례**:
- Red: `send_order_confirmation_email()` 호출 테스트 작성 → `ModuleNotFoundError`
- Green: 텍스트 이메일만 발송하는 최소 구현 → 테스트 통과
- Refactor: HTML 템플릿 분리, 에러 핸들링 추가 → 테스트 여전히 통과

---

### Gmail SMTP 인증 (앱 비밀번호)

**핵심**: 일반 비밀번호가 아닌 Google 계정에서 생성한 16자리 앱 전용 비밀번호 사용

**동작 원리**:
- 2단계 인증 필수 활성화
- Google 계정 → 보안 → 앱 비밀번호 생성
- `.env`에 `GMAIL_APP_PASSWORD` 저장

**환경 변수**:
```bash
GMAIL_ADDRESS=building.ensemble@gmail.com
GMAIL_APP_PASSWORD=czqi vxgm osqk vfxz
```

---

### MIME Multipart 이메일

**핵심**: 하나의 이메일에 텍스트/HTML 버전을 모두 포함하여 클라이언트 호환성 확보

**동작 원리**:
1. `MIMEMultipart("alternative")` 생성
2. `MIMEText(text_body, "plain")` 추가 (HTML 미지원 클라이언트용)
3. `MIMEText(html_body, "html")` 추가 (HTML 지원 클라이언트용)
4. 클라이언트가 자동으로 적절한 버전 선택

**코드 예시**:
```python
message = MIMEMultipart("alternative")
message.attach(MIMEText(text_body, "plain", "utf-8"))
message.attach(MIMEText(html_body, "html", "utf-8"))
```

# Webhook 서명 검증

## 개요

PayPal Webhook 서명 검증은 수신한 Webhook 요청이 실제 PayPal에서 보낸 것인지 확인하는 보안 메커니즘입니다.

### 왜 필요한가?

**보안 위협**:
```
공격자가 가짜 Webhook 전송
↓
"결제 완료" 이벤트 위조
↓
실제 결제 없이 주문 처리 및 상품 배송 😱
```

**서명 검증으로 방지**:
- PayPal만이 알고 있는 비밀 키로 서명 생성
- 서버가 PayPal 공개 키로 서명 검증
- 유효하지 않으면 요청 거부

---

## PayPal Webhook 서명 검증 원리

### 1. PayPal이 Webhook 전송 시

```
1. Webhook 이벤트 데이터 생성
2. PayPal 비밀 키로 서명(signature) 생성
3. HTTP 헤더에 서명 정보 포함하여 전송
```

**포함되는 헤더**:
```
PAYPAL-TRANSMISSION-ID: 고유 전송 ID
PAYPAL-TRANSMISSION-TIME: 타임스탬프
PAYPAL-TRANSMISSION-SIG: 서명 (암호화된 값)
PAYPAL-AUTH-ALGO: 서명 알고리즘 (예: SHA256withRSA)
PAYPAL-CERT-URL: PayPal 인증서 URL
```

### 2. 서버가 검증

```python
# PayPal SDK 사용 방법
from paypalrestsdk import WebhookEvent

is_valid = WebhookEvent.verify(
    transmission_id=headers["paypal-transmission-id"],
    timestamp=headers["paypal-transmission-time"],
    webhook_id=os.getenv("PAYPAL_WEBHOOK_ID"),  # PayPal에서 발급받은 Webhook ID
    event_body=request_body,
    cert_url=headers["paypal-cert-url"],
    actual_sig=headers["paypal-transmission-sig"],
    auth_algo=headers["paypal-auth-algo"],
)

if not is_valid:
    raise HTTPException(status_code=401, detail="Invalid signature")
```

---

## 구현 방법

### 1. PayPal Webhook ID 발급

**PayPal Developer Dashboard**:
1. https://developer.paypal.com 로그인
2. My Apps & Credentials → 앱 선택
3. Webhooks → Add Webhook
4. Webhook URL 입력 (예: `https://yourdomain.com/webhooks/paypal`)
5. 이벤트 타입 선택:
   - `PAYMENT.CAPTURE.COMPLETED`
   - `PAYMENT.CAPTURE.DENIED`
6. Save → **Webhook ID** 복사

**환경 변수 설정**:
```bash
# .env
PAYPAL_WEBHOOK_ID=your-webhook-id-here
```

### 2. 코드 구현

**파일**: `backend/api/webhooks.py`

```python
import os
from fastapi import APIRouter, HTTPException, Request, status
from paypalrestsdk import WebhookEvent

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/paypal")
async def handle_paypal_webhook(request: Request):
    """PayPal Webhook 처리 (서명 검증 포함)"""

    # 1. 헤더 및 바디 추출
    headers = dict(request.headers)
    body = await request.body()
    webhook_body = await request.json()

    # 2. 서명 검증
    try:
        is_valid = WebhookEvent.verify(
            transmission_id=headers.get("paypal-transmission-id"),
            timestamp=headers.get("paypal-transmission-time"),
            webhook_id=os.getenv("PAYPAL_WEBHOOK_ID"),
            event_body=body.decode("utf-8"),
            cert_url=headers.get("paypal-cert-url"),
            actual_sig=headers.get("paypal-transmission-sig"),
            auth_algo=headers.get("paypal-auth-algo"),
        )

        if not is_valid:
            logger.warning("Webhook 서명 검증 실패")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid webhook signature"
            )

    except Exception as e:
        logger.error(f"Webhook 서명 검증 오류: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Signature verification failed"
        )

    # 3. 검증 통과 후 이벤트 처리
    event_type = webhook_body.get("event_type")
    # ... 기존 로직
```

### 3. 의존성 추가

```bash
uv add paypalrestsdk
```

또는

```toml
# pyproject.toml
[project]
dependencies = [
    # ... 기존 의존성
    "paypalrestsdk>=1.13.0",
]
```

---

## 테스트 방법

### 1. 단위 테스트 (Mock)

**파일**: `tests/unit/test_webhook_signature.py`

```python
from unittest.mock import Mock, patch
import pytest
from fastapi.testclient import TestClient


def test_webhook_with_valid_signature_succeeds(test_client):
    """유효한 서명이 있으면 Webhook 처리 성공"""

    webhook_data = {
        "event_type": "PAYMENT.CAPTURE.COMPLETED",
        "resource": {
            "id": "test-capture-id",
            "custom_id": "ORD-TEST123",
        }
    }

    headers = {
        "paypal-transmission-id": "valid-transmission-id",
        "paypal-transmission-time": "2024-01-01T00:00:00Z",
        "paypal-transmission-sig": "valid-signature",
        "paypal-auth-algo": "SHA256withRSA",
        "paypal-cert-url": "https://api.paypal.com/cert",
    }

    # WebhookEvent.verify()를 Mock으로 대체
    with patch("backend.api.webhooks.WebhookEvent.verify") as mock_verify:
        mock_verify.return_value = True

        response = test_client.post(
            "/webhooks/paypal",
            json=webhook_data,
            headers=headers
        )

        assert response.status_code == 200
        mock_verify.assert_called_once()


def test_webhook_with_invalid_signature_fails(test_client):
    """잘못된 서명이면 401 에러"""

    webhook_data = {"event_type": "PAYMENT.CAPTURE.COMPLETED"}
    headers = {
        "paypal-transmission-sig": "INVALID_SIGNATURE",
    }

    with patch("backend.api.webhooks.WebhookEvent.verify") as mock_verify:
        mock_verify.return_value = False

        response = test_client.post(
            "/webhooks/paypal",
            json=webhook_data,
            headers=headers
        )

        assert response.status_code == 401
        assert "signature" in response.json()["detail"].lower()


def test_webhook_without_signature_fails(test_client):
    """서명 헤더 없으면 401 에러"""

    webhook_data = {"event_type": "PAYMENT.CAPTURE.COMPLETED"}

    response = test_client.post("/webhooks/paypal", json=webhook_data)

    # 서명 검증 시도 시 예외 발생 → 401
    assert response.status_code == 401
```

### 2. 통합 테스트 (실제 PayPal)

**PayPal Webhook Simulator 사용**:
1. PayPal Developer Dashboard → Webhooks
2. 등록한 Webhook 선택
3. "Webhook Simulator" 클릭
4. 이벤트 타입 선택 및 Send 클릭
5. 서버 로그에서 검증 성공 확인

---

## 로컬 개발 환경에서의 Webhook 개발

### 문제: HTTPS URL 요구사항

PayPal Webhook 등록 시 **HTTPS URL만 허용**:
```
❌ http://localhost:8000/webhooks/paypal  (등록 불가)
✅ https://yourdomain.com/webhooks/paypal  (등록 가능)
```

**에러 메시지**:
```
URL must contain https://
```

### 해결 방법 옵션

#### 옵션 1: ngrok 사용 (로컬 → HTTPS 터널링)

**ngrok으로 로컬 서버를 HTTPS로 노출**:

```bash
# 1. FastAPI 서버 실행 (터미널 1)
uv run uvicorn backend.main:app --reload

# 2. ngrok으로 HTTPS 터널링 (터미널 2)
ngrok http 8000

# 출력 예시:
# Forwarding: https://abc123.ngrok.io -> http://localhost:8000
```

**PayPal Webhook 등록**:
```
Webhook URL: https://abc123.ngrok.io/webhooks/paypal
```

**장점**:
- 실제 PayPal Webhook 수신 테스트 가능
- 실제 서명 검증 테스트 가능
- PayPal Webhook Simulator 사용 가능

**단점**:
- ngrok 무료 버전은 세션마다 URL 변경
- ngrok 설치 및 설정 필요
- 외부 의존성 추가

---

#### 옵션 2: Mock 테스트만 사용 (현재 방법 ⭐ 추천)

**서명 검증 없이 Mock으로 개발 완료**:

```python
# tests/e2e/test_payment_webhook_flow.py (이미 구현됨)

def test_customer_receives_email_after_successful_payment(test_client):
    """Mock으로 Webhook 이벤트 시뮬레이션"""

    webhook_event = {
        "event_type": "PAYMENT.CAPTURE.COMPLETED",
        "resource": {
            "id": "test-capture-id",
            "custom_id": "ORD-TEST123",
        }
    }

    response = test_client.post("/webhooks/paypal", json=webhook_event)
    assert response.status_code == 200
    # 이메일 발송, 주문 상태 변경 검증
```

**장점**:
- 빠르고 간편한 개발
- 외부 의존성 없음 (ngrok, PayPal 불필요)
- CI/CD에서도 안정적으로 실행 가능
- 비즈니스 로직 테스트에 집중

**단점**:
- 실제 PayPal Webhook 형식과 약간 다를 수 있음
- 서명 검증 로직은 프로덕션에서만 테스트 가능

**현재 상태**:
- ✅ Webhook 엔드포인트 구현 완료
- ✅ 이벤트 처리 로직 완료 (결제 완료/실패)
- ✅ Acceptance 테스트 통과 (Mock)
- ⏳ 서명 검증은 프로덕션 배포 시 추가

---

#### 옵션 3: 환경별 서명 검증 분기

**개발 환경에서는 서명 검증 스킵**:

```python
# backend/api/webhooks.py

import os
from fastapi import APIRouter, Request

@router.post("/paypal")
async def handle_paypal_webhook(request: Request):
    """PayPal Webhook 처리"""

    # 프로덕션 환경에서만 서명 검증
    if os.getenv("PAYPAL_MODE") == "live":
        # 서명 검증 로직
        headers = dict(request.headers)
        body = await request.body()

        is_valid = WebhookEvent.verify(...)
        if not is_valid:
            raise HTTPException(status_code=401, detail="Invalid signature")
    else:
        # 개발/테스트 환경: 서명 검증 스킵
        logger.info("Sandbox mode: Signature verification skipped")

    # 이벤트 처리 (기존 로직)
    webhook_body = await request.json()
    event_type = webhook_body.get("event_type")
    # ...
```

**환경 변수**:
```bash
# .env (개발)
PAYPAL_MODE=sandbox

# .env.production
PAYPAL_MODE=live
PAYPAL_WEBHOOK_ID=WH-XXXXXXXXXX
```

**장점**:
- 개발과 프로덕션 코드 통합
- 환경별 동작 명확히 구분
- 로컬에서는 Mock 테스트, 프로덕션에서는 실제 검증

**단점**:
- 코드에 분기 로직 추가
- 프로덕션 배포 전 환경 변수 설정 필수

---

### 추천 접근 방법

**현재 단계 (MVP 개발)**:
1. **옵션 2 (Mock 테스트)** 사용 ← 현재 상태
2. 서명 검증 로직은 **TODO로 문서화**
3. Acceptance 테스트로 비즈니스 로직 검증 완료

**프로덕션 배포 전**:
1. **옵션 3 (환경별 분기)** 구현
2. HTTPS 도메인 확보
3. PayPal Webhook ID 발급
4. 서명 검증 로직 추가 및 테스트

**장점**:
- 빠른 개발 속도 유지
- 보안 기능은 실제 배포 시 추가
- 불필요한 복잡도 제거

---

### PayPal Webhook Simulator 참고

**Webhook Simulator란?**:
- PayPal Developer Dashboard에서 제공하는 테스트 도구
- 실제 결제 없이 Webhook 이벤트를 서버로 전송
- **하지만 HTTPS Webhook URL 등록이 선행되어야 함**

**사용 방법** (프로덕션/ngrok 환경에서만):
```
1. PayPal Dashboard → Webhooks → 등록된 Webhook 선택
2. "Webhook Simulator" 클릭
3. Event Type 선택 (PAYMENT.CAPTURE.COMPLETED 등)
4. "Send Test" 클릭
5. 서버 로그에서 이벤트 수신 확인
```

**로컬 개발에서는**:
- Mock 테스트가 Webhook Simulator 역할 대체
- 더 빠르고 안정적

---

## 현재 상태 및 TODO

### ✅ 완료
- Webhook 엔드포인트 구현
- 이벤트 타입별 처리 로직
- Acceptance Test 작성

### ⏳ TODO (프로덕션 배포 전)
- [ ] PayPal Webhook ID 발급 및 환경 변수 설정
- [ ] 서명 검증 로직 추가 (`WebhookEvent.verify()`)
- [ ] `paypalrestsdk` 의존성 추가
- [ ] 서명 검증 단위 테스트 작성
- [ ] PayPal Webhook Simulator로 통합 테스트

### 🔒 보안 고려사항

**현재 (개발 환경)**:
- Mock 테스트 환경에서는 서명 검증 불필요
- 로컬에서 테스트 시 실제 PayPal Webhook 수신 불가

**프로덕션 배포 시**:
- **반드시 서명 검증 활성화 필수**
- 환경 변수 `PAYPAL_WEBHOOK_ID` 설정
- HTTPS 필수 (PayPal은 HTTP로 Webhook 전송 안 함)
- 서명 검증 실패 로그 모니터링

---

## 참고 자료

**PayPal 공식 문서**:
- [Webhook 서명 검증](https://developer.paypal.com/docs/api-basics/notifications/webhooks/notification-messages/#link-verifyyourwebhooksignature)
- [Python SDK - Webhook 검증](https://github.com/paypal/PayPal-Python-SDK#webhook-validation)

**환경 변수 예시**:
```bash
# .env
PAYPAL_CLIENT_ID=your-client-id
PAYPAL_CLIENT_SECRET=your-client-secret
PAYPAL_WEBHOOK_ID=your-webhook-id  # 추가 필요
PAYPAL_MODE=sandbox  # 또는 live
```

**디버깅 팁**:
- 서명 검증 실패 시 헤더 전체 로그 출력
- PayPal Dashboard에서 Webhook 전송 이력 확인
- 타임스탬프 검증 (시간 동기화 문제)

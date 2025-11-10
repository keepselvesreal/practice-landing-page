# PayPal Webhook Contract Test

PayPal Simulator에서 실제로 전송하는 데이터를 수신하고 검증하는 Contract Test입니다.

## 목적

1. **실제 PayPal 데이터 구조 확인**: Simulator가 보내는 실제 이벤트 형식 저장
2. **서명 검증 테스트**: PayPal SDK의 실제 서명 검증 동작 확인
3. **Fixture 생성**: Integration Test에서 사용할 실제 데이터 생성

## 실행 방법

### Prerequisites

1. PayPal Developer Account
2. ngrok 설치
3. `.env` 파일에 `PAYPAL_WEBHOOK_ID` 설정 (선택사항)

### Step 1: Contract Test Server 실행

```bash
# 방법 1: Python 직접 실행
uv run python tests/contract/contract_test_server.py

# 방법 2: 실행 스크립트 사용
chmod +x tests/contract/run_contract_test.sh
./tests/contract/run_contract_test.sh
```

서버가 http://localhost:8000 에서 실행됩니다.

### Step 2: ngrok 터널 생성

별도 터미널에서:

```bash
ngrok http 8000
```

ngrok URL 복사 (예: `https://abc123.ngrok-free.app`)

### Step 3: PayPal Dashboard Webhook 설정

1. https://developer.paypal.com 로그인
2. **My Apps & Credentials** → Sandbox 앱 선택
3. **Webhooks** → Add Webhook
4. **Webhook URL** 입력:
   ```
   https://[ngrok-url]/webhooks/paypal/contract-test
   ```
5. **Event types** 선택:
   - `PAYMENT.CAPTURE.COMPLETED`
   - `PAYMENT.CAPTURE.DENIED`
6. **Save**
7. **Webhook ID** 복사하여 `.env`에 저장:
   ```bash
   PAYPAL_WEBHOOK_ID=WH-xxxxxxxxxxxxx
   ```

### Step 4: Simulator로 이벤트 전송

1. PayPal Dashboard → Webhooks
2. 등록한 Webhook 선택
3. **Webhook Simulator** 클릭
4. Event Type: `PAYMENT.CAPTURE.COMPLETED` 선택
5. **Send Test** 클릭

### Step 5: 결과 확인

**Contract Test Server 로그**:
```
============================================================
📦 Contract Test - PayPal Simulator 데이터 수신
============================================================
✅ 이벤트 데이터 저장: tests/fixtures/paypal_simulator_event.json
✅ 헤더 데이터 저장: tests/fixtures/paypal_simulator_headers.json
✅ 서명 검증 성공!
이벤트 타입: PAYMENT.CAPTURE.COMPLETED
리소스 타입: capture
리소스 ID: 42311647XV020574X
Custom ID: d93e4fcb-d3af-137c-82fe-1a8101f1ad11
============================================================
```

**생성된 Fixture 파일**:
- `tests/fixtures/paypal_simulator_event.json`: PayPal 이벤트 전체 데이터
- `tests/fixtures/paypal_simulator_headers.json`: 서명 검증 헤더

## 검증 항목

### 1. 이벤트 구조 확인

`tests/fixtures/paypal_simulator_event.json` 파일을 열어 확인:

```json
{
  "event_type": "PAYMENT.CAPTURE.COMPLETED",
  "resource_type": "capture",
  "resource": {
    "id": "42311647XV020574X",
    "custom_id": "d93e4fcb-d3af-137c-82fe-1a8101f1ad11",
    "amount": {...},
    "seller_protection": {...},
    ...
  }
}
```

**확인 사항**:
- ✅ `event_type`이 우리가 처리하는 타입인가?
- ✅ `resource.custom_id` 필드가 존재하는가?
- ✅ 추가 필드들(`disbursement_mode`, `seller_protection` 등)이 있는가?

### 2. 서명 검증 결과

Contract Test Server 로그에서:

- ✅ **서명 검증 성공**: PayPal SDK가 올바르게 동작
- ⚠️  **서명 검증 실패**: `PAYPAL_WEBHOOK_ID` 확인 필요
- ❌ **서명 검증 오류**: 네트워크 문제, 인증서 문제 등

### 3. 헤더 정보

`tests/fixtures/paypal_simulator_headers.json`:

```json
{
  "paypal-transmission-id": "04d24199-be04-11f0-bca0-7de00938a839",
  "paypal-transmission-time": "2025-11-10T07:08:11Z",
  "paypal-transmission-sig": "Nh9WthknkkQjEcERb2vhoDJ...",
  "paypal-auth-algo": "SHA256withRSA",
  "paypal-cert-url": "https://api.paypal.com/v1/notifications/certs/..."
}
```

## 생성된 Fixture 활용

Integration Test에서 사용:

```python
# tests/integration/test_webhook_with_real_paypal_data.py

@pytest.fixture
def real_paypal_event():
    """PayPal Simulator에서 실제로 받은 이벤트"""
    fixture_path = Path(__file__).parent.parent / "fixtures" / "paypal_simulator_event.json"
    with open(fixture_path) as f:
        return json.load(f)
```

## Troubleshooting

### 401 Unauthorized

**원인**: 서명 검증 실패

**해결**:
1. `.env`에 `PAYPAL_WEBHOOK_ID` 설정 확인
2. PayPal Dashboard에서 Webhook ID 다시 확인
3. Webhook URL이 정확한지 확인

### 404 Not Found

**원인**: PayPal이 잘못된 URL로 전송

**해결**:
1. PayPal Webhook URL 확인: `/webhooks/paypal/contract-test`
2. ngrok URL이 만료되지 않았는지 확인

### Fixture 파일이 생성되지 않음

**원인**: 서버 권한 문제

**해결**:
```bash
mkdir -p tests/fixtures
chmod 755 tests/fixtures
```

## 주의사항

1. **프로덕션 배포 금지**: 이 서버는 테스트 전용입니다
2. **ngrok URL 관리**: 무료 버전은 세션마다 URL 변경됨
3. **Fixture 관리**: `.gitignore`에 추가하여 실제 데이터 커밋 방지
4. **보안**: `PAYPAL_WEBHOOK_ID`는 `.env`에만 저장

## 다음 단계

1. ✅ Fixture 생성 완료
2. → Integration Test 작성 (`tests/integration/test_webhook_with_real_paypal_data.py`)
3. → Acceptance Test 실행하여 회귀 확인

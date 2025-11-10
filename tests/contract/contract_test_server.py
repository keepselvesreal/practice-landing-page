"""Contract Test 전용 서버

PayPal Simulator에서 보낸 실제 데이터를 받아서 fixture로 저장

실행 방법:
    uv run python tests/contract/contract_test_server.py

    또는

    chmod +x tests/contract/run_contract_test.sh
    ./tests/contract/run_contract_test.sh
"""
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, Request
from paypalrestsdk import WebhookEvent

# 실제 webhook handler import
from backend.api.webhooks import handle_paypal_webhook

app = FastAPI(title="PayPal Webhook Contract Test Server")
logger = logging.getLogger(__name__)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(message)s"
)


@app.post("/webhooks/paypal/contract-test")
async def paypal_webhook_contract_test(request: Request) -> Dict[str, Any]:
    """Contract Test용 endpoint

    PayPal Simulator에서 보낸 실제 데이터를 받아서:
    1. tests/fixtures/paypal_simulator_event.json에 저장
    2. 서명 검증 시도 (성공/실패 로그)
    3. 헤더 정보 저장
    4. 결과 반환

    사용법:
    1. 이 서버 실행 + ngrok
    2. PayPal Webhook URL: https://xxx.ngrok.io/webhooks/paypal/contract-test
    3. PayPal Dashboard에서 Simulator 클릭
    4. 서버 응답 및 로그 확인
    5. tests/fixtures/paypal_simulator_event.json 생성 확인
    """
    # 1. 받은 데이터 추출
    headers = dict(request.headers)
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8")
    event_data = json.loads(body_str)

    logger.info("=" * 60)
    logger.info("📦 Contract Test - PayPal Simulator 데이터 수신")
    logger.info("=" * 60)

    # 2. Fixture 디렉토리 생성 (프로젝트 루트 기준)
    project_root = Path(__file__).parent.parent.parent
    fixture_dir = project_root / "tests" / "fixtures"
    fixture_dir.mkdir(parents=True, exist_ok=True)

    # 3. 이벤트 데이터 저장
    event_fixture_path = fixture_dir / "paypal_simulator_event.json"
    with open(event_fixture_path, "w") as f:
        json.dump(event_data, f, indent=2, ensure_ascii=False)

    logger.info(f"✅ 이벤트 데이터 저장: {event_fixture_path}")

    # 4. 헤더 데이터 저장
    signature_headers = {
        "paypal-transmission-id": headers.get("paypal-transmission-id"),
        "paypal-transmission-time": headers.get("paypal-transmission-time"),
        "paypal-transmission-sig": headers.get("paypal-transmission-sig"),
        "paypal-auth-algo": headers.get("paypal-auth-algo"),
        "paypal-cert-url": headers.get("paypal-cert-url"),
    }

    headers_fixture_path = fixture_dir / "paypal_simulator_headers.json"
    with open(headers_fixture_path, "w") as f:
        json.dump(signature_headers, f, indent=2, ensure_ascii=False)

    logger.info(f"✅ 헤더 데이터 저장: {headers_fixture_path}")

    # 5. 서명 검증 시도
    signature_valid = False
    signature_error = None
    webhook_id = os.getenv("PAYPAL_WEBHOOK_ID")

    try:
        if webhook_id:
            signature_valid = WebhookEvent.verify(
                transmission_id=headers.get("paypal-transmission-id"),
                timestamp=headers.get("paypal-transmission-time"),
                webhook_id=webhook_id,
                event_body=body_str,
                cert_url=headers.get("paypal-cert-url"),
                actual_sig=headers.get("paypal-transmission-sig"),
                auth_algo=headers.get("paypal-auth-algo"),
            )

            if signature_valid:
                logger.info("✅ 서명 검증 성공!")
            else:
                logger.warning("⚠️  서명 검증 실패")
        else:
            signature_error = "PAYPAL_WEBHOOK_ID 환경변수가 설정되지 않았습니다"
            logger.warning(f"⚠️  {signature_error}")

    except Exception as e:
        signature_error = str(e)
        logger.error(f"❌ 서명 검증 오류: {e}")

    # 6. 이벤트 정보 로깅
    event_type = event_data.get("event_type")
    resource_type = event_data.get("resource_type")
    resource = event_data.get("resource", {})
    resource_id = resource.get("id")
    custom_id = resource.get("custom_id")

    logger.info(f"이벤트 타입: {event_type}")
    logger.info(f"리소스 타입: {resource_type}")
    logger.info(f"리소스 ID: {resource_id}")
    logger.info(f"Custom ID: {custom_id}")
    logger.info("=" * 60)

    # 7. 응답 반환
    return {
        "status": "success",
        "message": "Contract test completed - PayPal Simulator data saved",
        "fixtures": {
            "event": str(event_fixture_path),
            "headers": str(headers_fixture_path),
        },
        "signature_verification": {
            "valid": signature_valid,
            "error": signature_error,
            "webhook_id_configured": webhook_id is not None,
        },
        "event_info": {
            "event_type": event_type,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "custom_id": custom_id,
        },
    }


@app.post("/webhooks/paypal")
async def paypal_webhook(request: Request) -> Dict[str, Any]:
    """실제 Webhook handler (테스트용)

    프로덕션 코드와 동일하게 동작
    """
    return await handle_paypal_webhook(request)


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "ok",
        "message": "PayPal Webhook Contract Test Server",
        "endpoints": {
            "contract_test": "/webhooks/paypal/contract-test",
            "webhook": "/webhooks/paypal",
        }
    }


if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 60)
    print("🚀 PayPal Webhook Contract Test Server 시작")
    print("=" * 60)
    print("\n다음 단계:")
    print("1. 터미널 2에서 ngrok 실행: ngrok http 8000")
    print("2. PayPal Dashboard에서 Webhook URL 설정:")
    print("   https://[ngrok-url]/webhooks/paypal/contract-test")
    print("3. Simulator 클릭")
    print("4. 이 터미널에서 로그 확인")
    print("\n" + "=" * 60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)

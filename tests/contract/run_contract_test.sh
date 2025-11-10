#!/bin/bash
# Contract Test Server 실행 스크립트

echo "=========================================="
echo "PayPal Webhook Contract Test Server"
echo "=========================================="
echo ""
echo "이 서버는 PayPal Simulator에서 보낸 실제 데이터를 받아 fixture로 저장합니다."
echo ""

# 프로젝트 루트로 이동
cd "$(dirname "$0")/../.." || exit

# .env 파일 확인
if [ ! -f .env ]; then
    echo "⚠️  경고: .env 파일이 없습니다."
    echo "   PAYPAL_WEBHOOK_ID를 설정하려면 .env 파일을 생성하세요."
    echo ""
fi

# Contract Test Server 실행
echo "🚀 Contract Test Server 시작 중..."
echo ""

uv run python tests/contract/contract_test_server.py

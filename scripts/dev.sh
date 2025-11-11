#!/bin/bash
# 개발 서버 실행 스크립트

set -e  # 에러 발생 시 스크립트 중단

echo "🚀 개발 서버를 시작합니다..."
echo ""

# 프로젝트 루트로 이동
cd "$(dirname "$0")/.."

# DB 마이그레이션 확인
echo "📊 DB 마이그레이션 상태 확인..."
uv run alembic current

echo ""
echo "🌱 Seed 데이터 확인..."
uv run python -m backend.db.seed

echo ""
echo "✅ 준비 완료!"
echo ""
echo "서버 시작: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "주문 조회: http://localhost:8000/order-check.html"
echo ""

# 개발 서버 실행
uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

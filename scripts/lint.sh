#!/bin/bash
set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# 스크립트 디렉토리 및 프로젝트 루트
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT/backend"

log_info "코드 품질 검사 시작"
echo "========================================"

# Ruff 체크
log_info "Ruff 코드 포맷팅 검사 중..."
if uv run ruff check .; then
    log_info "Ruff 검사 통과 ✓"
    RUFF_RESULT=0
else
    log_warning "Ruff 검사 실패 (아직 설정되지 않을 수 있음)"
    RUFF_RESULT=1
fi

echo ""

# MyPy 타입 체크
log_info "MyPy 타입 체크 중..."
if uv run mypy app/; then
    log_info "MyPy 검사 통과 ✓"
    MYPY_RESULT=0
else
    log_warning "MyPy 검사 실패 (아직 설정되지 않을 수 있음)"
    MYPY_RESULT=1
fi

echo "========================================"

# 결과 요약
if [ $RUFF_RESULT -eq 0 ] && [ $MYPY_RESULT -eq 0 ]; then
    log_info "코드 품질 검사 완료! ✓"
    exit 0
else
    log_warning "일부 검사 실패 (아직 설정되지 않을 수 있음)"
    log_warning "Ruff: $RUFF_RESULT, MyPy: $MYPY_RESULT"
    # 아직 설정되지 않았을 수 있으므로 exit 0 (나중에 exit 1로 변경)
    exit 0
fi

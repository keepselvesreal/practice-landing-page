#!/bin/bash
set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# 로깅 함수
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 스크립트 디렉토리 기준으로 프로젝트 루트 찾기
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "========================================"
log_info "환경변수 검증"
echo "========================================"

# 환경 파일 결정
ENV_FILE="${ENV_FILE:-.env.staging}"
ENV_PATH="$PROJECT_ROOT/$ENV_FILE"

log_info "파일: $ENV_FILE"

# .env 파일 존재 확인
if [ ! -f "$ENV_PATH" ]; then
    log_error ".env 파일이 없습니다: $ENV_PATH"
    exit 1
fi

# .env 파일에서 환경변수 추출 (주석과 빈 줄 제외)
log_info ".env 파일에서 환경변수 추출 중..."
REQUIRED_VARS=()
while IFS='=' read -r key value; do
    # 주석과 빈 줄 건너뛰기
    [[ "$key" =~ ^#.*$ ]] && continue
    [[ -z "$key" ]] && continue

    # 변수 이름 정리 (공백 제거)
    key=$(echo "$key" | xargs)

    # 유효한 변수명만 추가
    if [[ "$key" =~ ^[A-Z_][A-Z0-9_]*$ ]]; then
        REQUIRED_VARS+=("$key")
    fi
done < "$ENV_PATH"

log_info "필수 환경변수 ${#REQUIRED_VARS[@]}개 확인됨"
echo ""

# 검증 결과
PASSED=0
FAILED=0
FAILED_VARS=()

echo "검증 중..."
for var in "${REQUIRED_VARS[@]}"; do
    value="${!var}"

    # 환경변수가 설정되어 있는지 확인
    if [ -z "$value" ]; then
        log_error "✗ $var: 값이 비어있음"
        FAILED=$((FAILED + 1))
        FAILED_VARS+=("$var")
    else
        PASSED=$((PASSED + 1))
    fi
done

echo ""
echo "========================================"
echo "검증 결과"
echo "========================================"
echo -e "통과: ${GREEN}$PASSED${NC}/${#REQUIRED_VARS[@]}"
echo -e "실패: ${RED}$FAILED${NC}/${#REQUIRED_VARS[@]}"

if [ $FAILED -gt 0 ]; then
    echo ""
    log_error "누락된 환경변수:"
    for var in "${FAILED_VARS[@]}"; do
        echo "  - $var"
    done
fi

echo "========================================"

if [ $FAILED -eq 0 ]; then
    log_info "환경변수 검증 성공! ✓"
    exit 0
else
    log_error "환경변수 검증 실패! ($FAILED개 누락)"
    log_error "배포를 중단하고 환경변수를 설정하세요."
    exit 1
fi

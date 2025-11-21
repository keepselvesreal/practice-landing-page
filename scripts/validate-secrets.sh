#!/bin/bash
set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

log_check() {
    echo -e "${BLUE}[CHECK]${NC} $1"
}

# 스크립트 디렉토리
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# 환경 결정 (기본값: staging)
ENVIRONMENT="${1:-.staging}"
TEMPLATE_FILE="$PROJECT_ROOT/.env${ENVIRONMENT}.template"

echo "========================================"
log_info "GitHub Secrets 검증 (환경: $ENVIRONMENT)"
echo "========================================"
echo ""

# 템플릿 파일 확인
if [ ! -f "$TEMPLATE_FILE" ]; then
    log_error "템플릿 파일이 없습니다: $TEMPLATE_FILE"
    exit 1
fi

# GitHub Actions 환경에서는 검증 스킵 (시크릿 조회 권한 없음)
# 로컬 배포에서만 GitHub Secrets 검증 수행
if [ -n "$GITHUB_ACTIONS" ]; then
    log_info "GitHub Actions 환경: 시크릿 검증 스킵"
    log_info "이미 생성된 .env 파일로 배포 진행"
    exit 0
fi

log_check "1. 필수 변수 추출 중..."

# 템플릿에서 필수 변수 추출
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
done < "$TEMPLATE_FILE"

log_info "필수 변수: ${#REQUIRED_VARS[@]}개"
for var in "${REQUIRED_VARS[@]}"; do
    echo "  - $var"
done
echo ""

# GitHub CLI 확인
log_check "2. GitHub CLI 확인 중..."
if ! command -v gh &> /dev/null; then
    log_error "GitHub CLI(gh)가 설치되어 있지 않습니다."
    log_error "설치: https://cli.github.com/"
    exit 1
fi

# Repository Secrets 가져오기
log_check "3. GitHub Repository Secrets 확인 중..."
REPO_SECRETS=$(gh secret list --json name -q '.[].name' 2>/dev/null || echo "")
REPO_SECRETS_ARRAY=($REPO_SECRETS)
log_info "Repository Secrets: ${#REPO_SECRETS_ARRAY[@]}개"

# Environment Secrets 가져오기 (.staging -> staging, .production -> production)
ENV_NAME=$(echo "$ENVIRONMENT" | sed 's/^\.//') # .staging -> staging
log_check "4. GitHub Environment Secrets 확인 중 ($ENV_NAME)..."
ENV_SECRETS=$(gh secret list --env "$ENV_NAME" --json name -q '.[].name' 2>/dev/null || echo "")
ENV_SECRETS_ARRAY=($ENV_SECRETS)
log_info "Environment Secrets ($ENV_NAME): ${#ENV_SECRETS_ARRAY[@]}개"
echo ""

# 검증: GitHub Secrets와 템플릿 변수 비교
log_check "5. GitHub Secrets 검증 진행 중..."
MISSING_SECRETS=()
FOUND_SECRETS=0

for var in "${REQUIRED_VARS[@]}"; do
    # Repository Secrets 또는 Environment Secrets 중 하나에 있으면 OK
    if echo "$REPO_SECRETS" | grep -q "^$var$" || echo "$ENV_SECRETS" | grep -q "^$var$"; then
        FOUND_SECRETS=$((FOUND_SECRETS + 1))
    else
        MISSING_SECRETS+=("$var")
    fi
done

echo ""
echo "========================================"
log_info "검증 결과"
echo "========================================"
echo -e "찾음: ${GREEN}$FOUND_SECRETS${NC}/${#REQUIRED_VARS[@]}"

if [ ${#MISSING_SECRETS[@]} -gt 0 ]; then
    echo -e "누락: ${RED}${#MISSING_SECRETS[@]}${NC}/${#REQUIRED_VARS[@]}"
    echo ""
    log_error "GitHub Repository Secrets에 없는 변수:"
    for var in "${MISSING_SECRETS[@]}"; do
        echo "  - $var"
    done
    echo ""
    log_error "다음 명령으로 추가하세요:"
    echo "  gh secret set VAR_NAME --body \"value\""
    echo "========================================"
    exit 1
else
    echo -e "누락: ${GREEN}0${NC}/${#REQUIRED_VARS[@]}"
    echo ""
    log_info "✓ 모든 필수 GitHub Secrets이 등록되어 있습니다!"
    if [ -n "$GITHUB_ACTIONS" ]; then
        log_info "워크플로우 배포 진행 중..."
    else
        log_info "로컬 배포 준비 완료!"
    fi
    echo "========================================"
    exit 0
fi

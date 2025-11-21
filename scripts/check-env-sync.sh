#!/bin/bash

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

echo "========================================"
log_info "환경변수 동기화 검증"
echo "========================================"
echo ""

# GitHub CLI 확인
if ! command -v gh &> /dev/null; then
    log_error "GitHub CLI(gh)가 설치되어 있지 않습니다."
    log_error "설치: https://cli.github.com/"
    exit 1
fi

# .env 파일에서 변수 추출하는 함수
extract_env_vars() {
    local file=$1
    local vars=()

    while IFS='=' read -r key value; do
        [[ "$key" =~ ^#.*$ ]] && continue
        [[ -z "$key" ]] && continue
        key=$(echo "$key" | xargs)

        if [[ "$key" =~ ^[A-Z_][A-Z0-9_]*$ ]]; then
            vars+=("$key")
        fi
    done < "$file"

    echo "${vars[@]}"
}

# GitHub Repository Secrets 가져오기
log_info "GitHub Repository Secrets 가져오는 중..."
REPO_SECRETS=$(gh secret list --json name -q '.[].name' | sort)
REPO_SECRETS_ARRAY=($REPO_SECRETS)
log_info "Repository Secrets: ${#REPO_SECRETS_ARRAY[@]}개"
echo ""

# GitHub Environment Secrets 가져오기
log_info "Staging Environment Secrets 가져오는 중..."
STAGING_ENV_SECRETS=$(gh secret list --env staging --json name -q '.[].name' 2>/dev/null | sort)
STAGING_ENV_SECRETS_ARRAY=($STAGING_ENV_SECRETS)
log_info "Staging Environment Secrets: ${#STAGING_ENV_SECRETS_ARRAY[@]}개"

log_info "Production Environment Secrets 가져오는 중..."
PROD_ENV_SECRETS=$(gh secret list --env production --json name -q '.[].name' 2>/dev/null | sort)
PROD_ENV_SECRETS_ARRAY=($PROD_ENV_SECRETS)
log_info "Production Environment Secrets: ${#PROD_ENV_SECRETS_ARRAY[@]}개"
echo ""

# 전체 검증 결과
TOTAL_ISSUES=0

# ========================================
# 1. .env.staging 검증
# ========================================
log_check "1. .env.staging 파일 검증"

if [ ! -f "$PROJECT_ROOT/.env.staging" ]; then
    log_error ".env.staging 파일이 없습니다"
    TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
else
    STAGING_VARS=($(extract_env_vars "$PROJECT_ROOT/.env.staging"))
    log_info ".env.staging 변수: ${#STAGING_VARS[@]}개"

    # 각 변수가 GitHub에 있는지 확인
    missing_in_github=()
    for var in "${STAGING_VARS[@]}"; do
        # Repository secrets 또는 staging environment에 있어야 함
        if ! echo "$REPO_SECRETS" | grep -q "^$var$" && \
           ! echo "$STAGING_ENV_SECRETS" | grep -q "^$var$"; then
            missing_in_github+=("$var")
        fi
    done

    if [ ${#missing_in_github[@]} -gt 0 ]; then
        log_error "GitHub Secrets에 없는 변수 (${#missing_in_github[@]}개):"
        for var in "${missing_in_github[@]}"; do
            echo "  - $var"
        done
        TOTAL_ISSUES=$((TOTAL_ISSUES + ${#missing_in_github[@]}))
    else
        log_info "✓ 모든 변수가 GitHub Secrets에 존재"
    fi
fi
echo ""

# ========================================
# 2. .env.production 검증
# ========================================
log_check "2. .env.production 파일 검증"

if [ ! -f "$PROJECT_ROOT/.env.production" ]; then
    log_error ".env.production 파일이 없습니다"
    TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
else
    PROD_VARS=($(extract_env_vars "$PROJECT_ROOT/.env.production"))
    log_info ".env.production 변수: ${#PROD_VARS[@]}개"

    # 각 변수가 GitHub에 있는지 확인
    missing_in_github=()
    for var in "${PROD_VARS[@]}"; do
        # Repository secrets 또는 production environment에 있어야 함
        if ! echo "$REPO_SECRETS" | grep -q "^$var$" && \
           ! echo "$PROD_ENV_SECRETS" | grep -q "^$var$"; then
            missing_in_github+=("$var")
        fi
    done

    if [ ${#missing_in_github[@]} -gt 0 ]; then
        log_error "GitHub Secrets에 없는 변수 (${#missing_in_github[@]}개):"
        for var in "${missing_in_github[@]}"; do
            echo "  - $var"
        done
        TOTAL_ISSUES=$((TOTAL_ISSUES + ${#missing_in_github[@]}))
    else
        log_info "✓ 모든 변수가 GitHub Secrets에 존재"
    fi
fi
echo ""

# ========================================
# 3. GitHub Secrets 역검증
# ========================================
log_check "3. GitHub Secrets 역검증 (사용되지 않는 Secrets)"

if [ -f "$PROJECT_ROOT/.env.staging" ] && [ -f "$PROJECT_ROOT/.env.production" ]; then
    # 로컬 .env 파일들의 모든 변수 수집
    ALL_LOCAL_VARS=($(
        (extract_env_vars "$PROJECT_ROOT/.env.staging"
         extract_env_vars "$PROJECT_ROOT/.env.production") | sort -u
    ))

    # Repository Secrets 중 사용되지 않는 것
    unused_repo_secrets=()
    for secret in "${REPO_SECRETS_ARRAY[@]}"; do
        if ! printf '%s\n' "${ALL_LOCAL_VARS[@]}" | grep -q "^$secret$"; then
            unused_repo_secrets+=("$secret")
        fi
    done

    if [ ${#unused_repo_secrets[@]} -gt 0 ]; then
        log_warning "사용되지 않는 Repository Secrets (${#unused_repo_secrets[@]}개):"
        for secret in "${unused_repo_secrets[@]}"; do
            echo "  - $secret"
        done
    else
        log_info "✓ 모든 Repository Secrets가 사용됨"
    fi
fi
echo ""

# ========================================
# 4. 환경별 필수 변수 체크
# ========================================
log_check "4. 환경별 DATABASE_URL 확인"

has_staging_db=false
has_prod_db=false

if echo "$STAGING_ENV_SECRETS" | grep -q "^DATABASE_URL$"; then
    log_info "✓ Staging environment: DATABASE_URL 존재"
    has_staging_db=true
else
    log_error "✗ Staging environment: DATABASE_URL 누락"
    TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
fi

if echo "$PROD_ENV_SECRETS" | grep -q "^DATABASE_URL$"; then
    log_info "✓ Production environment: DATABASE_URL 존재"
    has_prod_db=true
else
    log_error "✗ Production environment: DATABASE_URL 누락"
    TOTAL_ISSUES=$((TOTAL_ISSUES + 1))
fi
echo ""

# ========================================
# 결과 요약
# ========================================
echo "========================================"
log_info "검증 결과"
echo "========================================"

if [ $TOTAL_ISSUES -eq 0 ]; then
    log_info "✓ 모든 환경변수가 동기화되어 있습니다!"
    exit 0
else
    log_error "✗ $TOTAL_ISSUES개의 동기화 문제가 발견되었습니다."
    log_error "GitHub Secrets를 업데이트하거나 .env 파일을 수정하세요."
    exit 1
fi

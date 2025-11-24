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

# 인자 파싱
STRICT_MODE=false

# 환경 인자 필수 확인
if [ -z "$1" ]; then
    echo "========================================"
    log_error "환경을 명시적으로 지정해야 합니다"
    echo "========================================"
    echo ""
    echo "사용법:"
    echo "  $0 <environment> [--strict]"
    echo ""
    echo "지원 환경:"
    echo "  staging     - 스테이징 배포 GitHub Secrets 검증"
    echo "  production  - 프로덕션 배포 GitHub Secrets 검증"
    echo ""
    echo "옵션:"
    echo "  --strict    - 엄격 모드: .env.example에 문서화되지 않은 Secrets 발견 시 에러"
    echo "              (기본: 경고만 출력)"
    echo ""
    echo "예시:"
    echo "  $0 staging              # 경고만"
    echo "  $0 staging --strict     # 엄격 검증"
    echo "  $0 production --strict  # 배포용"
    echo ""
    echo "참고:"
    echo "  로컬 환경변수 파일(.env.dev, .env.docker) 검증은"
    echo "  validate-env-file.sh 스크립트를 사용하세요."
    echo ""
    exit 1
fi

ENVIRONMENT="$1"

# --strict 플래그 확인
if [ "$2" == "--strict" ]; then
    STRICT_MODE=true
fi

EXAMPLE_FILE="$PROJECT_ROOT/.env.example"

echo "========================================"
if [ "$STRICT_MODE" = true ]; then
    log_info "GitHub Secrets 검증 (환경: $ENVIRONMENT, 모드: 엄격)"
else
    log_info "GitHub Secrets 검증 (환경: $ENVIRONMENT, 모드: 표준)"
fi
echo "========================================"
echo ""

# .env.example 파일 확인
if [ ! -f "$EXAMPLE_FILE" ]; then
    log_error ".env.example 파일이 없습니다: $EXAMPLE_FILE"
    exit 1
fi

# GitHub Actions 환경에서는 검증 스킵 (시크릿 조회 권한 없음)
# 로컬 배포에서만 GitHub Secrets 검증 수행
if [ -n "$GITHUB_ACTIONS" ]; then
    log_info "GitHub Actions 환경: 시크릿 검증 스킵"
    log_info "이미 생성된 .env 파일로 배포 진행"
    exit 0
fi

# 환경별 제외할 변수 정의
get_excluded_vars() {
    local env=$1
    case "$env" in
        staging)
            # Staging: Cloud Run 배포 시 제외할 변수
            # - TEST_ENV: 테스트 실행하지 않음
            # - GOOGLE_APPLICATION_CREDENTIALS: Cloud Run이 자동 주입
            echo "TEST_ENV GOOGLE_APPLICATION_CREDENTIALS"
            ;;
        production)
            # Production: Cloud Run 배포 시 제외할 변수
            # - TEST_ENV: 테스트 실행하지 않음
            # - GOOGLE_APPLICATION_CREDENTIALS: Cloud Run이 자동 주입
            echo "TEST_ENV GOOGLE_APPLICATION_CREDENTIALS"
            ;;
        *)
            log_error "지원하지 않는 환경입니다: $env"
            echo ""
            echo "이 스크립트는 staging, production 배포용 GitHub Secrets만 검증합니다."
            echo "로컬 환경변수 파일(.env.dev, .env.docker) 검증은 validate-env-file.sh를 사용하세요."
            echo ""
            exit 1
            ;;
    esac
}

log_check "1. .env.example에서 모든 변수 추출 중..."

# .env.example에서 모든 변수 자동 추출
ALL_VARS=()
while IFS='=' read -r key value; do
    # 주석과 빈 줄 건너뛰기
    [[ "$key" =~ ^#.*$ ]] && continue
    [[ -z "$key" ]] && continue

    # 변수 이름 정리 (공백 제거)
    key=$(echo "$key" | xargs)

    # 유효한 변수명만 추가
    if [[ "$key" =~ ^[A-Z_][A-Z0-9_]*$ ]]; then
        ALL_VARS+=("$key")
    fi
done < "$EXAMPLE_FILE"

log_info ".env.example의 전체 변수: ${#ALL_VARS[@]}개"

# 환경별 제외 변수 가져오기
EXCLUDED_VARS=($(get_excluded_vars "$ENVIRONMENT"))
if [ ${#EXCLUDED_VARS[@]} -gt 0 ]; then
    log_info "$ENVIRONMENT 환경에서 제외할 변수: ${#EXCLUDED_VARS[@]}개"
    for var in "${EXCLUDED_VARS[@]}"; do
        echo "  - $var"
    done
else
    log_info "$ENVIRONMENT 환경에서 제외할 변수: 없음"
fi

# 필수 변수 계산 (전체 - 제외)
REQUIRED_VARS=()
for var in "${ALL_VARS[@]}"; do
    # 제외 목록에 없으면 필수 변수로 추가
    if ! echo "${EXCLUDED_VARS[@]}" | grep -qw "$var"; then
        REQUIRED_VARS+=("$var")
    fi
done

log_info "$ENVIRONMENT 환경의 필수 변수: ${#REQUIRED_VARS[@]}개"
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

# Environment Secrets 가져오기
log_check "4. GitHub Environment Secrets 확인 중 ($ENVIRONMENT)..."
ENV_SECRETS=$(gh secret list --env "$ENVIRONMENT" --json name -q '.[].name' 2>/dev/null || echo "")
ENV_SECRETS_ARRAY=($ENV_SECRETS)
log_info "Environment Secrets ($ENVIRONMENT): ${#ENV_SECRETS_ARRAY[@]}개"
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

# 역방향 검증: GitHub Secrets에 있지만 .env.example에 없는 변수 찾기
log_check "6. .env.example에 문서화되지 않은 Secrets 확인 중..."
UNDOCUMENTED_SECRETS=()

# Repository Secrets + Environment Secrets 통합
ALL_SECRETS=$(echo -e "$REPO_SECRETS\n$ENV_SECRETS" | sort -u)

for secret in $ALL_SECRETS; do
    # .env.example의 모든 변수에 없으면
    if ! echo "${ALL_VARS[@]}" | grep -qw "$secret"; then
        UNDOCUMENTED_SECRETS+=("$secret")
    fi
done

if [ ${#UNDOCUMENTED_SECRETS[@]} -gt 0 ]; then
    echo ""
    echo "⚠️  추가 Secrets 발견: ${YELLOW}${#UNDOCUMENTED_SECRETS[@]}${NC}개"
    echo ""
    if [ "$STRICT_MODE" = true ]; then
        log_error "GitHub Secrets에 있지만 .env.example에 문서화되지 않은 변수:"
    else
        log_warning "GitHub Secrets에 있지만 .env.example에 문서화되지 않은 변수:"
    fi
    for secret in "${UNDOCUMENTED_SECRETS[@]}"; do
        echo "  - $secret"
    done
    echo ""
    if [ "$STRICT_MODE" = true ]; then
        log_error "엄격 모드: .env.example에 이 변수들을 추가하거나 GitHub Secrets에서 제거하세요."
    else
        log_info "권장: 이 변수들을 .env.example에 추가하여 문서화하세요."
        log_info "사용하지 않는 변수라면 GitHub Secrets에서 제거를 고려하세요."
    fi
    echo ""
fi

# 최종 결과
VALIDATION_FAILED=false

if [ ${#MISSING_SECRETS[@]} -gt 0 ]; then
    VALIDATION_FAILED=true
fi

# 엄격 모드에서는 문서화 안 된 Secrets도 실패
if [ "$STRICT_MODE" = true ] && [ ${#UNDOCUMENTED_SECRETS[@]} -gt 0 ]; then
    VALIDATION_FAILED=true
fi

if [ "$VALIDATION_FAILED" = true ]; then
    if [ ${#MISSING_SECRETS[@]} -gt 0 ]; then
        echo -e "누락: ${RED}${#MISSING_SECRETS[@]}${NC}/${#REQUIRED_VARS[@]}"
        echo ""
        log_error "GitHub Repository Secrets에 없는 변수:"
        for var in "${MISSING_SECRETS[@]}"; do
            echo "  - $var"
        done
        echo ""
        log_error "다음 명령으로 추가하세요:"
        echo "  gh secret set VAR_NAME --body \"value\" --env $ENVIRONMENT"
    fi
    log_error "검증 실패: GitHub Secrets을 확인하세요"
    echo "========================================"
    exit 1
else
    echo -e "누락: ${GREEN}0${NC}/${#REQUIRED_VARS[@]}"
    echo ""
    if [ ${#UNDOCUMENTED_SECRETS[@]} -gt 0 ]; then
        log_info "✓ 필수 GitHub Secrets 검증 통과 (경고 확인 권장)"
    else
        log_info "✓ 모든 GitHub Secrets이 올바르게 등록 및 문서화되어 있습니다!"
    fi
    if [ -n "$GITHUB_ACTIONS" ]; then
        log_info "워크플로우 배포 진행 중..."
    else
        log_info "로컬 배포 준비 완료!"
    fi
    echo "========================================"
    exit 0
fi

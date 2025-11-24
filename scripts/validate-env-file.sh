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
    echo "  dev         - 로컬 개발 환경 (.env.dev 검증)"
    echo "  docker      - 도커 테스트 환경 (.env.docker 검증)"
    echo "  staging     - 스테이징 환경 (.env.staging 검증)"
    echo "  production  - 프로덕션 환경 (.env.production 검증)"
    echo ""
    echo "옵션:"
    echo "  --strict    - 엄격 모드: .env.example에 문서화되지 않은 변수 발견 시 에러"
    echo "              (기본: 경고만 출력)"
    echo ""
    echo "예시:"
    echo "  $0 dev              # 로컬 개발 검증 (경고만)"
    echo "  $0 dev --strict     # 로컬 개발 엄격 검증"
    echo "  $0 docker --strict  # 도커 테스트 엄격 검증"
    echo "  $0 staging --strict # 스테이징 배포 전 검증 (CI/로컬)"
    echo "  $0 production --strict # 프로덕션 배포 전 검증 (CI/로컬)"
    echo ""
    exit 1
fi

ENVIRONMENT="$1"

# --strict 플래그 확인
if [ "$2" == "--strict" ]; then
    STRICT_MODE=true
fi

EXAMPLE_FILE="$PROJECT_ROOT/.env.example"
ENV_FILE="$PROJECT_ROOT/.env.$ENVIRONMENT"

echo "========================================"
if [ "$STRICT_MODE" = true ]; then
    log_info "환경변수 파일 검증 (환경: $ENVIRONMENT, 모드: 엄격)"
else
    log_info "환경변수 파일 검증 (환경: $ENVIRONMENT, 모드: 표준)"
fi
echo "========================================"
echo ""

# .env.example 파일 확인
if [ ! -f "$EXAMPLE_FILE" ]; then
    log_error ".env.example 파일이 없습니다: $EXAMPLE_FILE"
    exit 1
fi

# 환경 파일 확인
if [ ! -f "$ENV_FILE" ]; then
    log_error "환경변수 파일이 없습니다: $ENV_FILE"
    echo ""
    echo "다음 명령으로 생성하세요:"
    echo "  cp $EXAMPLE_FILE $ENV_FILE"
    echo "  # 그 후 $ENV_FILE을 편집하여 실제 값 입력"
    echo ""
    exit 1
fi

# 환경별 제외할 변수 정의
get_excluded_vars() {
    local env=$1
    case "$env" in
        dev)
            # Development: 로컬 개발 환경, 모든 변수 필요
            echo ""
            ;;
        docker)
            # Docker: 도커 테스트 환경, 모든 변수 필요
            echo ""
            ;;
        staging|production)
            # Staging/Production: 배포 환경
            # TEST_ENV는 테스트 전용이라 배포 환경에서 불필요
            echo "TEST_ENV"
            ;;
        *)
            log_error "지원하지 않는 환경입니다: $env"
            echo ""
            echo "지원 환경: dev, docker, staging, production"
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
echo ""

log_check "2. $ENV_FILE에서 변수 확인 중..."

# 환경 파일에서 변수 추출
ENV_VARS=()
while IFS='=' read -r key value; do
    # 주석과 빈 줄 건너뛰기
    [[ "$key" =~ ^#.*$ ]] && continue
    [[ -z "$key" ]] && continue

    # 변수 이름 정리 (공백 제거)
    key=$(echo "$key" | xargs)

    # 유효한 변수명만 추가
    if [[ "$key" =~ ^[A-Z_][A-Z0-9_]*$ ]]; then
        ENV_VARS+=("$key")
    fi
done < "$ENV_FILE"

log_info "$ENV_FILE의 변수: ${#ENV_VARS[@]}개"
echo ""

# 검증: 필수 변수가 환경 파일에 있는지 확인
log_check "3. 필수 변수 검증 진행 중..."
MISSING_VARS=()
EMPTY_VARS=()
FOUND_VARS=0

for var in "${REQUIRED_VARS[@]}"; do
    # 변수가 파일에 있는지 확인
    if echo "${ENV_VARS[@]}" | grep -qw "$var"; then
        # 변수가 있으면 값이 비어있는지 확인
        value=$(grep "^${var}=" "$ENV_FILE" | cut -d= -f2- | xargs)
        if [ -z "$value" ]; then
            EMPTY_VARS+=("$var")
        else
            FOUND_VARS=$((FOUND_VARS + 1))
        fi
    else
        MISSING_VARS+=("$var")
    fi
done

echo ""
echo "========================================"
log_info "검증 결과"
echo "========================================"
echo -e "설정됨: ${GREEN}$FOUND_VARS${NC}/${#REQUIRED_VARS[@]}"

# 누락된 변수 (파일에 아예 없음)
if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    echo -e "누락됨: ${RED}${#MISSING_VARS[@]}${NC}/${#REQUIRED_VARS[@]}"
    echo ""
    log_error "$ENV_FILE에 없는 변수:"
    for var in "${MISSING_VARS[@]}"; do
        echo "  - $var"
    done
    echo ""
fi

# 빈 값 변수 (파일에는 있지만 값이 없음)
if [ ${#EMPTY_VARS[@]} -gt 0 ]; then
    echo -e "빈 값:   ${YELLOW}${#EMPTY_VARS[@]}${NC}/${#REQUIRED_VARS[@]}"
    echo ""
    log_warning "$ENV_FILE에 값이 설정되지 않은 변수:"
    for var in "${EMPTY_VARS[@]}"; do
        echo "  - $var"
    done
    echo ""
fi

# 역방향 검증: 실제 파일에 있지만 .env.example에 없는 변수 찾기
log_check "4. .env.example에 문서화되지 않은 변수 확인 중..."
UNDOCUMENTED_VARS=()

for var in "${ENV_VARS[@]}"; do
    # .env.example의 모든 변수에 없으면
    if ! echo "${ALL_VARS[@]}" | grep -qw "$var"; then
        UNDOCUMENTED_VARS+=("$var")
    fi
done

if [ ${#UNDOCUMENTED_VARS[@]} -gt 0 ]; then
    echo ""
    echo "⚠️  추가 변수 발견: ${YELLOW}${#UNDOCUMENTED_VARS[@]}${NC}개"
    echo ""
    if [ "$STRICT_MODE" = true ]; then
        log_error "$ENV_FILE에 있지만 .env.example에 문서화되지 않은 변수:"
    else
        log_warning "$ENV_FILE에 있지만 .env.example에 문서화되지 않은 변수:"
    fi
    for var in "${UNDOCUMENTED_VARS[@]}"; do
        echo "  - $var"
    done
    echo ""
    if [ "$STRICT_MODE" = true ]; then
        log_error "엄격 모드: .env.example에 이 변수들을 추가하거나 $ENV_FILE에서 제거하세요."
    else
        log_info "권장: 이 변수들을 .env.example에 추가하여 팀과 문서를 공유하세요."
        log_info "임시 변수가 아니라면 $ENV_FILE에서 제거를 고려하세요."
    fi
    echo ""
fi

# 최종 결과
VALIDATION_FAILED=false

if [ ${#MISSING_VARS[@]} -gt 0 ] || [ ${#EMPTY_VARS[@]} -gt 0 ]; then
    VALIDATION_FAILED=true
fi

# 엄격 모드에서는 문서화 안 된 변수도 실패
if [ "$STRICT_MODE" = true ] && [ ${#UNDOCUMENTED_VARS[@]} -gt 0 ]; then
    VALIDATION_FAILED=true
fi

if [ "$VALIDATION_FAILED" = true ]; then
    log_error "검증 실패: $ENV_FILE을 확인하세요"
    echo "========================================"
    exit 1
else
    echo -e "누락됨: ${GREEN}0${NC}/${#REQUIRED_VARS[@]}"
    echo -e "빈 값:   ${GREEN}0${NC}/${#REQUIRED_VARS[@]}"
    echo ""
    if [ ${#UNDOCUMENTED_VARS[@]} -gt 0 ]; then
        log_info "✓ 필수 환경변수 검증 통과 (경고 확인 권장)"
    else
        log_info "✓ 모든 환경변수가 올바르게 설정 및 문서화되어 있습니다!"
    fi
    echo "========================================"
    exit 0
fi

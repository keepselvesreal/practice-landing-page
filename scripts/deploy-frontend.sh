#!/bin/bash
set -e  # 에러 발생 시 즉시 중단

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 로깅 함수
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# 스크립트 디렉토리 기준으로 프로젝트 루트 찾기
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

log_info "프로젝트 루트: $PROJECT_ROOT"

# 환경 파일 확인
if [ -z "$ENV_FILE" ]; then
    log_error "ENV_FILE 환경변수가 설정되지 않았습니다."
    log_error "사용법: ENV_FILE=.env.staging ./scripts/deploy-frontend.sh"
    log_error "또는: ENV_FILE=.env.production ./scripts/deploy-frontend.sh"
    exit 1
fi

# .env 파일 로드
if [ -f "$PROJECT_ROOT/$ENV_FILE" ]; then
    log_info "$ENV_FILE 파일 로드 중..."
    set -a
    source "$PROJECT_ROOT/$ENV_FILE"
    set +a
else
    log_error "$ENV_FILE 파일이 없습니다."
    log_error "다음 중 하나를 수행하세요:"
    log_error "  1. 로컬: 프로젝트 루트에 $ENV_FILE 파일 생성"
    log_error "  2. GitHub Actions: Secrets에서 환경변수 설정 후 워크플로우에서 파일 생성"
    exit 1
fi

# 환경 변수 검증 실행 (엄격 모드)
log_info "환경 변수 검증 중 (엄격 모드)..."

# ENV_FILE에서 환경 추출 (.env.staging -> staging)
DEPLOY_ENV=$(echo "$ENV_FILE" | sed 's/\.env\.//')

if ! "$SCRIPT_DIR/validate-env-file.sh" "$DEPLOY_ENV" --strict; then
    log_error "환경 변수 검증 실패. 배포를 중단합니다."
    exit 1
fi
log_info "환경 변수 검증 완료"
echo ""

# Firebase CLI 설치 확인
if ! command -v firebase &> /dev/null; then
    log_warning "Firebase CLI가 설치되어 있지 않습니다."
    log_info "Firebase CLI 설치 중..."
    npm install -g firebase-tools
else
    log_info "Firebase CLI 확인 완료"
fi

# Firebase 프로젝트 ID 확인
if [ -z "$FIREBASE_PROJECT_ID" ]; then
    log_error "FIREBASE_PROJECT_ID 환경변수가 설정되지 않았습니다."
    log_error "$ENV_FILE 파일에 FIREBASE_PROJECT_ID를 설정하세요."
    exit 1
fi
log_info "Firebase 프로젝트: $FIREBASE_PROJECT_ID"

# 인증 확인
log_info "Firebase 인증 확인 중..."

# CI 환경 (GitHub Actions/Cloud Build)에서는 인증 스킵
if [ -n "$CI" ] || [ -n "$GITHUB_ACTIONS" ] || [ -n "$BUILDER_OUTPUT" ]; then
    log_info "CI 환경 - 기존 인증 사용"
else
    # 로컬 환경 - gcloud 인증 확인
    log_info "로컬 환경 - gcloud 인증 확인 중..."
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null | grep -q .; then
        log_error "인증이 필요합니다: gcloud auth login"
        exit 1
    fi
    log_info "gcloud 인증 확인됨"
fi

# Firebase 프로젝트 설정
gcloud config set project "$FIREBASE_PROJECT_ID" 2>/dev/null || true

# 환경에 따라 Firebase Hosting 타겟 결정
if [[ "$ENV_FILE" == *"production"* ]]; then
    FIREBASE_TARGET="production"
    FIREBASE_URL="https://kbeauty-landing-page.web.app"
else
    FIREBASE_TARGET="staging"
    FIREBASE_URL="https://kbeauty-landing-page-staging.web.app"
fi

# Firebase 배포
log_info "Firebase Hosting ($FIREBASE_TARGET)에 프론트엔드 배포 시작..."
cd "$PROJECT_ROOT"

firebase deploy --only hosting:$FIREBASE_TARGET --project "$FIREBASE_PROJECT_ID"

if [ $? -eq 0 ]; then
    log_info "프론트엔드 배포 성공!"
    log_info "$FIREBASE_TARGET URL: $FIREBASE_URL"
else
    log_error "프론트엔드 배포 실패"
    exit 1
fi

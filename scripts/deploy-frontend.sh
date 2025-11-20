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

# 환경 파일 결정 (기본값: .env.staging)
ENV_FILE="${ENV_FILE:-.env.staging}"

# .env 파일 로드 (선택적)
if [ -f "$PROJECT_ROOT/$ENV_FILE" ]; then
    log_info "$ENV_FILE 파일 로드 중..."
    set -a
    source "$PROJECT_ROOT/$ENV_FILE"
    set +a
else
    log_warning "$ENV_FILE 파일이 없습니다. 기본 설정을 사용합니다."
fi

# Firebase CLI 설치 확인
if ! command -v firebase &> /dev/null; then
    log_warning "Firebase CLI가 설치되어 있지 않습니다."
    log_info "Firebase CLI 설치 중..."
    npm install -g firebase-tools
else
    log_info "Firebase CLI 확인 완료"
fi

# Firebase 프로젝트 ID 확인
FIREBASE_PROJECT_ID="${FIREBASE_PROJECT_ID:-kbeauty-landing-page}"
log_info "Firebase 프로젝트: $FIREBASE_PROJECT_ID"

# 인증 확인
log_info "Firebase 인증 확인 중..."

# GOOGLE_APPLICATION_CREDENTIALS가 설정되어 있으면 서비스 계정 활성화
if [ -n "$GOOGLE_APPLICATION_CREDENTIALS" ] && [ -f "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    log_info "서비스 계정으로 인증: $GOOGLE_APPLICATION_CREDENTIALS"
    # gcloud에서 서비스 계정 활성화 (Firebase CLI가 gcloud 인증을 따라감)
    gcloud auth activate-service-account --key-file="$GOOGLE_APPLICATION_CREDENTIALS" 2>/dev/null || true
else
    # gcloud 인증 사용 (로컬 개발 환경)
    log_info "gcloud 인증 사용"
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        log_error "gcloud 인증이 필요합니다. 'gcloud auth login'을 실행하세요."
        exit 1
    fi

    # gcloud 계정을 Firebase에도 적용
    log_info "gcloud 계정으로 Firebase 인증..."
    gcloud auth application-default login --quiet 2>/dev/null || true
fi

# Firebase 배포
log_info "Firebase Hosting (staging)에 프론트엔드 배포 시작..."
cd "$PROJECT_ROOT"

firebase deploy --only hosting:staging --project "$FIREBASE_PROJECT_ID"

if [ $? -eq 0 ]; then
    log_info "프론트엔드 배포 성공!"
    log_info "Staging URL: https://kbeauty-landing-page-staging.web.app"
else
    log_error "프론트엔드 배포 실패"
    exit 1
fi

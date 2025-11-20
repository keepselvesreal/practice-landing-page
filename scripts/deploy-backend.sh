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

# .env 파일 로드
if [ -f "$PROJECT_ROOT/$ENV_FILE" ]; then
    log_info "$ENV_FILE 파일 로드 중..."
    set -a  # 자동으로 export
    source "$PROJECT_ROOT/$ENV_FILE"
    set +a
else
    log_error "$ENV_FILE 파일이 없습니다."
    log_info "GitHub Secrets의 값으로 .env.staging 파일을 생성하세요."
    exit 1
fi

# 필수 환경 변수 확인
REQUIRED_VARS=(
    "DATABASE_URL"
    "GMAIL_ADDRESS"
    "GMAIL_APP_PASSWORD"
    "SMTP_HOST"
    "SMTP_PORT"
    "GOOGLE_PLACES_API_KEY"
    "PAYPAL_CLIENT_ID"
    "PAYPAL_CLIENT_SECRET"
    "PAYPAL_API_BASE"
)

log_info "필수 환경 변수 확인 중..."
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        log_error "환경 변수 '$var'가 설정되지 않았습니다."
        exit 1
    fi
done
log_info "모든 환경 변수 확인 완료"

# gcloud 인증 확인
log_info "gcloud 인증 상태 확인 중..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    log_error "gcloud 인증이 필요합니다. 'gcloud auth login'을 실행하세요."
    exit 1
fi
log_info "gcloud 인증 확인 완료"

# 프로젝트 ID 가져오기
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    log_error "GCP 프로젝트가 설정되지 않았습니다. 'gcloud config set project PROJECT_ID'를 실행하세요."
    exit 1
fi
log_info "GCP 프로젝트: $PROJECT_ID"

# Cloud Build로 백엔드 배포
log_info "Cloud Build로 백엔드 배포 시작..."
cd "$PROJECT_ROOT"

gcloud builds submit backend/ \
    --config=backend/cloudbuild.yaml \
    --substitutions="_DATABASE_URL=$DATABASE_URL,_GMAIL_ADDRESS=$GMAIL_ADDRESS,_GMAIL_APP_PASSWORD=$GMAIL_APP_PASSWORD,_SMTP_HOST=$SMTP_HOST,_SMTP_PORT=$SMTP_PORT,_GOOGLE_PLACES_API_KEY=$GOOGLE_PLACES_API_KEY,_PAYPAL_CLIENT_ID=$PAYPAL_CLIENT_ID,_PAYPAL_CLIENT_SECRET=$PAYPAL_CLIENT_SECRET,_PAYPAL_API_BASE=$PAYPAL_API_BASE"

if [ $? -eq 0 ]; then
    log_info "백엔드 배포 성공!"
    log_info "Cloud Run 서비스: https://console.cloud.google.com/run?project=$PROJECT_ID"
else
    log_error "백엔드 배포 실패"
    exit 1
fi

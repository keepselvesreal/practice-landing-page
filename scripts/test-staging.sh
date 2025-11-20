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
    set -a
    source "$PROJECT_ROOT/$ENV_FILE"
    set +a
else
    log_error "$ENV_FILE 파일이 없습니다."
    exit 1
fi

# BASE_URL 확인
if [ -z "$BASE_URL" ]; then
    log_error "BASE_URL 환경변수가 설정되지 않았습니다."
    exit 1
fi
log_info "테스트 대상 URL: $BASE_URL"

# Python 및 uv 확인
if ! command -v uv &> /dev/null; then
    log_error "uv가 설치되어 있지 않습니다. 'pip install uv'를 실행하세요."
    exit 1
fi
log_info "uv 확인 완료"

# backend 디렉토리로 이동
cd "$PROJECT_ROOT/backend"

# 의존성 설치 확인
if [ ! -d ".venv" ]; then
    log_info "가상 환경이 없습니다. 의존성 설치 중..."
    uv sync
else
    log_info "가상 환경 확인 완료"
fi

# Playwright 브라우저 설치 확인
log_info "Playwright 브라우저 확인 중..."
if ! uv run python -c "from playwright.sync_api import sync_playwright; sync_playwright()" 2>/dev/null; then
    log_warning "Playwright 브라우저를 설치합니다..."
    uv run playwright install chromium
else
    # chromium이 설치되어 있는지 확인
    if ! uv run playwright install --dry-run chromium 2>&1 | grep -q "is already installed"; then
        log_info "Playwright chromium 브라우저 설치 중..."
        uv run playwright install chromium
    else
        log_info "Playwright 브라우저 확인 완료"
    fi
fi

# E2E 테스트 실행
log_info "E2E 테스트 시작..."
log_info "TEST_ENV=production"
log_info "BASE_URL=$BASE_URL"

TEST_ENV=production BASE_URL="$BASE_URL" uv run pytest tests/e2e/ -v --tb=short

if [ $? -eq 0 ]; then
    log_info "모든 테스트 통과! ✓"
else
    log_error "테스트 실패"
    exit 1
fi

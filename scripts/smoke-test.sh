#!/bin/bash
# Note: set -e is intentionally NOT used here to allow all tests to run

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

log_test() {
    echo -e "${BLUE}[TEST]${NC} $1"
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
    log_error "다음 중 하나를 수행하세요:"
    log_error "  1. 로컬: 프로젝트 루트에 $ENV_FILE 파일 생성"
    log_error "  2. GitHub Actions: Secrets에서 환경변수 설정 후 워크플로우에서 파일 생성"
    exit 1
fi

# BASE_URL 확인
if [ -z "$BASE_URL" ]; then
    log_error "BASE_URL 환경변수가 설정되지 않았습니다."
    exit 1
fi

log_info "스모크 테스트 대상: $BASE_URL"
log_info "전체 테스트 시간 제한: 30초"
echo ""

# 테스트 카운터
PASSED=0
FAILED=0
TOTAL=4

# 테스트 시작 시간
START_TIME=$(date +%s)

# ========================================
# Test 1: Frontend HTML 컨텐츠 검증
# ========================================
log_test "Test 1/4: Frontend HTML 컨텐츠 검증"
if response=$(curl -f -s --max-time 5 "$BASE_URL" 2>&1); then
    # HTTP 200 + HTML 구조 검증
    if echo "$response" | grep -q "<!DOCTYPE html>" && \
       echo "$response" | grep -q "<title>K-Beauty" && \
       echo "$response" | grep -q "<html lang=\"ko\">"; then
        log_info "✓ Frontend HTML 컨텐츠 정상"
        log_info "  DOCTYPE: 확인"
        log_info "  Title: K-Beauty Landing Page"
        log_info "  Language: ko"
        ((PASSED++))
    else
        log_error "✗ Frontend HTML 구조 비정상"
        log_error "  응답 일부: ${response:0:200}..."
        ((FAILED++))
    fi
else
    log_error "✗ Frontend 접근 실패"
    log_error "  URL: $BASE_URL"
    ((FAILED++))
fi
echo ""

# ========================================
# Test 2: 정적 리소스 확인
# ========================================
log_test "Test 2/4: 정적 리소스 확인"
STATIC_PASSED=0
STATIC_FAILED=0

# CSS 파일 확인
css_status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$BASE_URL/css/style.css" 2>&1)
if [ "$css_status" = "200" ]; then
    log_info "✓ CSS 파일 접근 가능 (/css/style.css)"
    ((STATIC_PASSED++))
else
    log_error "✗ CSS 파일 접근 실패 (/css/style.css) - HTTP $css_status"
    ((STATIC_FAILED++))
fi

# JS 파일 확인
js_status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$BASE_URL/js/main.js" 2>&1)
if [ "$js_status" = "200" ]; then
    log_info "✓ JS 파일 접근 가능 (/js/main.js)"
    ((STATIC_PASSED++))
else
    log_error "✗ JS 파일 접근 실패 (/js/main.js) - HTTP $js_status"
    ((STATIC_FAILED++))
fi

# 정적 리소스 테스트 결과
if [ $STATIC_FAILED -eq 0 ]; then
    log_info "✓ 모든 정적 리소스 정상 ($STATIC_PASSED/2)"
    ((PASSED++))
else
    log_error "✗ 일부 정적 리소스 실패 ($STATIC_FAILED/2)"
    ((FAILED++))
fi
echo ""

# ========================================
# Test 3: API Health Check
# ========================================
log_test "Test 3/4: API Health Check"
health_status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$BASE_URL/health" 2>&1)
if [ "$health_status" = "200" ]; then
    response=$(curl -s --max-time 5 "$BASE_URL/health" 2>&1)
    if echo "$response" | grep -q "ok" || echo "$response" | grep -q "healthy"; then
        log_info "✓ API Health Check 통과"
        log_info "  응답: $response"
        ((PASSED++))
    else
        log_error "✗ API Health Check 응답 비정상"
        log_error "  응답: $response"
        ((FAILED++))
    fi
else
    log_error "✗ API Health Check 실패 - HTTP $health_status"
    log_error "  URL: $BASE_URL/health"
    # 에러 응답 내용 표시
    error_response=$(curl -s --max-time 5 "$BASE_URL/health" 2>&1 | head -10)
    log_error "  응답 일부: ${error_response:0:300}"
    ((FAILED++))
fi
echo ""

# ========================================
# Test 4: Config Endpoint
# ========================================
log_test "Test 4/4: Config Endpoint"
config_status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$BASE_URL/api/config" 2>&1)
if [ "$config_status" = "200" ]; then
    response=$(curl -s --max-time 5 "$BASE_URL/api/config" 2>&1)
    if echo "$response" | grep -q "google_places_api_key" && echo "$response" | grep -q "paypal_client_id"; then
        log_info "✓ Config Endpoint 정상"
        log_info "  google_places_api_key: 존재"
        log_info "  paypal_client_id: 존재"
        ((PASSED++))
    else
        log_error "✗ Config Endpoint 응답 형식 비정상"
        log_error "  응답: ${response:0:200}"
        ((FAILED++))
    fi
else
    log_error "✗ Config Endpoint 실패 - HTTP $config_status"
    log_error "  URL: $BASE_URL/api/config"
    error_response=$(curl -s --max-time 5 "$BASE_URL/api/config" 2>&1 | head -10)
    log_error "  응답 일부: ${error_response:0:300}"
    ((FAILED++))
fi
echo ""

# ========================================
# Note: Places API 테스트 제거됨
# ========================================
# Google Places API는 프론트엔드에서 직접 호출하므로
# 백엔드에 /api/places 엔드포인트가 없음
# 실제 Places API 동작은 E2E 테스트에서 검증

# 테스트 종료 시간
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# ========================================
# 결과 요약
# ========================================
echo "========================================"
log_info "스모크 테스트 결과"
echo "========================================"
echo -e "통과: ${GREEN}$PASSED${NC}/$TOTAL"
echo -e "실패: ${RED}$FAILED${NC}/$TOTAL"
echo "소요 시간: ${DURATION}초"
echo "========================================"

if [ $FAILED -eq 0 ]; then
    log_info "모든 스모크 테스트 통과! ✓"
    exit 0
else
    log_error "스모크 테스트 실패 ($FAILED/$TOTAL)"
    exit 1
fi

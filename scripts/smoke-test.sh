#!/bin/bash
set -e  # 에러 발생 시 즉시 중단

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
# Test 1: Frontend 접근 가능 여부 (최우선)
# ========================================
log_test "Test 1/4: Frontend 접근 가능 여부"
if response=$(curl -f -s -o /dev/null -w "%{http_code}" --max-time 5 "$BASE_URL" 2>&1); then
    if [ "$response" = "200" ]; then
        log_info "✓ Frontend 접근 가능 (HTTP $response)"
        ((PASSED++))
    else
        log_error "✗ Frontend 응답 코드 비정상 (HTTP $response)"
        ((FAILED++))
    fi
else
    log_error "✗ Frontend 접근 실패"
    log_error "  URL: $BASE_URL"
    ((FAILED++))
fi
echo ""

# ========================================
# Test 2: API Health Check
# ========================================
log_test "Test 2/4: API Health Check"
if response=$(curl -f -s --max-time 5 "$BASE_URL/api/health" 2>&1); then
    if echo "$response" | grep -q "healthy"; then
        log_info "✓ API Health Check 통과"
        log_info "  응답: $response"
        ((PASSED++))
    else
        log_error "✗ API Health Check 응답 비정상"
        log_error "  응답: $response"
        ((FAILED++))
    fi
else
    log_error "✗ API Health Check 실패"
    log_error "  URL: $BASE_URL/api/health"
    ((FAILED++))
fi
echo ""

# ========================================
# Test 3: Config Endpoint
# ========================================
log_test "Test 3/4: Config Endpoint"
if response=$(curl -f -s --max-time 5 "$BASE_URL/api/config" 2>&1); then
    if echo "$response" | grep -q "google_places_api_key" && echo "$response" | grep -q "paypal_client_id"; then
        log_info "✓ Config Endpoint 정상"
        log_info "  google_places_api_key: 존재"
        log_info "  paypal_client_id: 존재"
        ((PASSED++))
    else
        log_error "✗ Config Endpoint 응답 형식 비정상"
        log_error "  응답: $response"
        ((FAILED++))
    fi
else
    log_error "✗ Config Endpoint 실패"
    log_error "  URL: $BASE_URL/api/config"
    ((FAILED++))
fi
echo ""

# ========================================
# Test 4: Places API 연동
# ========================================
log_test "Test 4/4: Places API 연동"
if response=$(curl -f -s --max-time 10 "$BASE_URL/api/places?query=Seoul" 2>&1); then
    if echo "$response" | grep -q "results" || echo "$response" | grep -q "\["; then
        log_info "✓ Places API 연동 정상"
        # 결과 개수 표시
        count=$(echo "$response" | grep -o "\"name\"" | wc -l)
        log_info "  검색 결과: $count개"
        ((PASSED++))
    else
        log_error "✗ Places API 응답 형식 비정상"
        log_error "  응답: ${response:0:200}..."
        ((FAILED++))
    fi
else
    log_error "✗ Places API 호출 실패"
    log_error "  URL: $BASE_URL/api/places?query=Seoul"
    log_error "  응답: $response"
    ((FAILED++))
fi
echo ""

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

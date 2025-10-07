# 10장: Developing a testing strategy - 추출된 정보

## 핵심 내용
조직 차원의 테스트 전략 수립 방법을 다루며, 다양한 테스트 레벨의 장단점, 테스트 레시피 전략, 배포 차단/비차단 테스트, 병렬 처리 등을 포함합니다.

## 상세 핵심 내용
- **테스트 레벨별 특성**: 단위 테스트부터 E2E 테스트까지의 속도, 신뢰성, 유지보수성 트레이드오프
- **테스트 피라미드**: 각 레벨별 테스트 수량 분배와 최적 비율
- **테스트 레시피 전략**: 기능별로 어느 레벨에서 테스트할지 결정하는 방법
- **배포 파이프라인**: 배포 차단 테스트와 발견용 테스트의 구분
- **병렬 처리**: 테스트 실행 속도 최적화 전략

## 상세 내용

### 일반적인 테스트 유형과 레벨

#### 테스트 레벨 분류 (하위부터 상위로)
1. **단위 테스트 (Unit Tests)**
   - **특징**: 메모리 내 실행, 가장 빠름
   - **장점**: 작성하기 쉬움, 유지보수 쉬움, 빠른 피드백
   - **단점**: 시스템 전체 신뢰도는 낮음

2. **컴포넌트 테스트 (Component Tests)**
   - **특징**: 메모리 내에서 여러 단위의 상호작용 테스트
   - **범위**: 관련된 클래스들의 협력 검증

3. **통합 테스트 (Integration Tests)**
   - **특징**: 메모리 내에서 실제 의존성과의 통합 테스트
   - **범위**: 데이터베이스, 파일시스템 등 일부 실제 의존성 사용

4. **API 테스트 (Out of Process)**
   - **특징**: 별도 프로세스에서 API 호출 테스트
   - **범위**: REST API, GraphQL 등 외부 인터페이스 검증

5. **E2E/UI 격리 테스트**
   - **특징**: UI 레벨에서 일부 의존성 격리
   - **범위**: 사용자 워크플로우 검증 (일부 가짜 백엔드)

6. **E2E/UI 시스템 테스트**
   - **특징**: 모든 실제 의존성 사용
   - **장점**: 최고 신뢰도
   - **단점**: 가장 느림, 플레이키, 유지보수 어려움

### 테스트 피라미드 전략

#### 전통적 피라미드
```
     E2E (적음)
    ───────────
   API (보통)
  ─────────────
 Integration (많음)
──────────────────
Unit Tests (가장 많음)
```

#### 현실적 고려사항
- **70% 단위 테스트**: 빠른 피드백과 높은 커버리지
- **20% 통합 테스트**: 컴포넌트 간 상호작용 검증
- **10% E2E 테스트**: 핵심 사용자 경로 검증

### 테스트 레시피 전략

#### 기능별 테스트 레벨 결정
```javascript
// 복잡한 비즈니스 로직 - 단위 테스트 중심
const calculateTax = (income, deductions, taxRates) => {
    // 세금 계산 로직
    // → 90% 단위 테스트, 10% 통합 테스트
};

// API 엔드포인트 - API 테스트 중심
app.post('/api/orders', (req, res) => {
    // 주문 처리 로직
    // → 70% API 테스트, 20% 단위 테스트, 10% E2E 테스트
});

// 사용자 워크플로우 - E2E 테스트 중심
const checkoutProcess = () => {
    // 장바구니 → 결제 → 주문 확인
    // → 60% E2E 테스트, 30% API 테스트, 10% 단위 테스트
};
```

#### 레시피 결정 요소
- **복잡성**: 로직이 복잡할수록 낮은 레벨 테스트
- **변경 빈도**: 자주 바뀌는 코드는 빠른 테스트 필요
- **비즈니스 중요도**: 핵심 기능은 여러 레벨에서 테스트
- **외부 의존성**: 의존성이 많을수록 높은 레벨 테스트 필요

### 배포 차단 vs 발견 테스트

#### 배포 차단 테스트 (Delivery-Blocking)
```yaml
# CI/CD 파이프라인 예시
stages:
  - name: "Fast Tests"
    tests:
      - unit_tests
      - component_tests
    max_time: 5분
    failure_action: block_deployment
    
  - name: "Integration Tests"
    tests:
      - api_tests
      - database_integration
    max_time: 15분
    failure_action: block_deployment
```

**특징**:
- 빠른 실행 (5-15분 이내)
- 높은 안정성 (플레이키 테스트 제외)
- 핵심 기능 커버
- 실패 시 배포 차단

#### 발견 테스트 (Discovery Tests)
```yaml
  - name: "Discovery Tests"
    tests:
      - full_e2e_suite
      - performance_tests
      - security_scans
    max_time: 2시간
    failure_action: notify_team
    schedule: nightly
```

**특징**:
- 느린 실행 (1-2시간)
- 포괄적 커버리지
- 플레이키 테스트 포함 가능
- 실패 시 알림만 (배포 차단 안 함)

### 배포 vs 발견 파이프라인

#### 배포 파이프라인 (Delivery Pipeline)
```javascript
// 예시: Express.js API 배포 파이프라인
const deploymentPipeline = {
    triggers: ['push_to_main', 'pull_request'],
    stages: [
        {
            name: 'unit_tests',
            command: 'npm test',
            timeout: '3m'
        },
        {
            name: 'api_tests',
            command: 'npm run test:api',
            timeout: '10m'
        },
        {
            name: 'deploy',
            condition: 'all_tests_pass',
            target: 'production'
        }
    ]
};
```

#### 발견 파이프라인 (Discovery Pipeline)
```javascript
const discoveryPipeline = {
    triggers: ['nightly', 'weekly'],
    stages: [
        {
            name: 'comprehensive_e2e',
            command: 'npm run test:e2e:full',
            timeout: '2h'
        },
        {
            name: 'performance_tests',
            command: 'npm run test:performance',
            timeout: '1h'
        },
        {
            name: 'security_scan',
            command: 'npm run security:scan',
            timeout: '30m'
        }
    ],
    on_failure: 'notify_slack_channel'
};
```

### 테스트 병렬화 전략

#### 병렬 실행 최적화
```javascript
// Jest 병렬 설정 예시
module.exports = {
    // CPU 코어 수에 따른 워커 조정
    maxWorkers: process.env.CI ? 2 : '50%',
    
    // 테스트 분할
    testPathIgnorePatterns: ['/node_modules/', '/build/'],
    
    // 느린 테스트 우선 실행
    testSequencer: './jest-sequencer.js'
};

// 사용자 정의 시퀀서
class CustomSequencer {
    sort(tests) {
        // 느린 테스트를 먼저 실행하여 전체 시간 단축
        return tests.sort((a, b) => b.duration - a.duration);
    }
}
```

#### 리소스 기반 분할
```yaml
# GitHub Actions 병렬 실행
strategy:
  matrix:
    test-group: [unit, integration, e2e-auth, e2e-checkout]
    
steps:
  - name: Run Tests
    run: |
      case ${{ matrix.test-group }} in
        unit) npm run test:unit ;;
        integration) npm run test:integration ;;
        e2e-auth) npm run test:e2e -- --grep "authentication" ;;
        e2e-checkout) npm run test:e2e -- --grep "checkout" ;;
      esac
```

### 테스트 전략 결정 요소

#### 조직 요소
- **팀 크기**: 작은 팀은 단순한 전략, 큰 팀은 정교한 전략
- **릴리즈 주기**: 빈번한 배포는 빠른 테스트 필요
- **위험 허용도**: 높은 품질 요구사항은 포괄적 테스트 필요

#### 기술적 요소
- **시스템 복잡도**: 복잡한 시스템은 다층 테스트 전략
- **외부 의존성**: 많은 의존성은 격리 테스트 중요
- **성능 요구사항**: 높은 성능 요구는 성능 테스트 포함

## 주요 화제

### 테스트 전략 수립 프로세스
- **현상 분석**: 현재 테스트 상태와 문제점 파악
- **목표 설정**: 품질, 속도, 비용의 균형점 정의
- **단계적 적용**: 점진적 개선을 통한 전략 구현

### ROI 최적화
- **비용 대비 효과**: 각 테스트 레벨의 투자 대비 효과 분석
- **위험 기반 테스트**: 높은 위험 영역에 테스트 집중
- **자동화 우선순위**: 반복적이고 중요한 테스트부터 자동화

### 팀 협업과 책임
- **역할 분담**: 개발자, QA, DevOps의 테스트 역할 정의
- **기술 공유**: 테스트 기술과 도구 공유 문화
- **지속적 개선**: 정기적인 전략 검토와 개선

## 부차 화제

### 도구와 인프라
- **테스트 환경**: 다양한 환경에서의 테스트 실행 관리
- **모니터링**: 테스트 성능과 안정성 모니터링
- **보고**: 테스트 결과의 시각화와 분석

### 특수 상황 대응
- **레거시 시스템**: 기존 시스템에 테스트 전략 도입
- **마이크로서비스**: 분산 시스템의 테스트 전략
- **모바일 앱**: 플랫폼별 테스트 고려사항

### 품질 메트릭
- **커버리지**: 코드 커버리지와 기능 커버리지 측정
- **안정성**: 테스트 성공률과 플레이키 테스트 비율
- **효율성**: 테스트 실행 시간과 리소스 사용률

### 조직 문화
- **품질 문화**: 테스트를 중시하는 조직 문화 구축
- **학습 문화**: 테스트 실패로부터 학습하는 문화
- **협업 문화**: 개발과 테스트의 협업 강화
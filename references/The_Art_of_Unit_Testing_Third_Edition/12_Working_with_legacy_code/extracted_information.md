# 12장: Working with legacy code - 추출된 정보

## 핵심 내용
레거시 코드에 테스트를 추가하는 방법을 다루며, 테스트 도입 우선순위 결정, 안전한 리팩토링 전략, 레거시 시스템의 일반적인 문제점과 해결 방안을 제시합니다.

## 상세 핵심 내용
- **레거시 코드의 일반적 문제**: 기존 코드에 대한 테스트 작성의 어려움과 장애 요인
- **테스트 시작점 결정**: 논리적 복잡성, 의존성 수준, 우선순위를 고려한 체계적 접근
- **테스트 가능성 표**: 컴포넌트별 테스트 도입 우선순위를 정량적으로 평가하는 방법
- **안전한 리팩토링**: 테스트가 없는 코드를 안전하게 리팩토링하는 전략
- **점진적 개선**: 전체 시스템을 한 번에 바꾸는 것이 아닌 점진적 개선 접근법

## 상세 내용

### 레거시 코드의 일반적인 문제점

#### 대규모 개발 환경에서의 현실
- **규모**: 10,000명 이상의 개발자, 5년 이상된 시스템
- **기술 스택**: .NET, Java, C++ 혼재 환경
- **개발 현황**: 90%의 개발자가 기존 기능 유지보수 담당

#### TDD 도입 실패 원인
1. **기존 코드에 대한 테스트 작성 어려움**
   - 심(seam)이 없는 코드 구조
   - 강하게 결합된 의존성
   - 테스트하기 어려운 설계

2. **리팩토링의 실질적 어려움**
   - 리팩토링할 시간 부족
   - 기존 코드 변경에 대한 위험부담
   - 테스트 없이는 안전한 리팩토링 불가능

3. **조직적 저항**
   - 기존 설계 변경을 원하지 않는 사람들
   - 변화에 대한 두려움
   - 단기적 생산성 저하 우려

4. **도구와 환경의 한계**
   - 적절한 테스트 도구 부족
   - 레거시 시스템과 호환되지 않는 최신 도구
   - 복잡한 빌드 시스템

5. **시작점의 불명확성**
   - 어디서부터 시작해야 할지 모름
   - 우선순위 결정의 어려움

### 테스트 추가 시작점 결정

#### 평가 요소

##### 1. 논리적 복잡성 (Logical Complexity)
```javascript
// 높은 복잡성 예시
function processOrder(order) {
    if (order.type === 'premium') {
        if (order.amount > 1000) {
            if (order.customer.vipLevel > 3) {
                // 복잡한 중첩 로직
                switch (order.paymentMethod) {
                    case 'credit':
                        // 신용카드 처리
                        break;
                    case 'debit':
                        // 직불카드 처리
                        break;
                    // 더 많은 케이스들...
                }
            }
        }
    }
    // 더 많은 중첩 조건들...
}
```

**측정 방법**:
- 순환 복잡도(Cyclomatic Complexity) 계산
- 중첩된 if문, switch문, 반복문의 수
- 자동화 도구를 통한 복잡도 측정

##### 2. 의존성 수준 (Dependency Level)
```javascript
// 높은 의존성 예시
class OrderProcessor {
    process(order) {
        // 정적 메서드 호출 - 테스트하기 어려움
        Logger.log('Processing order');
        
        // 하드코딩된 의존성
        const emailService = new EmailService();
        emailService.sendConfirmation(order.email);
        
        // 전역 상태 의존
        if (GlobalConfig.isProductionMode) {
            PaymentGateway.charge(order.amount);
        }
        
        // 파일시스템 접근
        FileSystem.writeOrderToFile(order);
    }
}
```

**평가 기준**:
- 외부 서비스 호출 수
- 정적 메서드 의존성
- 전역 상태 참조
- 파일시스템, 네트워크 접근

##### 3. 우선순위 (Priority)
- 비즈니스 중요도
- 변경 빈도
- 버그 발생률
- 유지보수 필요성

#### 테스트 가능성 표 (Test-Feasibility Table)

```javascript
const testFeasibilityTable = [
    {
        component: 'OrderProcessor',
        logicalComplexity: 8,    // 1-10 scale
        dependencyLevel: 9,      // 1-10 scale  
        priority: 10,            // 1-10 scale
        totalScore: 27,
        recommendation: 'High priority - start here'
    },
    {
        component: 'UserValidator',
        logicalComplexity: 6,
        dependencyLevel: 3,
        priority: 7,
        totalScore: 16,
        recommendation: 'Medium priority'
    },
    {
        component: 'ConfigLoader',
        logicalComplexity: 2,
        dependencyLevel: 8,
        priority: 3,
        totalScore: 13,
        recommendation: 'Low priority'
    }
];

// 우선순위 계산 함수
const calculatePriority = (complexity, dependency, priority) => {
    // 가중치 적용 가능
    const complexityWeight = 0.4;
    const dependencyWeight = 0.3;
    const priorityWeight = 0.3;
    
    return (complexity * complexityWeight) + 
           (dependency * dependencyWeight) + 
           (priority * priorityWeight);
};
```

### 안전한 리팩토링 전략

#### 1. 캐릭터라이제이션 테스트 (Characterization Tests)
```javascript
// 기존 코드의 현재 동작을 기록하는 테스트
describe('Legacy OrderProcessor - Characterization Tests', () => {
    it('should behave as currently implemented', () => {
        const order = createLegacyOrder();
        
        // 현재 동작을 그대로 테스트
        // 올바른지는 모르지만 현재 동작을 보장
        const result = legacyOrderProcessor.process(order);
        
        expect(result.status).toBe('processed');
        expect(result.fees).toBe(25.50); // 현재 계산되는 값
        expect(result.taxes).toBe(8.25); // 현재 계산되는 값
    });
});
```

#### 2. 스프라우트 메서드 (Sprout Method)
```javascript
// 기존 코드에 새 기능을 추가할 때
class LegacyOrderProcessor {
    process(order) {
        // 기존 레거시 코드 (건드리지 않음)
        this.validateLegacyOrder(order);
        
        // 새로운 기능은 별도 메서드로 분리 (테스트 가능)
        const discountAmount = this.calculateDiscount(order);
        order.discount = discountAmount;
        
        this.processLegacyPayment(order);
    }
    
    // 새로운 메서드 - 테스트 가능하게 설계
    calculateDiscount(order) {
        if (order.customer.isVip && order.amount > 100) {
            return order.amount * 0.1;
        }
        return 0;
    }
}

// 새 메서드만 테스트
describe('OrderProcessor.calculateDiscount', () => {
    it('should apply 10% discount for VIP customers', () => {
        const processor = new LegacyOrderProcessor();
        const order = { customer: { isVip: true }, amount: 200 };
        
        const discount = processor.calculateDiscount(order);
        
        expect(discount).toBe(20);
    });
});
```

#### 3. 스프라우트 클래스 (Sprout Class)
```javascript
// 복잡한 새 기능은 별도 클래스로 분리
class DiscountCalculator {
    constructor(ruleEngine) {
        this.ruleEngine = ruleEngine;
    }
    
    calculate(order) {
        const rules = this.ruleEngine.getRules(order.type);
        return rules.reduce((total, rule) => {
            return total + rule.apply(order);
        }, 0);
    }
}

// 기존 레거시 코드에서 사용
class LegacyOrderProcessor {
    process(order) {
        // 기존 코드...
        
        // 새 클래스 사용
        const calculator = new DiscountCalculator(this.ruleEngine);
        order.discount = calculator.calculate(order);
        
        // 기존 코드 계속...
    }
}
```

### 점진적 개선 전략

#### 1. 스트랭글러 피그 패턴 (Strangler Fig Pattern)
```javascript
// 점진적으로 레거시 시스템을 새 시스템으로 교체
class OrderProcessorFacade {
    constructor() {
        this.legacyProcessor = new LegacyOrderProcessor();
        this.newProcessor = new NewOrderProcessor();
    }
    
    process(order) {
        // 기능별로 점진적 마이그레이션
        if (this.shouldUseNewProcessor(order)) {
            return this.newProcessor.process(order);
        } else {
            return this.legacyProcessor.process(order);
        }
    }
    
    shouldUseNewProcessor(order) {
        // 특정 조건에서만 새 프로세서 사용
        return order.type === 'premium' && 
               order.amount < 1000 &&
               Feature.isEnabled('new-order-processor');
    }
}
```

#### 2. 브랜치 바이 추상화 (Branch by Abstraction)
```javascript
// 추상화를 통한 점진적 교체
interface PaymentProcessor {
    processPayment(amount: number, method: string): PaymentResult;
}

class LegacyPaymentProcessor implements PaymentProcessor {
    processPayment(amount: number, method: string): PaymentResult {
        // 기존 레거시 구현
    }
}

class NewPaymentProcessor implements PaymentProcessor {
    processPayment(amount: number, method: string): PaymentResult {
        // 새로운 구현
    }
}

class PaymentService {
    constructor() {
        this.processor = Feature.isEnabled('new-payment') 
            ? new NewPaymentProcessor()
            : new LegacyPaymentProcessor();
    }
}
```

## 주요 화제

### 레거시 코드 특성
- **테스트 부족**: 기존 코드에 테스트가 거의 없음
- **강한 결합**: 의존성이 하드코딩되어 있음
- **복잡한 로직**: 단일 메서드나 클래스에 많은 책임
- **문서 부족**: 코드의 의도나 동작을 파악하기 어려움

### 위험 관리
- **안전한 변경**: 테스트 없이도 안전하게 변경할 수 있는 방법
- **점진적 접근**: 한 번에 모든 것을 바꾸지 않는 전략
- **롤백 계획**: 문제 발생 시 신속한 롤백 방안

### 도구와 기법
- **코드 분석 도구**: 복잡도 측정, 의존성 분석
- **리팩토링 도구**: 자동화된 리팩토링 지원
- **테스트 생성 도구**: 기존 코드 기반 테스트 자동 생성

## 부차 화제

### 조직적 고려사항
- **시간 투자**: 레거시 개선을 위한 충분한 시간 확보
- **리스크 관리**: 변경으로 인한 비즈니스 위험 최소화
- **팀 교육**: 레거시 코드 다루는 기법 교육

### 기술적 전략
- **마이크로서비스**: 레거시 모놀리스 분해 전략
- **API 게이트웨이**: 새 기능과 레거시 기능 통합
- **데이터 마이그레이션**: 점진적 데이터 이전 전략

### 성공 요인
- **명확한 목표**: 개선하고자 하는 목표의 명확성
- **단계적 계획**: 실현 가능한 단계적 개선 계획
- **지속적 평가**: 개선 효과의 지속적 측정과 평가

### 일반적인 함정
- **빅뱅 접근**: 모든 것을 한 번에 바꾸려는 시도
- **과도한 완벽주의**: 완벽한 테스트를 만들려는 강박
- **도구 의존**: 도구에만 의존하고 원리를 무시하는 접근
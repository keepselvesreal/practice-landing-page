# 8장: Maintainability - 추출된 정보

## 핵심 내용
테스트의 유지보수성을 향상시키기 위한 방법들을 다루며, 프로덕션 코드 변경 시 테스트 코드 변경을 최소화하고 테스트 실패의 근본 원인을 분석하는 전략을 제시합니다.

## 상세 핵심 내용
- **유지보수성 정의**: 테스트 변경을 강요당하는 빈도를 최소화하는 것
- **거짓 실패 vs 진짜 실패**: 실제 버그가 아닌 이유로 실패하는 테스트 식별과 대응
- **API 변경 대응**: 생산자 API 변경이 테스트에 미치는 영향 최소화
- **팩토리 패턴**: 테스트 객체 생성을 중앙화하여 변경 영향 범위 제한
- **테스트 간 결합도**: 과도한 어서션과 내부 구현 의존성 제거

## 상세 내용

### 실패하는 테스트로 인한 강제 변경

#### 진짜 실패 vs 거짓 실패
- **진짜 실패(True Failures)**: 프로덕션 코드의 실제 버그 발견
- **거짓 실패(False Failures)**: 버그 이외의 이유로 발생하는 테스트 실패
- **측정 지표**: 거짓 테스트 실패 수와 각 실패의 원인을 시간에 따라 측정

#### 거짓 실패의 주요 원인

##### 1. 관련성 없는 테스트 또는 테스트 간 충돌
```javascript
// 예시: 새로운 기능이 기존 테스트와 충돌
describe('old feature', () => {
    it('should work in old way', () => {
        // 이 테스트가 새 요구사항과 충돌할 수 있음
        expect(oldBehavior()).toBe(true);
    });
});

describe('new feature', () => {
    it('should work in new way', () => {
        // 새 요구사항을 테스트
        expect(newBehavior()).toBe(true);
    });
});
```

**대응 방법**:
- 더 이상 관련 없는 테스트 삭제
- 피처 토글 환경에서는 예외적으로 테스트 유지 가능

##### 2. 프로덕션 코드 API 변경
```javascript
// 변경 전
export class PasswordVerifier {
    constructor(rules: ((input) => boolean)[], logger: ILogger) {
        this._rules = rules;
        this._logger = logger;
    }
}

// 변경 후 - 매개변수 순서 변경
export class PasswordVerifier {
    constructor(logger: ILogger, rules: ((input) => boolean)[]) {
        this._logger = logger;
        this._rules = rules;
    }
}
```

**문제점**: API 변경으로 모든 테스트가 깨짐

### 팩토리 패턴을 통한 유지보수성 개선

#### 문제가 있는 접근법
```javascript
describe("password verifier", () => {
    it("test 1", () => {
        const verifier = new PasswordVerifier([], fakeLogger);
        // API 변경 시 이 줄이 모든 테스트에서 깨짐
    });
    
    it("test 2", () => {
        const verifier = new PasswordVerifier([], fakeLogger);
        // 중복된 생성 코드
    });
});
```

#### 팩토리 메서드 적용
```javascript
describe("password verifier", () => {
    const makeVerifier = (rules = [], logger = fakeLogger) => {
        return new PasswordVerifier(rules, logger);
    };
    
    it("test 1", () => {
        const verifier = makeVerifier();
        // API 변경 시 팩토리만 수정하면 됨
    });
    
    it("test 2", () => {
        const verifier = makeVerifier([customRule]);
        // 필요한 경우에만 매개변수 전달
    });
});
```

#### 고급 팩토리 패턴
```javascript
class VerifierBuilder {
    constructor() {
        this.rules = [];
        this.logger = fakeLogger;
    }
    
    withRules(rules) {
        this.rules = rules;
        return this;
    }
    
    withLogger(logger) {
        this.logger = logger;
        return this;
    }
    
    build() {
        return new PasswordVerifier(this.rules, this.logger);
    }
}

const makeVerifier = () => new VerifierBuilder();

// 사용법
it("test with custom rules", () => {
    const verifier = makeVerifier()
        .withRules([rule1, rule2])
        .withLogger(customLogger)
        .build();
});
```

### 과도한 어서션 방지

#### 문제가 있는 테스트
```javascript
it("should verify password", () => {
    const result = verifier.verify("password123");
    
    // 너무 많은 어서션
    expect(result.isValid).toBe(true);
    expect(result.errors).toHaveLength(0);
    expect(result.score).toBeGreaterThan(5);
    expect(result.timestamp).toBeDefined();
    expect(result.version).toBe("1.0");
    // ... 더 많은 어서션
});
```

#### 개선된 테스트
```javascript
it("should return valid result for good password", () => {
    const result = verifier.verify("password123");
    
    expect(result.isValid).toBe(true);
    // 핵심 동작만 검증
});

it("should include validation score", () => {
    const result = verifier.verify("password123");
    
    expect(result.score).toBeGreaterThan(5);
    // 별도 관심사는 별도 테스트
});
```

### 내부 구현 의존성 제거

#### 취약한 테스트
```javascript
it("should call validation in correct order", () => {
    const mockRule1 = jest.fn().mockReturnValue(true);
    const mockRule2 = jest.fn().mockReturnValue(true);
    
    verifier.verify("password", [mockRule1, mockRule2]);
    
    // 내부 구현에 의존적인 어서션
    expect(mockRule1).toHaveBeenCalledBefore(mockRule2);
    expect(mockRule1).toHaveBeenCalledTimes(1);
    expect(mockRule2).toHaveBeenCalledTimes(1);
});
```

#### 견고한 테스트
```javascript
it("should apply all rules to password", () => {
    const mockRule1 = jest.fn().mockReturnValue(true);
    const mockRule2 = jest.fn().mockReturnValue(false);
    
    const result = verifier.verify("password", [mockRule1, mockRule2]);
    
    // 결과에 집중, 구현 방식은 무시
    expect(result.isValid).toBe(false);
    expect(mockRule1).toHaveBeenCalledWith("password");
    expect(mockRule2).toHaveBeenCalledWith("password");
});
```

### 테스트 데이터 관리

#### 중앙화된 테스트 데이터
```javascript
const TestData = {
    validPasswords: ["StrongPass123!", "MySecure456#"],
    invalidPasswords: ["weak", "123", "password"],
    mockLogger: {
        info: jest.fn(),
        error: jest.fn()
    }
};

describe("password validation", () => {
    it("should accept strong passwords", () => {
        TestData.validPasswords.forEach(password => {
            expect(verifier.verify(password).isValid).toBe(true);
        });
    });
});
```

## 주요 화제

### 설계 원칙과 테스트
- **단일 책임 원칙**: 테스트도 하나의 관심사만 검증
- **개방/폐쇄 원칙**: 새 기능 추가 시 기존 테스트 변경 최소화
- **의존성 역전**: 테스트가 구체적 구현이 아닌 추상화에 의존

### 변경 영향 최소화 전략
- **계층화**: 테스트 유틸리티와 헬퍼 함수를 계층별로 구성
- **캡슐화**: 테스트 내부 복잡성을 헬퍼 함수로 숨김
- **표준화**: 팀 내 일관된 테스트 작성 패턴 확립

### 리팩토링과 테스트
- **안전한 리팩토링**: 테스트가 깨지지 않으면서 내부 구현 변경
- **테스트 주도 리팩토링**: 테스트를 먼저 개선한 후 프로덕션 코드 변경
- **점진적 개선**: 한 번에 모든 테스트를 고치지 말고 점진적으로 개선

## 부차 화제

### 도구와 자동화
- **테스트 생성 도구**: 반복적인 테스트 코드 생성 자동화
- **리팩토링 도구**: IDE의 자동 리팩토링 기능 활용
- **정적 분석**: 테스트 코드 품질 검사 도구 사용

### 팀 프랙티스
- **코드 리뷰**: 테스트 유지보수성도 리뷰 대상에 포함
- **페어 프로그래밍**: 테스트 작성 시 경험 공유
- **지식 공유**: 좋은 테스트 패턴과 안티패턴 공유

### 성능 고려사항
- **테스트 실행 시간**: 유지보수성과 실행 속도의 균형
- **병렬 실행**: 테스트 격리와 병렬 실행 최적화
- **리소스 관리**: 테스트 환경의 효율적 리소스 사용

### 문서화와 표준
- **테스트 가이드라인**: 팀 내 테스트 작성 표준 문서화
- **패턴 라이브러리**: 재사용 가능한 테스트 패턴 모음
- **베스트 프랙티스**: 업계 표준과 팀 경험 결합한 가이드
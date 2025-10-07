# 9장: Readability - 추출된 정보

## 핵심 내용
테스트의 가독성을 향상시키는 방법을 다루며, 명명 규칙, 변수명, 어서션과 액션 분리, 설정과 정리에 관한 모범 사례를 제시합니다.

## 상세 핵심 내용
- **가독성의 중요성**: 테스트는 다음 세대 프로그래머들에게 전하는 이야기
- **명명 규칙**: 진입점, 시나리오, 예상 동작의 3가지 요소를 포함한 테스트 명명
- **변수 명명**: 의도를 명확히 드러내는 변수명 사용
- **구조적 분리**: Arrange-Act-Assert 패턴의 명확한 구분
- **설정과 정리**: 테스트 환경 준비와 정리의 명확한 표현

## 상세 내용

### 단위 테스트 명명 규칙

#### 3가지 필수 정보 요소
1. **진입점(Entry Point)**: 테스트되는 작업 단위나 기능의 이름
2. **시나리오(Scenario)**: 진입점을 테스트하는 상황이나 조건
3. **예상 동작(Expected Behavior)**: 작업 단위의 출구점에서 예상되는 동작

#### 명명 방식의 다양한 예시

##### 1. 단일 테스트 함수명
```javascript
test('verifyPassword, with a failing rule, returns error based on rule.reason', () => {
    // 모든 정보가 함수명에 포함
});
```

##### 2. 중첩된 describe 구조
```javascript
describe('verifyPassword', () => {          // 진입점
    describe('with a failing rule', () => { // 시나리오
        it('returns error based on the rule.reason', () => { // 예상 동작
            // 구조적으로 정보를 분리
        });
    });
});
```

##### 3. 언더스코어 방식 (일부 언어/프레임워크)
```javascript
verifyPassword_withFailingRule_returnsErrorBasedOnRuleReason() {
    // 언더스코어로 요소 구분
}
```

### 변수 명명 모범 사례

#### 의도를 드러내는 명명
```javascript
// 나쁜 예
it('should work', () => {
    const v = new PasswordVerifier([r], l);
    const res = v.verify('abc');
    expect(res).toBe(false);
});

// 좋은 예
it('should reject weak password', () => {
    const strongPasswordRule = (password) => password.length > 8;
    const mockLogger = createMockLogger();
    const verifier = new PasswordVerifier([strongPasswordRule], mockLogger);
    
    const result = verifier.verify('abc');
    
    expect(result.isValid).toBe(false);
});
```

#### 테스트 더블 명명 규칙
```javascript
// 스텁 명명
const stubConfigService = {
    getLogLevel: () => 'DEBUG'
};

// 목 명명
const mockLogger = {
    info: jest.fn(),
    error: jest.fn()
};

// 스파이 명명
const spyEmailSender = jest.spyOn(emailService, 'send');
```

### Arrange-Act-Assert 패턴 강화

#### 명확한 섹션 분리
```javascript
it('should log password verification result', () => {
    // Arrange - 테스트 준비
    const passingRule = () => true;
    const mockLogger = createMockLogger();
    const verifier = new PasswordVerifier([passingRule], mockLogger);
    const testPassword = 'ValidPassword123';
    
    // Act - 테스트 실행
    const result = verifier.verify(testPassword);
    
    // Assert - 결과 검증
    expect(result.isValid).toBe(true);
    expect(mockLogger.info).toHaveBeenCalledWith('Password verification passed');
});
```

#### 복잡한 테스트의 헬퍼 메서드 활용
```javascript
describe('PasswordVerifier', () => {
    // 테스트 헬퍼 메서드들
    const createStrongPasswordRule = () => (password) => password.length > 8;
    const createWeakPasswordRule = () => (password) => password.length < 5;
    const createMockLogger = () => ({
        info: jest.fn(),
        error: jest.fn()
    });
    
    it('should handle multiple rules correctly', () => {
        // Arrange
        const rules = [
            createStrongPasswordRule(),
            createWeakPasswordRule()
        ];
        const logger = createMockLogger();
        const verifier = new PasswordVerifier(rules, logger);
        
        // Act
        const result = verifier.verify('medium');
        
        // Assert
        expect(result.isValid).toBe(false);
    });
});
```

### 테스트 설정과 정리

#### beforeEach/afterEach 사용 시 주의사항
```javascript
// 문제가 있는 사용
describe('PasswordVerifier', () => {
    let verifier;
    let logger;
    
    beforeEach(() => {
        logger = createMockLogger();
        verifier = new PasswordVerifier([], logger);
    });
    
    it('test 1', () => {
        // verifier가 어떻게 설정되었는지 스크롤해서 확인해야 함
    });
});

// 개선된 사용
describe('PasswordVerifier', () => {
    const setupVerifier = (rules = []) => {
        const logger = createMockLogger();
        return {
            verifier: new PasswordVerifier(rules, logger),
            logger
        };
    };
    
    it('test 1', () => {
        const { verifier, logger } = setupVerifier();
        // 설정이 명확하고 로컬에서 확인 가능
    });
});
```

### 어서션 품질 향상

#### 구체적이고 의미 있는 어서션
```javascript
// 모호한 어서션
it('should work correctly', () => {
    const result = verifier.verify('password');
    expect(result).toBeTruthy(); // 무엇이 참인지 불명확
});

// 명확한 어서션
it('should return validation result with isValid property', () => {
    const result = verifier.verify('password');
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain('Password too weak');
});
```

#### 에러 메시지 개선
```javascript
// 기본 어서션
expect(result.score).toBe(expectedScore);

// 의미 있는 에러 메시지
expect(result.score).toBe(expectedScore, 
    `Password score should be ${expectedScore} for input "${testPassword}"`);
```

### 테스트 데이터 관리

#### 테스트 데이터 상수화
```javascript
const TestPasswords = {
    WEAK: 'abc',
    MEDIUM: 'password123',
    STRONG: 'StrongP@ssw0rd!',
    EMPTY: '',
    VERY_LONG: 'a'.repeat(1000)
};

const TestRules = {
    LENGTH_RULE: (min) => (password) => password.length >= min,
    UPPERCASE_RULE: (password) => /[A-Z]/.test(password),
    SPECIAL_CHAR_RULE: (password) => /[!@#$%^&*]/.test(password)
};
```

#### 테스트별 데이터 생성 함수
```javascript
const createTestUser = (overrides = {}) => ({
    name: 'Test User',
    email: 'test@example.com',
    age: 25,
    ...overrides
});

it('should validate user age', () => {
    const underageUser = createTestUser({ age: 16 });
    const result = validateUser(underageUser);
    expect(result.errors).toContain('User must be 18 or older');
});
```

## 주요 화제

### 테스트 문서화 역할
- **살아있는 문서**: 테스트는 시스템의 동작을 설명하는 실행 가능한 문서
- **의도 전달**: 코드가 왜 그렇게 작성되었는지 의도 전달
- **예제 제공**: API나 기능 사용법의 구체적 예제 역할

### 팀 협업과 가독성
- **코드 리뷰**: 가독성도 리뷰의 중요한 요소
- **온보딩**: 새 팀원이 시스템을 이해하는 데 도움
- **지식 전수**: 도메인 지식과 비즈니스 로직 이해 촉진

### 유지보수와 가독성
- **디버깅 효율성**: 읽기 쉬운 테스트는 문제 진단 시간 단축
- **수정 용이성**: 의도가 명확한 테스트는 수정과 확장이 쉬움
- **회귀 방지**: 명확한 테스트는 의도치 않은 변경 방지

## 부차 화제

### 도구와 자동화
- **IDE 지원**: 자동 완성과 네비게이션 기능 활용
- **린터 설정**: 테스트 코드 스타일 자동 검사
- **템플릿**: 일관된 테스트 구조를 위한 코드 템플릿

### 언어별 관례
- **JavaScript/TypeScript**: describe/it 구조와 명명 관례
- **다른 언어**: 각 언어와 프레임워크의 테스트 명명 패턴
- **크로스 플랫폼**: 여러 언어를 사용하는 팀의 일관성 유지

### 복잡성 관리
- **테스트 길이**: 너무 길거나 짧은 테스트 방지
- **중첩 수준**: 과도한 중첩 구조 피하기
- **추상화 수준**: 적절한 추상화로 복잡성 숨기기

### 문화적 측면
- **명명 문화**: 팀 내 일관된 명명 규칙 확립
- **리뷰 문화**: 가독성을 중시하는 코드 리뷰 문화
- **학습 문화**: 좋은 테스트 예제 공유와 학습
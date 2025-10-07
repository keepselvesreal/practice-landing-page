# 5장: Isolation frameworks - 추출된 정보

## 핵심 내용
격리 프레임워크(isolation framework)를 사용하여 동적으로 스텁과 목 객체를 생성하고 설정하는 방법을 다루며, 수동으로 작성하는 것보다 간단하고 효율적인 방법을 제시합니다.

## 상세 핵심 내용
- **격리 프레임워크 정의**: 런타임에 가짜 객체를 동적으로 생성, 설정, 검증할 수 있는 프로그래밍 가능한 API 집합
- **두 가지 주요 유형**: 느슨한 타입(Jest, Sinon)과 강타입(substitute.js) 프레임워크
- **모듈 페이킹**: Jest의 jest.mock()을 사용한 전체 모듈 동적 대체
- **함수 페이킹**: 개별 함수에 대한 스파이와 목 생성
- **객체지향 페이킹**: substitute.js를 사용한 클래스와 인터페이스 처리

## 상세 내용

### 격리 프레임워크 정의
- **목적**: 동적 스텁과 동적 목 생성을 통한 의존성 격리
- **장점**: 수동 작성 대비 간단하고 빠르며 짧은 코드
- **적절한 사용**: 객체 상호작용 어서션과 시뮬레이션의 반복 코드 제거
- **위험성**: 잘못 사용시 테스트 가독성과 신뢰성 저하

### 프레임워크 유형 분류

#### 느슨한 JavaScript 격리 프레임워크
- **특징**: 바닐라 JavaScript 친화적, 느슨한 타입
- **예시**: Jest, Sinon
- **적합한 사용**: 함수형 스타일, 의식과 보일러플레이트 코드 최소화
- **대상 의존성**: 모듈 의존성, 함수형 의존성

#### 타입화된 JavaScript 격리 프레임워크
- **특징**: 객체지향적, TypeScript 친화적
- **예시**: substitute.js
- **적합한 사용**: 전체 클래스와 인터페이스 처리
- **대상 의존성**: 완전한 객체, 객체 계층, 인터페이스

### 모듈 동적 페이킹

#### 기존 문제점
```javascript
const { info, debug } = require("./complicated-logger");
const { getLogLevel } = require("./configuration-service");

const verifyPassword = (input, rules) => {
    // 하드코딩된 의존성으로 테스트 어려움
    if (failed.length === 0) {
        log("PASSED");  // 검증하기 어려운 부분
        return true;
    }
    log("FAIL");
    return false;
};
```

#### Jest를 사용한 해결책
```javascript
// jest.mock()을 사용한 전체 모듈 페이킹
jest.mock("./complicated-logger");
jest.mock("./configuration-service");

describe('password verifier', () => {
    it('calls logger info with PASSED when all rules pass', () => {
        // 모듈의 함수들이 자동으로 Jest 목으로 교체됨
        require("./configuration-service").getLogLevel.mockReturnValue("info");
        
        verifyPassword('input', []);
        
        expect(require("./complicated-logger").info)
            .toHaveBeenCalledWith("PASSED");
    });
});
```

### Command/Query 분리 패턴
- **Query**: 상태를 변경하지 않고 정보를 반환 (configuration service)
- **Command**: 상태를 변경하지만 값을 반환하지 않음 (logger)
- **의존성 분류**: Query는 스텁으로, Command는 목으로 처리

### Jest의 모킹 기능

#### 자동 모킹
- **jest.mock()**: 전체 모듈을 자동으로 목으로 교체
- **동적 생성**: 모든 함수가 Jest의 목 함수로 자동 교체
- **API 유지**: 원본 모듈과 동일한 API 구조 유지

#### 스파이 함수
- **jest.spyOn()**: 기존 객체의 특정 메서드만 감시
- **부분 목킹**: 일부 기능은 실제로 동작시키고 일부만 목으로 교체
- **복원 가능**: 테스트 후 원래 구현으로 복원 가능

### 객체지향 페이킹 (substitute.js)

#### 인터페이스 기반 목킹
```typescript
interface Logger {
    info(message: string): void;
    debug(message: string): void;
}

// substitute.js를 사용한 인터페이스 목 생성
const mockLogger = Substitute.for<Logger>();
mockLogger.info("PASSED");
mockLogger.received().info("PASSED");
```

#### 클래스 기반 목킹
- **완전한 객체**: 클래스의 모든 메서드 자동 구현
- **타입 안전성**: TypeScript와 완벽 호환
- **설정 가능**: 메서드별 개별 동작 설정 가능

## 주요 화제

### 프레임워크 선택 기준
- **의존성 유형**: 모듈/함수 vs 객체/인터페이스
- **언어 스타일**: JavaScript vs TypeScript
- **팀 선호도**: 함수형 vs 객체지향 스타일
- **복잡도**: 단순한 함수 vs 복잡한 객체 계층

### 동적 vs 수동 생성
- **동적 생성 장점**: 코드량 감소, 빠른 개발, 런타임 설정
- **수동 생성 장점**: 명확한 의도, 디버깅 용이성, 컴파일 타임 검증
- **선택 기준**: 복잡도와 유지보수성 균형점 찾기

### 테스트 품질 고려사항
- **과도한 사용 위험**: 프레임워크에 과도하게 의존하는 문제
- **가독성 vs 편의성**: 간편함과 명확성 사이의 균형
- **장기 유지보수**: 프레임워크 변경이 테스트에 미치는 영향

## 부차 화제

### Jest의 고급 기능
- **mockImplementation()**: 목 함수의 사용자 정의 구현
- **mockReturnValue()**: 반환값 설정
- **toHaveBeenCalledWith()**: 호출 인자 검증
- **mock.calls**: 호출 기록 직접 접근

### 프레임워크별 특성
- **Jest**: 테스트 러너와 통합된 내장 모킹 기능
- **Sinon**: 독립적인 모킹 라이브러리, 다양한 테스트 러너와 호환
- **substitute.js**: TypeScript 중심, 강타입 인터페이스 지원

### 모킹 전략
- **전체 모듈 vs 부분 모킹**: 필요한 범위에 따른 선택
- **자동 모킹 vs 수동 설정**: 기본 동작 vs 세밀한 제어
- **복원과 정리**: 테스트 간 격리를 위한 목 상태 관리

### 성능과 효율성
- **런타임 오버헤드**: 동적 생성의 성능 영향
- **메모리 사용**: 목 객체의 메모리 효율성
- **병렬 테스트**: 여러 테스트 간 목 상태 격리

### 디버깅과 문제 해결
- **목 호출 추적**: 호출 기록을 통한 디버깅
- **설정 검증**: 목이 올바르게 설정되었는지 확인
- **예상치 못한 호출**: 의도하지 않은 목 호출 감지
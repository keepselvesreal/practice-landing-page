# 3장: Breaking dependencies with stubs - 추출된 정보

## 핵심 내용
외부 의존성을 가진 코드를 테스트하기 위해 스텁(stub)을 사용하여 의존성을 끊는 방법을 다루며, 다양한 의존성 주입 기법을 소개합니다.

## 상세 핵심 내용
- **의존성 유형**: 발신 의존성(outgoing dependencies)과 수신 의존성(incoming dependencies)의 구분
- **테스트 더블**: 스텁(stub), 목(mock), 스파이(spy) 등 가짜 의존성의 분류와 역할
- **스텁의 역할**: 수신 의존성을 대체하여 테스트에 특정 데이터나 동작을 제공
- **의존성 주입 기법**: 함수형, 모듈형, 객체지향 방식의 다양한 주입 방법
- **시간 의존성**: 시간에 의존하는 코드의 테스트 문제와 해결책

## 상세 내용

### 의존성의 분류
- **발신 의존성(Outgoing Dependencies)**:
  - 단위 작업의 출구점을 나타내는 의존성
  - 로거 호출, 데이터베이스 저장, 이메일 전송, API 알림 등
  - 행동을 나타내는 동사형: "호출하기", "전송하기", "알리기"
  - Fire-and-forget 시나리오로 외부로 흘러나가는 형태
  
- **수신 의존성(Incoming Dependencies)**:
  - 출구점이 아닌 의존성으로 단위 작업의 최종 동작 요구사항을 나타내지 않음
  - 데이터베이스 쿼리 결과, 파일 시스템 내용, 네트워크 응답 등
  - 이전 작업의 결과로 단위 작업으로 흘러들어오는 수동적 데이터

### 테스트 더블 분류
- **스텁(Stub)**:
  - 수신 의존성(간접 입력)을 끊는 데 사용
  - 가짜 모듈, 객체, 함수로 테스트 중인 코드에 가짜 동작이나 데이터 제공
  - 스텁에 대해서는 어서션하지 않음
  - 단일 테스트에서 여러 스텁 사용 가능

- **목(Mock)**:
  - 발신 의존성(간접 출력 또는 출구점)을 끊는 데 사용
  - 테스트에서 호출되었는지 어서션하는 가짜 모듈, 객체, 함수
  - 단위 테스트에서 출구점을 나타냄
  - 테스트당 하나의 목만 사용 권장

### 스텁 사용 이유
- **테스트 일관성**: 변수값이 변하지 않는 일관된 테스트 실행
- **반복 가능성**: 시간, 네트워크, 파일시스템 등 외부 요인에 독립적
- **시나리오 시뮬레이션**: 특정 상황이나 예외 상황 쉽게 재현
- **플레이키 테스트 방지**: 외부 요인으로 인한 간헐적 실패 방지

### 함수형 의존성 주입 기법

#### 1. 매개변수 주입
```javascript
const verifyPassword = (input, rules, currentDay) => {
    if ([SATURDAY, SUNDAY].includes(currentDay)) {
        throw Error("It's the weekend!");
    }
    return [];
};
```

#### 2. 함수 주입
```javascript
const verifyPassword = (input, rules, getDayFn) => {
    const dayOfWeek = getDayFn();
    if ([SATURDAY, SUNDAY].includes(dayOfWeek)) {
        throw Error("It's the weekend!");
    }
    return [];
};
```

#### 3. 부분 적용(커링) 및 팩토리 함수
```javascript
const makeVerifier = (rules, dayOfWeekFn) => {
    return function (input) {
        if ([SATURDAY, SUNDAY].includes(dayOfWeekFn())) {
            throw new Error("It's the weekend!");
        }
    };
};
```

### 모듈형 주입 기법
- **의존성 래핑**: 직접 의존성을 중간 객체로 래핑
- **inject 함수**: 실제 의존성을 가짜 의존성으로 교체하는 메커니즘
- **reset 함수**: 원래 의존성으로 복원하는 기능
- **단점**: 타사 라이브러리 API에 강하게 결합되어 취약성 발생

### 객체지향 주입 기법

#### 1. 생성자 주입
```javascript
class PasswordVerifier {
    constructor(rules, dayOfWeekFn) {
        this.rules = rules;
        this.dayOfWeek = dayOfWeekFn;
    }
    verify(input) {
        if ([SATURDAY, SUNDAY].includes(this.dayOfWeek())) {
            throw new Error("It's the weekend!");
        }
        return [];
    }
}
```

#### 2. 객체 주입 (덕 타이핑)
- 함수 대신 객체를 매개변수로 전달
- JavaScript의 허용적 특성 활용
- 실제 객체와 가짜 객체가 같은 함수 구현

#### 3. 공통 인터페이스 활용 (TypeScript)
```typescript
interface TimeProviderInterface {
    getDay(): number;
}

class RealTimeProvider implements TimeProviderInterface {
    getDay(): number {
        return moment().day();
    }
}

class FakeTimeProvider implements TimeProviderInterface {
    fakeDay: number;
    getDay(): number {
        return this.fakeDay;
    }
}
```

## 주요 화제

### 의존성 제어와 역전
- **제어(Control)**: 의존성의 동작을 지시할 수 있는 능력
- **제어의 역전(Inversion of Control)**: 의존성 생성 책임을 내부에서 외부로 이전
- **의존성 주입(Dependency Injection)**: 설계 인터페이스를 통해 의존성을 전달하는 행위
- **심(Seam)**: 두 소프트웨어 조각이 만나는 지점으로 다른 것을 주입할 수 있는 곳

### 설계 철학과 권장사항
- **순수 함수**: 부작용이 없고 모든 의존성이 내장 주입된 함수
- **함수형 vs 객체지향**: 각 스타일의 장단점과 팀 상황에 따른 선택
- **모듈 주입의 위험성**: 타사 의존성 API 변경 시 테스트 취약성
- **중간 추상화**: 직접 제어하지 않는 타사 의존성에 대한 중간 계층 권장

### 아키텍처 패턴
- **포트와 어댑터**: 외부 의존성에 대한 중간 추상화 제공
- **헥사고날 아키텍처**: 동일한 개념의 다른 명칭
- **어니언 아키텍처**: 계층적 의존성 관리 방식

## 부차 화제

### 시간 관련 테스트 문제
- **플레이키 테스트**: 시간에 따라 간헐적으로 실패하는 테스트
- **주말/평일 시나리오**: 특정 시간에만 실행되는 테스트의 문제점
- **Moment.js 의존성**: JavaScript에서 날짜/시간 처리의 복잡성

### 테스트 유지보수성
- **팩토리 함수**: 테스트에서 객체 생성을 추상화하여 유지보수성 향상
- **생성자 시그니처 변경**: 단일 지점에서 변경 사항 관리
- **스크롤 피로 방지**: 테스트 코드의 가독성 향상

### JavaScript 특성 활용
- **덕 타이핑**: 같은 메서드를 구현하면 같은 타입으로 취급
- **런타임 검증**: 컴파일 타임이 아닌 실행 시점에서 타입 검증
- **TypeScript 도입**: 컴파일 타임 타입 안전성 확보

### IoC 컨테이너와 DI 프레임워크
- **Angular**: 생성자 주입을 통한 서비스(의존성) 주입
- **Spring, Autofac, StructureMap**: 다른 언어의 DI 컨테이너
- **수동 주입 선호**: 테스트에서는 프레임워크보다 수동 팩토리 함수 권장
# 6장: Unit testing asynchronous code - 추출된 정보

## 핵심 내용
비동기 코드의 단위 테스트 작성 방법을 다루며, 콜백, Promise, async/await 패턴에 대한 테스트 전략과 Extract Entry Point, Extract Adapter 패턴을 소개합니다.

## 상세 핵심 내용
- **비동기 테스트 복잡성**: 동작 완료를 명시적으로 기다려야 하는 비동기 코드의 테스트 어려움
- **다양한 비동기 패턴**: 콜백, Promise, async/await 각각에 대한 테스트 접근법
- **Extract Entry Point 패턴**: 비동기 로직을 분리하여 테스트 가능하게 만드는 리팩토링
- **Extract Adapter 패턴**: 외부 의존성을 추상화하여 비동기 코드를 테스트 가능하게 만드는 패턴
- **타이머 테스트**: setTimeout, setInterval 등 시간 기반 비동기 코드의 테스트

## 상세 내용

### 비동기 데이터 페칭 테스트

#### 기본 문제점
```javascript
// 콜백 버전
const isWebsiteAliveWithCallback = (callback) => {
    fetch("http://example.com")
        .then(response => {
            if (!response.ok) {
                throw Error(response.statusText);  // 네트워크 문제 시뮬레이션 어려움
            }
            return response.text();
        })
        .then(text => {
            if (text.includes("illustrative")) {
                callback({ success: true, status: "ok" });
            } else {
                callback({ success: false, status: "text missing" });  // 경로 테스트 어려움
            }
        })
        .catch(err => {
            callback({ success: false, status: err });  // 출구점 테스트 어려움
        });
};

// async/await 버전
const isWebsiteAliveWithAsyncAwait = async () => {
    try {
        const resp = await fetch("http://example.com");
        if (!resp.ok) {
            throw resp.statusText;  // 응답 시뮬레이션 어려움
        }
        const text = await resp.text();
        return text.includes("illustrative") 
            ? { success: true, status: "ok" }
            : { success: false, status: "text missing" };
    } catch (err) {
        return { success: false, status: err };
    }
};
```

### Jest의 비동기 테스트 지원

#### 1. done() 콜백 사용
```javascript
test('callback version works', (done) => {
    isWebsiteAliveWithCallback((result) => {
        expect(result.success).toBe(true);
        done();  // 테스트 완료 신호
    });
});
```

#### 2. Promise 반환
```javascript
test('promise version works', () => {
    return isWebsiteAlivePromise().then(result => {
        expect(result.success).toBe(true);
    });
});
```

#### 3. async/await 사용
```javascript
test('async version works', async () => {
    const result = await isWebsiteAliveWithAsyncAwait();
    expect(result.success).toBe(true);
});
```

### Extract Entry Point 패턴

#### 문제점
- 네트워크 호출로 인한 테스트 속도 저하
- 외부 서비스 의존성으로 인한 테스트 불안정성
- 다양한 응답 시나리오 시뮬레이션 어려움

#### 해결책: 로직 분리
```javascript
// 1. 데이터 페칭 로직 분리
const fetchWebsiteText = async (url) => {
    const resp = await fetch(url);
    if (!resp.ok) {
        throw resp.statusText;
    }
    return resp.text();
};

// 2. 비즈니스 로직만 테스트
const checkWebsiteText = (text) => {
    return text.includes("illustrative")
        ? { success: true, status: "ok" }
        : { success: false, status: "text missing" };
};

// 3. 통합 함수
const isWebsiteAlive = async (url = "http://example.com") => {
    try {
        const text = await fetchWebsiteText(url);
        return checkWebsiteText(text);
    } catch (err) {
        return { success: false, status: err };
    }
};
```

### Extract Adapter 패턴

#### 의존성 주입을 통한 테스트 개선
```javascript
// 어댑터 인터페이스 정의
class HttpAdapter {
    async get(url) {
        const resp = await fetch(url);
        if (!resp.ok) {
            throw resp.statusText;
        }
        return resp.text();
    }
}

// 테스트용 가짜 어댑터
class FakeHttpAdapter {
    constructor(fakeText) {
        this.fakeText = fakeText;
    }
    
    async get(url) {
        return this.fakeText;
    }
}

// 의존성 주입된 함수
const isWebsiteAliveWithAdapter = async (adapter, url = "http://example.com") => {
    try {
        const text = await adapter.get(url);
        return checkWebsiteText(text);
    } catch (err) {
        return { success: false, status: err };
    }
};
```

### 타이머 기반 비동기 코드 테스트

#### 시간 의존적 코드 문제
```javascript
const delayedFunction = (callback, delay = 1000) => {
    setTimeout(() => {
        callback("completed");
    }, delay);
};
```

#### Jest의 타이머 모킹
```javascript
test('delayed function calls callback', () => {
    jest.useFakeTimers();  // 가짜 타이머 사용
    
    const mockCallback = jest.fn();
    delayedFunction(mockCallback, 1000);
    
    // 타이머를 1000ms 진행
    jest.advanceTimersByTime(1000);
    
    expect(mockCallback).toHaveBeenCalledWith("completed");
    
    jest.useRealTimers();  // 실제 타이머로 복원
});
```

### 비동기 테스트 레벨

#### 단위 테스트 레벨
- **순수 로직**: 비동기 부분을 제거하고 순수 함수만 테스트
- **의존성 주입**: 외부 서비스를 가짜로 교체
- **빠른 실행**: 네트워크 호출 없이 즉시 완료

#### 통합 테스트 레벨
- **실제 의존성**: 진짜 HTTP 호출, 데이터베이스 연결 등
- **End-to-End**: 전체 워크플로우 검증
- **느린 실행**: 실제 네트워크 지연 포함

## 주요 화제

### 비동기 테스트 전략
- **테스트 피라미드**: 단위 테스트(많음) > 통합 테스트(보통) > E2E 테스트(적음)
- **격리 vs 통합**: 각 레벨에서 검증해야 할 내용의 구분
- **속도 vs 신뢰성**: 빠른 테스트와 현실적인 테스트 사이의 균형

### 패턴 적용 가이드라인
- **Extract Entry Point**: 네트워크/파일시스템 호출을 포함한 함수에 적용
- **Extract Adapter**: 외부 API나 서비스에 의존하는 코드에 적용
- **의존성 주입**: 테스트 가능성을 위한 설계 개선

### 타이머와 시간 처리
- **실제 시간 vs 가짜 시간**: 테스트 실행 속도와 정확성 고려
- **시간 진행 제어**: jest.advanceTimersByTime(), jest.runAllTimers()
- **정리와 복원**: 테스트 간 격리를 위한 타이머 상태 관리

## 부차 화제

### Jest의 비동기 테스트 기능
- **타임아웃 설정**: 테스트별 또는 전역 타임아웃 조정
- **Promise rejection 처리**: expect().rejects.toThrow() 패턴
- **병렬 실행**: 여러 비동기 테스트의 동시 실행

### 실제 프로젝트 적용
- **API 클라이언트 테스트**: REST API 호출 로직의 단위 테스트
- **데이터베이스 작업**: 비동기 DB 쿼리의 테스트 전략
- **이벤트 기반 코드**: EventEmitter, DOM 이벤트 처리 테스트

### 성능과 안정성
- **테스트 실행 시간**: 비동기 테스트의 성능 최적화
- **플레이키 테스트**: 타이밍 이슈로 인한 불안정한 테스트 방지
- **메모리 누수**: 비동기 테스트에서의 리소스 정리

### 디버깅과 문제 해결
- **비동기 스택 트레이스**: 에러 발생 지점 추적의 어려움
- **테스트 행업**: 무한 대기 상태의 테스트 진단
- **리소스 정리**: 테스트 후 열린 연결이나 타이머 정리
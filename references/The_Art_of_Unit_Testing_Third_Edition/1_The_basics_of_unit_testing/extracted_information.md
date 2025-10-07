# 1장: 단위 테스트의 기초 - 추출된 정보

## 핵심 내용
- 단위 테스트의 정의와 기본 개념
- Entry Point와 Exit Point를 통한 단위 작업(Unit of Work) 이해
- 좋은 단위 테스트의 특성과 통합 테스트와의 차이점
- 테스트 주도 개발(TDD)의 기본 원리

## 상세 핵심 내용

### 단위 테스트 정의
- **단위 테스트**: 자동화된 코드 조각으로 진입점을 통해 작업 단위를 호출하고 출구점 중 하나를 확인하는 테스트
- **SUT (Subject Under Test)**: 테스트 대상인 시스템, 수트, 또는 주제
- **단위 작업**: 진입점 호출부터 하나 이상의 출구점을 통한 눈에 띄는 최종 결과까지의 모든 행동

### Entry Point와 Exit Point
- **Entry Point**: 외부에서 트리거할 수 있는 진입점 (예: 함수 호출)
- **Exit Point 유형**:
  1. 반환 값 (Return Value)
  2. 상태 변경 (State Change)
  3. 제3자 종속성 호출 (Third-party Dependency Call)

### 좋은 단위 테스트의 특성
- 빠른 실행 속도
- 테스트 대상 코드에 대한 완전한 제어
- 완전한 격리 (다른 테스트와 독립적 실행)
- 메모리에서 실행 (파일시스템, 네트워크, 데이터베이스 불필요)
- 동기적이고 선형적 실행

## 상세 내용

### 테스트 프레임워크 없이 테스트 작성
```javascript
const assertEquals = (expected, actual) => {
  if (actual !== expected) {
    throw new Error(`Expected ${expected} but was ${actual}`);
  }
};

const check = (name, implementation) => {
  try {
    implementation();
    console.log(`${name} passed`);
  } catch (e) {
    console.error(`${name} FAILED`, e.stack);
  }
};
```

### 통합 테스트 vs 단위 테스트
- **통합 테스트**: 실제 종속성을 사용하는 테스트
- **단위 테스트**: 모든 종속성을 메모리 내에서 제어하는 테스트
- 통합 테스트는 느리고 디버그하기 어려우며 여러 실패 지점을 가짐

### TDD의 3단계 사이클
1. **실패하는 테스트 작성**: 기능이 누락되었음을 증명
2. **테스트를 통과시키는 코드 작성**: 가장 단순한 구현
3. **리팩터링**: 코드 품질 개선 (기능 변경 없이)

## 주요 화제

### 1. 단위 테스트 기본 개념
- 수동 테스트의 문제점과 자동화의 필요성
- JavaScript/TypeScript를 사용한 테스트 예제
- 절차형, 함수형, 객체지향 패러다임에서의 테스트

### 2. Entry Point와 Exit Point 분석
- 함수 수준에서의 진입점과 출구점
- 여러 출구점을 가진 함수의 테스트 전략
- 각 출구점별 개별 테스트 작성의 중요성

### 3. 테스트 품질 기준
- 읽기 쉬움 (Readability)
- 유지보수성 (Maintainability) 
- 신뢰성 (Trust)
- 일관된 결과 제공

### 4. 통합 테스트와의 구분
- 실제 종속성 사용 시 발생하는 문제점
- 격리된 환경에서의 테스트의 장점
- 회귀 테스트의 중요성

## 부차 화제

### 1. JavaScript vs TypeScript 사용법
- 절차형/함수형 예제에는 JavaScript 사용
- 객체지향 예제에는 TypeScript 사용
- 다양한 프로그래밍 패러다임 지원

### 2. 레거시 코드 정의
- "테스트가 없는 코드"로 정의
- 유지보수가 어려운 오래된 코드
- 테스트 도입의 어려움

### 3. 종속성 관리
- 종속성의 정의: 테스트에서 완전히 제어할 수 없는 요소
- 로거, 네트워크, 데이터베이스 등의 외부 종속성
- Stub을 통한 종속성 대체 방법

### 4. TDD 학습 전략
- 세 가지 핵심 기술: 좋은 테스트 작성, 테스트 우선 작성, 설계
- 단계적 학습 접근법
- 각 기술을 개별적으로 학습하는 것의 중요성

### 5. 코드 예제와 실습
- GitHub 저장소: https://github.com/royosherove/aout3-samples
- Node.js 12.8 이상 요구
- CommonJS 모듈 시스템 사용
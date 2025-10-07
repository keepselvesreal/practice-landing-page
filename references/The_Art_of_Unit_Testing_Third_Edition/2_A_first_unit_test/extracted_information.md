# 2장: A first unit test - 추출된 정보

## 핵심 내용
Jest 프레임워크를 사용한 첫 번째 단위 테스트 작성법을 다루며, 테스트 구조, 명명 규칙, 어서션 라이브러리, 코드 중복 제거 방법을 설명합니다.

## 상세 핵심 내용
- **Jest 프레임워크**: Facebook에서 개발한 오픈소스 테스트 프레임워크로, 테스트 라이브러리, 어서션 라이브러리, 테스트 러너, 테스트 리포터 역할을 모두 수행
- **AAA 패턴**: Arrange-Act-Assert 구조로 테스트를 작성하는 표준 패턴
- **USE 명명법**: Unit under test, Scenario, Expectation을 포함한 테스트 명명 규칙
- **코드 중복 제거**: beforeEach(), 팩토리 메소드, 매개변수화된 테스트를 통한 중복 코드 제거
- **테스트 구조화**: describe(), it() 함수를 사용한 테스트 그룹화 및 구조화

## 상세 내용

### Jest 프레임워크 도입
- **설치 및 설정**: npm/yarn을 통한 Jest 설치, package.json 또는 jest.config.js 설정
- **테스트 파일 발견**: __tests__ 폴더 또는 *.spec.js, *.test.js 패턴
- **실행 방법**: npx jest, 전역 설치, npm scripts를 통한 실행
- **출력 정보**: 실패한 테스트 목록, 상세 오류 보고서, 실행 시간, 성공/실패 통계

### Password Verifier 프로젝트
- **함수형 구현**: verifyPassword(input, rules) 함수
- **상태형 구현**: PasswordVerifier 클래스 기반 구현
- **규칙 시스템**: 각 규칙은 {passed: boolean, reason: string} 반환

### 테스트 구조와 명명
- **AAA 패턴**: 
  - Arrange: 테스트 입력 설정
  - Act: 진입점 호출
  - Assert: 결과 검증
- **USE 명명법**: 테스트 이름에 Unit, Scenario, Expectation 포함
- **예시**: "verifyPassword, given a failing rule, returns errors"

### 테스트 구조화 기법
- **describe() 블록**: 테스트 그룹화를 위한 스코핑 함수
- **중첩 구조**: describe() 내부에 describe() 중첩 가능
- **it() vs test()**: it()는 test()의 별칭으로 describe와 함께 사용 시 가독성 향상

### 코드 중복 제거 전략
- **beforeEach() 접근법**:
  - 장점: 중복 코드 제거
  - 단점: 스크롤 피로(scroll fatigue), 복잡성 증가
- **팩토리 메소드 접근법**:
  - makeVerifier(), makeVerifierWithFailedRule() 등
  - 가독성 향상, 자체 캡슐화된 테스트
- **매개변수화된 테스트**: test.each()를 사용한 반복 테스트

### 고급 테스트 기법
- **문자열 비교**: toContain(), toMatch() 사용으로 테스트 견고성 향상
- **예외 테스트**: toThrowError() 사용
- **테스트 카테고리**: --testPathPattern 플래그 또는 분리된 설정 파일 사용

## 주요 화제

### Jest 프레임워크 특징
- 올인원 프레임워크로서의 Jest의 장점
- JavaScript 생태계에서의 단편화된 도구들과의 비교
- xUnit, TAP 프레임워크와의 관계

### 테스트 코드 품질
- 테스트 가독성과 유지보수성의 중요성
- 중복 코드 제거와 가독성 사이의 균형
- 스크롤 피로 문제와 해결책

### 테스트 패턴과 안티패턴
- Assertion Roulette 안티패턴
- beforeEach() 오남용 문제
- BDD 스타일의 장단점

## 부차 화제

### 개발 환경 설정
- Node.js 및 npm 설치 요구사항
- Git 초기화의 필요성 (Jest의 변경 추적용)
- IDE 플러그인을 통한 테스트-코드 간 탐색

### Jest 고급 기능
- --watch 모드를 통한 연속 테스트
- Snapshot 테스트의 장단점
- 병렬 테스트 실행과 주의사항

### 코드 설계 영향
- 함수형 vs 객체지향 설계가 테스트에 미치는 영향
- 상태를 가진 객체 테스트의 복잡성
- 진입점과 출구점의 범위 변화

### 테스트 조직화
- 테스트 파일 배치 전략 (테스트 폴더 vs 코드 옆 배치)
- 팩토리 메소드의 위치와 재사용성
- 테스트 헬퍼 파일 관리
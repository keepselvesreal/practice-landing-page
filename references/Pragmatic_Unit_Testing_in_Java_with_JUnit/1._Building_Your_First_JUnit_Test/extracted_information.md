# 1장: 첫 번째 JUnit 테스트 작성하기 - 추출된 정보

## 핵심 내용
- JUnit을 사용한 첫 번째 단위 테스트 작성 과정
- 테스트 실행, 실패 처리, 통과시키기의 전체 워크플로우
- AAA 패턴(Arrange-Act-Assert)과 ZOM 패턴(Zero-One-Many)
- 테스트 코드의 가독성과 유지보수성 향상 기법

## 상세 핵심 내용

### 단위 테스트를 작성하는 이유
- **Joe의 수동 테스트 방식**: 코드 변경 → 빌드 → 배포 → 브라우저 테스트 → 오류 발견 → 수정 반복
- **Lucia의 자동 테스트 방식**: 작은 코드 변경 → 단위 테스트 실행 → 즉시 피드백 → 문제 조기 발견
- **자동 테스트의 장점**: 빠른 실행, 회귀 방지, 시스템 동작 문서화 역할

### JUnit 기본 개념
- **@Test 어노테이션**: 테스트 메서드 표시 (@org.junit.jupiter.api.Test)
- **테스트 메서드 요구사항**: void 반환, 매개변수 없음, @Test 어노테이션
- **테스트 통과 조건**: 예외 없이 메서드 실행 완료
- **테스트 실패 조건**: 예외 발생 또는 assertion 실패

### CreditHistory 예제
- **CreditHistory 클래스**: CreditRating 객체들의 평균 계산
- **CreditRating 레코드**: 단일 rating 필드를 가진 Java 레코드
- **arithmeticMean 메서드**: 평균 계산 로직 구현

## 상세 내용

### 프로젝트 구조
```
utj3-credit-history/
src/
  main/
    java/
      credit/
        CreditHistory.java
        CreditRating.java
  test/
    java/
      credit/
        ACreditHistory.java (테스트 클래스)
```

### 테스트 작성 단계별 과정

#### 1. 빈 테스트 작성
```java
class ACreditHistory {
    @org.junit.jupiter.api.Test
    void whatever() {
        // 빈 테스트는 통과함
    }
}
```

#### 2. 첫 번째 실제 테스트
```java
@Test
void withNoCreditRatingsHas0Mean() {
    var creditHistory = new CreditHistory();
    var result = creditHistory.arithmeticMean();
    assertEquals(0, result);
}
```

#### 3. 테스트 실패와 수정
- **발생 문제**: ArithmeticException (0으로 나누기)
- **해결 방법**: 가드 클로즈 추가
```java
public int arithmeticMean() {
    if (ratings.isEmpty()) return 0;
    var total = ratings.stream().mapToInt(CreditRating::rating).sum();
    return total / ratings.size();
}
```

### assertEquals 사용법
- **매개변수 순서**: assertEquals(expected, actual)
- **실패 시 메시지**: "Expected :780 Actual :0"
- **순서 중요성**: 잘못된 순서는 혼란스러운 에러 메시지 생성

### 테스트 실행 방법
- **IDE 사용**: 녹색 화살표 클릭 또는 키보드 단축키 (Ctrl-Shift-R)
- **전체 테스트 실행**: test/java 디렉토리 우클릭 → Run 'All Tests'
- **빠른 피드백**: 키보드 단축키 사용으로 효율성 증대

### 테스트 검증 원칙
- **반드시 실패 확인**: 테스트가 실제로 검증하는지 확인
- **코드 변경으로 실패**: 어서션 변경보다 프로덕션 코드 변경으로 실패 유도
- **신뢰할 수 있는 테스트**: 실패한 적 없는 테스트는 신뢰하지 말 것

## 주요 화제

### 1. AAA 패턴 (Arrange-Act-Assert)
- **Arrange**: 테스트를 위한 시스템 상태 설정
- **Act**: 테스트할 동작 실행
- **Assert**: 기대 결과 검증
- **시각적 구분**: 빈 줄로 각 단계 분리하여 가독성 향상

### 2. 테스트 리팩터링
- **@BeforeEach 활용**: 공통 초기화 코드 분리
```java
class ACreditHistory {
    CreditHistory creditHistory;

    @BeforeEach
    void createInstance() {
        creditHistory = new CreditHistory();
    }
}
```

### 3. ZOM 패턴 (Zero-One-Many)
- **Zero 케이스**: 빈 상태 테스트 (평균이 0인 경우)
- **One 케이스**: 단일 요소 테스트 (하나의 평점)
- **Many 케이스**: 다중 요소 테스트 (여러 평점의 평균)

### 4. 테스트 코드 품질
- **추상화**: 중요하지 않은 세부사항 숨기기
- **스캔 가능성**: 빠른 이해를 위한 코드 구조화
- **간결성**: 1-5개 문장으로 대부분의 테스트 작성

## 부차 화제

### 1. JUnit 5 특징
- **접근 제한자 생략**: public 수식어 불필요 (패키지 수준 접근)
- **클러터 제거**: 불필요한 키워드 제거로 가독성 향상
- **문서화 지향**: 구현 세부사항보다 동작 설명에 집중

### 2. 테스트 명명 규칙
- **서술적 이름**: 테스트가 검증하는 동작 요약
- **문장 완성**: "A Credit History...with no credit ratings...has a 0 mean"
- **일관성**: 팀 전체의 일관된 명명 규칙 적용

### 3. IDE 활용
- **스크린샷 의존성 탈피**: 코드 중심 학습으로 전환
- **단축키 활용**: 마우스 사용 최소화로 효율성 증대
- **JUnit 실행기 이해**: 테스트 결과 해석 능력 향상

### 4. 테스트 목록 관리
- **브레인스토밍**: 추가로 필요한 테스트 케이스 발굴
- **테스트 목록**: 종이, 노트패드, TODO 주석 등으로 관리
- **점진적 구현**: 모든 테스트를 미리 구현하지 않고 필요시 작성

### 5. 예외 처리와 테스트
- **AssertionFailedError**: 모든 실패한 어서션이 던지는 예외
- **실행 중단**: 첫 번째 실패 시 나머지 어서션 실행 안 됨
- **단일 동작 집중**: 테스트당 하나의 동작에 집중하는 것이 바람직
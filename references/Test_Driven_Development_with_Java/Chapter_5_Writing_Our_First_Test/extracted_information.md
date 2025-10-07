# Test_Driven_Development_with_Java_Chapter_5_Writing_Our_First_Test

## 압축 내용

TDD에서 첫 번째 테스트를 작성할 때는 **Arrange-Act-Assert(AAA) 구조**를 따라 **FIRST 원칙**(Fast, Isolated, Repeatable, Self-verifying, Timely)을 준수하며, **테스트를 먼저 작성(Test-First)**함으로써 **코드의 외부 인터페이스 설계**를 우선하고 **구현 세부사항보다 행동(behavior) 검증**에 집중한다.

---

## 핵심 내용

### 핵심 개념
1. **Arrange-Act-Assert(AAA) 구조** → 상세 내용 1.1, 1.2, 1.3
2. **FIRST 원칙** → 상세 내용 2.1~2.5
3. **Test-First 접근** → 상세 내용 3.1, 3.2
4. **외부 인터페이스 우선 설계** → 상세 내용 4.1, 4.2
5. **행동 검증 vs 구현 검증** → 상세 내용 5.1, 5.2

### 핵심 개념 설명

#### 1. Arrange-Act-Assert(AAA) 구조 → [상세 내용 섹션 1]
단위 테스트의 표준 구조로, Kent Beck이 정의한 템플릿이다. 테스트 코드를 세 부분으로 나누어 가독성과 명확성을 확보한다.
- **Arrange**: 테스트 실행을 위한 객체 생성, 설정, 의존성 연결
- **Act**: 테스트 대상 코드 실행 및 결과 캡처
- **Assert**: 예상 결과와 실제 결과 비교

**관계**: AAA 구조는 FIRST 원칙의 Self-verifying 속성을 구현하는 구체적 방법이며, Test-First 접근의 기본 템플릿이다.

#### 2. FIRST 원칙 → [상세 내용 섹션 2]
효과적인 테스트가 갖춰야 할 5가지 속성이다.
- **Fast**: 2초 이내(이상적으로는 밀리초), 느린 테스트는 TDD 사이클을 방해
- **Isolated**: 테스트 간 독립성, 실행 순서 무관
- **Repeatable**: 동일 코드에 대해 항상 동일 결과
- **Self-verifying**: 자동화된 검증, 수동 확인 불필요
- **Timely**: 프로덕션 코드 작성 직전에 테스트 작성

**관계**: FIRST 원칙은 AAA 구조로 작성된 테스트의 품질을 평가하는 기준이며, Test-First 접근의 "Timely" 속성을 강조한다.

#### 3. Test-First 접근 → [상세 내용 섹션 3]
프로덕션 코드 작성 전에 테스트를 먼저 작성하는 TDD의 핵심 방법론이다.
- 테스트는 코드의 첫 번째 사용자(first use)
- 설계 피드백을 즉각적으로 제공
- 구현보다 인터페이스 설계를 우선

**관계**: Test-First는 외부 인터페이스 우선 설계를 강제하며, 행동 검증에 자연스럽게 집중하게 만든다.

#### 4. 외부 인터페이스 우선 설계 → [상세 내용 섹션 4]
TDD는 "어떻게(how)" 구현할지보다 "무엇(what)"을 할지를 먼저 결정한다.
- Outside-in 관점: 코드 사용자 입장에서 설계
- 공개(public) 메서드만 테스트
- 구현 세부사항은 감춤(encapsulation)

**관계**: 외부 인터페이스 우선 설계는 Test-First 접근의 자연스러운 결과이며, 행동 검증을 가능하게 한다.

#### 5. 행동 검증 vs 구현 검증 → [상세 내용 섹션 5]
TDD는 컴포넌트의 행동(behavior)을 테스트하지, 구현(implementation)을 테스트하지 않는다.
- 테스트는 "무엇"을 하는지 명시
- 구현 방법은 자유롭게 선택 가능
- 하나의 테스트가 여러 클래스를 생성할 수 있음

**관계**: 행동 검증은 외부 인터페이스 우선 설계의 목적이며, Test-First 접근이 제공하는 설계 자유도의 핵심이다.

### 핵심 개념 간 관계
**Test-First 접근** → **AAA 구조**를 템플릿으로 사용 → **외부 인터페이스 우선 설계** 강제 → **행동 검증**에 집중 → **FIRST 원칙**으로 품질 평가

---

## 상세 내용

### 목차
1. Arrange-Act-Assert(AAA) 구조의 정의와 적용
2. FIRST 원칙: 효과적인 테스트의 5가지 속성
3. Test-First 접근: TDD의 사고방식 전환
4. 테스트로부터 배우기: 설계 피드백
5. 일반적인 에러 포착
6. 예외 단언(Asserting Exceptions)
7. 공개 메서드만 테스트하기
8. Wordz 애플리케이션: 첫 번째 테스트 작성
9. 테스트의 한계와 품질 보증

---

### 1. Arrange-Act-Assert(AAA) 구조의 정의와 적용 → [핵심 개념 1]

**출처**: Lines 28-90

#### 1.1 AAA 구조의 정의

**Arrange-Act-Assert**는 Kent Beck이 Chrysler Comprehensive Compensation Project에서 발견한 단위 테스트의 공통 패턴이다.

```java
// Java 코드 예제 (Lines 47-56)
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

public class UsernameTest {
    @Test
    public void convertsToLowerCase() {
        // Arrange: 테스트 실행을 위한 객체 생성
        var username = new Username("SirJakington35179");

        // Act: 테스트 대상 코드 실행
        String actual = username.asLowerCase();

        // Assert: 결과 검증
        assertThat(actual).isEqualTo("sirjakington35179");
    }
}
```

```python
# Python 버전
import pytest

class UsernameTest:
    def test_converts_to_lower_case(self):
        # Arrange: 테스트 실행을 위한 객체 생성
        username = Username("SirJakington35179")

        # Act: 테스트 대상 코드 실행
        actual = username.as_lower_case()

        # Assert: 결과 검증
        assert actual == "sirjakington35179"
```

**AAA의 각 단계**:
- **Arrange** (Lines 72-77): 객체 생성, 설정, 의존성 연결. 간단한 함수 테스트의 경우 생략 가능
- **Act** (Lines 78-82): 테스트 대상 코드 호출, 매개변수 전달, 결과 캡처
- **Assert** (Lines 83-87): AssertJ의 `assertThat()` 등을 사용해 예상 결과와 실제 결과 비교

#### 1.2 테스트 명명 규칙

**출처**: Lines 61-70

- **클래스명**: `UsernameTest` - 테스트 대상 행동 영역 설명
- **메서드명**: `convertsToLowerCase()` - 예상 결과 설명
- **스토리텔링 접근**: 코드 독자가 문제와 해결 방법을 명확히 이해하도록 작성

#### 1.3 AAA 구조의 유연성

**출처**: Lines 651-655 (Q&A)

- Arrange 단계는 정적 메서드 테스트 시 생략 가능
- Act와 Assert는 간단한 메서드 호출의 경우 통합 가능
- 공통 Arrange 코드는 JUnit의 `@BeforeEach`로 분리 가능

---

### 2. FIRST 원칙: 효과적인 테스트의 5가지 속성 → [핵심 개념 2]

**출처**: Lines 145-200

#### 2.1 Fast (빠른 실행)

**출처**: Lines 160-166

- **목표**: 2초 이내, 이상적으로는 밀리초 단위
- **중요성**: 느린 테스트(15초+)는 TDD 사이클을 방해하고, 개발자가 테스트를 건너뛰게 만듦
- **결과**: 큰 코드 덩어리를 테스트 없이 작성하게 되어 TDD의 목적 상실

#### 2.2 Isolated (격리됨)

**출처**: Lines 167-175

- **정의**: 각 테스트는 다른 테스트와 독립적으로 실행 가능
- **요구사항**:
  - 테스트 실행 순서와 무관하게 동일한 결과
  - 한 테스트가 다른 테스트의 실행에 의존하지 않음
- **위험**: 격리되지 않은 테스트는 false negative를 발생시켜 신뢰성 저하

#### 2.3 Repeatable (반복 가능)

**출처**: Lines 176-182

- **정의**: 동일한 프로덕션 코드에 대해 항상 동일한 pass/fail 결과
- **주의 사항**:
  - 랜덤 값 테스트 (예: 1~10 사이 난수)
  - 데이터베이스 의존 테스트
  - 시간 의존 테스트
  - UI 의존 테스트
- **해결**: Chapter 8에서 Test Doubles(Stubs, Mocks) 기법으로 해결

#### 2.4 Self-verifying (자가 검증)

**출처**: Lines 183-187

- **정의**: 테스트 결과를 자동으로 검증하는 실행 코드 포함
- **금지 사항**: 콘솔 출력 후 수동 검증
- **가치**: 자동화로 인한 속도, 정확성, 테스트 계획 준수 보장

#### 2.5 Timely (적시성)

**출처**: Lines 192-200

- **이상적 시점**: 프로덕션 코드 작성 직전
- **피해야 할 접근**:
  - 단위 테스트를 전혀 작성하지 않고 수동 QA 의존
  - 분석가가 모든 테스트를 사전에 작성
  - 코드 작성 후 테스트 작성 (설계 피드백 손실)

---

### 3. Test-First 접근: TDD의 사고방식 전환 → [핵심 개념 3]

**출처**: Lines 108-142

#### 3.1 Outside-in 설계 (Lines 108-125)

**전통적 접근**:
1. 구현 방법 고민 (how)
2. 알고리즘과 자료구조 설계
3. 호출 가능한 인터페이스로 래핑

**TDD 접근**:
1. 호출 가능한 인터페이스 설계 (what)
2. 테스트로 설정 방법, 호출 방법, 예상 결과 명시
3. 구현 방법은 나중에 결정

**핵심**: "코드가 어떻게 작동하는지(how)"보다 "코드가 무엇을 하는지(what)"를 먼저 정의

#### 3.2 워크플로우 효율성 증가 (Lines 126-142)

**Test-First의 장점**:

1. **즉각적 검증** (Lines 127-132):
   - 수동 QA 프로세스 대기 불필요
   - 버그를 메인 소스에 릴리스하기 전에 발견 및 수정
   - 동료를 위한 문서화: `Username` 클래스 사용법이 테스트에 명시

2. **격리된 실행 환경** (Lines 133-138):
   - 전체 애플리케이션 빌드 불필요
   - 데이터베이스 설정 불필요
   - UI 네비게이션 불필요
   - 단순히 테스트 실행

3. **모듈성 향상** (Lines 139-142):
   - 작은 조각으로 실행 가능한 코드 설계 강제
   - 1960년대부터 유효한 설계 원칙 준수

---

### 4. 테스트로부터 배우기: 설계 피드백 → [핵심 개념 4]

**출처**: Lines 348-382

테스트는 프로덕션 코드의 첫 번째 사용자이므로, AAA 각 단계에서 설계 문제를 드러낸다.

#### 4.1 Messy Arrange Step (Lines 354-359)

**증상**:
- 생성자에 너무 많은 매개변수
- 많은 선택적 매개변수가 테스트에서 `null`로 남음
- 너무 많은 의존성 주입 필요
- 너무 많은 기본 데이터 매개변수

**원인**: 객체가 너무 많은 책임을 가지거나 설정이 복잡함

**해결**: 객체 생성 방식 재설계

#### 4.2 Messy Act Step (Lines 364-371)

**증상**:
- 불명확한 매개변수 (예: 여러 개의 `Boolean` 또는 `String`)
- 특정 순서로 여러 메서드 호출 필요

**해결**:
- 불명확한 매개변수를 설정 객체로 래핑
- 여러 호출을 단일 메서드로 래핑

#### 4.3 Messy Assert Step (Lines 372-376)

**증상**:
- 특정 순서로 접근자 호출 필요
- 각 인덱스가 다른 의미를 가진 배열 반환

**해결**: 더 안전한 구조 사용

**핵심**: 테스트 코드의 code smell은 프로덕션 코드 설계의 code smell을 반영

---

### 5. 일반적인 에러 포착 → [핵심 개념 5]

**출처**: Lines 233-276

단위 테스트가 자동으로 포착하는 일반적 실수들:

#### 5.1 일반적 에러 유형 (Lines 238-244)

1. **Off-by-one 에러**: 루프 인덱스 초기화 실수
2. **반전된 조건 로직**: 조건문의 논리 오류
3. **누락된 조건**: 필요한 조건 검사 누락
4. **초기화되지 않은 데이터**: 변수 초기화 실수
5. **잘못된 알고리즘**: 알고리즘 선택 오류
6. **깨진 동등성 검사**: 비교 연산 오류

#### 5.2 에러 포착 예제 (Lines 245-276)

**잘못된 구현 코드** (Lines 248-269):

```java
public class Username {
    private final String name;

    public Username(String username) {
        name = username;
    }

    public String asLowerCase() {
        var result = new StringBuilder();
        for (int i=1; i < name.length(); i++) {  // 에러 1: i=1 (off-by-one)
            char current = name.charAt(i);
            if (current > 'A' && current < 'Z') {  // 에러 2: < 대신 <=
                result.append(current + 'a' - 'A');
            } else {
                result.append(current);
            }
        }
        return result.toString();
    }
}
```

```python
# Python 버전
class Username:
    def __init__(self, username: str):
        self.name = username

    def as_lower_case(self) -> str:
        result = []
        for i in range(1, len(self.name)):  # 에러 1: range(1, ...) - off-by-one
            current = self.name[i]
            if 'A' < current < 'Z':  # 에러 2: < 대신 <=
                result.append(chr(ord(current) + ord('a') - ord('A')))
            else:
                result.append(current)
        return ''.join(result)
```

**테스트 실패 결과** (Lines 270-276):
- 예상: `"sirjakington35179"`
- 실제: `"irjakington35179"` (첫 문자 누락)
- 코드에는 4개의 에러가 존재하며, 테스트가 즉시 2개를 발견

---

### 6. 예외 단언(Asserting Exceptions) → [핵심 개념 5]

**출처**: Lines 277-305

#### 6.1 예외 발생 테스트 (Lines 279-287)

**비즈니스 요구사항**: 사용자명은 최소 4자 이상

```java
@Test
public void rejectsShortName() {
    assertThatExceptionOfType(InvalidNameException.class)
            .isThrownBy(() -> new Username("Abc"));
}
```

```python
# Python 버전
def test_rejects_short_name():
    with pytest.raises(InvalidNameException):
        Username("Abc")
```

#### 6.2 예외 미발생 테스트 (Lines 292-298)

```java
@Test
public void acceptsMinimumLengthName() {
    assertThatNoException()
            .isThrownBy(() -> new Username("Abcd"));
}
```

```python
# Python 버전
def test_accepts_minimum_length_name():
    # pytest에서는 예외가 발생하지 않으면 테스트 통과
    Username("Abcd")  # 예외가 발생하지 않아야 함
```

**권장사항** (Lines 299-303):
- 두 테스트 모두 작성하여 의도 명확화
- 또는 다른 테스트에서 암묵적으로 커버
- 테스트명은 일반적으로 시작 (`rejects`, `accepts`)하여 에러 처리 방식 변경 시 유연성 확보

---

### 7. 공개 메서드만 테스트하기 → [핵심 개념 4, 5]

**출처**: Lines 306-346

#### 7.1 행동 vs 구현 테스트 (Lines 307-319)

**TDD 원칙**:
- 컴포넌트의 **행동(behavior)** 테스트, **구현(implementation)** 테스트 아님
- **what**(무엇을 하는지)에 집중, **how**(어떻게 하는지)는 자유

**테스트 작성 방법**:
- 공개 메서드/함수 호출
- 공개 클래스와 패키지 사용
- 비공개 데이터와 지원 코드는 숨김

**일반적 실수**: 테스트를 간단히 하기 위해 비공개 데이터를 공개로 변경 (예: getter 추가)

#### 7.2 캡슐화 보존 (Lines 320-346)

**문제**: 모든 비공개 필드에 getter를 추가하면 캡슐화 약화

**해결책: Value Object 사용** (Lines 321-324)

**Value Object 정의**:
- 정체성(identity)이 없는 객체
- 동일한 데이터를 포함하면 동등(equal)으로 간주

**Java 구현** (Lines 329-339):

```java
@Override
public boolean equals(Object other) {
    return EqualsBuilder.reflectionEquals(this, other);
}

@Override
public int hashCode() {
    return HashCodeBuilder.reflectionHashCode(this);
}
```

```python
# Python 버전 (dataclass 사용)
from dataclasses import dataclass

@dataclass(frozen=True)
class Username:
    name: str

    # equals와 hashCode가 자동 생성됨
```

**장점**:
- 모든 필드를 비공개로 유지
- 예상 필드를 가진 새 객체 생성 후 동등성 검사
- Apache Commons Lang 라이브러리 사용 권장

---

### 8. Wordz 애플리케이션: 첫 번째 테스트 작성 → [핵심 개념 1, 3, 4, 5]

**출처**: Lines 429-615

#### 8.1 프로젝트 구조 설정 (Lines 440-446)

**Java 프로젝트 구조**:
- 프로덕션 코드: `src/main/java`
- 테스트 코드: `src/test/java`
- 패키지 명명: `com.wordz` (회사/프로젝트명)

**철학**: 테스트 코드는 프로덕션 코드와 동등하게 중요, 소스 코드와 함께 배포

#### 8.2 테스트 주도 설계 프로세스 (Lines 447-563)

**1단계: 테스트 클래스 및 메서드 생성** (Lines 447-458)

```java
public class WordTest {
    @Test
    public void oneIncorrectLetter() {
    }
}
```

**설계 결정**:
- 클래스명: `WordTest` - 테스트 영역(단어 추측) 설명
- 메서드명: `oneIncorrectLetter` - 단순한 happy path부터 시작

**2단계: Arrange - 객체 생성 설계** (Lines 460-489)

```java
@Test
public void oneIncorrectLetter() {
    var word = new Word("A");
}
```

**설계 결정**:
- `Word` 클래스로 단어 표현
- 생성자에 추측할 단어를 매개변수로 전달

**3단계: Act - 메서드 호출 설계** (Lines 490-509)

```java
@Test
public void oneIncorrectLetter() {
    var word = new Word("A");
    word.guess("Z");
}
```

**설계 결정**:
- `guess()` 메서드로 추측 전달

**4단계: 반환 타입 설계 (Lines 510-553)**

**고려한 설계 옵션**:
1. 5개의 getter를 가진 클래스, 각각 enum 반환
2. 동일한 getter를 가진 Java 17 record 타입
3. 5개의 enum 상수를 순회하는 iterator 메서드를 가진 클래스
4. 각 문자 점수에 대해 하나의 인터페이스를 반환하는 iterator 메서드
5. 각 결과에 대한 Java 8 람다 함수를 전달하는 클래스

**최종 설계 결정** (Lines 545-552):
- 가변 개수의 문자 지원
- `INCORRECT`, `PART_CORRECT`, `CORRECT` enum으로 점수 표현
- 0-based 인덱스로 각 점수 접근
- **KISS 원칙** 준수: Keep It Simple, Stupid

**5단계: Assert - 결과 검증 설계** (Lines 554-570)

```java
@Test
public void oneIncorrectLetter() {
    var word = new Word("A");
    var score = word.guess("Z");
    var result = score.letter(0);
    assertThat(result).isEqualTo(Letter.INCORRECT);
}
```

```python
# Python 버전
def test_one_incorrect_letter():
    # Arrange
    word = Word("A")

    # Act
    score = word.guess("Z")
    result = score.letter(0)

    # Assert
    assert result == Letter.INCORRECT
```

**설계 문서화**: 테스트가 설계 결정을 실행 가능한 명세로 캡처

#### 8.3 Red-Green 사이클 (Lines 571-615)

**테스트 실패 확인** (Lines 571-576):
- 프로덕션 코드 작성 전에 테스트 실패 확인
- 목적: 테스트가 올바른 것을 검증하는지 확신

**최소 구현으로 테스트 통과** (Lines 578-595):

```java
// Word 클래스
public class Word {
    public Word(String correctWord) {
        // Not Implemented
    }

    public Score guess(String attempt) {
        var score = new Score();
        return score;
    }
}

// Score 클래스
public class Score {
    public Letter letter(int position) {
        return Letter.INCORRECT;  // 하드코딩
    }
}
```

```python
# Python 버전
class Word:
    def __init__(self, correct_word: str):
        pass  # Not Implemented

    def guess(self, attempt: str) -> Score:
        return Score()

class Score:
    def letter(self, position: int) -> Letter:
        return Letter.INCORRECT  # 하드코딩
```

**테스트 통과 확인** (Lines 595-602):
- 실행 시간: 0.139초
- 수동 테스트 대비 큰 시간 절약
- 프로젝트 수명 주기 동안 반복 가능

**Triangulation 기법** (Lines 605-612):
- 첫 번째 테스트는 인터페이스 설계만 수행
- 이후 테스트들이 전체 구현을 유도
- 결과: 100% 의미 있는 코드 커버리지
- 작업을 작은 덩어리로 분해, 빈번한 전달 가능

**다중 클래스 생성** (Lines 613-615):
- 하나의 테스트가 두 개의 클래스(`Word`, `Score`) 생성
- 단위 테스트는 행동을 커버, 특정 구현을 커버하지 않음

---

### 9. 테스트의 한계와 품질 보증 → [핵심 개념 5]

**출처**: Lines 383-428

#### 9.1 자동화된 테스트의 한계 (Lines 383-397)

**핵심 원칙**:
> "자동화된 테스트는 결함의 존재만 증명할 수 있고, 부재는 증명할 수 없다."

**의미**:
- 테스트 실패 → 결함 존재 확인
- 모든 테스트 통과 → 생각한 결함들이 없음을 의미, 결함이 전혀 없음을 의미하지 않음

**결과**: TDD는 코드 품질을 크게 향상시키지만, 결함이 전혀 없다고 주장할 수는 없음

#### 9.2 QA 엔지니어와의 협업 (Lines 391-397)

**QA의 지속적 중요성**:
- TDD로 많은 결함이 예방되고 제거됨
- QA는 더 나은 출발점에서 시작
- **탐색적 테스트**에 집중 가능: 개발자가 생각하지 못한 것들 찾기
- QA 결함 리포트 → 추가 단위 테스트 작성 → 결함 수정
- 고품질 소프트웨어를 위해 팀 전체의 협력 필요

#### 9.3 코드 커버리지의 의미 없음 (Lines 402-417)

**코드 커버리지 정의**:
- 실행된 코드 라인 수 측정
- 테스트 스위트 실행 중 실행된 라인 비율

**이론적 가치**:
- 실행되지 않은 코드 라인 → 누락된 테스트 발견

**실제 한계**:
- **100% 코드 커버리지 ≠ 완전한 테스트**
- 예: `if (x < 2)` 문장 하나의 테스트로 커버
  - 라인은 실행되지만 모든 동작 조합을 탐색하지 않음
  - 잘못된 연산자 (`<` vs `<=`)
  - 잘못된 값 (2 vs 20)
- 단일 테스트로는 문장의 모든 동작 조합을 탐색할 수 없음

**결론**: 100% 코드 커버리지로도 누락된 테스트가 존재할 수 있음

#### 9.4 잘못된 테스트 작성 (Lines 418-428)

**개인 사례** (Lines 419-428):
- **상황**: 학자금 대출 체크박스 기능, 6가지 결과에 대해 TDD 적용
- **실수**: 사용자 스토리를 잘못 읽어 모든 테스트를 반전
- **결과**:
  - 체크박스가 세금을 적용해야 할 때 적용하지 않음
  - 그 반대도 마찬가지
- **발견**: QA 엔지니어가 발견 (우회 방법이 전혀 없는 결함)
- **교훈**: TDD는 원하는 대로 코드를 만드는 데 탁월하지만, "원하는 것"이 무엇인지 파악하는 것은 별개의 문제
- **결과**: 빠른 수정 및 재테스트 가능

---

## 요약 및 다음 단계

**출처**: Lines 616-628

### 이 장에서 배운 내용

1. **AAA 구조**: 각 테스트의 표준 템플릿
2. **FIRST 원칙**: 효과적인 테스트의 속성
3. **Test-First 설계**: 프로덕션 코드 전에 테스트 작성
4. **설계 피드백**: 테스트 코드가 설계 품질을 드러냄
5. **일반적 에러 포착**: 단위 테스트가 자동으로 잡는 실수들
6. **예외 테스트**: 에러 핸들링 코드 검증
7. **공개 메서드 테스트**: 행동 검증, 구현 검증 아님
8. **Wordz 첫 테스트**: 실제 TDD 적용 사례

### 다음 장 예고 (Chapter 6)

- Wordz의 단어 점수 객체 완전 구현
- TDD의 리듬: **Red, Green, Refactor**
- 코드와 테스트를 깨끗하게 유지하면서 과도한 엔지니어링 방지

---

## Q&A

**출처**: Lines 629-661

### Q1: 테스트할 코드가 없는데 어떤 테스트를 작성하나?

**출처**: Lines 631-636

**답변**: 사고방식 전환 필요
- 테스트는 소규모 코드 섹션을 사전에 설계하는 데 도움
- 원하는 인터페이스 결정 → AAA 단계에서 결정 캡처
- 컴파일 가능한 최소 코드 작성 → 테스트 실행 및 실패 확인
- 이 시점에서 프로덕션 코드 작성을 안내하는 실행 가능한 명세 확보

### Q2: 프로덕션 클래스당 하나의 테스트 클래스를 고수해야 하나?

**출처**: Lines 642-648

**답변**: 아니오, 일반적인 오해
- 각 테스트의 목표는 행동 명시 및 실행
- 행동은 코드로 구현되지만, 테스트는 구현 방식을 제약하지 않음
- 테스트 범위는 다양:
  - 하나의 함수만 테스트
  - 클래스당 공개 메서드당 하나의 테스트
  - 하나의 테스트로 여러 클래스 생성 (Wordz 예제)

### Q3: 항상 AAA 구조를 사용해야 하나?

**출처**: Lines 650-655

**답변**: 시작 시 권장, 하지만 유연성 허용
- 가독성 향상을 위해 단계 생략 또는 통합 가능
- **Arrange 생략**: 정적 메서드 테스트 시
- **Act와 Assert 통합**: 간단한 메서드 호출 시
- **공통 Arrange 분리**: JUnit `@BeforeEach` 사용

### Q4: 테스트는 일회용 코드인가?

**출처**: Lines 657-661

**답변**: 아니오
- 프로덕션 코드와 동일한 중요성과 관리
- 테스트 코드도 깨끗하게 유지
- 테스트 코드의 가독성이 최우선
- 빠르게 훑어보고 존재 이유와 동작 파악 가능해야 함
- 프로덕션에 배포되지 않지만 중요도는 동일

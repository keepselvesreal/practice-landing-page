# Test_Driven_Development_with_Java_Chapter_6_Following_the_Rhythms_of_TDD

## 압축 내용

TDD는 Arrange-Act-Assert 템플릿과 Red-Green-Refactor(RGR) 사이클이라는 두 가지 리듬을 통해 체계적이고 점진적으로 코드를 개발하며, 각 단계에서 설계 결정을 문서화하고 검증한다.

## 핵심 내용

1. **TDD의 두 가지 리듬** → [상세 내용 섹션 1, 2]
   - Arrange-Act-Assert: 각 테스트의 내부 구조를 정의하고 코드의 외부 인터페이스 설계
   - Red-Green-Refactor: 테스트 실패 → 통과 → 리팩토링의 반복적인 개발 사이클
   - 두 리듬은 상호 보완적으로 작동하여 체계적인 개발 프로세스 제공

2. **RGR 사이클의 세 단계** → [상세 내용 섹션 2]
   - Red(실패): 실패하는 테스트를 먼저 작성하여 테스트가 올바르게 작동함을 확인
   - Green(통과): 가장 단순한 코드로 테스트를 통과시키며, 구현 세부사항에 대한 과도한 고민 회피
   - Refactor(리팩토링): 통과하는 테스트의 보호 아래 코드 품질 개선

3. **점진적 설계 접근** → [상세 내용 섹션 3]
   - 작은 단계로 기능을 확장하며 삼각측량(triangulation) 기법 활용
   - 테스트와 프로덕션 코드 모두에 대한 지속적인 리팩토링
   - 코드 스멜 식별 및 제거를 통한 유지보수성 향상

**관계도**: Arrange-Act-Assert 리듬이 각 테스트의 구조를 정의하면, RGR 사이클은 여러 테스트를 거쳐 전체 기능을 점진적으로 구현하는 더 큰 사이클을 형성한다.

## 상세 내용

### 목차

1. RGR 사이클의 이해
2. Red 단계: 실패하는 테스트 작성
3. Green 단계: 가장 단순한 구현
4. Refactor 단계: 코드 품질 개선
5. Wordz 애플리케이션에 테스트 추가
6. 단일 문자 검증 테스트 작성
7. 두 문자 조합으로 설계 확장
8. 리스트를 이용한 다중 결과 저장
9. 리팩토링을 통한 코드 정리

---

### 1. RGR 사이클의 이해

**이전 내용과의 관계**: Chapter 5에서 Arrange-Act-Assert 템플릿을 배웠으며, 이는 개별 테스트의 구조를 정의했다.

RGR 사이클은 더 큰 범위의 리듬으로, 여러 테스트를 거쳐 코드를 점진적으로 발전시키는 3단계 프로세스다 (Lines 26-45).

**핵심 개념**:
- 음악의 리듬처럼 일정하고 반복적인 작업 패턴 제공
- 테스트 작성 → 코드 작성 → 코드 개선의 규칙적인 흐름
- 각 테스트와 코드는 다르지만 작업 리듬은 일관적으로 유지

```java
// RGR 사이클의 세 단계
// 1. Red: 실패하는 테스트 작성
@Test
public void oneCorrectLetter() {
    var word = new Word("A");
    var score = word.guess("A");
    assertThat(score.letter(0)).isEqualTo(Letter.CORRECT);  // 이 테스트는 실패해야 함
}

// 2. Green: 테스트를 통과시키는 최소한의 코드
public void assess(int position, String attempt) {
    if (isCorrectLetter(position, attempt)){
        result = Letter.CORRECT;  // 가장 단순한 구현
    }
}

// 3. Refactor: 코드 품질 개선
private boolean isCorrectLetter(int position, String attempt) {
    return correct.charAt(position) == attempt.charAt(position);  // 명확성을 위해 별도 메서드로 추출
}
```

**Python 버전**:
```python
# RGR 사이클의 세 단계
# 1. Red: 실패하는 테스트 작성
def test_one_correct_letter():
    word = Word("A")
    score = word.guess("A")
    assert score.letter(0) == Letter.CORRECT  # 이 테스트는 실패해야 함

# 2. Green: 테스트를 통과시키는 최소한의 코드
def assess(self, position, attempt):
    if self.is_correct_letter(position, attempt):
        self.result = Letter.CORRECT  # 가장 단순한 구현

# 3. Refactor: 코드 품질 개선
def is_correct_letter(self, position, attempt):
    return self.correct[position] == attempt[position]  # 명확성을 위해 별도 메서드로 추출
```

(출처: Lines 26-45, 98-113)

### 2. Red 단계: 실패하는 테스트 작성 → [핵심 개념 2]

Red 단계의 목표는 Arrange-Act-Assert 템플릿을 사용하여 테스트를 작성하고 실행하여 실패하는지 확인하는 것이다 (Lines 45-59).

**핵심 원칙**:
- 테스트가 실패해야 테스트가 올바르게 작동함을 확신할 수 있음
- 테스트가 통과하면 문제가 있음 - 코드를 작성하지 않았는데 통과한다면 테스트 오류
- 가장 일반적인 실수는 assertion을 잘못 작성하는 것

```java
// Red 단계: 실패하는 테스트
@Test
public void oneCorrectLetter() {
    var word = new Word("A");               // Arrange: 테스트 설정
    var score = word.guess("A");            // Act: 테스트 실행
    assertThat(score.letter(0))             // Assert: 결과 검증
       .isEqualTo(Letter.CORRECT);          // 아직 구현되지 않았으므로 실패해야 함
}
```

**Python 버전**:
```python
# Red 단계: 실패하는 테스트
def test_one_correct_letter():
    word = Word("A")                          # Arrange: 테스트 설정
    score = word.guess("A")                   # Act: 테스트 실행
    assert score.letter(0) == Letter.CORRECT  # Assert: 결과 검증, 아직 구현되지 않았으므로 실패해야 함
```

**왜 실패가 중요한가**:
- 실패를 보면 테스트가 실제로 무언가를 검증하고 있음을 확인
- 코드 작성 없이 통과하면 테스트나 코드에 문제가 있을 가능성
- Red → Green 전환을 보면 코드가 올바르게 작동함을 확신

(출처: Lines 45-59)

### 3. Green 단계: 가장 단순한 구현 → [핵심 개념 2]

**이전 내용과의 관계**: Red 단계에서 실패하는 테스트를 작성했다면, Green 단계에서는 이를 통과시키는 코드를 작성한다.

Green 단계는 테스트를 통과시키는 프로덕션 코드를 작성하는 단계다 (Lines 64-93).

**핵심 지침**:
- 가능한 가장 단순한 코드 사용 - 과도하게 엔지니어링된 알고리즘이나 최신 언어 기능 사용 자제
- 구현 세부사항에 대해 과도하게 생각하지 말것 - 다음 단계에서 개선할 것
- 테스트를 통과시키고 그 이상은 하지 말 것

```java
// Green 단계: 테스트를 통과시키는 코드
public class Word {
    private final String word;

    public Word(String correctWord) {
        this.word = correctWord;  // 단순하게 단어 저장
    }

    public Score guess(String attempt) {
        var score = new Score(word);
        score.assess(0, attempt);  // 가장 단순한 접근: 위치 0만 평가
        return score;
    }
}

public class Score {
    private final String correct;
    private Letter result = Letter.INCORRECT;  // 기본값은 INCORRECT

    public Score(String correct) {
        this.correct = correct;
    }

    public Letter letter(int position) {
        return result;  // 단순히 결과 반환
    }

    public void assess(int position, String attempt) {
        if (correct.charAt(position) == attempt.charAt(position)){
            result = Letter.CORRECT;  // 일치하면 CORRECT
        }
    }
}
```

**Python 버전**:
```python
# Green 단계: 테스트를 통과시키는 코드
class Word:
    def __init__(self, correct_word):
        self.word = correct_word  # 단순하게 단어 저장

    def guess(self, attempt):
        score = Score(self.word)
        score.assess(0, attempt)  # 가장 단순한 접근: 위치 0만 평가
        return score

class Score:
    def __init__(self, correct):
        self.correct = correct
        self.result = Letter.INCORRECT  # 기본값은 INCORRECT

    def letter(self, position):
        return self.result  # 단순히 결과 반환

    def assess(self, position, attempt):
        if self.correct[position] == attempt[position]:
            self.result = Letter.CORRECT  # 일치하면 CORRECT
```

**블랙박스 컴포넌트 개념**:
- 내부(inside): 구현 세부사항을 숨기는 곳 - 데이터와 알고리즘
- 외부(outside): API - public 메서드를 통한 인터페이스
- 캡슐화로 인해 내부 구현을 나중에 변경해도 테스트는 깨지지 않음

(출처: Lines 64-93)

### 4. Refactor 단계: 코드 품질 개선 → [핵심 개념 2]

**이전 내용과의 관계**: Green 단계에서 테스트를 통과시켰다면, Refactor 단계에서는 코드 품질을 개선한다.

Refactor 단계는 통과하는 테스트의 보호 아래 코드를 정리하고 개선하는 소프트웨어 엔지니어링 단계다 (Lines 94-113).

**리팩토링 기법**:
- 중복 코드 제거를 위한 메서드 추출
- 의미를 더 잘 전달하기 위한 메서드 이름 변경
- 변수 내용을 더 잘 표현하기 위한 변수 이름 변경
- 긴 메서드를 여러 개의 짧은 메서드로 분할
- 더 작은 클래스 추출
- 긴 매개변수 목록을 자체 클래스로 결합

```java
// 리팩토링 전: 복잡한 조건문
public void assess(int position, String attempt) {
    if (correct.charAt(position) == attempt.charAt(position)){
        result = Letter.CORRECT;  // 조건이 무엇을 확인하는지 명확하지 않음
    }
}

// 리팩토링 후: 메서드 추출로 가독성 향상
public void assess(int position, String attempt) {
    if (isCorrectLetter(position, attempt)){  // 의도가 명확해짐
        result = Letter.CORRECT;
    }
}

private boolean isCorrectLetter(int position, String attempt) {
    return correct.charAt(position) == attempt.charAt(position);  // 로직이 명명된 메서드로 캡슐화됨
}
```

**Python 버전**:
```python
# 리팩토링 전: 복잡한 조건문
def assess(self, position, attempt):
    if self.correct[position] == attempt[position]:
        self.result = Letter.CORRECT  # 조건이 무엇을 확인하는지 명확하지 않음

# 리팩토링 후: 메서드 추출로 가독성 향상
def assess(self, position, attempt):
    if self.is_correct_letter(position, attempt):  # 의도가 명확해짐
        self.result = Letter.CORRECT

def is_correct_letter(self, position, attempt):
    return self.correct[position] == attempt[position]  # 로직이 명명된 메서드로 캡슐화됨
```

**목표**: 코드를 이해하기 쉽게 만들어 미래의 유지보수를 쉽게 함. 리팩토링 전반에 걸쳐 테스트가 통과 상태를 유지해야 함.

**가독성에 대한 중요한 통찰** (Lines 256-262):
- 가독성은 읽는 동안이 아니라 작성하는 동안 결정됨
- 코드는 작성된 횟수보다 훨씬 더 많이 읽힘
- 읽기 쉬운 코드와 읽기 어려운 코드는 작성 시 선택 사항
- 다른 무엇보다 읽기 쉬움을 일관되게 선택하면 코드가 읽기 쉬워짐

(출처: Lines 94-113, 234-262)

### 5. Wordz 애플리케이션에 테스트 추가 → [핵심 개념 3]

**이전 내용과의 관계**: RGR 사이클의 이론을 배웠으므로, 이제 Wordz 애플리케이션에 적용한다.

Wordz 채점 시스템을 구축하기 위해 작고 안전한 단계로 진행하며, 다음 테스트를 신중하게 선택한다 (Lines 116-157).

**테스트 선택 전략**:
- 안전하게 플레이하고 작은 단계만 앞으로 나아감
- 테스트가 지원할 수 있는 것 이상을 작성하는 함정에 빠지지 않음
- 이전 테스트와 의도적으로 유사하지만 다른 결과를 테스트하는 테스트 작성

```java
// 단계 1: Red - 단일 정답 문자에 대한 실패 테스트 작성
@Test
public void oneCorrectLetter() {
    var word = new Word("A");     // 동일한 단어 "A" 사용
    var score = word.guess("A");  // 이번에는 정답 추측
    assertThat(score.letter(0))
       .isEqualTo(Letter.CORRECT); // INCORRECT가 아닌 CORRECT 기대
}
```

**Python 버전**:
```python
# 단계 1: Red - 단일 정답 문자에 대한 실패 테스트 작성
def test_one_correct_letter():
    word = Word("A")                        # 동일한 단어 "A" 사용
    score = word.guess("A")                 # 이번에는 정답 추측
    assert score.letter(0) == Letter.CORRECT  # INCORRECT가 아닌 CORRECT 기대
```

**설계 고려사항**:
- 테스트 데이터를 사용하여 스토리 전달 - 동일한 단어, 다른 추측, 다른 점수
- 단일 문자 단어의 두 가지 가능한 결과 완전히 커버
- 각 테스트는 하나의 특정 동작에 집중

(출처: Lines 116-157)

### 6. 단일 문자 검증 테스트 작성

**이전 내용과의 관계**: 이전 섹션에서 실패하는 테스트를 작성했으므로, 이제 Green 단계로 넘어간다.

테스트를 통과시키기 위해 프로덕션 코드를 추가하되, 기존 테스트가 계속 통과하도록 유지한다 (Lines 140-212).

```java
// 단계 2: Green - 테스트를 통과시키는 프로덕션 코드
public class Word {
    private final String word;  // 정답 단어를 저장할 필드

    public Word(String correctWord) {
        this.word = correctWord;  // 생성자에서 초기화
    }

    public Score guess(String attempt) {
        var score = new Score(word);  // 정답 단어로 Score 생성
        score.assess(0, attempt);     // 위치 0 평가
        return score;
    }
}

public class Score {
    private final String correct;          // 정답 단어
    private Letter result = Letter.INCORRECT; // 기본 결과

    public Score(String correct) {
        this.correct = correct;
    }

    public Letter letter(int position) {
        return result;  // 현재 결과 반환
    }

    public void assess(int position, String attempt) {
        if (correct.charAt(position) == attempt.charAt(position)){
            result = Letter.CORRECT;  // 문자가 일치하면 CORRECT로 설정
        }
    }
}
```

**Python 버전**:
```python
# 단계 2: Green - 테스트를 통과시키는 프로덕션 코드
class Word:
    def __init__(self, correct_word):
        self.word = correct_word  # 정답 단어를 저장할 필드

    def guess(self, attempt):
        score = Score(self.word)  # 정답 단어로 Score 생성
        score.assess(0, attempt)  # 위치 0 평가
        return score

class Score:
    def __init__(self, correct):
        self.correct = correct           # 정답 단어
        self.result = Letter.INCORRECT   # 기본 결과

    def letter(self, position):
        return self.result  # 현재 결과 반환

    def assess(self, position, attempt):
        if self.correct[position] == attempt[position]:
            self.result = Letter.CORRECT  # 문자가 일치하면 CORRECT로 설정
```

**테스트 실행 결과** (Lines 193-201):
- 두 테스트 모두 통과 - 기존 기능을 깨뜨리지 않음
- 0.103초 만에 완료 - 수동 테스트보다 훨씬 빠름
- 설계가 발전 - assess() 메서드 개념 도입
- 코드가 이제 정답과 오답 추측을 모두 감지 가능

**단계 3: Refactor - 명확성을 위해 isCorrectLetter() 메서드 추출** (Lines 234-251):

```java
public void assess(int position, String attempt) {
    if (isCorrectLetter(position, attempt)){  // 명확성 향상
        result = Letter.CORRECT;
    }
}

private boolean isCorrectLetter(int position, String attempt) {
    return correct.charAt(position) == attempt.charAt(position);  // 복잡한 로직 캡슐화
}
```

**Python 버전**:
```python
def assess(self, position, attempt):
    if self.is_correct_letter(position, attempt):  # 명확성 향상
        self.result = Letter.CORRECT

def is_correct_letter(self, position, attempt):
    return self.correct[position] == attempt[position]  # 복잡한 로직 캡슐화
```

**리팩토링 이유**:
- 복잡한 조건문을 명명된 메서드로 추출
- 메서드 이름이 코드에 대한 주석 역할
- assess() 메서드가 이제 거의 영어로 읽힘: "if this is a correct letter"
- 컴파일러가 주석을 최신 상태로 유지하도록 도움

(출처: Lines 140-251)

### 7. 두 문자 조합으로 설계 확장 → [핵심 개념 3]

**이전 내용과의 관계**: 단일 문자 단어를 완료했으므로, 이제 두 문자 단어로 확장하여 더 복잡한 동작을 테스트한다.

두 문자 조합을 처리하기 위해 진행하며, 새로운 개념을 도입한다: 문자가 단어에 있지만 올바른 위치에 없는 경우 (Lines 334-406).

```java
// 단계 1: Red - 잘못된 위치의 두 번째 문자 테스트
@Test
void secondLetterWrongPosition() {
    var word = new Word("AR");           // 두 문자 단어
    var score = word.guess("ZA");        // 'A'는 있지만 잘못된 위치
    assertScoreForLetter(score, 1,       // 위치 1 확인
                        Letter.PART_CORRECT);  // 부분 정답 기대
}
```

**Python 버전**:
```python
# 단계 1: Red - 잘못된 위치의 두 번째 문자 테스트
def test_second_letter_wrong_position():
    word = Word("AR")                           # 두 문자 단어
    score = word.guess("ZA")                    # 'A'는 있지만 잘못된 위치
    assert_score_for_letter(score, 1,           # 위치 1 확인
                           Letter.PART_CORRECT) # 부분 정답 기대
```

**단계 2: Green - 모든 문자를 확인하도록 코드 추가** (Lines 351-377):

```java
public void assess(String attempt) {
    for (char current: attempt.toCharArray()) {  // 모든 문자 반복
        if (isCorrectLetter(current)) {
            result = Letter.CORRECT;
        }
    }
}

private boolean isCorrectLetter(char currentLetter) {
    return correct.charAt(position) == currentLetter;  // char 입력을 받도록 변경
}
```

**Python 버전**:
```python
def assess(self, attempt):
    for current in attempt:  # 모든 문자 반복
        if self.is_correct_letter(current):
            self.result = Letter.CORRECT

def is_correct_letter(self, current_letter):
    return self.correct[self.position] == current_letter  # 단일 문자 입력
```

**삼각측량(Triangulation)** (Lines 373-377):
- 더 구체적인 테스트를 추가하면서 코드를 더 일반적으로 만듦
- 여기서는 result 필드를 덮어쓰는 것이 문제임을 알지만 테스트가 있을 때까지 수정하지 않음
- 의도적으로 불완전한 구현을 남겨두고 다음 테스트에서 수정

**단계 3: Green - 잘못된 위치의 정답 문자 감지 코드 추가** (Lines 379-405):

```java
public void assess(String attempt) {
    for (char current: attempt.toCharArray()) {
        if (isCorrectLetter(current)) {
            result = Letter.CORRECT;
        } else if (occursInWord(current)) {  // 단어에 있지만 잘못된 위치
            result = Letter.PART_CORRECT;
        }
    }
}

private boolean occursInWord(char current) {
    return correct.contains(String.valueOf(current));  // 단어의 어디에나 있는지 확인
}
```

**Python 버전**:
```python
def assess(self, attempt):
    for current in attempt:
        if self.is_correct_letter(current):
            self.result = Letter.CORRECT
        elif self.occurs_in_word(current):  # 단어에 있지만 잘못된 위치
            self.result = Letter.PART_CORRECT

def occurs_in_word(self, current):
    return current in self.correct  # 단어의 어디에나 있는지 확인
```

**테스트 약점** (Lines 398-405):
- 3개의 테스트가 모두 통과하지만 의심스러움
- result 필드 덮어쓰기 로직이 여전히 문제
- 테스트가 약함 - 더 강력한 테스트가 필요하거나 다른 테스트 작성
- TDD의 일반적인 딜레마 - 어느 쪽이든 진전

(출처: Lines 334-405)

### 8. 리스트를 이용한 다중 결과 저장

**이전 내용과의 관계**: 단일 result 필드의 한계를 식별했으므로, 이제 모든 문자 위치에 대한 결과를 저장할 방법이 필요하다.

세 가지 채점 가능성을 모두 실행하는 새로운 테스트를 추가하여 단일 결과 필드 문제를 드러낸다 (Lines 410-470).

```java
// 단계 1: Red - 모든 채점 조합을 실행하는 테스트
@Test
void allScoreCombinations() {
    var word = new Word("ARI");
    var score = word.guess("ZAI");
    assertScoreForLetter(score, 0, Letter.INCORRECT);      // Z는 틀림
    assertScoreForLetter(score, 1, Letter.PART_CORRECT);  // A는 맞지만 잘못된 위치
    assertScoreForLetter(score, 2, Letter.CORRECT);       // I는 정확히 맞음
}
```

**Python 버전**:
```python
# 단계 1: Red - 모든 채점 조합을 실행하는 테스트
def test_all_score_combinations():
    word = Word("ARI")
    score = word.guess("ZAI")
    assert_score_for_letter(score, 0, Letter.INCORRECT)      # Z는 틀림
    assert_score_for_letter(score, 1, Letter.PART_CORRECT)  # A는 맞지만 잘못된 위치
    assert_score_for_letter(score, 2, Letter.CORRECT)       # I는 정확히 맞음
```

예상대로 테스트 실패 - 단일 필드에 결과를 저장했기 때문.

**단계 2: Green - 결과 리스트 추가하여 각 문자 위치 개별 저장** (Lines 425-470):

```java
public class Score {
    private final String correct;
    private final List<Letter> results = new ArrayList<>();  // 단일 결과 대신 리스트
    private int position;

    public Score(String correct) {
        this.correct = correct;
    }

    public Letter letter(int position) {
        return results.get(position);  // 리스트에서 특정 위치 가져오기
    }

    public void assess(String attempt) {
        for (char current: attempt.toCharArray()) {
            if (isCorrectLetter(current)) {
                results.add(Letter.CORRECT);          // 리스트에 추가
            } else if (occursInWord(current)) {
                results.add(Letter.PART_CORRECT);     // 리스트에 추가
            } else {
                results.add(Letter.INCORRECT);        // 명시적으로 INCORRECT 추가
            }
            position++;  // 위치 추적
        }
    }

    private boolean occursInWord(char current) {
        return correct.contains(String.valueOf(current));
    }

    private boolean isCorrectLetter(char currentLetter) {
        return correct.charAt(position) == currentLetter;
    }
}
```

**Python 버전**:
```python
class Score:
    def __init__(self, correct):
        self.correct = correct
        self.results = []  # 단일 결과 대신 리스트
        self.position = 0

    def letter(self, position):
        return self.results[position]  # 리스트에서 특정 위치 가져오기

    def assess(self, attempt):
        for current in attempt:
            if self.is_correct_letter(current):
                self.results.append(Letter.CORRECT)       # 리스트에 추가
            elif self.occurs_in_word(current):
                self.results.append(Letter.PART_CORRECT)  # 리스트에 추가
            else:
                self.results.append(Letter.INCORRECT)     # 명시적으로 INCORRECT 추가
            self.position += 1  # 위치 추적

    def occurs_in_word(self, current):
        return current in self.correct

    def is_correct_letter(self, current_letter):
        return self.correct[self.position] == current_letter
```

**구현 세부사항** (Lines 463-470):
- 단일 값 result 필드를 ArrayList로 교체
- letter(position) 메서드가 컬렉션을 사용하도록 변경
- 이전에는 기본값으로 처리되던 INCORRECT를 명시적으로 추가해야 함
- 루프 내에서 position 추적하여 어떤 문자 위치를 평가하는지 알기

이 변경으로 모든 4개의 테스트가 통과하며, 3문자 단어의 모든 조합을 올바르게 채점할 수 있음을 증명.

(출처: Lines 410-470)

### 9. 리팩토링을 통한 코드 정리 → [핵심 개념 3]

**이전 내용과의 관계**: 테스트를 통과시켰으므로, 이제 Refactor 단계에서 코드 품질을 개선한다.

테스트와 프로덕션 코드 모두 개선이 필요하다 - TDD에서는 테스트 코드가 프로덕션 코드와 동등한 우선순위를 갖는다 (Lines 471-602).

**프로덕션 코드 리팩토링 - scoreFor() 메서드 추출** (Lines 474-503):

```java
// 리팩토링 전: 긴 루프 본문과 if-else-if 블록
public void assess(String attempt) {
    for (char current: attempt.toCharArray()) {
        if (isCorrectLetter(current)) {
            results.add(Letter.CORRECT);
        } else if (occursInWord(current)) {
            results.add(Letter.PART_CORRECT);
        } else {
            results.add(Letter.INCORRECT);
        }
        position++;
    }
}

// 리팩토링 후: 명확하고 간결한 루프
public void assess(String attempt) {
    for (char current: attempt.toCharArray()) {
        results.add(scoreFor(current));  // 메서드 이름이 의도를 전달
        position++;
    }
}

private Letter scoreFor(char current) {
    if (isCorrectLetter(current)) {
        return Letter.CORRECT;  // if-return으로 단순화
    }
    if (occursInWord(current)) {
        return Letter.PART_CORRECT;
    }
    return Letter.INCORRECT;  // 명시적 기본값
}
```

**Python 버전**:
```python
# 리팩토링 후: 명확하고 간결한 루프
def assess(self, attempt):
    for current in attempt:
        self.results.append(self.score_for(current))  # 메서드 이름이 의도를 전달
        self.position += 1

def score_for(self, current):
    if self.is_correct_letter(current):
        return Letter.CORRECT  # 조기 반환으로 단순화
    if self.occurs_in_word(current):
        return Letter.PART_CORRECT
    return Letter.INCORRECT  # 명시적 기본값
```

**개선 사항**:
- scoreFor() 메서드 본문이 이제 채점 규칙의 간결한 설명
- if-else-if 구조를 더 단순한 if-return 구조로 교체
- 점수를 계산한 다음 즉시 메서드 종료
- 훨씬 더 명확하게 읽힘

**테스트 코드 리팩토링 - assertScoreForGuess() 메서드** (Lines 504-541):

```java
// 중복 제거: 가변 개수의 문자 검증을 위한 헬퍼 메서드
@Test
void allScoreCombinations() {
    var word = new Word("ARI");
    var score = word.guess("ZAI");
    assertScoreForGuess(score, INCORRECT, PART_CORRECT, CORRECT);  // 간결하고 명확
}

private void assertScoreForGuess(Score score, Letter... expectedScores) {
    for (int position=0; position < expectedScores.length; position++){
        Letter expected = expectedScores[position];
        assertThat(score.letter(position)).isEqualTo(expected);
    }
}
```

**Python 버전**:
```python
# 중복 제거: 가변 개수의 문자 검증을 위한 헬퍼 메서드
def test_all_score_combinations():
    word = Word("ARI")
    score = word.guess("ZAI")
    assert_score_for_guess(score, INCORRECT, PART_CORRECT, CORRECT)  # 간결하고 명확

def assert_score_for_guess(score, *expected_scores):
    for position, expected in enumerate(expected_scores):
        assert score.letter(position) == expected
```

**개선 사항**:
- 복사-붙여넣기된 assert 라인 제거
- 추상화 수준 향상
- 테스트가 이제 예상 순서로 점수를 설명: INCORRECT, PART_CORRECT, CORRECT
- enum에 대한 정적 import 추가로 구문 혼란 감소
- 이전 테스트를 수동으로 수정하여 새로운 assertion 헬퍼 사용 가능

**최종 테스트 스위트** (Lines 542-599):
- 포괄적인 테스트 케이스 세트
- 프로덕션 코드의 모든 라인이 새로운 동작 측면을 탐색하는 새 테스트의 직접적인 결과로 도출됨
- 테스트 코드와 프로덕션 코드 모두 읽기 쉬움
- 테스트는 단어 추측 채점 규칙의 실행 가능한 명세를 형성

**달성한 것** (Lines 595-602):
- TDD를 사용하여 Score 클래스의 기능 확장
- RGR 사이클을 따라 테스트 코드와 프로덕션 코드 모두 우수한 엔지니어링 관행 유지
- 단위 테스트로 검증된 견고한 코드
- 더 넓은 애플리케이션에서 호출하기 쉬운 설계

(출처: Lines 471-602)

---

## 요약 (Lines 603-610)

이 장에서는 코드에 RGR 사이클을 적용했다. 이를 통해 작업을 별도의 작업으로 분할하여 테스트에 대한 확신, 간단한 프로덕션 코드로 가는 빠른 경로, 코드 유지보수성을 개선하는 데 소요되는 시간 단축을 얻었다. 프로덕션 코드와 테스트 코드 모두에서 코드 스멜을 제거하는 방법을 살펴보았다. 이 장의 작업의 일부로 앞으로 나아가고 다음에 작성해야 할 테스트를 결정하는 데 도움이 되는 아이디어를 사용했다. 이 장의 기술을 통해 여러 테스트를 작성하고 프로덕션 코드의 세부 로직을 점진적으로 도출할 수 있다.

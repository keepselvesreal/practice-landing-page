## 압축 내용
SRP와 CQS를 기반으로 Profile과 Matcher 구조를 단계적으로 리팩터링해 테스트가 설계를 뒷받침하도록 만드는 과정을 추적한다 (Refactoring Your Code’s Structure 도입, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:38`; Command-Query Separation, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:545`; Refocusing Tests, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:602`).

## 핵심 내용
**핵심 개념**
- Profile과 Matcher를 단일 책임 단위로 분리해 응집도를 높이는 SRP 적용 (The Profile Class and the SRP, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:52`; Extracting a New Class, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:159`)
- 명령-질의 분리로 matches와 score 인터페이스를 정리 (Command-Query Separation, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:528`; Profile score 재설계, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:545`)
- 테스트 재구성과 서비스 위임으로 설계와 검증을 정렬 (디자인과 테스트 상호작용, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:27`; Refocusing Tests, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:602`; MatcherService 소개, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:691`)

**압축 설명**
- SRP 적용: Profile이 매칭과 점수를 모두 처리하던 구조에서 Matcher로 점수 계산을 위임해 변경 이유를 분리하고 테스트 안전망으로 진행을 검증한다 (The Profile Class and the SRP, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:105`; Extracting a New Class, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:163`).
- CQS 정리: matches는 불린만, score는 수치만 돌려주도록 분리해 클라이언트가 부작용 없이 메서드를 재호출할 수 있게 했다 (Command-Query Separation, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:528`; Profile score 재설계, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:549`).
- 테스트·서비스 정렬: Profile에서 제거된 로직을 Matcher와 MatcherService로 옮기면서 테스트 클래스를 재구성해 검증 대상과 구현 책임을 일치시켰다 (Refocusing Tests, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:602`; MatcherService 소개, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:691`).

**개념 관계**
- OTAAT 사고방식을 따라 SRP로 책임을 분할하고, CQS와 테스트 재구성을 연쇄적으로 적용해 설계 개선과 검증 신뢰성을 동시에 높였다 (One Thing At A Time 언급, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:48`; Cleaning Up After a Move, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:340`).

## 상세 핵심 내용
**중요 개념**
- SRP 기반 Matcher 추출과 Profile 축소 (Extracting a New Class, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:163`)
- Matcher 정비와 조건식 단순화 (Cleaning Up After a Move, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:340`; matches 정리, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:431`)
- CQS 준수를 위한 Profile·Matcher 인터페이스 재설계 (Command-Query Separation, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:528`; Profile score 재설계, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:545`)
- SOLID와 응집/결합도 지표로 설계 품질을 평가 (SOLID Class-Design Principles, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:121`; Cohesion·Coupling, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:142`)

**상세 설명**
- SRP 기반 Matcher 추출과 Profile 축소: calculateScore와 matches 로직을 Matcher로 이동시키며 Profile이 프로필 데이터 관리에 집중하도록 했고, 각 단계마다 테스트를 실행해 안전하게 책임 이동을 마쳤다 (Extracting a New Class, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:164`; Profile 정리, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:300`).
- Matcher 정비와 조건식 단순화: criteria를 필드로 저장하고 matches를 단일 표현식으로 바꿔 가독성을 높였으며, score 계산은 지연 평가로 전환해 필요할 때만 비용을 치르게 했다 (Cleaning Up After a Move, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:345`; matches 단일 표현식, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:431`; score 지연 평가, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:467`).
- CQS 준수를 위한 Profile·Matcher 인터페이스 재설계: matches는 부울 검증만, score는 Criteria를 입력받아 합계를 계산하도록 분리해 클라이언트 코드가 의도치 않은 상태 변경 없이 동작을 재호출할 수 있게 했다 (Command-Query Separation, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:528`; Profile score 재설계, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:545`).
- SOLID와 응집/결합도 지표로 설계 품질을 평가: SRP와 함께 OCP·LSP·ISP·DIP를 상기시키며 높은 응집도와 낮은 결합도를 목표로 설계 결정을 평가하도록 안내한다 (SOLID Class-Design Principles, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:121`; Cohesion·Coupling, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:142`).

**개념 관계**
- SRP로 시작한 구조 분리는 SOLID가 제시하는 평가 기준을 만족시키며, Matcher 정비와 CQS 재설계가 결합돼 테스트 재구성이 자연스럽게 이어졌다 (SOLID Class-Design Principles, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:121`; Refocusing Tests, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:602`).

## 상세 내용
### 화제 1. 마이크로·매크로 설계 관점과 테스트의 상호작용
코드는 필드 구성과 메서드 구조 같은 마이크로 설계와 클래스·패키지 배치 같은 매크로 설계가 모두 유지보수성을 좌우하며, 단위 테스트는 이 설계 결정과 분리될 수 없다는 점을 상기시킨다 (Micro vs. Macro Design, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:5`; 디자인과 테스트 상호작용, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:27`).

### 화제 2. Profile의 SRP 위반과 SOLID 재조명
앞선 화제에서 설계와 테스트가 분리될 수 없다는 메시지를 바탕으로, Profile 클래스가 매칭과 점수 계산을 동시에 맡아 SRP를 어기고 있음을 짚으며 SOLID 원칙과 응집/결합도 지표가 필요한 배경을 제시한다 (The Profile Class and the SRP, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:52`; SOLID Class-Design Principles, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:121`).

초기 Profile 구현은 데이터 저장과 매칭 알고리즘을 모두 포함하며 SRP를 위반한다 (Profile 초기 구현, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:52`).
```java
import java.util.HashMap;
import java.util.Map;
import static iloveyouboss.Weight.REQUIRED;

// Profile initially mixes data storage and matching logic, breaking SRP.
public class Profile {
    private final Map<String, Answer> answers = new HashMap<>(); // questionText -> answer map
    private final String name;
    private int score;

    public Profile(String name) { this.name = name; } // store profile name

    public void add(Answer... newAnswers) {
        // store each answer by the text of its question
        for (var answer : newAnswers) {
            answers.put(answer.questionText(), answer);
        }
    }

    public boolean matches(Criteria criteria) {
        calculateScore(criteria); // mutates score as a side effect
        if (anyRequiredCriteriaNotMet(criteria)) return false; // block if required criteria fail
        return anyMatches(criteria); // otherwise report any match
    }

    private boolean anyRequiredCriteriaNotMet(Criteria criteria) {
        return criteria.stream()
            .filter(criterion -> !criterion.isMatch(profileAnswerMatching(criterion))) // find mismatches
            .anyMatch(criterion -> criterion.weight() == REQUIRED); // fail when a required criterion is unmet
    }

    private void calculateScore(Criteria criteria) {
        score = criteria.stream()
            .filter(criterion -> criterion.isMatch(profileAnswerMatching(criterion))) // score matching criteria
            .mapToInt(criterion -> criterion.weight().value()) // translate weight to numeric value
            .sum();
    }

    private boolean anyMatches(Criteria criteria) {
        return criteria.stream()
            .anyMatch(criterion -> criterion.isMatch(profileAnswerMatching(criterion))); // detect any match
    }

    private Answer profileAnswerMatching(Criterion criterion) {
        return answers.get(criterion.questionText()); // look up answer by question text
    }

    public int score() { return score; } // expose stored score

    @Override
    public String toString() { return name; } // use name for printing
}
```
```python
from typing import Dict, Iterable

# NOTE: Answer, Criterion, Criteria, and Weight are expected to provide the methods used below.
class Profile:
    """Profile mixes data storage and matching logic, which will later be split."""

    def __init__(self, name: str) -> None:
        self._answers: Dict[str, "Answer"] = {}
        self._name = name
        self._score = 0

    def add(self, *new_answers: "Answer") -> None:
        # store each answer keyed by question text
        for answer in new_answers:
            self._answers[answer.question_text()] = answer

    def matches(self, criteria: "Criteria") -> bool:
        self._calculate_score(criteria)  # side effect updates score
        if self._any_required_criteria_not_met(criteria):
            return False
        return self._any_matches(criteria)

    def _any_required_criteria_not_met(self, criteria: "Criteria") -> bool:
        # required criteria that do not match cause the profile to fail
        return any(
            criterion.weight() == Weight.REQUIRED and
            not criterion.is_match(self._profile_answer_matching(criterion))
            for criterion in criteria
        )

    def _calculate_score(self, criteria: "Criteria") -> None:
        # accumulate weight values for matching criteria
        self._score = sum(
            criterion.weight().value()
            for criterion in criteria
            if criterion.is_match(self._profile_answer_matching(criterion))
        )

    def _any_matches(self, criteria: "Criteria") -> bool:
        # determine whether any criterion matches the stored answers
        return any(
            criterion.is_match(self._profile_answer_matching(criterion))
            for criterion in criteria
        )

    def _profile_answer_matching(self, criterion: "Criterion") -> "Answer | None":
        return self._answers.get(criterion.question_text())

    def score(self) -> int:
        return self._score

    def __str__(self) -> str:
        return self._name
```

### 화제 3. Matcher 추출로 책임 분리
앞선 화제의 SRP 위반 진단을 바탕으로, matches가 점수 계산을 Matcher에게 위임하도록 작은 단계로 리팩터링을 진행한다 (Extracting a New Class, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:164`).

먼저 matches는 Matcher를 생성해 score를 계산하도록 바뀐다 (utj3-refactor/14 Profile.matches, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:169`).
```java
public boolean matches(Criteria criteria) {
    score = new Matcher(criteria, answers).score(); // delegate scoring to Matcher
    if (anyRequiredCriteriaNotMet(criteria)) return false;
    return anyMatches(criteria);
}
```
```python
class ProfileWithMatcherStep1(Profile):
    """First refactoring step delegates scoring to a Matcher object."""

    def matches(self, criteria: "Criteria") -> bool:
        matcher = Matcher(criteria, self._answers)  # type: ignore[arg-type]
        self._score = matcher.score()  # reuse score returned by Matcher
        if self._any_required_criteria_not_met(criteria):
            return False
        return self._any_matches(criteria)
```

두 문장을 추출해 메서드 분리를 준비한 중간 형태도 거친다 (utj3-refactor/15 Profile.matches, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:226`).
```java
public boolean matches(Criteria criteria) {
    score = new Matcher(criteria, answers).score(); // still delegates scoring
    if (anyRequiredCriteriaNotMet(criteria)) return false; // candidate for extraction
    return anyMatches(criteria); // candidate for extraction
}
```
```python
class ProfileWithMatcherStep2(Profile):
    """Intermediate shape before extracting a helper method."""

    def matches(self, criteria: "Criteria") -> bool:
        matcher = Matcher(criteria, self._answers)  # type: ignore[arg-type]
        self._score = matcher.score()
        if self._any_required_criteria_not_met(criteria):
            return False
        return self._any_matches(criteria)
```

이후 matches는 isMatchFor로 위임해 매칭 책임만 추출할 수 있는 준비를 마친다 (utj3-refactor/16 Profile.matches, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:241`).
```java
public boolean matches(Criteria criteria) {
    score = new Matcher(criteria, answers).score();
    return isMatchFor(criteria); // encapsulate matching logic
}

private boolean isMatchFor(Criteria criteria) {
    if (anyRequiredCriteriaNotMet(criteria)) return false;
    return anyMatches(criteria);
}
```
```python
class ProfileWithMatcherStep3(Profile):
    """Extracts matching logic into a dedicated helper method."""

    def matches(self, criteria: "Criteria") -> bool:
        matcher = Matcher(criteria, self._answers)  # type: ignore[arg-type]
        self._score = matcher.score()
        return self._is_match_for(criteria)

    def _is_match_for(self, criteria: "Criteria") -> bool:
        if self._any_required_criteria_not_met(criteria):
            return False
        return self._any_matches(criteria)
```

Matcher는 score 계산과 profileAnswerMatching을 받아들여 새 책임을 수행한다 (utj3-refactor/14 Matcher, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:185`).
```java
import java.util.Map;

// Matcher starts owning scoring logic copied from Profile.
public class Matcher {
    private final Map<String, Answer> answers;
    private int score;

    public Matcher(Criteria criteria, Map<String, Answer> answers) {
        this.answers = answers;
        calculateScore(criteria); // compute score eagerly
    }

    private void calculateScore(Criteria criteria) {
        score = criteria.stream()
            .filter(criterion -> criterion.isMatch(profileAnswerMatching(criterion)))
            .mapToInt(criterion -> criterion.weight().value())
            .sum();
    }

    private Answer profileAnswerMatching(Criterion criterion) {
        return answers.get(criterion.questionText());
    }

    public int score() {
        return score;
    }
}
```
```python
from typing import Dict

class Matcher:
    """Initial Matcher copies scoring logic from Profile."""

    def __init__(self, criteria: "Criteria", answers: Dict[str, "Answer"]) -> None:
        self._criteria = criteria
        self._answers = answers
        self._score = self._calculate_score(criteria)

    def _calculate_score(self, criteria: "Criteria") -> int:
        return sum(
            criterion.weight().value()
            for criterion in criteria
            if criterion.is_match(self._profile_answer_matching(criterion))
        )

    def _profile_answer_matching(self, criterion: "Criterion") -> "Answer | None":
        return self._answers.get(criterion.question_text())

    def score(self) -> int:
        return self._score
```

isMatchFor와 관련 메서드도 Matcher로 이동한다 (utj3-refactor/17 Matcher, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:255`).
```java
public class Matcher {
    // ... existing fields and constructor ...

    public boolean isMatchFor(Criteria criteria) {
        if (anyRequiredCriteriaNotMet(criteria)) return false;
        return anyMatches(criteria);
    }

    private boolean anyMatches(Criteria criteria) {
        return criteria.stream()
            .anyMatch(criterion -> criterion.isMatch(profileAnswerMatching(criterion)));
    }

    private boolean anyRequiredCriteriaNotMet(Criteria criteria) {
        return criteria.stream()
            .filter(criterion -> !criterion.isMatch(profileAnswerMatching(criterion)))
            .anyMatch(criterion -> criterion.weight() == REQUIRED);
    }

    Answer profileAnswerMatching(Criterion criterion) {
        return answers.get(criterion.questionText());
    }
    // ...
}
```
```python
class MatcherWithMatching(Matcher):
    """Adds matching logic migrated from Profile."""

    def is_match_for(self, criteria: "Criteria") -> bool:
        if self._any_required_criteria_not_met(criteria):
            return False
        return self._any_matches(criteria)

    def _any_matches(self, criteria: "Criteria") -> bool:
        return any(
            criterion.is_match(self._profile_answer_matching(criterion))
            for criterion in criteria
        )

    def _any_required_criteria_not_met(self, criteria: "Criteria") -> bool:
        return any(
            criterion.weight() == Weight.REQUIRED and
            not criterion.is_match(self._profile_answer_matching(criterion))
            for criterion in criteria
        )
```

Profile은 두 개의 Matcher 인스턴스를 생성하던 중간 단계 후 로컬 변수로 정리된다 (utj3-refactor/17 Profile.matches, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:288`; utj3-refactor/18 Profile.matches, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:295`).
```java
public boolean matches(Criteria criteria) {
    score = new Matcher(criteria, answers).score();
    return new Matcher(criteria, answers).isMatchFor(criteria);
}
```
```java
public boolean matches(Criteria criteria) {
    var matcher = new Matcher(criteria, answers); // reuse single matcher instance
    score = matcher.score();
    return matcher.isMatchFor(criteria);
}
```
```python
class ProfileWithMatcherStep4(Profile):
    """Reduces double Matcher instantiation to a single reusable instance."""

    def matches(self, criteria: "Criteria") -> bool:
        matcher = MatcherWithMatching(criteria, self._answers)  # type: ignore[arg-type]
        self._score = matcher.score()
        return matcher.is_match_for(criteria)
```

모든 매칭 로직이 빠진 Profile은 데이터 관리 중심으로 다듬어진다 (utj3-refactor/18 Profile 전체, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:302`).
```java
import java.util.HashMap;
import java.util.Map;

// Profile now focuses on storing answers and delegating work to Matcher.
public class Profile {
    private final Map<String, Answer> answers = new HashMap<>();
    private final String name;
    private int score;

    public Profile(String name) {
        this.name = name;
    }

    public void add(Answer... newAnswers) {
        for (var answer : newAnswers) {
            answers.put(answer.questionText(), answer);
        }
    }

    public boolean matches(Criteria criteria) {
        var matcher = new Matcher(criteria, answers);
        score = matcher.score();
        return matcher.isMatchFor(criteria);
    }

    public int score() {
        return score;
    }

    @Override
    public String toString() {
        return name;
    }
}
```
```python
class ProfileAfterMatcherExtraction(Profile):
    """Data-focused Profile that delegates both scoring and matching."""

    def matches(self, criteria: "Criteria") -> bool:
        matcher = MatcherWithMatching(criteria, self._answers)  # type: ignore[arg-type]
        self._score = matcher.score()
        return matcher.is_match_for(criteria)
```
```python
class ProfileAfterMatcherExtractionFull:
    """Python equivalent of the post-extraction Profile."""

    def __init__(self, name: str) -> None:
        self._answers: Dict[str, "Answer"] = {}
        self._name = name
        self._score = 0

    def add(self, *new_answers: "Answer") -> None:
        for answer in new_answers:
            self._answers[answer.question_text()] = answer

    def matches(self, criteria: "Criteria") -> bool:
        matcher = MatcherWithMatching(criteria, self._answers)  # type: ignore[arg-type]
        self._score = matcher.score()
        return matcher.is_match_for(criteria)

    def score(self) -> int:
        return self._score

    def __str__(self) -> str:
        return self._name
```

### 화제 4. Matcher 정비와 조건식 단순화
앞선 화제의 책임 이전을 마무리한 뒤, Matcher와 Profile 호출부를 정리해 응집도를 높이고 가독성을 개선한다 (Cleaning Up After a Move, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:340`).

Profile은 matcher.matches()를 호출하도록 정리돼 두 책임 위임을 명확히 표현한다 (utj3-refactor/19 Profile.matches, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:351`).
```java
public boolean matches(Criteria criteria) {
    var matcher = new Matcher(criteria, answers); // prepare reusable matcher
    score = matcher.score();
    return matcher.matches(); // delegate existence check to Matcher
}
```
```python
class ProfileAfterMatcherCleanup(ProfileAfterMatcherExtractionFull):
    """Profile now calls Matcher.matches() for clarity."""

    def matches(self, criteria: "Criteria") -> bool:
        matcher = MatcherWithMatching(criteria, self._answers)  # type: ignore[arg-type]
        self._score = matcher.score()
        return matcher.matches()
```

Matcher는 criteria를 필드에 저장해 중복 인자를 제거하고 계산을 일관되게 수행한다 (utj3-refactor/19 Matcher 전체, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:360`).
```java
public class Matcher {
    private final Criteria criteria;
    private final Map<String, Answer> answers;
    private int score;

    public Matcher(Criteria criteria, Map<String, Answer> answers) {
        this.criteria = criteria;
        this.answers = answers;
        calculateScore();
    }

    private void calculateScore() {
        score = criteria.stream()
            .filter(criterion -> criterion.isMatch(profileAnswerMatching(criterion)))
            .mapToInt(criterion -> criterion.weight().value())
            .sum();
    }

    public boolean matches() {
        if (anyRequiredCriteriaNotMet()) return false;
        return anyMatches();
    }

    private boolean anyMatches() {
        return criteria.stream()
            .anyMatch(criterion -> criterion.isMatch(profileAnswerMatching(criterion)));
    }

    private boolean anyRequiredCriteriaNotMet() {
        return criteria.stream()
            .filter(criterion -> !criterion.isMatch(profileAnswerMatching(criterion)))
            .anyMatch(criterion -> criterion.weight() == REQUIRED);
    }

    private Answer profileAnswerMatching(Criterion criterion) {
        return answers.get(criterion.questionText());
    }

    public int score() {
        return score;
    }
}
```
```python
class MatcherCleaned:
    """Stores criteria as state and removes redundant arguments."""

    def __init__(self, criteria: "Criteria", answers: Dict[str, "Answer"]) -> None:
        self._criteria = criteria
        self._answers = answers
        self._score = self._calculate_score()

    def _calculate_score(self) -> int:
        return sum(
            criterion.weight().value()
            for criterion in self._criteria
            if criterion.is_match(self._profile_answer_matching(criterion))
        )

    def matches(self) -> bool:
        if self._any_required_criteria_not_met():
            return False
        return self._any_matches()

    def _any_matches(self) -> bool:
        return any(
            criterion.is_match(self._profile_answer_matching(criterion))
            for criterion in self._criteria
        )

    def _any_required_criteria_not_met(self) -> bool:
        return any(
            criterion.weight() == Weight.REQUIRED and
            not criterion.is_match(self._profile_answer_matching(criterion))
            for criterion in self._criteria
        )

    def _profile_answer_matching(self, criterion: "Criterion") -> "Answer | None":
        return self._answers.get(criterion.question_text())

    def score(self) -> int:
        return self._score
```

조건식을 단일 표현식으로 합쳐 보다 선언적으로 matches를 표현한다 (utj3-refactor/20 Matcher.matches, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:431`).
```java
public boolean matches() {
    return !anyRequiredCriteriaNotMet() && anyMatches();
}
```
```python
class MatcherCombinedCondition(MatcherCleaned):
    """Combines the matching condition into a single boolean expression."""

    def matches(self) -> bool:
        return (not self._any_required_criteria_not_met()) and self._any_matches()
```

부정 로직을 제거하고 allRequiredCriteriaMet 이름을 도입해 읽기 쉬운 구조로 바꾼다 (utj3-refactor/21 Matcher.matches, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:446`).
```java
public boolean matches() {
    return allRequiredCriteriaMet() && anyMatches();
}

private boolean allRequiredCriteriaMet() {
    return criteria.stream()
        .filter(criterion -> criterion.weight() == REQUIRED)
        .allMatch(criterion -> criterion.isMatch(profileAnswerMatching(criterion)));
}
```
```python
class MatcherPositiveLogic(MatcherCombinedCondition):
    """Uses positive logic by checking that all required criteria are met."""

    def matches(self) -> bool:
        return self._all_required_criteria_met() and self._any_matches()

    def _all_required_criteria_met(self) -> bool:
        required = [criterion for criterion in self._criteria if criterion.weight() == Weight.REQUIRED]
        return all(
            criterion.is_match(self._profile_answer_matching(criterion))
            for criterion in required
        )
```

score는 필요할 때 계산하도록 지연 평가 형태로 바뀐다 (utj3-refactor/21 Matcher.score, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:467`).
```java
public int score() {
    return criteria.stream()
        .filter(criterion -> criterion.isMatch(profileAnswerMatching(criterion)))
        .mapToInt(criterion -> criterion.weight().value())
        .sum();
}
```
```python
class MatcherLazyScore(MatcherPositiveLogic):
    """Calculates the score lazily when requested."""

    def score(self) -> int:
        return sum(
            criterion.weight().value()
            for criterion in self._criteria
            if criterion.is_match(self._profile_answer_matching(criterion))
        )
```

### 화제 5. CQS 구현과 인터페이스 수정
앞선 Matcher 정비 이후, 명령-질의 분리 위반을 해소하기 위해 matches와 score의 책임을 분리하고 테스트를 보정한다 (Command-Query Separation, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:528`; Profile score 재설계, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:545`).

Profile은 matches와 score 각각이 부작용 없이 하나의 역할만 수행하도록 바뀐다 (utj3-refactor/22 Profile, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:545`).
```java
public boolean matches(Criteria criteria) {
    return new Matcher(criteria, answers).matches(); // returns boolean only
}

public int score(Criteria criteria) {
    return new Matcher(criteria, answers).score(); // computes numeric score on demand
}
```
```python
class ProfileCQS:
    """CQS-compliant Profile that delegates per-call to Matcher."""

    def __init__(self, name: str) -> None:
        self._answers: Dict[str, "Answer"] = {}
        self._name = name

    def add(self, *new_answers: "Answer") -> None:
        for answer in new_answers:
            self._answers[answer.question_text()] = answer

    def matches(self, criteria: "Criteria") -> bool:
        matcher = MatcherLazyScore(criteria, self._answers)  # type: ignore[arg-type]
        return matcher.matches()

    def score(self, criteria: "Criteria") -> int:
        matcher = MatcherLazyScore(criteria, self._answers)  # type: ignore[arg-type]
        return matcher.score()
```

점수 계산 인터페이스가 달라졌기에 테스트도 Criteria 인자를 전달하도록 수정된다 (utj3-refactor/22 AProfile, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:566`).
```java
@Test
void isZeroWhenThereAreNoMatches() {
    profile.add(bonusNo);
    criteria = new Criteria(
        new Criterion(bonusYes, IMPORTANT));
    var score = profile.score(criteria); // score now requires criteria argument
    assertEquals(0, score);
}
```
```python
import pytest

class TestProfileCQS:
    """Mirrors the Java test ensuring score requires criteria input."""

    def test_is_zero_when_there_are_no_matches(self) -> None:
        profile = ProfileCQS("x")
        profile.add(bonus_no)
        criteria = Criteria(Criterion(bonus_yes, Weight.IMPORTANT))
        score = profile.score(criteria)
        assert score == 0
```

### 화제 6. 테스트 재구성과 Matcher 보조 생성자
CQS 조정 뒤에는 테스트가 Profile이 아닌 Matcher를 직접 검증하도록 재구성되고, Matcher는 테스트 편의를 위한 보조 생성자를 제공한다 (Refocusing Tests, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:602`; Matcher varargs 생성자, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:645`).

Matcher는 가변 인자나 리스트를 받아 내부적으로 맵으로 변환하는 생성자를 추가한다 (utj3-refactor/22 Matcher, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:645`).
```java
public Matcher(Criteria criteria, Answer... matcherAnswers) {
    this.criteria = criteria;
    this.answers = toMap(matcherAnswers); // convert answers to a map by question text
}

private Map<String, Answer> toMap(Answer[] answers) {
    return Stream.of(answers).collect(
        Collectors.toMap(Answer::questionText, answer -> answer));
}
```
```python
class MatcherConvenience(MatcherLazyScore):
    """Adds convenience constructors for tests."""

    @classmethod
    def from_answers(cls, criteria: "Criteria", *answers: "Answer") -> "MatcherConvenience":
        answer_map = {answer.question_text(): answer for answer in answers}
        return cls(criteria, answer_map)
```

테스트는 Profile 대신 Matcher를 직접 구성해 명확한 의도를 표현한다 (utj3-refactor/22 AMatcher, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:624`).
```java
@Test
void whenNoneOfMultipleCriteriaMatch() {
    criteria = new Criteria(
        new Criterion(bonusYes, IMPORTANT),
        new Criterion(freeLunchYes, IMPORTANT));
    matcher = new Matcher(criteria, bonusNo, freeLunchNo);
    var matches = matcher.matches();
    assertFalse(matches);
}
```
```python
class TestMatcher:
    """Deliberately verifies Matcher without going through Profile."""

    def test_when_none_of_multiple_criteria_match(self) -> None:
        criteria = Criteria(
            Criterion(bonus_yes, Weight.IMPORTANT),
            Criterion(free_lunch_yes, Weight.IMPORTANT),
        )
        matcher = MatcherConvenience.from_answers(criteria, bonus_no, free_lunch_no)
        assert matcher.matches() is False
```

### 화제 7. 서비스 위임과 Profile 단순화
테스트 재구성 이후 책임을 더 분산하기 위해 서비스 계층이 Matcher 협력을 담당하고, Profile과 Matcher는 보다 단순한 형태로 마무리된다 (MatcherService 소개, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:691`; Profile 최종 정리, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:711`).

서비스는 데이터를 조회한 뒤 Matcher를 생성해 matches와 score를 호출한다 (utj3-refactor/23 MatcherService, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:691`).
```java
public class MatcherService {
    public boolean matches(int profileId, int criteriaId) {
        var profile = profileData.retrieve(profileId);
        var criteria = criteriaData.retrieve(criteriaId);
        return new Matcher(criteria, profile.answers()).matches();
    }

    public int score(int profileId, int criteriaId) {
        var profile = profileData.retrieve(profileId);
        var criteria = criteriaData.retrieve(criteriaId);
        return new Matcher(criteria, profile.answers()).score();
    }
    // ...
}
```
```python
class MatcherService:
    """Service layer coordinates fetching data and delegating to Matcher."""

    def matches(self, profile_id: int, criteria_id: int) -> bool:
        profile = profile_data.retrieve(profile_id)  # placeholder gateway
        criteria = criteria_data.retrieve(criteria_id)
        matcher = MatcherConvenience(criteria, {answer.question_text(): answer for answer in profile.answers()})
        return matcher.matches()

    def score(self, profile_id: int, criteria_id: int) -> int:
        profile = profile_data.retrieve(profile_id)
        criteria = criteria_data.retrieve(criteria_id)
        matcher = MatcherConvenience(criteria, {answer.question_text(): answer for answer in profile.answers()})
        return matcher.score()
```

Profile은 리스트로 답변을 저장하며 add와 accessor만 유지한다 (utj3-refactor/23 Profile, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:711`).
```java
import java.util.ArrayList;
import java.util.List;

// Final Profile stores answers as a simple list and exposes read-only access.
public class Profile {
    private final List<Answer> answers = new ArrayList<>();
    private final String name;

    public Profile(String name) {
        this.name = name;
    }

    public void add(Answer... newAnswers) {
        for (var answer : newAnswers) {
            answers.add(answer);
        }
    }

    public List<Answer> answers() {
        return answers;
    }

    public String name() {
        return name;
    }
}
```
```python
class ProfileFinal:
    """Simplified Profile that only stores answers and exposes them."""

    def __init__(self, name: str) -> None:
        self._answers: list["Answer"] = []
        self._name = name

    def add(self, *new_answers: "Answer") -> None:
        self._answers.extend(new_answers)

    def answers(self) -> list["Answer"]:
        return list(self._answers)

    def name(self) -> str:
        return self._name
```

간단한 Profile 테스트는 리스트 반환을 검증한다 (utj3-refactor/23 AProfile, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:736`).
```java
@Test
void supportsAddingIndividualAnswers() {
    var answer = new Answer(question, "Y");
    profile.add(answer);
    assertEquals(List.of(answer), profile.answers());
}
```
```python
class TestProfileFinal:
    """Ensures Profile exposes stored answers exactly."""

    def test_supports_adding_individual_answers(self) -> None:
        question = Question("?", ["Y", "N"], 1)
        profile = ProfileFinal("x")
        answer = Answer(question, "Y")
        profile.add(answer)
        assert profile.answers() == [answer]
```

최종 Matcher는 Java record로 정의되며 다양한 팩토리 생성자를 제공한다 (utj3-refactor/23 Matcher, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:753`).
```java
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public record Matcher(Criteria criteria, Map<String, Answer> answers) {
    public Matcher(Criteria criteria, List<Answer> matcherAnswers) {
        this(criteria, asMap(matcherAnswers));
    }

    public Matcher(Criteria criteria, Answer... matcherAnswers) {
        this(criteria, asList(matcherAnswers));
    }

    private static Map<String, Answer> asMap(List<Answer> answers) {
        return answers.stream().collect(
            Collectors.toMap(Answer::questionText, answer -> answer));
    }

    public boolean matches() {
        return allRequiredCriteriaMet() && anyMatches();
    }

    private boolean allRequiredCriteriaMet() {
        return criteria.stream()
            .filter(criterion -> criterion.weight() == REQUIRED)
            .allMatch(criterion -> criterion.isMatch(profileAnswerMatching(criterion)));
    }

    private boolean anyMatches() {
        return criteria.stream()
            .anyMatch(criterion -> criterion.isMatch(profileAnswerMatching(criterion)));
    }

    private Answer profileAnswerMatching(Criterion criterion) {
        return answers.get(criterion.questionText());
    }

    public int score() {
        return criteria.stream()
            .filter(criterion -> criterion.isMatch(profileAnswerMatching(criterion)))
            .mapToInt(criterion -> criterion.weight().value())
            .sum();
    }
}
```
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class MatcherFinal:
    """Python analogue of the record-based Matcher."""

    criteria: "Criteria"
    answers: dict[str, "Answer"]

    @classmethod
    def from_list(cls, criteria: "Criteria", answers: list["Answer"]) -> "MatcherFinal":
        return cls(criteria, {answer.question_text(): answer for answer in answers})

    @classmethod
    def from_varargs(cls, criteria: "Criteria", *answers: "Answer") -> "MatcherFinal":
        return cls.from_list(criteria, list(answers))

    def matches(self) -> bool:
        return self._all_required_criteria_met() and self._any_matches()

    def _all_required_criteria_met(self) -> bool:
        required = [criterion for criterion in self.criteria if criterion.weight() == Weight.REQUIRED]
        return all(
            criterion.is_match(self._profile_answer_matching(criterion))
            for criterion in required
        )

    def _any_matches(self) -> bool:
        return any(
            criterion.is_match(self._profile_answer_matching(criterion))
            for criterion in self.criteria
        )

    def _profile_answer_matching(self, criterion: "Criterion") -> "Answer | None":
        return self.answers.get(criterion.question_text())

    def score(self) -> int:
        return sum(
            criterion.weight().value()
            for criterion in self.criteria
            if criterion.is_match(self._profile_answer_matching(criterion))
        )
```
※ `profile_data`와 `criteria_data`는 서비스 계층 예시에서 데이터를 조회하는 저장소 게이트웨이를 뜻하는 플레이스홀더다 (MatcherService 소개, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:691`).

### 화제 8. 설계 원칙 요약과 실천 촉구
서비스와 클래스 구조 정리가 끝난 뒤, 장은 SRP와 CQS 같은 기본 원칙이 장기 유지보수성과 개발자 고통을 줄인다는 점을 다시 강조하며 작은 리팩터링을 꾸준히 실행하라고 권한다 (Chapter Summary, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:799`; Summary 강조, `refactoring/tests/data/Pragmatic_Unit_Testing_in_Java_with_JUnit/9._Refactoring_Your_Codes_Structure/content.md:812`).

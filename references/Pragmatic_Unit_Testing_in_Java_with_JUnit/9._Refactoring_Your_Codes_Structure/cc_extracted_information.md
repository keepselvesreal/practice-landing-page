<!--
생성 시간: Mon Sep 29 20:55:45 KST 2025
핵심 내용: 코드 구조 리팩토링을 통한 설계 개선 - SRP와 CQS 원칙 적용
상세 내용:
    - Profile 클래스의 SRP 위반 문제 (라인 52-98): 프로필 정보 관리와 매칭 로직의 이중 책임
    - Matcher 클래스 추출 과정 (라인 155-210): 매칭 로직을 별도 클래스로 분리
    - CQS 원칙 적용 (라인 504-557): 명령과 쿼리의 분리를 통한 설계 개선
    - 테스트 리팩토링 (라인 602-654): AMatcher 클래스로 테스트 이동 및 적응
    - 최종 설계 (라인 711-793): Profile, Matcher, MatcherService 클래스의 역할 분담
상태: active
참조: 없음
-->

# 9장: 코드 구조 리팩토링 (Refactoring Your Code's Structure)

## 압축 내용

코드 설계의 거시적/미시적 관점을 이해하고, SRP(단일 책임 원칙)와 CQS(명령-쿼리 분리) 원칙을 적용하여 Profile 클래스를 Matcher 클래스로 분리함으로써 더 나은 시스템 설계를 달성하는 과정을 다룬다.

## 핵심 내용

### 핵심 개념
1. **설계 관점의 구분**: 미시적 설계 vs 거시적 설계
2. **SRP (단일 책임 원칙)**: 클래스는 변경되는 이유가 하나만 있어야 함
3. **CQS (명령-쿼리 분리)**: 메서드는 부수 효과를 생성하거나 값을 반환하는 것 중 하나만 수행
4. **OTAAT (한 번에 한 가지)**: 점진적 소프트웨어 개발의 핵심 철학

### 핵심 개념 설명
- **미시적 설계**: 필드의 상태 관리, 메서드 구성, 메서드 간 상호작용 등 코드 내부 구조 (참조: 라인 11-15)
- **거시적 설계**: 클래스를 패키지로, 메서드를 클래스로 구성하는 방식, 클래스 간 상호작용 (참조: 라인 16-19)
- **SRP**: 클래스가 여러 책임을 가질수록 기존 동작을 깨뜨릴 위험이 증가하므로 변경 위험을 줄임 (참조: 라인 115-120)
- **CQS**: 메서드가 값 반환과 부수 효과를 동시에 수행하면 클라이언트 코드에 잠재적 문제 야기 (참조: 라인 528-532)

### 핵심 개념 간 관계
SRP와 CQS는 모두 설계의 명확성과 예측 가능성을 높이는 원칙이며, OTAAT 철학 하에서 점진적으로 적용되어 시스템의 유지보수성과 테스트 용이성을 향상시킨다.

## 상세 핵심 내용

### 중요 개념
1. **설계 관점의 구분**: 미시적 설계 vs 거시적 설계
2. **SRP (단일 책임 원칙)**: 클래스는 변경되는 이유가 하나만 있어야 함
3. **CQS (명령-쿼리 분리)**: 메서드는 부수 효과를 생성하거나 값을 반환하는 것 중 하나만 수행
4. **OTAAT (한 번에 한 가지)**: 점진적 소프트웨어 개발의 핵심 철학
5. **SOLID 원칙**: 객체지향 클래스 설계의 5가지 핵심 원칙
6. **응집도와 결합도**: 높은 응집도와 낮은 결합도가 좋은 설계의 기반
7. **리팩토링 전략**: 점진적 변경과 테스트 기반 검증

### 중요 개념 설명

**설계 관점의 구분** (참조: 라인 11-19, 23-24)
- 미시적 설계: 필드의 상태 관리, 메서드 구성, 메서드 간 상호작용, 외부 세계와의 상호작용
- 거시적 설계: 클래스를 패키지로 구성, 메서드를 클래스로 구성, 클래스 간 상호작용
- 소프트웨어 시스템의 설계는 거시적/미시적 수준에서 내린 모든 선택의 결합체

**SRP (단일 책임 원칙)** (참조: 라인 115-120, 126-127)
- 클래스는 변경되는 이유가 하나만 있어야 함
- 더 많은 책임을 가진 클래스일수록 클래스 내 코드 변경 시 기존 동작을 깨뜨리기 쉬움
- 작고 집중된 클래스는 재사용 가능성이 높고 다른 컨텍스트에서 가치 제공

**CQS (명령-쿼리 분리)** (참조: 라인 528-532)
- 메서드는 명령(부수 효과 생성) 또는 쿼리(값 반환) 중 하나만 수행해야 함
- 둘 다 수행하면 클라이언트 코드에 잠재적 고통 야기
- 쿼리 메서드가 객체 상태를 변경하면 재호출 시 동일한 답을 얻지 못할 수 있음

**SOLID 원칙** (참조: 라인 121-138)
- Single Responsibility Principle: 클래스는 하나의 변경 이유만 가져야 함
- Open-Closed Principle: 확장에는 열려있고 수정에는 닫혀있어야 함
- Liskov Substitution Principle: 하위 타입은 기본 타입으로 대체 가능해야 함
- Interface Segregation Principle: 클라이언트는 사용하지 않는 메서드에 의존하지 않아야 함
- Dependency Inversion Principle: 고수준 모듈은 저수준 모듈에 의존하지 않아야 함

**응집도와 결합도** (참조: 라인 142-149)
- 시스템의 클래스는 높은 응집도와 낮은 결합도를 보여야 함
- 이러한 시스템은 변경을 쉽게 만들고 단위 테스트도 쉽게 만듦
- 원칙들은 절대적이지 않으며 성능 등 다른 고려사항과 균형을 맞춰야 함

**리팩토링 전략** (참조: 라인 162-163)
- 점진적 경로: 작은 변경을 만들고 테스트를 실행하여 여전히 통과하는지 확인
- 프로덕션 코드 또는 테스트 중 하나만 변경하고 둘 다 동시에 변경하지 않음

### 중요 개념 간 관계
SOLID 원칙은 응집도와 결합도 개념을 기반으로 하며, SRP와 CQS는 이러한 원칙들의 구체적 적용 사례이다. OTAAT 철학은 이 모든 원칙들을 점진적으로 적용하는 방법론을 제공하며, 리팩토링 전략은 이를 안전하게 실행하는 구체적 방법을 제시한다. 설계 개선은 테스트와 상호 영향을 미치며, 좋은 설계는 테스트 작성을 쉽게 만들고, 테스트는 설계 개선의 신뢰도를 높인다.

## 상세 내용

### 1. 설계의 이해와 테스트의 관계 (참조: 라인 5-35)

코드 리팩토링은 이전 장에서 matches 메서드를 여러 구성 메서드로 분해하고 각 메서드의 명확성과 간결성에 집중한 작업의 연장선이다. 이러한 지속적인 소규모 코드 편집은 설계의 기본 요소로, 코드 이해와 유지보수 비용을 낮게 유지하는 방식으로 솔루션을 구현하는 선택을 만드는 것이다.

소프트웨어 시스템의 설계는 거시적/미시적 수준에서 내린 선택들의 결합체이며, 단위 테스트 작성은 진공 상태에서 발생하는 작업이 아니다. 시스템 설계는 테스트 작성 능력에 영향을 미치고 그 반대도 마찬가지다.

**핵심 원칙**: 시스템 설계의 가장 중요한 측면은 의도한 대로 작동한다는 것이다. (참조: 라인 36-37)

### 2. Profile 클래스와 SRP 위반 분석 (참조: 라인 50-120)

Profile 클래스는 70줄 미만의 소스 코드로 과도하게 크거나 복잡해 보이지 않지만, 이상적이지 않은 설계를 암시한다.

```java
// Profile 클래스의 구조 (라인 52-98)
public class Profile {
    private final Map<String,Answer> answers = new HashMap<>();  // 답변 저장
    private final String name;  // 프로필 이름
    private int score;  // 점수 (부수 효과로 저장됨)

    public Profile(String name) { this.name = name; }

    public void add(Answer... newAnswers) {
        for (var answer: newAnswers)
            answers.put(answer.questionText(), answer);
    }

    public boolean matches(Criteria criteria) {
        calculateScore(criteria);  // 부수 효과: 점수 계산 및 저장
        if (anyRequiredCriteriaNotMet(criteria)) return false;
        return anyMatches(criteria);
    }

    // 매칭 관련 private 메서드들
    private boolean anyRequiredCriteriaNotMet(Criteria criteria) { /* ... */ }
    private void calculateScore(Criteria criteria) { /* ... */ }
    private boolean anyMatches(Criteria criteria) { /* ... */ }
    private Answer profileAnswerMatching(Criterion criterion) { /* ... */ }

    public int score() { return score; }
    @Override
    public String toString() { return name; }
}
```

Profile 클래스는 두 가지 책임을 수행한다:
1. **주요 책임**: 회사나 개인의 정보(이름과 질문 답변 모음) 추적 및 관리
2. **보조 책임**: 기준 세트가 프로필과 일치하는지, 어느 정도 일치하는지 나타내는 점수 계산

이는 SRP를 위반한다. 클래스는 변경되는 이유가 하나만 있어야 하는데, Profile 클래스는 두 가지 이유로 변경될 수 있다:
- 프로필 정보 구조 변경 (정보 추가/제거/변경)
- 매칭 알고리즘의 정교함 변경

### 3. SOLID 클래스 설계 원칙 (참조: 라인 121-149)

Robert C. Martin이 1990년대 중반에 수집한 객체지향 클래스 설계의 5가지 원칙:

```python
# SOLID 원칙의 Python 적용 예시

# S - Single Responsibility Principle
class Profile:
    """프로필 정보만 관리 (하나의 책임)"""
    def __init__(self, name):
        self.name = name
        self.answers = []

    def add_answer(self, answer):
        self.answers.append(answer)

class Matcher:
    """매칭 로직만 담당 (하나의 책임)"""
    def __init__(self, criteria, answers):
        self.criteria = criteria
        self.answers = answers

    def matches(self):
        return self.all_required_met() and self.any_matches()

# O - Open-Closed Principle
from abc import ABC, abstractmethod

class MatchingStrategy(ABC):
    @abstractmethod
    def calculate_score(self, criteria, answers):
        pass

class WeightedMatchingStrategy(MatchingStrategy):
    """확장을 위해 열려있지만 수정에는 닫혀있음"""
    def calculate_score(self, criteria, answers):
        # 가중치 기반 점수 계산
        pass

# L - Liskov Substitution Principle
class BaseMatcher:
    def matches(self):
        return True

class StrictMatcher(BaseMatcher):
    """기본 타입으로 대체 가능해야 함"""
    def matches(self):
        # 더 엄격한 매칭이지만 기본 계약 유지
        return super().matches() and self.additional_checks()

# I - Interface Segregation Principle
class Scorable(ABC):
    @abstractmethod
    def score(self):
        pass

class Matchable(ABC):
    @abstractmethod
    def matches(self):
        pass

# D - Dependency Inversion Principle
class MatcherService:
    def __init__(self, matcher_strategy: MatchingStrategy):
        self.strategy = matcher_strategy  # 추상화에 의존
```

### 4. Matcher 클래스 추출 과정 (참조: 라인 155-216)

점진적 리팩토링을 통해 Profile에서 Matcher로 책임을 분리:

**1단계: calculateScore 로직 이동** (참조: 라인 164-180)
```java
// Profile.java 변경
public boolean matches(Criteria criteria) {
    score = new Matcher(criteria, answers).score();  // 새로운 Matcher 사용
    if (anyRequiredCriteriaNotMet(criteria)) return false;
    return anyMatches(criteria);
}

// 새로운 Matcher.java
public class Matcher {
    private final Map<String, Answer> answers;
    private int score;

    public Matcher(Criteria criteria, Map<String, Answer> answers) {
        this.answers = answers;
        calculateScore(criteria);  // 생성자에서 점수 계산
    }

    private void calculateScore(Criteria criteria) {
        score = criteria.stream()
            .filter(criterion ->
                criterion.isMatch(profileAnswerMatching(criterion)))
            .mapToInt(criterion -> criterion.weight().value())
            .sum();
    }

    public int score() { return score; }
}
```

**2단계: 매칭 기능을 Matcher로 이동** (참조: 라인 217-283)
Profile의 matches 메서드에서 매칭 로직을 추출하여 isMatchFor 메서드로 만들고, 이를 Matcher로 이동:

```java
// Matcher.java에 추가된 메서드들
public boolean isMatchFor(Criteria criteria) {
    if (anyRequiredCriteriaNotMet(criteria)) return false;
    return anyMatches(criteria);
}

private boolean anyMatches(Criteria criteria) {
    return criteria.stream()
        .anyMatch(criterion ->
            criterion.isMatch(profileAnswerMatching(criterion)));
}

private boolean anyRequiredCriteriaNotMet(Criteria criteria) {
    return criteria.stream()
        .filter(criterion ->
            !criterion.isMatch(profileAnswerMatching(criterion)))
        .anyMatch(criterion -> criterion.weight() == REQUIRED);
}

Answer profileAnswerMatching(Criterion criterion) {
    return answers.get(criterion.questionText());
}
```

### 5. 리팩토링 후 정리 작업 (참조: 라인 339-409)

Matcher 클래스를 더 효율적으로 만들기 위한 개선:

**criteria를 필드로 저장하여 매개변수 전달 제거** (참조: 라인 344-409)
```java
public class Matcher {
    private final Criteria criteria;  // 필드로 저장
    private final Map<String, Answer> answers;

    public Matcher(Criteria criteria, Map<String, Answer> answers) {
        this.criteria = criteria;
        this.answers = answers;
    }

    public boolean matches() {  // criteria 매개변수 제거
        return allRequiredCriteriaMet() && anyMatches();
    }

    private boolean allRequiredCriteriaMet() {  // 개선된 로직
        return criteria.stream()
            .filter(criterion -> criterion.weight() == REQUIRED)
            .allMatch(criterion ->
                criterion.isMatch(profileAnswerMatching(criterion)));
    }

    // 점수 계산을 지연 실행으로 변경
    public int score() {
        return criteria.stream()
            .filter(criterion ->
                criterion.isMatch(profileAnswerMatching(criterion)))
            .mapToInt(criterion -> criterion.weight().value())
            .sum();
    }
}
```

### 6. CQS 문제와 해결 (참조: 라인 504-557)

**CQS 위반 문제 분석** (참조: 라인 505-539)
Profile의 matches 메서드는 CQS를 위반한다:
- boolean 값을 반환 (쿼리)
- score 필드를 변경하는 부수 효과 (명령)

```java
// 문제가 있는 코드
public boolean matches(Criteria criteria) {
    var matcher = new Matcher(criteria, answers);
    score = matcher.score();  // 부수 효과
    return matcher.matches(); // 값 반환
}
```

이로 인한 문제점:
- 클라이언트가 점수만 원해도 matches()를 먼저 호출해야 함 (시간적 결합)
- 매칭 여부만 확인하려 해도 점수가 변경됨
- 개발자가 부수 효과를 놓칠 수 있음

**CQS 문제 해결** (참조: 라인 540-557)
```java
// 해결된 코드
public boolean matches(Criteria criteria) {
    return new Matcher(criteria, answers).matches();  // 쿼리만
}

public int score(Criteria criteria) {  // 매개변수 추가
    return new Matcher(criteria, answers).score();   // 쿼리만
}
```

```python
# Python 버전의 CQS 해결
class Profile:
    def __init__(self, name):
        self.name = name
        self.answers = []

    def add_answer(self, answer):
        """명령: 답변 추가 (부수 효과만)"""
        self.answers.append(answer)

    def matches(self, criteria):
        """쿼리: 매칭 여부 반환 (부수 효과 없음)"""
        return Matcher(criteria, self.answers).matches()

    def score(self, criteria):
        """쿼리: 점수 반환 (부수 효과 없음)"""
        return Matcher(criteria, self.answers).score()
```

### 7. 테스트 리팩토링과 이동 (참조: 라인 577-667)

**테스트가 깨지는 이유와 의미** (참조: 라인 577-597)
- 리팩토링은 일반적으로 테스트를 깨뜨리지 않아야 함
- 하지만 여기서는 Profile 인터페이스의 결함으로 인한 행동 변경이 필요했음
- 테스트가 깨진 것은 잘못된 설계를 인식하고 수정할 수 있게 해줌

**AMatcher 테스트 클래스 생성** (참조: 라인 602-654)
Profile에서 Matcher로 동작을 이동한 후, 테스트도 새로운 AMatcher 클래스로 이동:

```java
// 기존 Profile 테스트
@Test
void whenNoneOfMultipleCriteriaMatch() {
    profile.add(bonusNo, freeLunchNo);
    criteria = new Criteria(/*...*/);
    var matches = profile.matches(criteria);
    assertFalse(matches);
}

// 새로운 Matcher 테스트
@Test
void whenNoneOfMultipleCriteriaMatch() {
    criteria = new Criteria(/*...*/);
    matcher = new Matcher(criteria, bonusNo, freeLunchNo);  // 생성자에 직접 전달
    var matches = matcher.matches();  // 매개변수 불필요
    assertFalse(matches);
}

// Matcher에 편의 생성자 추가
public Matcher(Criteria criteria, Answer... matcherAnswers) {
    this.criteria = criteria;
    this.answers = toMap(matcherAnswers);  // 배열을 Map으로 변환
}

private Map<String, Answer> toMap(Answer[] answers) {
    return Stream.of(answers).collect(
        Collectors.toMap(Answer::questionText, answer -> answer));
}
```

### 8. 최종 설계와 MatcherService (참조: 라인 668-734)

**Profile 클래스 단순화** (참조: 라인 711-734)
매칭 로직을 제거한 후 Profile은 단순한 데이터 홀더가 됨:

```java
public class Profile {
    private final List<Answer> answers = new ArrayList<>();  // Map에서 List로 변경
    private final String name;

    public Profile(String name) {
        this.name = name;
    }

    public void add(Answer... newAnswers) {
        for (var answer: newAnswers)
            answers.add(answer);  // List에 추가
    }

    public List<Answer> answers() { return answers; }
    public String name() { return name; }
}
```

**MatcherService를 통한 조정** (참조: 라인 691-704)
Profile과 Matcher 간의 조정은 서비스 클래스에서 처리:

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
}
```

```python
# Python 버전의 최종 설계
class Profile:
    """프로필 정보만 관리"""
    def __init__(self, name):
        self.name = name
        self.answers = []

    def add_answer(self, *answers):
        self.answers.extend(answers)

class Matcher:
    """매칭 로직만 담당"""
    def __init__(self, criteria, answers):
        self.criteria = criteria
        self.answers = {answer.question_text: answer for answer in answers}

    def matches(self):
        return self.all_required_met() and self.any_matches()

    def score(self):
        return sum(criterion.weight.value for criterion in self.criteria
                  if criterion.is_match(self.answers.get(criterion.question_text)))

class MatcherService:
    """Profile과 Matcher 간 조정"""
    def __init__(self, profile_data, criteria_data):
        self.profile_data = profile_data
        self.criteria_data = criteria_data

    def matches(self, profile_id, criteria_id):
        profile = self.profile_data.retrieve(profile_id)
        criteria = self.criteria_data.retrieve(criteria_id)
        return Matcher(criteria, profile.answers).matches()

    def score(self, profile_id, criteria_id):
        profile = self.profile_data.retrieve(profile_id)
        criteria = self.criteria_data.retrieve(criteria_id)
        return Matcher(criteria, profile.answers).score()
```

**Java Record를 사용한 최종 Matcher** (참조: 라인 753-793)
```java
public record Matcher(Criteria criteria, Map<String, Answer> answers) {
    // 편의 생성자들
    public Matcher(Criteria criteria, List<Answer> matcherAnswers) {
        this(criteria, asMap(matcherAnswers));
    }

    public Matcher(Criteria criteria, Answer... matcherAnswers) {
        this(criteria, asList(matcherAnswers));
    }

    // 매칭 로직
    public boolean matches() {
        return allRequiredCriteriaMet() && anyMatches();
    }

    // 점수 계산
    public int score() {
        return criteria.stream()
            .filter(criterion ->
                criterion.isMatch(profileAnswerMatching(criterion)))
            .mapToInt(criterion -> criterion.weight().value())
            .sum();
    }
}
```

### 9. 설계 개선의 효과와 향후 과제 (참조: 라인 794-825)

**개선된 설계의 장점**:
- Profile: 단일 책임(정보 관리)으로 높은 응집도
- Matcher: 매칭/점수 계산 로직의 캡슐화
- CQS 준수: 명령과 쿼리의 명확한 분리

**남은 과제**: Matcher의 응집도 개선
매칭 로직과 점수 계산 로직을 Scorer 클래스로 분리하여 더 높은 응집도 달성 (참조: 라인 794-797)

**설계 철학** (참조: 라인 799-815):
- 작고 지속적인 코드 편집이 큰 차이를 만듦
- 설계 품질은 고통과 좌절 수준과 반비례
- 유연성을 위해 작고 구성된 빌딩 블록 생성
- 자동화된 리팩토링 도구 활용
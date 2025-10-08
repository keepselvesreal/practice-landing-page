# Growing_object_oriented_software_guided_by_tests_Chapter_20_Listening_to_the_Tests

## 압축 내용

테스트 작성의 어려움은 설계 개선이 필요하다는 신호이며, 테스트가 쉬운 코드는 변경에도 쉽게 대응할 수 있다.

## 핵심 내용

### 1. 테스트의 피드백 역할 (Section: Introduction, Lines 8-25)
- **TDD의 이중 목적**: TDD는 코드의 외부적 품질(기능, 성능)뿐만 아니라 내부적 품질(결합도, 응집도, 의존성, 정보 은닉)에 대한 피드백을 제공한다.
- **테스트 작성의 어려움**: 테스트 작성이 어렵다면 설계 개선이 필요하다는 신호다. 테스트를 복잡하게 만들기보다 코드를 개선해야 한다.
- **테스트가 설계를 주도**: 테스트가 설계를 이끌어야 한다(test-driven development).
- **관련 상세 내용**: 2.1 테스트 냄새의 두 가지 범주

### 2. 테스트 냄새 (Test Smells) (Section: Introduction, Lines 26-33)
- **두 가지 범주**: 테스트 자체의 문제(불명확하거나 취약함)와 대상 코드의 문제
- **이 챕터의 초점**: 대상 코드의 문제를 드러내는 테스트 냄새에 집중
- **관련 상세 내용**: 2.1 테스트 냄새의 두 가지 범주

### 3. 싱글톤과 의존성 (Section: I Need to Mock an Object I Can't Replace, Lines 37-101)
- **싱글톤의 문제**: 전역으로 접근 가능한 객체(싱글톤)는 숨겨진 의존성이며 테스트를 어렵게 만든다.
- **해결책 - Clock 도입**: `new Date()`처럼 싱글톤에 의존하는 대신 `Clock` 객체를 주입하여 의존성을 명시적으로 만든다.
- **명시적 의존성의 장점**: 객체가 시간에 의존한다는 사실이 명확해지고, 테스트가 쉬워진다.
- **관련 상세 내용**: 3.1 싱글톤은 의존성이다, 3.2 절차에서 객체로, 3.3 암시적 의존성도 여전히 의존성이다

### 4. 절차에서 객체로의 전환 (Section: From Procedures to Objects, Lines 102-159)
- **도메인 개념 발견**: Clock을 도입한 후, 날짜 검사 로직을 Clock으로 이동하거나 `SameDayChecker` 같은 새로운 도메인 개념을 발견할 수 있다.
- **책임의 명확화**: 각 객체가 명확한 책임을 가지도록 분리하면 단위 테스트가 깔끔해진다.
- **관련 상세 내용**: 3.2 절차에서 객체로

### 5. 암시적 의존성 (Section: Implicit Dependencies Are Still Dependencies, Lines 160-180)
- **정보 은닉의 오해**: 전역 값을 통해 의존성을 숨기면 의존성이 사라지는 것이 아니라 접근 불가능해질 뿐이다.
- **명시적 경계**: 객체 지향의 목표는 객체의 경계를 명확히 하는 것이며, 로컬이거나 명시적으로 전달된 값/인스턴스만 다뤄야 한다.
- **관련 상세 내용**: 3.3 암시적 의존성도 여전히 의존성이다

### 6. 프로덕션 코드와 같은 기법 사용 (Section: Use the Same Techniques, Lines 181-195)
- **고급 테스팅 도구의 함정**: 클래스 로더나 바이트코드 조작으로 의존성을 끊는 도구는 설계 피드백을 낭비한다.
- **설계 약점 누적**: 나중에 긴급한 기능을 추가할 때 설계 약점이 시스템 전체에 영향을 미쳐 변경이 어려워진다.
- **관련 상세 내용**: 3.4 프로덕션 코드와 같은 기법 사용

### 7. 로깅은 기능이다 (Section: Logging Is a Feature, Lines 196-227)
- **두 가지 로깅**: Support logging(운영/지원팀용)과 Diagnostic logging(개발자용)은 별개의 기능이다.
- **Support logging**: 테스트 주도로 개발해야 하는 사용자 인터페이스의 일부다.
- **Diagnostic logging**: 프로그래머를 위한 인프라이며, 프로덕션에서는 켜지 않아야 한다.
- **관련 상세 내용**: 4.1 로깅은 기능이다

### 8. 알림 패턴 (Section: Notification Rather Than Logging, Lines 228-265)
- **로깅의 문제**: 정적 전역 객체에 대한 단위 테스트는 번거롭고, 코드가 두 가지 수준(도메인과 로깅 인프라)에서 작동한다.
- **Support 객체 도입**: `support.notifyFiltering()`처럼 로깅 대신 알림 객체를 사용하면 테스트가 쉬워지고 표현력이 높아진다.
- **단일 책임 원칙**: 로깅 로직을 분리하면 코드가 하나의 책임만 가진다.
- **관련 상세 내용**: 4.2 로깅 대신 알림

### 9. 구체 클래스 모킹의 문제 (Section: Mocking Concrete Classes, Lines 299-376)
- **관계의 암시성**: 구체 클래스를 모킹하면 객체 간 관계가 암시적으로 남아 있어 재사용이나 분석이 어렵다.
- **인터페이스 분리 원칙**: 클라이언트는 사용하지 않는 인터페이스에 의존하지 않아야 한다. 인터페이스 추출로 관계를 명시적으로 만든다.
- **네이밍의 중요성**: 인터페이스를 추출하면 관계에 이름을 붙이게 되고, 이는 도메인에 대한 사고를 깊게 한다.
- **관련 상세 내용**: 5.1 구체 클래스 모킹, 5.2 비상시에만 사용

### 10. 값 객체는 모킹하지 않는다 (Section: Don't Mock Values, Lines 377-408)
- **값 객체의 특성**: 불변이며 단순히 인스턴스를 생성해서 사용하면 된다.
- **모킹이 불필요한 이유**: 값 객체를 위한 인터페이스/구현 쌍을 만들 필요가 없다.
- **휴리스틱**: 값이 불변이고, 인터페이스에 의미 있는 이름을 붙이기 어렵다면(예: VideoImpl) 모킹하지 않는다.
- **관련 상세 내용**: 6.1 값 객체는 모킹하지 않는다

### 11. 비대한 생성자 (Section: Bloated Constructor, Lines 409-505)
- **원인**: TDD 과정에서 의존성을 하나씩 추가하다 보면 생성자 인자가 많아질 수 있다.
- **해결책 1 - 개념 추출**: 함께 사용되는 인자들을 묶어 새로운 객체로 추출한다(예: MessageDispatcher).
- **해결책 2 - 책임 명확화**: 객체의 책임이 명확해지고 테스트가 쉬워진다.
- **관련 상세 내용**: 7.1 비대한 생성자, 7.2 혼란스러운 객체, 7.3 너무 많은 의존성

### 12. 혼란스러운 객체 (Section: Confused Object, Lines 506-552)
- **여러 책임**: 객체가 너무 많은 관련 없는 책임을 가지면 많은 의존성이 필요하다.
- **테스트 스위트의 혼란**: 테스트들이 서로 관계가 없고, 한 영역의 변경이 다른 영역에 영향을 주지 않는다.
- **해결책**: 객체를 더 작은 부분으로 분리한다.
- **관련 상세 내용**: 7.2 혼란스러운 객체

### 13. 의존성과 조정 구분 (Section: Too Many Dependencies, Lines 553-617)
- **Peer Stereotypes**: 의존성(dependencies), 알림(notifications), 조정(adjustments)을 구분한다.
- **의존성만 생성자에**: 알림과 조정은 기본값으로 설정하고 나중에 재설정할 수 있다.
- **예시**: RacingCar에서 Track만 의존성이고 나머지는 조정 가능한 값들이다.
- **관련 상세 내용**: 7.3 너무 많은 의존성

### 14. 너무 많은 기대값 (Section: Too Many Expectations, Lines 618-678)
- **가독성 문제**: 모든 것이 기대값이면 무엇이 중요한지 알 수 없다.
- **스텁과 기대값 구분**: 스텁(시뮬레이션)은 `allowing`, 기대값(검증)은 `one`으로 표현한다.
- **부작용 중심**: 부작용이 있는 메서드만 기대값으로 만들고, 쿼리는 스텁으로 만든다.
- **관련 상세 내용**: 8.1 너무 많은 기대값, 8.2 적은 기대값 작성

### 15. 테스트가 알려주는 것들 (Section: What the Tests Will Tell Us, Lines 704-773)
- **지식의 지역성**: 객체 내부나 전달된 인자로 지식을 유지하면 컴포넌트가 독립적이고 플러그 가능해진다.
- **명시적 네이밍**: 관계에 이름을 붙이면 통제하고 재사용할 수 있다.
- **도메인 정보 증가**: 객체의 통신 방식을 강조하면 도메인 어휘가 코드에 더 많이 반영된다.
- **행동 전달**: "Tell, Don't Ask"를 일관되게 적용하면 값을 끌어올리는 대신 행동(콜백)을 전달하게 된다.
- **관련 상세 내용**: 9.1 테스트가 알려주는 것들

## 상세 내용

### 목차
1. 서론 (Introduction)
2. 테스트 냄새의 범주
   - 2.1 테스트 냄새의 두 가지 범주
3. 교체할 수 없는 객체 모킹
   - 3.1 싱글톤은 의존성이다
   - 3.2 절차에서 객체로
   - 3.3 암시적 의존성도 여전히 의존성이다
   - 3.4 프로덕션 코드와 같은 기법 사용
4. 로깅
   - 4.1 로깅은 기능이다
   - 4.2 로깅 대신 알림
   - 4.3 과도한 설계처럼 보이는가
5. 구체 클래스 모킹
   - 5.1 구체 클래스 모킹
   - 5.2 비상시에만 사용
6. 값 객체
   - 6.1 값 객체는 모킹하지 않는다
7. 생성자 문제
   - 7.1 비대한 생성자
   - 7.2 혼란스러운 객체
   - 7.3 너무 많은 의존성
8. 기대값
   - 8.1 너무 많은 기대값
   - 8.2 적은 기대값 작성
   - 8.3 특별 보너스
9. 결론
   - 9.1 테스트가 알려주는 것들

---

### 1. 서론 (Introduction)

**관계**: 이 섹션은 챕터의 기초를 제공하며, 다음 섹션(2.1)으로 이어진다.

**Lines 8-25**: 테스트 작성이 어렵다면 설계 개선의 기회다. TDD는 코드의 외부적 품질(기능, 성능)뿐만 아니라 내부적 품질(결합도, 응집도, 의존성, 정보 은닉)에 대한 피드백을 제공한다. 테스트를 복잡하게 만들기보다 코드를 개선해야 한다.

> Sometimes we find it difficult to write a test for some functionality we want to add to our code. In our experience, this usually means that our design can be improved—perhaps the class is too tightly coupled to its environment or does not have clear responsibilities. (Lines 8-11)

**핵심 개념 참조**: 1. 테스트의 피드백 역할

---

### 2.1 테스트 냄새의 두 가지 범주

**이전 섹션과의 관계**: 서론에서 테스트 작성의 어려움이 설계 개선 신호라는 개념을 소개했다. 이 섹션은 그 어려움을 구체적인 범주로 분류한다.

**Lines 26-33**: 테스트 냄새는 두 가지 범주가 있다. 첫 번째는 테스트 자체가 잘 작성되지 않은 경우(불명확하거나 취약함)이고, 두 번째는 대상 코드에 문제가 있음을 드러내는 경우다. 이 챕터는 두 번째 범주에 집중한다.

> One is where the test itself is not well written—it may be unclear or brittle. [...] This chapter is concerned with the other category, where a test is highlighting that the target code is the problem. (Lines 28-31)

**핵심 개념 참조**: 2. 테스트 냄새 (Test Smells)

---

### 3.1 싱글톤은 의존성이다

**이전 섹션과의 관계**: 테스트 냄새의 두 번째 범주(대상 코드의 문제)에 대한 첫 번째 구체적 사례다.

**Lines 37-101**: 전역으로 접근 가능한 싱글톤은 숨겨진 의존성이며 테스트를 어렵게 만든다. `new Date()`는 내부적으로 `System.currentTimeMillis()`를 호출하는데, 이를 테스트하려면 하루를 기다리거나 복잡한 기법이 필요하다.

**Java 원본 코드** (Lines 47-51):
```java
@Test public void rejectsRequestsNotWithinTheSameDay() {
  receiver.acceptRequest(FIRST_REQUEST);
  // the next day
  assertFalse("too late now", receiver.acceptRequest(SECOND_REQUEST));
}
```

**Python 버전**:
```python
def test_rejects_requests_not_within_the_same_day():
    """다른 날짜의 요청을 거부해야 한다"""
    receiver.accept_request(FIRST_REQUEST)
    # 다음 날
    assert not receiver.accept_request(SECOND_REQUEST), "too late now"
```

**Java 원본 코드 - 문제가 있는 구현** (Lines 53-62):
```java
public boolean acceptRequest(Request request) {
  final Date now = new Date();  // 싱글톤 System에 암시적으로 의존
  if (dateOfFirstRequest == null) {
    dateOfFirstRequest = now;
  } else if (firstDateIsDifferentFrom(now)) {
    return false;
  }
  // process the request
  return true;
}
```

**Python 버전**:
```python
def accept_request(request):
    """요청을 처리한다 (문제가 있는 버전)"""
    now = datetime.now()  # datetime 모듈에 암시적으로 의존
    if self.date_of_first_request is None:
        self.date_of_first_request = now
    elif self.first_date_is_different_from(now):
        return False
    # 요청 처리
    return True
```

**해결책 - Clock 주입** (Lines 71-77):
```java
@Test public void rejectsRequestsNotWithinTheSameDay() {
  Receiver receiver = new Receiver(stubClock);  // Clock을 주입
  stubClock.setNextDate(TODAY);
  receiver.acceptRequest(FIRST_REQUEST);
  stubClock.setNextDate(TOMORROW);
  assertFalse("too late now", receiver.acceptRequest(SECOND_REQUEST));
}
```

**Python 버전**:
```python
def test_rejects_requests_not_within_the_same_day():
    """Clock 주입으로 테스트 가능하게 만든다"""
    stub_clock = StubClock()
    receiver = Receiver(stub_clock)  # Clock을 주입
    stub_clock.set_next_date(TODAY)
    receiver.accept_request(FIRST_REQUEST)
    stub_clock.set_next_date(TOMORROW)
    assert not receiver.accept_request(SECOND_REQUEST), "too late now"
```

**개선된 구현** (Lines 84-93):
```java
public boolean acceptRequest(Request request) {
  final Date now = clock.now();  // 명시적인 Clock 의존성
  if (dateOfFirstRequest == null) {
    dateOfFirstRequest = now;
  } else if (firstDateIsDifferentFrom(now)) {
    return false;
  }
  // process the request
  return true;
}
```

**Python 버전**:
```python
def accept_request(request):
    """요청을 처리한다 (개선된 버전)"""
    now = self.clock.now()  # 명시적인 Clock 의존성
    if self.date_of_first_request is None:
        self.date_of_first_request = now
    elif self.first_date_is_different_from(now):
        return False
    # 요청 처리
    return True
```

**핵심 개념 참조**: 3. 싱글톤과 의존성

---

### 3.2 절차에서 객체로

**이전 섹션과의 관계**: Clock을 도입하여 의존성을 명시적으로 만든 후, 더 나은 추상화를 발견하는 과정이다.

**Lines 102-159**: Clock을 도입한 후, 날짜 검사 로직을 Clock으로 이동하거나 도메인 개념(`SameDayChecker`)을 발견할 수 있다. Receiver는 날짜 조작의 세부 사항을 알 필요가 없고, 날짜가 변경되었는지만 알면 된다.

**개선된 테스트 - Clock.dayHasChangedFrom 사용** (Lines 112-120):
```java
@Test public void rejectsRequestsNotWithinTheSameDay() {
  Receiver receiver = new Receiver(clock);
  context.checking(new Expectations() {{
    allowing(clock).now(); will(returnValue(NOW));
    one(clock).dayHasChangedFrom(NOW); will(returnValue(false));
  }});
  receiver.acceptRequest(FIRST_REQUEST);
  assertFalse("too late now", receiver.acceptRequest(SECOND_REQUEST));
}
```

**Python 버전 (pytest + pytest-mock)**:
```python
def test_rejects_requests_not_within_the_same_day(mocker):
    """Clock의 dayHasChangedFrom 메서드를 사용"""
    clock = mocker.Mock()
    clock.now.return_value = NOW
    clock.day_has_changed_from.return_value = False

    receiver = Receiver(clock)
    receiver.accept_request(FIRST_REQUEST)

    assert not receiver.accept_request(SECOND_REQUEST), "too late now"
    clock.day_has_changed_from.assert_called_once_with(NOW)
```

**개선된 구현** (Lines 126-134):
```java
public boolean acceptRequest(Request request) {
  if (dateOfFirstRequest == null) {
    dateOfFirstRequest = clock.now();
  } else if (clock.dayHasChangedFrom(dateOfFirstRequest)) {
    return false;
  }
  // process the request
  return true;
}
```

**Python 버전**:
```python
def accept_request(request):
    """Clock의 dayHasChangedFrom을 사용하는 버전"""
    if self.date_of_first_request is None:
        self.date_of_first_request = self.clock.now()
    elif self.clock.day_has_changed_from(self.date_of_first_request):
        return False
    # 요청 처리
    return True
```

**최종 개선 - SameDayChecker 도입** (Lines 142-156):
```java
@Test public void rejectsRequestsOutsideAllowedPeriod() {
  Receiver receiver = new Receiver(sameDayChecker);
  context.checking(new Expectations() {{
    allowing(sameDayChecker).hasExpired(); will(returnValue(false));
  }});
  assertFalse("too late now", receiver.acceptRequest(REQUEST));
}
```

**Python 버전**:
```python
def test_rejects_requests_outside_allowed_period(mocker):
    """SameDayChecker를 사용하여 더 명확한 도메인 개념으로"""
    same_day_checker = mocker.Mock()
    same_day_checker.has_expired.return_value = False

    receiver = Receiver(same_day_checker)
    assert not receiver.accept_request(REQUEST), "too late now"
```

**최종 구현** (Lines 150-156):
```java
public boolean acceptRequest(Request request) {
  if (sameDayChecker.hasExpired()) {
    return false;
  }
  // process the request
  return true;
}
```

**Python 버전**:
```python
def accept_request(request):
    """SameDayChecker를 사용하는 최종 버전"""
    if self.same_day_checker.has_expired():
        return False
    # 요청 처리
    return True
```

**핵심 개념 참조**: 4. 절차에서 객체로의 전환

---

### 3.3 암시적 의존성도 여전히 의존성이다

**이전 섹션과의 관계**: 의존성을 명시적으로 만드는 것의 중요성을 강조한다.

**Lines 160-180**: 전역 값을 통해 의존성을 숨기면 의존성이 사라지는 것이 아니라 접근 불가능해질 뿐이다. 예를 들어, Microsoft .Net 라이브러리가 ActiveDirectory 없이는 로드되지 않아 사용할 수 없었던 사례가 있다. 객체 지향의 목표는 객체의 경계를 명확히 하는 것이며, 로컬이거나 명시적으로 전달된 값/인스턴스만 다뤄야 한다.

> We can hide a dependency from the caller of a component by using a global value to bypass encapsulation, but that doesn't make the dependency go away—it just makes it inaccessible. (Lines 161-162)

**핵심 개념 참조**: 5. 암시적 의존성

---

### 3.4 프로덕션 코드와 같은 기법 사용

**이전 섹션과의 관계**: 암시적 의존성의 문제를 피하기 위한 실천 방법을 제시한다.

**Lines 181-195**: 클래스 로더나 바이트코드 조작으로 의존성을 끊는 고급 테스팅 도구는 설계 피드백을 낭비한다. 나중에 긴급한 기능을 추가할 때 설계 약점이 시스템 전체에 영향을 미쳐 변경이 어려워진다. 더러운 냄비처럼, 기름이 굳기 전에 닦는 것이 쉽다.

> Unit-testing tools that let the programmer sidestep poor dependency management in the design waste a valuable source of feedback. (Lines 189-191)

**핵심 개념 참조**: 6. 프로덕션 코드와 같은 기법 사용

---

### 4.1 로깅은 기능이다

**이전 섹션과의 관계**: 교체하기 어려운 객체(싱글톤)의 또 다른 사례로 로깅을 다룬다.

**Lines 196-227**: 로깅은 두 가지 별개의 기능이다. Support logging(error, info)은 운영/지원팀이 사용하는 애플리케이션의 사용자 인터페이스이며 테스트 주도로 개발해야 한다. Diagnostic logging(debug, trace)은 프로그래머를 위한 인프라이며 프로덕션에서는 켜지 않아야 한다.

**로깅 예시** (Lines 199-200):
```java
log.error("Lost touch with Reality after " + timeout + "seconds");
log.trace("Distance traveled in the wilderness: " + distance);
```

**Python 버전**:
```python
# Support logging - 운영팀용, 테스트 필요
log.error(f"Lost touch with Reality after {timeout} seconds")

# Diagnostic logging - 개발자용, 테스트 불필요
log.trace(f"Distance traveled in the wilderness: {distance}")
```

**핵심 개념 참조**: 7. 로깅은 기능이다

---

### 4.2 로깅 대신 알림

**이전 섹션과의 관계**: 로깅의 두 가지 유형을 구분한 후, Support logging을 어떻게 테스트 가능하게 만들 것인가에 대한 해결책을 제시한다.

**Lines 228-265**: 정적 전역 로거 객체에 대한 단위 테스트는 번거롭다. 코드가 두 가지 수준(도메인과 로깅 인프라)에서 작동하며 단일 책임 원칙을 위반한다.

**문제가 있는 로깅 코드** (Lines 235-243):
```java
Location location = tracker.getCurrentLocation();
for (Filter filter : filters) {
  filter.selectFor(location);
  if (logger.isInfoEnabled()) {
    logger.info("Filter " + filter.getName() + ", " + filter.getDate()
                + " selected for " + location.getName()
                + ", is current: " + tracker.isCurrent(location));
  }
}
```

**Python 버전**:
```python
# 문제가 있는 버전 - 도메인 로직과 로깅이 섞여 있음
location = tracker.get_current_location()
for filter in filters:
    filter.select_for(location)
    if logger.is_info_enabled():
        logger.info(f"Filter {filter.get_name()}, {filter.get_date()}"
                   f" selected for {location.get_name()}"
                   f", is current: {tracker.is_current(location)}")
```

**개선된 코드 - Support 객체 사용** (Lines 248-251):
```java
Location location = tracker.getCurrentLocation();
for (Filter filter : filters) {
  filter.selectFor(location);
  support.notifyFiltering(tracker, location, filter);  // 알림 객체 사용
}
```

**Python 버전**:
```python
# 개선된 버전 - 알림 객체로 분리
location = tracker.get_current_location()
for filter in filters:
    filter.select_for(location)
    support.notify_filtering(tracker, location, filter)  # 알림 객체 사용
```

**핵심 개념 참조**: 8. 알림 패턴

---

### 4.3 과도한 설계처럼 보이는가

**이전 섹션과의 관계**: Support 객체 패턴이 과도한 설계처럼 보일 수 있지만, 실제로는 많은 이점이 있음을 설명한다.

**Lines 266-298**: Support reporting을 캡슐화하면 의도(지원팀 돕기)를 구현(로깅)보다 명확히 표현할 수 있다. 일관성 있는 리포팅, 도메인 관점의 구조화, 예외 처리 개선 등의 이점이 있다. 한 시스템에서는 로그가 너무 많아 일주일 후 삭제되어 유용한 정보가 없었던 사례도 있다.

> If they'd logged nothing at all, the system would have run faster with no loss of useful information. (Lines 297-298)

**핵심 개념 참조**: 8. 알림 패턴

---

### 5.1 구체 클래스 모킹

**이전 섹션과의 관계**: 교체하기 어려운 객체의 또 다른 접근 방법인 구체 클래스 모킹의 문제를 다룬다.

**Lines 299-353**: 구체 클래스를 상속하여 메서드를 오버라이드하는 방식은 최후의 수단으로만 사용해야 한다. 이 방식은 객체 간 관계를 암시적으로 남겨둔다.

**구체 클래스 모킹 예시** (Lines 314-327):
```java
public class MusicCentreTest {
  @Test public void startsCdPlayerAtTimeRequested() {
    final MutableTime scheduledTime = new MutableTime();
    CdPlayer player = new CdPlayer() {
      @Override public void scheduleToStartAt(Time startTime) {
        scheduledTime.set(startTime);  // 오버라이드로 검증
      }
    }
    MusicCentre centre = new MusicCentre(player);
    centre.startMediaAt(LATER);
    assertEquals(LATER, scheduledTime.get());
  }
}
```

**Python 버전**:
```python
class MusicCentreTest:
    def test_starts_cd_player_at_time_requested(self):
        """구체 클래스를 상속하여 모킹 (권장하지 않음)"""
        scheduled_time = MutableTime()

        class MockCdPlayer(CdPlayer):
            def schedule_to_start_at(self, start_time):
                scheduled_time.set(start_time)  # 오버라이드로 검증

        player = MockCdPlayer()
        centre = MusicCentre(player)
        centre.start_media_at(LATER)
        assert scheduled_time.get() == LATER
```

**CdPlayer 구현** (Lines 336-342):
```java
public class CdPlayer {
  public void scheduleToStartAt(Time startTime) { […] }
  public void stop() { […] }
  public void gotoTrack(int trackNumber) { […] }
  public void spinUpDisk() { […] }
  public void eject() { […] }
}
```

**Python 버전**:
```python
class CdPlayer:
    """여러 메서드가 있는 CdPlayer - 일부만 사용됨"""
    def schedule_to_start_at(self, start_time):
        ...  # MusicCentre가 사용

    def stop(self):
        ...  # MusicCentre가 사용

    def goto_track(self, track_number):
        ...  # 다른 곳에서 사용

    def spin_up_disk(self):
        ...  # 다른 곳에서 사용

    def eject(self):
        ...  # 다른 곳에서 사용
```

MusicCentre는 시작/중지 메서드만 사용하므로 `ScheduledDevice` 인터페이스로 추출하는 것이 좋다. Robert Martin의 Interface Segregation Principle: "클라이언트는 사용하지 않는 인터페이스에 의존하지 않아야 한다."

**더 중요한 이유** (Lines 355-360): 인터페이스를 추출하면 관계에 이름(`ScheduledDevice`)을 붙이게 되고, 이는 도메인에 대한 사고를 깊게 한다. 이름이 있으면 그것에 대해 이야기할 수 있다.

**핵심 개념 참조**: 9. 구체 클래스 모킹의 문제

---

### 5.2 비상시에만 사용

**이전 섹션과의 관계**: 구체 클래스 모킹의 문제를 설명한 후, 불가피한 상황을 인정한다.

**Lines 361-376**: 레거시 코드나 변경할 수 없는 서드파티 라이브러리를 다룰 때는 구체 클래스 모킹을 사용할 수 있다. 외부 라이브러리 위에 veneer를 작성하는 것이 거의 항상 더 좋지만, 때로는 그만한 가치가 없을 수도 있다. 내부 기능을 오버라이드하지 말고 가시적인 메서드만 오버라이드해야 한다.

> Above all, do not override a class' internal features—this just locks down your test to the quirks of the current implementation. Only override visible methods. (Lines 372-373)

**핵심 개념 참조**: 9. 구체 클래스 모킹의 문제

---

### 6.1 값 객체는 모킹하지 않는다

**이전 섹션과의 관계**: 모킹해서는 안 되는 또 다른 경우를 설명한다.

**Lines 377-408**: 값 객체(불변이어야 함)는 모킹할 필요가 없고 단순히 인스턴스를 생성해서 사용하면 된다.

**값 객체를 모킹하는 나쁜 예** (Lines 381-392):
```java
@Test public void sumsTotalRunningTime() {
  Show show = new Show();
  Video video1 = context.mock(Video.class); // 이렇게 하지 말 것
  Video video2 = context.mock(Video.class);
  context.checking(new Expectations(){{
    one(video1).time(); will(returnValue(40));
    one(video2).time(); will(returnValue(23));
  }});
  show.add(video1);
  show.add(video2);
  assertEqual(63, show.runningTime())
}
```

**Python 버전 (나쁜 예)**:
```python
def test_sums_total_running_time(mocker):
    """값 객체를 모킹하는 나쁜 예"""
    show = Show()
    video1 = mocker.Mock(spec=Video)  # 이렇게 하지 말 것
    video2 = mocker.Mock(spec=Video)
    video1.time.return_value = 40
    video2.time.return_value = 23

    show.add(video1)
    show.add(video2)
    assert show.running_time() == 63
```

**좋은 예 - 실제 인스턴스 사용**:
```python
def test_sums_total_running_time():
    """값 객체는 실제 인스턴스를 사용"""
    show = Show()
    video1 = Video(time=40)  # 실제 인스턴스 생성
    video2 = Video(time=23)

    show.add(video1)
    show.add(video2)
    assert show.running_time() == 63
```

**휴리스틱**:
1. 값이 불변이다
2. 인터페이스에 의미 있는 이름을 붙이기 어렵다 (VideoImpl 같은 모호한 이름만 가능)

**핵심 개념 참조**: 10. 값 객체는 모킹하지 않는다

---

### 7.1 비대한 생성자

**이전 섹션과의 관계**: 테스트 작성 과정에서 발생하는 구조적 문제를 다룬다.

**Lines 409-505**: TDD 과정에서 의존성을 하나씩 추가하다 보면 생성자 인자가 많아질 수 있다. 함께 사용되는 인자들을 묶어 새로운 개념으로 추출한다.

**비대한 생성자 예시** (Lines 420-440):
```java
public class MessageProcessor {
  public MessageProcessor(MessageUnpacker unpacker,
                          AuditTrail auditor,
                          CounterPartyFinder counterpartyFinder,
                          LocationFinder locationFinder,
                          DomesticNotifier domesticNotifier,
                          ImportedNotifier importedNotifier)
  {
    // set the fields here
  }
  public void onMessage(Message rawMessage) {
    UnpackedMessage unpacked = unpacker.unpack(rawMessage, counterpartyFinder);
    auditor.recordReceiptOf(unpacked);
    // some other activity here
    if (locationFinder.isDomestic(unpacked)) {
      domesticNotifier.notify(unpacked.asDomesticMessage());
    } else {
      importedNotifier.notify(unpacked.asImportedMessage())
    }
  }
}
```

**Python 버전**:
```python
class MessageProcessor:
    """비대한 생성자 예시"""
    def __init__(self,
                 unpacker: MessageUnpacker,
                 auditor: AuditTrail,
                 counterparty_finder: CounterPartyFinder,
                 location_finder: LocationFinder,
                 domestic_notifier: DomesticNotifier,
                 imported_notifier: ImportedNotifier):
        self.unpacker = unpacker
        self.auditor = auditor
        self.counterparty_finder = counterparty_finder
        self.location_finder = location_finder
        self.domestic_notifier = domestic_notifier
        self.imported_notifier = imported_notifier

    def on_message(self, raw_message: Message):
        unpacked = self.unpacker.unpack(raw_message, self.counterparty_finder)
        self.auditor.record_receipt_of(unpacked)
        # 기타 활동
        if self.location_finder.is_domestic(unpacked):
            self.domestic_notifier.notify(unpacked.as_domestic_message())
        else:
            self.imported_notifier.notify(unpacked.as_imported_message())
```

**첫 번째 개선 - counterpartyFinder를 unpacker로 이동** (Lines 451-460):
```java
public class MessageProcessor {
  public MessageProcessor(MessageUnpacker unpacker,
                          AuditTrail auditor,
                          LocationFinder locationFinder,
                          DomesticNotifier domesticNotifier,
                          ImportedNotifier importedNotifier) { […] }
  public void onMessage(Message rawMessage) {
    UnpackedMessage unpacked = unpacker.unpack(rawMessage);  // counterpartyFinder 제거
    // etc.
  }
}
```

**Python 버전**:
```python
class MessageProcessor:
    """첫 번째 개선"""
    def __init__(self,
                 unpacker: MessageUnpacker,
                 auditor: AuditTrail,
                 location_finder: LocationFinder,
                 domestic_notifier: DomesticNotifier,
                 imported_notifier: ImportedNotifier):
        self.unpacker = unpacker  # counterparty_finder는 unpacker 내부로
        self.auditor = auditor
        self.location_finder = location_finder
        self.domestic_notifier = domestic_notifier
        self.imported_notifier = imported_notifier

    def on_message(self, raw_message: Message):
        unpacked = self.unpacker.unpack(raw_message)  # 인자 하나 줄어듦
        # ...
```

**최종 개선 - MessageDispatcher 도입** (Lines 463-473):
```java
public class MessageProcessor {
  public MessageProcessor(MessageUnpacker unpacker,
                          AuditTrail auditor,
                          MessageDispatcher dispatcher) { […] }
  public void onMessage(Message rawMessage) {
    UnpackedMessage unpacked = unpacker.unpack(rawMessage);
    auditor.recordReceiptOf(unpacked);
    // some other activity here
    dispatcher.dispatch(unpacked);  // 라우팅 로직 분리
  }
}
```

**Python 버전**:
```python
class MessageProcessor:
    """최종 개선 - MessageDispatcher로 라우팅 분리"""
    def __init__(self,
                 unpacker: MessageUnpacker,
                 auditor: AuditTrail,
                 dispatcher: MessageDispatcher):
        self.unpacker = unpacker
        self.auditor = auditor
        self.dispatcher = dispatcher  # 세 개의 인자만!

    def on_message(self, raw_message: Message):
        """수신, 처리, 전달의 세 단계가 명확"""
        unpacked = self.unpacker.unpack(raw_message)
        self.auditor.record_receipt_of(unpacked)
        # 기타 활동
        self.dispatcher.dispatch(unpacked)  # 라우팅 로직 분리
```

**객체 생성 코드 변경** (Lines 492-505):

변경 전:
```java
messageProcessor =
  new MessageProcessor(new XmlMessageUnpacker(),
                       auditor, counterpartyFinder,
                       locationFinder, domesticNotifier,
                       importedNotifier);
```

변경 후:
```java
messageProcessor =
  new MessageProcessor(new XmlMessageUnpacker(counterpartyFinder),
                       auditor,
                       new MessageDispatcher(
                         locationFinder,
                         domesticNotifier, importedNotifier));
```

**Python 버전**:
```python
# 변경 전
message_processor = MessageProcessor(
    XmlMessageUnpacker(),
    auditor,
    counterparty_finder,
    location_finder,
    domestic_notifier,
    imported_notifier
)

# 변경 후
message_processor = MessageProcessor(
    XmlMessageUnpacker(counterparty_finder),
    auditor,
    MessageDispatcher(location_finder, domestic_notifier, imported_notifier)
)
```

**핵심 개념 참조**: 11. 비대한 생성자

---

### 7.2 혼란스러운 객체

**이전 섹션과의 관계**: 비대한 생성자의 또 다른 원인을 설명한다.

**Lines 506-552**: 객체가 너무 많은 관련 없는 책임을 가지면 많은 의존성이 필요하다. 휴대폰처럼 관련 없는 기능들이 서로 간섭한다.

**혼란스러운 객체 예시** (Lines 509-535):
```java
public class Handset {
  public Handset(Network network, Camera camera, Display display,
                DataNetwork dataNetwork, AddressBook addressBook,
                Storage storage, Tuner tuner, …)
  {
    // set the fields here
  }
  public void placeCallTo(DirectoryNumber number) {
    network.openVoiceCallTo(number);
  }
  public void takePicture() {
    Frame frame = storage.allocateNewFrame();
    camera.takePictureInto(frame);
    display.showPicture(frame);
  }
  public void showWebPage(URL url) {
    display.renderHtml(dataNetwork.retrievePage(url));
  }
  public void showAddress(SearchTerm searchTerm) {
    display.showAddress(addressBook.findAddress(searchTerm));
  }
  public void playRadio(Frequency frequency) {
    tuner.tuneTo(frequency);
    tuner.play();
  }
  // and so on
}
```

**Python 버전**:
```python
class Handset:
    """여러 관련 없는 책임을 가진 혼란스러운 클래스"""
    def __init__(self,
                 network: Network,
                 camera: Camera,
                 display: Display,
                 data_network: DataNetwork,
                 address_book: AddressBook,
                 storage: Storage,
                 tuner: Tuner,
                 ...):
        self.network = network
        self.camera = camera
        self.display = display
        self.data_network = data_network
        self.address_book = address_book
        self.storage = storage
        self.tuner = tuner

    def place_call_to(self, number: DirectoryNumber):
        """전화 기능"""
        self.network.open_voice_call_to(number)

    def take_picture(self):
        """카메라 기능"""
        frame = self.storage.allocate_new_frame()
        self.camera.take_picture_into(frame)
        self.display.show_picture(frame)

    def show_web_page(self, url: URL):
        """웹 브라우저 기능"""
        self.display.render_html(self.data_network.retrieve_page(url))

    def show_address(self, search_term: SearchTerm):
        """주소록 기능"""
        self.display.show_address(self.address_book.find_address(search_term))

    def play_radio(self, frequency: Frequency):
        """라디오 기능"""
        self.tuner.tune_to(frequency)
        self.tuner.play()
```

이 클래스는 분리되어야 한다. 테스트 스위트도 혼란스러울 것이며, 각 기능의 테스트가 서로 관계가 없을 것이다.

**핵심 개념 참조**: 12. 혼란스러운 객체

---

### 7.3 너무 많은 의존성

**이전 섹션과의 관계**: 비대한 생성자의 세 번째 원인을 설명한다.

**Lines 553-617**: 모든 인자가 의존성(dependencies)인 것은 아니다. 알림(notifications)과 조정(adjustments)은 기본값으로 설정하고 나중에 재설정할 수 있다.

**RacingCar 예시** (Lines 565-587):
```java
public class RacingCar {
  private final Track track;
  private Tyres tyres;
  private Suspension suspension;
  private Wing frontWing;
  private Wing backWing;
  private double fuelLoad;
  private CarListener listener;
  private DrivingStrategy driver;
  public RacingCar(Track track, DrivingStrategy driver, Tyres tyres,
                  Suspension suspension, Wing frontWing, Wing backWing,
                  double fuelLoad, CarListener listener)
  {
    this.track = track;
    this.driver = driver;
    this.tyres = tyres;
    this.suspension = suspension;
    this.frontWing = frontWing;
    this.backWing = backWing;
    this.fuelLoad = fuelLoad;
    this.listener = listener;
  }
}
```

**Python 버전**:
```python
class RacingCar:
    """레이싱 게임의 자동차 (개선 전)"""
    def __init__(self,
                 track: Track,
                 driver: DrivingStrategy,
                 tyres: Tyres,
                 suspension: Suspension,
                 front_wing: Wing,
                 back_wing: Wing,
                 fuel_load: float,
                 listener: CarListener):
        self.track = track  # 유일한 의존성 (final)
        self.driver = driver
        self.tyres = tyres
        self.suspension = suspension
        self.front_wing = front_wing
        self.back_wing = back_wing
        self.fuel_load = fuel_load
        self.listener = listener
```

track만 의존성(final)이고 나머지는 조정 가능한 값들이다.

**개선된 버전** (Lines 597-613):
```java
public class RacingCar {
  private final Track track;
  private DrivingStrategy driver = DriverTypes.borderlineAggressiveDriving();
  private Tyres tyres = TyreTypes.mediumSlicks();
  private Suspension suspension = SuspensionTypes.mediumStiffness();
  private Wing frontWing = WingTypes.mediumDownforce();
  private Wing backWing = WingTypes.mediumDownforce();
  private double fuelLoad = 0.5;
  private CarListener listener = CarListener.NONE;
  public RacingCar(Track track) {
    this.track = track;
  }
  public void setSuspension(Suspension suspension) { […] }
  public void setTyres(Tyres tyres) { […] }
  public void setEngine(Engine engine) { […] }
  public void setListener(CarListener listener) { […] }
}
```

**Python 버전**:
```python
class RacingCar:
    """개선된 버전 - 기본값 사용"""
    def __init__(self, track: Track):
        self.track = track  # 유일한 의존성
        # 나머지는 기본값으로 초기화 (조정 가능)
        self.driver = DriverTypes.borderline_aggressive_driving()
        self.tyres = TyreTypes.medium_slicks()
        self.suspension = SuspensionTypes.medium_stiffness()
        self.front_wing = WingTypes.medium_downforce()
        self.back_wing = WingTypes.medium_downforce()
        self.fuel_load = 0.5
        self.listener = CarListener.NONE  # Null Object 패턴

    def set_suspension(self, suspension: Suspension):
        self.suspension = suspension

    def set_tyres(self, tyres: Tyres):
        self.tyres = tyres

    def set_engine(self, engine: Engine):
        self.engine = engine

    def set_listener(self, listener: CarListener):
        self.listener = listener
```

**핵심 개념 참조**: 13. 의존성과 조정 구분

---

### 8.1 너무 많은 기대값

**이전 섹션과의 관계**: 테스트 자체의 복잡성 문제를 다룬다.

**Lines 618-680**: 테스트에 기대값이 너무 많으면 무엇이 중요한지 알 수 없다. 부작용이 있는 메서드만 기대값으로 만들고, 쿼리는 스텁으로 만들어야 한다.

**너무 많은 기대값 예시** (Lines 621-630):
```java
@Test public void decidesCasesWhenFirstPartyIsReady() {
  context.checking(new Expectations(){{
    one(firstPart).isReady(); will(returnValue(true));
    one(organizer).getAdjudicator(); will(returnValue(adjudicator));
    one(adjudicator).findCase(firstParty, issue); will(returnValue(case));
    one(thirdParty).proceedWith(case);
  }});
  claimsProcessor.adjudicateIfReady(thirdParty, issue);
}
```

**Python 버전 (나쁜 예)**:
```python
def test_decides_cases_when_first_party_is_ready(mocker):
    """모든 것이 기대값인 나쁜 예"""
    first_party = mocker.Mock()
    organizer = mocker.Mock()
    adjudicator = mocker.Mock()
    third_party = mocker.Mock()

    first_party.is_ready.return_value = True
    organizer.get_adjudicator.return_value = adjudicator
    adjudicator.find_case.return_value = case

    claims_processor.adjudicate_if_ready(third_party, issue)

    # 모든 메서드 호출을 검증 (너무 많음)
    first_party.is_ready.assert_called_once()
    organizer.get_adjudicator.assert_called_once()
    adjudicator.find_case.assert_called_once_with(first_party, issue)
    third_party.proceed_with.assert_called_once_with(case)
```

**구현** (Lines 637-645):
```java
public void adjudicateIfReady(ThirdParty thirdParty, Issue issue) {
  if (firstParty.isReady()) {
    Adjudicator adjudicator = organization.getAdjudicator();
    Case case = adjudicator.findCase(firstParty, issue);
    thirdParty.proceedWith(case);  // 부작용!
  } else{
    thirdParty.adjourn();  // 부작용!
  }
}
```

**Python 버전**:
```python
def adjudicate_if_ready(self, third_party: ThirdParty, issue: Issue):
    """구현 코드"""
    if self.first_party.is_ready():
        adjudicator = self.organization.get_adjudicator()
        case = adjudicator.find_case(self.first_party, issue)
        third_party.proceed_with(case)  # 부작용 있음!
    else:
        third_party.adjourn()  # 부작용 있음!
```

부작용이 있는 메서드는 `proceedWith()`와 `adjourn()` 뿐이다. 나머지는 쿼리이므로 스텁으로 만든다.

**개선된 테스트** (Lines 660-668):
```java
@Test public void decidesCasesWhenFirstPartyIsReady() {
  context.checking(new Expectations(){{
    allowing(firstPart).isReady(); will(returnValue(true));  // 스텁
    allowing(organizer).getAdjudicator(); will(returnValue(adjudicator));  // 스텁
    allowing(adjudicator).findCase(firstParty, issue); will(returnValue(case));  // 스텁
    one(thirdParty).proceedWith(case);  // 기대값
  }});
  claimsProcessor.adjudicateIfReady(thirdParty, issue);
}
```

**Python 버전 (좋은 예)**:
```python
def test_decides_cases_when_first_party_is_ready(mocker):
    """스텁과 기대값을 구분한 좋은 예"""
    first_party = mocker.Mock()
    organizer = mocker.Mock()
    adjudicator = mocker.Mock()
    third_party = mocker.Mock()

    # 스텁 - 테스트를 통과시키기 위한 시뮬레이션
    first_party.is_ready.return_value = True
    organizer.get_adjudicator.return_value = adjudicator
    adjudicator.find_case.return_value = case

    claims_processor.adjudicate_if_ready(third_party, issue)

    # 기대값 - 부작용이 있는 메서드만 검증
    third_party.proceed_with.assert_called_once_with(case)
```

**핵심 개념 참조**: 14. 너무 많은 기대값

---

### 8.2 적은 기대값 작성

**이전 섹션과의 관계**: 기대값과 스텁을 구분한 후, 일반적인 원칙을 제시한다.

**Lines 671-678**: 단위 테스트에서 기대값을 적게 작성해야 한다. 기대값이 많다면 너무 큰 단위를 테스트하거나 객체의 상호작용을 과도하게 고정하고 있는 것이다.

> Just like "everyone" has now learned to avoid too many assertions in a test, we try to avoid too many expectations. (Lines 673-675)

**핵심 개념 참조**: 14. 너무 많은 기대값

---

### 8.3 특별 보너스

**이전 섹션과의 관계**: 기대값 테스트를 더 개선할 수 있는 방법을 제시한다.

**Lines 681-703**: 객체 체인을 끌어내는 대신 가장 가까운 객체에게 작업을 시켜야 한다.

**개선 옵션 1** (Lines 687-693):
```java
public void adjudicateIfReady(ThirdParty thirdParty, Issue issue) {
  if (firstParty.isReady()) {
    organization.adjudicateBetween(firstParty, thirdParty, issue);  // Tell, Don't Ask
  } else {
    thirdParty.adjourn();
  }
}
```

**Python 버전**:
```python
def adjudicate_if_ready(self, third_party: ThirdParty, issue: Issue):
    """개선 1 - organization에게 위임"""
    if self.first_party.is_ready():
        self.organization.adjudicate_between(self.first_party, third_party, issue)
    else:
        third_party.adjourn()
```

**개선 옵션 2** (Lines 695-701):
```java
public void adjudicateIfReady(ThirdParty thirdParty, Issue issue) {
  if (firstParty.isReady()) {
    thirdParty.startAdjudication(organization, firstParty, issue);  // 더 균형잡힌 방식
  } else{
    thirdParty.adjourn();
  }
}
```

**Python 버전**:
```python
def adjudicate_if_ready(self, third_party: ThirdParty, issue: Issue):
    """개선 2 - third_party에게 위임 (더 균형잡힘)"""
    if self.first_party.is_ready():
        third_party.start_adjudication(self.organization, self.first_party, issue)
    else:
        third_party.adjourn()
```

**핵심 개념 참조**: 14. 너무 많은 기대값

---

### 9.1 테스트가 알려주는 것들

**이전 섹션과의 관계**: 챕터 전체의 교훈을 정리한다.

**Lines 704-773**: 테스트 냄새를 듣는 법을 배우면 다음과 같은 이점을 얻는다:

1. **지식의 지역성 유지** (Lines 707-712): 지식을 객체 내부나 전달된 인자로 유지하면 컴포넌트가 컨텍스트에 독립적이고 어디든 이동 가능하다. 플러그 가능한 컴포넌트로 애플리케이션을 구축하면 변경이 쉽다.

2. **명시적이면 이름을 붙일 수 있다** (Lines 713-718): 구체 클래스를 모킹하지 않는 이유는 객체뿐만 아니라 객체 간 관계에도 이름을 붙이고 싶기 때문이다. 진정한 이름을 알면 통제할 수 있다.

3. **더 많은 이름은 더 많은 도메인 정보를 의미** (Lines 724-730): 객체의 통신 방식을 강조하면 구현보다 도메인 관점에서 정의된 타입과 역할을 얻게 된다. 더 많은 도메인 어휘가 코드에 들어간다.

4. **데이터보다 행동을 전달** (Lines 731-739): "Tell, Don't Ask"를 일관되게 적용하면 값을 끌어올리는 대신 행동(콜백)을 전달하는 코딩 스타일이 된다. 더 정확한 인터페이스는 더 나은 정보 은닉과 명확한 추상화를 제공한다.

**1000줄 테스트 문제** (Lines 746-761): 한 사용자가 jMock을 사용했지만 테스트가 읽을 수 없고, 500줄 이상이며, 리팩토링 시 대규모 변경이 필요했다고 보고했다. 단위 테스트는 1000줄이 되어서는 안 된다! 큰 fixture나 많은 준비 작업이 필요하다면 테스트가 이해하기 어렵고 취약하다.

> A unit test shouldn't be 1000 lines long! It should focus on at most a few classes and should not need to create a large fixture or perform lots of preparation just to get the objects into a state where the target feature can be exercised. (Lines 756-759)

**TDD의 엄격함** (Lines 762-773): TDD는 용서가 없다. 품질이 낮은 테스트는 개발을 느리게 만들고, 시스템의 내부 품질이 낮으면 품질이 낮은 테스트가 나온다. 테스트를 작성하면서 얻는 내부 품질 피드백에 민감하면 문제를 초기에 해결할 수 있다. 읽기 쉽고 유연한 테스트를 작성하려는 노력은 테스트 대상 코드의 내부 품질에 대한 더 많은 피드백을 제공한다.

> By being alert to the internal quality feedback we get from writing tests, we can nip this problem in the bud, long before our unit tests approach 1000 lines of code, and end up with tests we can live with. (Lines 764-767)

**핵심 개념 참조**: 15. 테스트가 알려주는 것들

# Growing_object_oriented_software_guided_by_tests_Chapter_21_Test_Readability

## 압축 내용
테스트 코드는 프로덕션 코드의 동작을 검증할 뿐만 아니라 그 동작을 명확하게 표현해야 하며, 이를 위해 의미 있는 테스트 이름, 표준화된 구조, 간결한 코드, 명확한 단언문을 사용해야 한다.

## 핵심 내용

### 핵심 개념 목록
1. **테스트 가독성의 중요성** - TDD의 지속 가능성을 위한 필수 요소 (→ [상세: 테스트 가독성과 유지보수성](#1-테스트-가독성과-유지보수성))
2. **테스트와 프로덕션 코드의 차이** - 구체성과 추상성의 상반된 접근 (→ [상세: 테스트 코드의 특성](#2-테스트-코드의-특성))
3. **일반적인 테스트 문제점** - 5가지 주요 가독성 문제 (→ [상세: 테스트 스멜](#3-테스트-스멜test-smells))
4. **TestDox 명명 규칙** - 기능 중심의 서술형 테스트 이름 (→ [상세: TestDox 명명 규칙](#4-testdox-명명-규칙))
5. **정규 테스트 구조** - Setup-Execute-Verify-Teardown 패턴 (→ [상세: 정규 테스트 구조](#5-정규-테스트-구조))
6. **테스트 코드 간소화** - 노이즈 제거와 의도 강조 (→ [상세: 테스트 코드 간소화 기법](#6-테스트-코드-간소화-기법))
7. **명확한 단언문** - 정확하고 좁게 정의된 검증 (→ [상세: 단언문과 기대값 작성](#7-단언문과-기대값-작성))
8. **리터럴과 변수 사용** - 의미 있는 명명을 통한 역할 표현 (→ [상세: 리터럴과 변수의 역할](#8-리터럴과-변수의-역할))

### 핵심 개념 간 관계

```
테스트 가독성의 중요성
    ↓
테스트와 프로덕션 코드의 차이 인식
    ↓
일반적인 테스트 문제점 파악
    ↓
├─→ TestDox 명명 규칙 (무엇을 테스트하는가)
├─→ 정규 테스트 구조 (어떻게 구조화하는가)
├─→ 테스트 코드 간소화 (어떻게 간결하게 만드는가)
├─→ 명확한 단언문 (무엇을 검증하는가)
└─→ 리터럴과 변수 사용 (의미를 어떻게 전달하는가)
```

**압축 설명:**

1. **테스트 가독성의 중요성**: TDD 초기에는 생산성이 향상되지만, 테스트가 유지보수 부담이 되면 속도가 느려진다. 테스트는 코드 동작을 검증할 뿐만 아니라 명확하게 표현해야 지속 가능하다.

2. **테스트와 프로덕션 코드의 차이**: 테스트 코드는 값에 대해 구체적이고 동작 방식에 대해 추상적인 반면, 프로덕션 코드는 값에 대해 추상적이고 동작 방식에 대해 구체적이다. 테스트는 의존성 체인의 끝에 있어 의도를 표현하는 것이 더 중요하다.

3. **일반적인 테스트 문제점**: (1) 불명확한 테스트 이름, (2) 여러 기능을 테스트하는 단일 테스트, (3) 일관성 없는 구조, (4) 설정과 예외 처리 코드가 본질적 로직을 가림, (5) 의미 불명확한 리터럴 값("매직 넘버")

4. **TestDox 명명 규칙**: 메소드 이름이 아닌 기능을 기준으로 테스트를 명명한다. "대상 클래스 + 동사구" 형태로 문장처럼 읽히게 작성하며, 기대 결과, 액션, 시나리오 동기를 포함한다.

5. **정규 테스트 구조**: (1) Setup-준비, (2) Execute-실행, (3) Verify-검증, (4) Teardown-정리의 4단계 구조를 따른다. Mock 객체 사용 시에는 Expect-Execute-Assert 변형을 사용한다.

6. **테스트 코드 간소화**: (1) 작은 메소드로 의도 표현, (2) 공통 기능을 메소드로 추출하여 공유, (3) 불필요한 예외 처리 제거, (4) 헬퍼 객체로 복잡성 위임

7. **명확한 단언문**: 테스트에서 중요한 것만 검증하고 나머지는 무시한다. assertFalse 대신 명시적인 matcher를 사용하여 부정 로직을 명확히 한다.

8. **리터럴과 변수 사용**: 리터럴 값의 역할과 의미를 설명하는 변수명과 상수명을 사용한다. 테스트에서 해당 값이 중요한지(예: 허용 범위 밖) 아니면 단순 플레이스홀더인지 명확히 한다.

## 상세 내용

### 목차
1. [테스트 가독성과 유지보수성](#1-테스트-가독성과-유지보수성)
2. [테스트 코드의 특성](#2-테스트-코드의-특성)
3. [테스트 스멜(Test Smells)](#3-테스트-스멜test-smells)
4. [TestDox 명명 규칙](#4-testdox-명명-규칙)
5. [정규 테스트 구조](#5-정규-테스트-구조)
6. [테스트 코드 간소화 기법](#6-테스트-코드-간소화-기법)
7. [단언문과 기대값 작성](#7-단언문과-기대값-작성)
8. [리터럴과 변수의 역할](#8-리터럴과-변수의-역할)

---

### 1. 테스트 가독성과 유지보수성

**관련 핵심 개념**: [테스트 가독성의 중요성](#핵심-개념-목록)

**출처**: 272페이지, Lines 8-17

TDD를 도입한 팀은 초기에 생산성이 향상되는 것을 경험한다. 테스트가 자신감 있게 기능을 추가하게 하고 즉시 오류를 잡아주기 때문이다. 하지만 일부 팀은 시간이 지나면서 테스트 자체가 유지보수 부담이 되어 속도가 느려진다.

**TDD의 지속 가능성을 위한 조건**:
- 테스트는 코드의 동작을 검증하는 것 이상을 해야 한다
- 그 동작을 명확하게 표현해야 한다 - 가독성이 필수다
- 코드 가독성이 중요한 것과 같은 이유로 테스트 가독성도 중요하다

```java
// 나쁜 예: 의미를 파악하기 어려운 테스트
@Test
public void test1() {
    TargetObject obj = new TargetObject();
    obj.setValue(100);
    obj.process();
    assertEquals(200, obj.getValue());
}

// 좋은 예: 의도가 명확한 테스트
@Test
public void doublesValueWhenProcessingWithPositiveNumber() {
    TargetObject obj = new TargetObject();
    obj.setValue(100);

    obj.process();

    assertThat(obj.getValue(), equalTo(200));
}
```

**생산성에 미치는 영향**:
- 개발자가 테스트를 이해하려고 멈춰서 고민해야 할 때마다
- 새로운 기능을 만드는 데 쓸 시간이 줄어든다
- 팀 속도(velocity)가 떨어진다

---

### 2. 테스트 코드의 특성

**이전 내용과의 관계**: [테스트 가독성과 유지보수성](#1-테스트-가독성과-유지보수성)에서 테스트가 명확하게 표현되어야 한다는 것을 확인했다면, 이제 테스트 코드가 프로덕션 코드와 어떻게 다른지 이해해야 한다.

**관련 핵심 개념**: [테스트와 프로덕션 코드의 차이](#핵심-개념-목록)

**출처**: 272-273페이지, Lines 18-29

**테스트 코드와 프로덕션 코드의 스타일 차이**:

| 측면 | 테스트 코드 | 프로덕션 코드 |
|------|------------|--------------|
| **값에 대한 접근** | 구체적 (concrete) - 예시로 사용되는 구체적 값 | 추상적 (abstract) - 다양한 값에 대해 동작 |
| **동작 방식에 대한 접근** | 추상적 - 어떻게 동작하는지 숨김 | 구체적 - 어떻게 작업을 수행하는지 명확함 |
| **의존성 관리** | 의존성 체인의 끝 - 연결보다 의도 표현 중요 | 객체 조합과 의존성 관리가 중요 |
| **목표** | 선언적 설명처럼 읽힘 | 작업을 실제로 수행 |

```python
# 프로덕션 코드: 값에 대해 추상적, 동작에 대해 구체적
class Calculator:
    def add(self, a, b):  # a, b는 추상적인 매개변수
        # 구체적인 동작 방식
        result = 0
        result += a
        result += b
        return result

# 테스트 코드: 값에 대해 구체적, 동작에 대해 추상적
def test_adds_two_numbers():
    calculator = Calculator()

    # 구체적인 예시 값
    result = calculator.add(2, 3)

    # 어떻게 더하는지는 관심 없고, 결과만 검증
    assert result == 5
```

**테스트 코드가 지향해야 할 것**:
```java
// 테스트 코드는 선언적 설명처럼 읽혀야 한다
// "WHAT"을 강조하고 "HOW"는 숨긴다

// 나쁜 예: 구현 세부사항 노출
@Test
public void testCalculation() {
    int step1 = obj.getValue();
    int step2 = step1 * 2;
    int step3 = step2 + 10;
    obj.setValue(step3);
    assertEquals(step3, obj.calculate());
}

// 좋은 예: 의도 명확히 표현
@Test
public void calculatesResultByDoublingValueAndAddingTen() {
    obj.setValue(5);

    assertThat(obj.calculate(), equalTo(20));
}
```

---

### 3. 테스트 스멜(Test Smells)

**이전 내용과의 관계**: [테스트 코드의 특성](#2-테스트-코드의-특성)을 이해했다면, 이제 실제로 어떤 문제들이 자주 발생하는지 파악해야 한다.

**관련 핵심 개념**: [일반적인 테스트 문제점](#핵심-개념-목록)

**출처**: 273페이지, Lines 35-53

저자들이 많은 단위 테스트 스위트에서 발견한 가독성 문제들:

#### 1. 불명확한 테스트 이름
**문제**: 각 테스트 케이스의 핵심과 다른 테스트와의 차이를 명확히 설명하지 않는 이름

```java
// 나쁜 예 1: 의미 없는 이름
public class TargetObjectTest {
    @Test public void test1() { /* ... */ }
    @Test public void test2() { /* ... */ }
    @Test public void test3() { /* ... */ }
}

// 나쁜 예 2: 메소드 이름 반복
public class TargetObjectTest {
    @Test public void isReady() { /* ... */ }
    @Test public void choose() { /* ... */ }
    @Test public void choose1() { /* ... */ }
}
```

```python
# Python 나쁜 예: 의미 없는 이름
class TestTargetObject:
    def test_1(self):
        pass

    def test_2(self):
        pass

# Python 나쁜 예: 메소드 이름 반복
class TestTargetObject:
    def test_is_ready(self):
        pass

    def test_choose(self):
        pass

    def test_choose_1(self):  # 숫자로 구분하는 것은 의미가 없음
        pass
```

#### 2. 여러 기능을 테스트하는 단일 테스트
**문제**: 하나의 테스트 케이스가 여러 기능을 동시에 검사

```python
# 나쁜 예: 여러 기능을 한 번에 테스트
def test_user_operations(self):
    user = User("john")

    # 생성 기능 테스트
    assert user.name == "john"

    # 수정 기능 테스트
    user.update_email("john@example.com")
    assert user.email == "john@example.com"

    # 삭제 기능 테스트
    user.deactivate()
    assert user.is_active == False

# 좋은 예: 각 기능을 별도로 테스트
def test_creates_user_with_given_name(self):
    user = User("john")
    assert user.name == "john"

def test_updates_user_email(self):
    user = User("john")
    user.update_email("john@example.com")
    assert user.email == "john@example.com"

def test_deactivates_user_when_requested(self):
    user = User("john")
    user.deactivate()
    assert user.is_active == False
```

#### 3. 일관성 없는 구조
**문제**: 테스트마다 다른 구조를 사용하여 의도를 빠르게 파악하기 어려움

```python
# 나쁜 예: 일관성 없는 구조
def test_feature_a(self):
    obj = MyClass()
    result = obj.process()
    assert result == expected

def test_feature_b(self):
    # 순서가 다름
    expected = calculate_expected()
    obj = MyClass()
    assert obj.process() == expected

def test_feature_c(self):
    # 구조가 완전히 다름
    assert MyClass().process() == expected

# 좋은 예: 일관된 구조
def test_feature_a(self):
    obj = MyClass()  # Setup
    result = obj.process()  # Execute
    assert result == expected  # Verify

def test_feature_b(self):
    obj = MyClass()  # Setup
    result = obj.process()  # Execute
    assert result == expected  # Verify
```

#### 4. 본질적 로직을 가리는 설정/예외 처리 코드
**문제**: 많은 설정 코드와 예외 처리가 실제 테스트하려는 내용을 가림

```python
# 나쁜 예: 설정 코드가 본질을 가림
def test_processes_data(self):
    # 복잡한 설정 코드
    config = Configuration()
    config.set_param1("value1")
    config.set_param2("value2")
    config.set_param3("value3")
    db = Database(config)
    db.connect()
    db.create_schema()
    db.populate_test_data()
    processor = DataProcessor(db, config)

    try:
        # 실제 테스트하려는 내용
        result = processor.process()
        assert result.status == "success"
    except Exception as e:
        self.fail(f"Processing failed: {e}")
    finally:
        db.cleanup()
        db.disconnect()

# 좋은 예: 헬퍼 메소드로 설정 분리
def test_processes_data_successfully(self):
    processor = self.create_configured_processor()  # Setup 분리

    result = processor.process()

    assert result.status == "success"
```

#### 5. 의미 불명확한 리터럴 값
**문제**: "매직 넘버"를 사용하지만 그 값이 중요한지 명확하지 않음

```python
# 나쁜 예: 리터럴의 의미 불명확
def test_validates_age(self):
    user = User(18)  # 18이 왜 중요한가?
    assert user.is_valid() == True

    user2 = User(17)  # 17이 왜 중요한가?
    assert user2.is_valid() == False

# 좋은 예: 의미 있는 이름 사용
def test_validates_age(self):
    MINIMUM_VALID_AGE = 18
    JUST_BELOW_MINIMUM_AGE = 17

    adult_user = User(MINIMUM_VALID_AGE)
    assert adult_user.is_valid() == True

    minor_user = User(JUST_BELOW_MINIMUM_AGE)
    assert minor_user.is_valid() == False
```

---

### 4. TestDox 명명 규칙

**이전 내용과의 관계**: [테스트 스멜](#3-테스트-스멜test-smells) 중 첫 번째 문제인 불명확한 테스트 이름을 해결하는 구체적 방법이다.

**관련 핵심 개념**: [TestDox 명명 규칙](#핵심-개념-목록)

**출처**: 273-275페이지, Lines 54-114

#### TestDox의 핵심 원칙

TestDox는 Chris Stevenson이 발명한 명명 규칙으로, 각 테스트 이름이 문장처럼 읽히며 대상 클래스가 암묵적 주어가 된다.

**명명 원칙**:
```
[대상 클래스] + [동사구로 표현한 기능]
```

**예시**:
```java
// TestDox 형식의 테스트 이름
public class ListTests {
    // "A List holds items in the order they were added"
    @Test public void holdsItemsInTheOrderTheyWereAdded() { /* ... */ }

    // "A List can hold multiple references to the same item"
    @Test public void canHoldMultipleReferencesToTheSameItem() { /* ... */ }

    // "A List throws an exception when removing an item it doesn't hold"
    @Test public void throwsAnExceptionWhenRemovingAnItemItDoesntHold() { /* ... */ }
}
```

```python
# Python TestDox 형식
class TestList:
    # "A List holds items in the order they were added"
    def test_holds_items_in_the_order_they_were_added(self):
        items = [1, 2, 3]
        list_obj = List(items)

        assert list_obj.get_all() == [1, 2, 3]

    # "A List can hold multiple references to the same item"
    def test_can_hold_multiple_references_to_the_same_item(self):
        item = "duplicate"
        list_obj = List()
        list_obj.add(item)
        list_obj.add(item)

        assert list_obj.count(item) == 2

    # "A List throws an exception when removing an item it doesn't hold"
    def test_throws_exception_when_removing_item_it_doesnt_hold(self):
        list_obj = List([1, 2, 3])

        with pytest.raises(ValueError):
            list_obj.remove(999)
```

#### 좋은 테스트 이름의 3요소

테스트 이름은 다음을 포함해야 한다:
1. **기대 결과 (Expected Result)**: 무엇이 일어나야 하는가
2. **액션 (Action)**: 객체에 대한 어떤 동작
3. **시나리오 동기 (Motivation)**: 왜 그런 시나리오인가

```java
// 나쁜 예: 동기 없음
pollsTheServersMonitoringPort()
// 왜 polling하는가? 결과는 무엇인가?

// 좋은 예: 3요소 모두 포함
notifiesListenersThatServerIsUnavailableWhenCannotConnectToItsMonitoringPort()
// 기대 결과: notifies listeners that server is unavailable
// 액션: (tries to) connect to monitoring port
// 시나리오 동기: when cannot connect
```

```python
# Python 예시

# 나쁜 예: 동기와 결과 불명확
def test_polls_monitoring_port(self):
    pass

# 좋은 예: 3요소 포함
def test_notifies_listeners_server_unavailable_when_cannot_connect_to_monitoring_port(self):
    # Setup
    monitor = ConnectionMonitor()
    listener = Mock()
    monitor.add_listener(listener)
    unavailable_server = create_unavailable_server()

    # Execute
    monitor.check(unavailable_server)

    # Verify: 기대 결과 검증
    listener.on_server_unavailable.assert_called_once()
```

#### TestDox의 장점

1. **개발자의 사고 전환**: 객체가 무엇인지보다 무엇을 하는지 생각하게 함
2. **점진적 개발과 호환**: 한 번에 하나씩 기능을 추가하는 접근 방식과 일치
3. **일관된 명명**: 사용자 스토리 → 태스크 → 인수 테스트 → 단위 테스트까지 일관된 스타일
4. **자동 문서화**: TestDox 도구로 읽기 쉬운 문서 생성 가능

#### 테스트 이름 작성 시점

**출처**: 275페이지, Lines 119-124

두 가지 접근법이 있다:
1. **나중에 작성**: 플레이스홀더 이름으로 시작 → 테스트 본문 작성 → 최종 이름 결정
2. **먼저 작성**: 테스트 이름 먼저 결정(의도 명확화) → 테스트 코드 작성

중요한 것은 최종적으로 테스트가 일관되고 표현력 있게 만드는 것이다.

```python
# 접근법 1: 플레이스홀더로 시작
def test_feature_x(self):  # 임시 이름
    # 테스트 작성...
    pass

# 나중에 이름 수정
def test_sends_notification_when_order_is_completed(self):
    # 동일한 테스트 코드
    pass

# 접근법 2: 이름 먼저 (Steve의 선호)
def test_sends_notification_when_order_is_completed(self):
    # 이름에 맞춰 테스트 작성
    pass
```

#### TestDox 도구 활용

**출처**: 275-276페이지, Lines 125-139

TestDox 플러그인(예: IntelliJ용)은 camelCase 메소드 이름을 풀어서 읽기 쉬운 문서로 변환한다.

```
KeyboardLayout
  - translates numbers to key strokes in all known layouts
  - translates letters to key strokes
  - translates punctuation to key strokes
  - throws exception when character cannot be translated
```

**정기적 문서 검토의 중요성**:
- 생성된 문서를 정기적으로 훑어보면 코드와 너무 가까워서 보지 못하는 문제를 발견할 수 있다
- 예: 위 예시에서 첫 번째 테스트 이름이 불명확하다는 것을 발견

---

### 5. 정규 테스트 구조

**이전 내용과의 관계**: [TestDox 명명 규칙](#4-testdox-명명-규칙)에서 "무엇을" 테스트하는지 명확히 했다면, 이제 테스트를 "어떻게 구조화"할지 다룬다.

**관련 핵심 개념**: [정규 테스트 구조](#핵심-개념-목록)

**출처**: 276-277페이지, Lines 145-202

#### 표준 4단계 구조

표준화된 형식으로 테스트를 작성하면 이해하기 쉽다. 표준 형식으로 작성하기 어렵다면 코드가 너무 복잡하거나 아이디어가 명확하지 않다는 힌트다.

**가장 일반적인 테스트 형식**:

```
1. Setup (준비): 테스트 컨텍스트 준비, 대상 코드가 실행될 환경
2. Execute (실행): 대상 코드 호출, 테스트할 동작 트리거
3. Verify (검증): 기대하는 가시적 효과 확인
4. Teardown (정리): 다른 테스트를 오염시킬 수 있는 남은 상태 정리
```

다른 버전으로는 "Arrange, Act, Assert"가 있으며 일부 단계를 합친다.

#### 기본 예제: Setup-Execute-Verify 패턴

```java
// Java 예제
public class StringTemplateTest {
    @Test public void expandsMacrosSurroundedWithBraces() {
        // Setup: 컨텍스트 준비
        StringTemplate template = new StringTemplate("{a}{b}");
        HashMap<String,Object> macros = new HashMap<String,Object>();
        macros.put("a", "A");
        macros.put("b", "B");

        // Execute: 대상 코드 실행
        String expanded = template.expand(macros);

        // Verify: 결과 검증
        assertThat(expanded, equalTo("AB"));

        // Teardown: 이 경우 필요 없음
    }
}
```

```python
# Python 버전
class TestStringTemplate:
    def test_expands_macros_surrounded_with_braces(self):
        # Setup: 컨텍스트 준비
        template = StringTemplate("{a}{b}")
        macros = {
            "a": "A",
            "b": "B"
        }

        # Execute: 대상 코드 실행
        expanded = template.expand(macros)

        # Verify: 결과 검증
        assert expanded == "AB"

        # Teardown: cleanup() 메소드가 있다면 자동으로 호출됨
```

#### Mock 객체를 사용하는 변형: Expect-Execute-Assert

Mock 객체를 사용하는 테스트는 일부 단언이 실행 단계 전에 선언되고 나중에 암묵적으로 검증된다.

```java
// Chapter 19의 LoggingXMPPFailureReporterTest 예제
@RunWith(JMock.class)
public class LoggingXMPPFailureReporterTest {
    // Setup: 공통 설정 (모든 테스트에서 사용)
    private final Mockery context = new Mockery() {{
        setImposteriser(ClassImposteriser.INSTANCE);
    }};
    final Logger logger = context.mock(Logger.class);
    final LoggingXMPPFailureReporter reporter =
        new LoggingXMPPFailureReporter(logger);

    @Test public void writesMessageTranslationFailureToLog() {
        // Setup: 예외 준비
        Exception exception = new Exception("an exception");

        // Expect: 기대값 설정 (Execute 전에 선언)
        context.checking(new Expectations() {{
            oneOf(logger).severe("expected log message here");
        }});

        // Execute: 대상 코드 실행
        reporter.cannotTranslateMessage("auction id",
                                       "failed message", exception);

        // Assert: jMock이 자동으로 기대값 충족 여부 검증
        // (명시적 검증 코드 없음)
    }

    // Teardown: 테스트 클래스 수준
    @AfterClass public static void resetLogging() {
        LogManager.getLogManager().reset();
    }
}
```

```python
# Python Mock 예제 (unittest.mock 사용)
class TestLoggingXMPPFailureReporter:
    def setup_method(self):
        # Setup: 각 테스트 전 실행
        self.logger = Mock()
        self.reporter = LoggingXMPPFailureReporter(self.logger)

    def test_writes_message_translation_failure_to_log(self):
        # Setup: 테스트별 준비
        exception = Exception("an exception")

        # Execute: 대상 코드 실행
        self.reporter.cannot_translate_message(
            "auction id",
            "failed message",
            exception
        )

        # Verify: Mock 호출 검증
        self.logger.severe.assert_called_once_with(
            "expected log message here"
        )

    @classmethod
    def teardown_class(cls):
        # Teardown: 모든 테스트 후 정리
        logging.getLogger().handlers.clear()
```

#### 테스트 역방향 작성

**출처**: 277페이지, Lines 203-211

표준 형식을 따르지만 반드시 위에서 아래로 작성할 필요는 없다. 종종 다음 순서로 작성한다:

1. **테스트 이름 작성**: 무엇을 달성하고 싶은지 명확히
2. **대상 코드 호출 작성**: 기능의 진입점
3. **기대값과 단언 작성**: 기능이 가져야 할 효과
4. **설정과 정리 작성**: 테스트 컨텍스트 정의

```python
# 작성 순서 예시

# 1단계: 테스트 이름 (의도 명확화)
def test_calculates_total_price_including_tax(self):
    pass

# 2단계: 대상 코드 호출 (진입점)
def test_calculates_total_price_including_tax(self):
    total = calculator.calculate_total(order)

# 3단계: 기대값 (원하는 효과)
def test_calculates_total_price_including_tax(self):
    total = calculator.calculate_total(order)

    assert total == 110.0  # 100 + 10% tax

# 4단계: 설정 (컨텍스트)
def test_calculates_total_price_including_tax(self):
    # Setup
    calculator = TaxCalculator(tax_rate=0.10)
    order = Order(items=[Item(price=100.0)])

    # Execute
    total = calculator.calculate_total(order)

    # Verify
    assert total == 110.0
```

컴파일러를 위해 약간의 순서 조정이 있을 수 있지만, 이 순서가 새 단위 테스트를 생각하는 방식을 반영한다. 그런 다음 실행하고 실패하는 것을 확인한다.

#### 한 테스트 메소드에 몇 개의 단언문?

**출처**: 277페이지, Lines 212-220

일부 TDD 실천자는 각 테스트가 하나의 기대값이나 단언만 포함해야 한다고 제안한다. 이는 TDD를 배울 때 유용한 규칙이지만 실용적이지 않다.

**더 나은 규칙**:
- 테스트당 하나의 일관된 기능을 생각한다
- 이는 최대 몇 개의 단언으로 표현될 수 있다
- 단일 테스트가 대상 객체의 다른 기능들에 대해 단언하는 것처럼 보인다면 분리를 고려한다

```python
# 나쁜 예: 관련 없는 여러 기능 테스트
def test_user_class(self):
    user = User("john", 25)

    # 이름 관련 기능
    assert user.name == "john"
    assert user.name.isupper() == False

    # 나이 관련 기능
    assert user.age == 25
    assert user.is_adult() == True

    # 이메일 관련 기능 (전혀 다른 기능!)
    user.set_email("john@example.com")
    assert user.email == "john@example.com"

# 좋은 예: 일관된 하나의 기능, 여러 측면 검증
def test_formats_name_with_title_and_surname(self):
    user = User(first_name="john", last_name="doe")

    formatted = user.format_name_with_title("Dr.")

    # 하나의 기능에 대한 여러 측면 검증 (OK)
    assert "Dr." in formatted
    assert "john" in formatted.lower()
    assert "doe" in formatted.lower()
    assert formatted.startswith("Dr.")
```

**핵심**: 표현력이 중요하다. 이 테스트를 읽는 사람이 무엇이 중요한지 파악할 수 있는가?

---

### 6. 테스트 코드 간소화 기법

**이전 내용과의 관계**: [정규 테스트 구조](#5-정규-테스트-구조)로 테스트를 구조화했다면, 이제 각 부분을 더 읽기 쉽게 만드는 방법을 다룬다.

**관련 핵심 개념**: [테스트 코드 간소화](#핵심-개념-목록)

**출처**: 278-279페이지, Lines 221-308

#### 원칙: "What" over "How"

모든 코드는 "어떻게"보다 "무엇을" 강조해야 하며, 테스트 코드도 마찬가지다. 테스트 메소드에 구현 세부사항이 많이 포함될수록 독자가 무엇이 중요한지 이해하기 어렵다.

**목표**: 도메인 용어로 기능을 설명하는 데 기여하지 않는 모든 것을 테스트 메소드 밖으로 이동한다.

#### 기법 1: 구조로 설명하기 (Use Structure to Explain)

**출처**: 278페이지, Lines 233-254

작은 메소드로 의도를 표현하라. Part III에서 본 것처럼 Java 문법 노이즈를 줄이기 위해 `translatorFor()`같은 작은 메소드를 작성한다.

**Hamcrest와 jMock의 조합 가능한 구문**:

```java
// 복잡한 검증을 읽기 쉽게 표현
assertThat(instruments, hasItem(instrumentWithPrice(greaterThan(81))));
// "instruments 컬렉션이 81보다 큰 가격의 Instrument를 최소 하나 가지고 있는지"

// 헬퍼 메소드로 matcher 생성
private Matcher<? super Instrument>
instrumentWithPrice(Matcher<? super Integer> priceMatcher) {
    return new FeatureMatcher<Instrument, Integer>(
                 priceMatcher, "instrument at price", "price") {
        @Override protected Integer featureValueOf(Instrument actual) {
            return actual.getStrikePrice();
        }
    };
}
```

```python
# Python 버전 (사용자 정의 matcher)

# 사용: 읽기 쉬운 단언
assert_that(instruments, has_item(instrument_with_price(greater_than(81))))

# 헬퍼 함수: matcher 생성
def instrument_with_price(price_matcher):
    """주어진 가격 조건을 만족하는 Instrument를 찾는 matcher"""
    class InstrumentPriceMatcher:
        def __init__(self, price_matcher):
            self.price_matcher = price_matcher

        def matches(self, item):
            return (isinstance(item, Instrument) and
                   self.price_matcher.matches(item.strike_price))

        def describe_mismatch(self, item):
            if not isinstance(item, Instrument):
                return f"{item} is not an Instrument"
            return f"instrument price was {item.strike_price}"

    return InstrumentPriceMatcher(price_matcher)
```

더 많은 프로그램 텍스트를 만들 수 있지만, 소스 라인을 최소화하는 것보다 표현력을 우선시한다.

#### 기법 2: 구조로 공유하기 (Use Structure to Share)

**출처**: 278페이지, Lines 255-265

공통 기능을 메소드로 추출하여 테스트 간 공유:
- 값 설정
- 상태 정리
- 단언 수행
- 때때로 이벤트 트리거

```java
// Chapter 19의 예: 반복되는 동작을 메소드로 추출
expectSniperToFailWhenItIs(...)
// jMock의 여러 기대값 블록 설정 기능을 활용
```

```python
# 공통 기능 추출 예시

class TestAuctionSniper:
    def expect_sniper_to_fail_when_it_is(self, state, defect):
        """Sniper가 특정 상태에서 실패할 것을 기대하는 헬퍼 메소드"""
        self.context.checking(
            Expectations()
                .one_of(self.listener).sniper_state_changed(
                    with_sniper_state(state))
                .one_of(self.failure_reporter).report_failure(
                    defect)
        )

    def test_reports_losing_when_auction_closes_immediately(self):
        # 공유 메소드 사용 - 의도가 명확함
        self.expect_sniper_to_fail_when_it_is(
            SniperState.LOSING,
            "Auction closed too soon"
        )

        self.sniper.auction_closed()

    def test_reports_losing_when_price_too_high(self):
        # 동일한 패턴 재사용
        self.expect_sniper_to_fail_when_it_is(
            SniperState.LOSING,
            "Price exceeded limit"
        )

        self.sniper.current_price(1000, 10, PriceSource.FROM_OTHER_BIDDER)
```

**주의사항**:
- 테스트를 너무 추상화하면 무엇을 하는지 볼 수 없게 된다
- 가장 중요한 관심사는 테스트가 대상 코드가 무엇을 하는지 설명하는 것
- 흐름을 볼 수 있을 만큼만 리팩터링하되, 프로덕션 코드만큼 강하게 리팩터링하지는 않는다

#### 기법 3: 긍정에 집중하기 (Accentuate the Positive)

**출처**: 278-279페이지, Lines 266-291

예외에 대해 단언할 것이 없다면 테스트에서 예외를 catch하지 말라.

```java
// 나쁜 예: 불필요한 예외 처리
@Test public void expandsMacrosSurroundedWithBraces() {
    StringTemplate template = new StringTemplate("{a}{b}");
    try {
        String expanded = template.expand(macros);
        assertThat(expanded, equalTo("AB"));
    } catch (TemplateFormatException e) {
        fail("Template failed: " + e);  // 정보를 오히려 잃어버림
    }
}

// 좋은 예 1: 예외를 전파시킴
@Test public void expandsMacrosSurroundedWithBraces() throws Exception {
    StringTemplate template = new StringTemplate("{a}{b}");
    String expanded = template.expand(macros);
    assertThat(expanded, equalTo("AB"));
}

// 좋은 예 2: 더 간결하게
@Test public void expandsMacrosSurroundedWithBraces() throws Exception {
    assertThat(new StringTemplate("{a}{b}").expand(macros),
               equalTo("AB"));
}
```

```python
# Python에서는 예외 처리가 더 간단함

# 나쁜 예: 불필요한 try-except
def test_expands_macros_surrounded_with_braces(self):
    template = StringTemplate("{a}{b}")
    try:
        expanded = template.expand(macros)
        assert expanded == "AB"
    except TemplateFormatException as e:
        pytest.fail(f"Template failed: {e}")  # 불필요

# 좋은 예: 예외는 자연스럽게 전파됨
def test_expands_macros_surrounded_with_braces(self):
    template = StringTemplate("{a}{b}")
    expanded = template.expand(macros)
    assert expanded == "AB"

# 더 간결한 버전
def test_expands_macros_surrounded_with_braces(self):
    assert StringTemplate("{a}{b}").expand(macros) == "AB"
```

테스트를 통과시키려는 경우 예외를 변환하면 실제로 스택 트레이스에서 정보를 잃는다. 가장 간단한 방법은 예외를 전파시키는 것이다. 테스트 메소드 시그니처에 임의의 예외를 추가할 수 있다(리플렉션으로만 호출되므로).

#### 기법 4: 하위 객체에 위임하기 (Delegate to Subordinate Objects)

**출처**: 279페이지, Lines 292-308

헬퍼 메소드로 충분하지 않을 때는 테스트를 지원하는 헬퍼 객체가 필요하다.

**Chapter 11의 테스트 리그**:
- `ApplicationRunner`
- `AuctionSniperDriver`
- `FakeAuctionServer`

이들 덕분에 Swing과 메시징 용어가 아닌 경매와 Sniper 용어로 테스트를 작성할 수 있었다.

**Test Data Builder 패턴**:
적절한 값만으로 복잡한 데이터 구조를 구축하는 기법. Chapter 22에서 자세히 다룬다. 테스트에 관련된 값만 포함하고 나머지는 기본값으로 처리한다.

```python
# Test Data Builder 예시

class OrderBuilder:
    """테스트용 Order 객체를 쉽게 만드는 빌더"""
    def __init__(self):
        # 기본값 설정
        self.customer = "default_customer"
        self.items = []
        self.status = "pending"
        self.shipping_address = "default_address"

    def with_customer(self, customer):
        """필요한 것만 오버라이드"""
        self.customer = customer
        return self

    def with_items(self, *items):
        """필요한 것만 오버라이드"""
        self.items = list(items)
        return self

    def with_status(self, status):
        """필요한 것만 오버라이드"""
        self.status = status
        return self

    def build(self):
        return Order(
            customer=self.customer,
            items=self.items,
            status=self.status,
            shipping_address=self.shipping_address
        )

# 테스트에서 사용: 관련 있는 것만 명시
def test_calculates_total_for_multiple_items(self):
    order = (OrderBuilder()
             .with_items(Item(price=10), Item(price=20))
             .build())

    # items만 중요하고 customer, status는 이 테스트와 무관
    assert order.calculate_total() == 30
```

**하위 객체 작성의 두 가지 접근법**:

1. **테스트 우선 접근 (Chapter 11 방식)**:
   - 원하는 테스트를 먼저 작성
   - 지원 객체를 나중에 채움
   - 문제 설명부터 시작하여 어디로 가는지 확인

2. **리팩터링 접근 (WindowLicker 프레임워크의 기원)**:
   - 코드를 테스트에 직접 작성
   - 동작 클러스터를 리팩터링하여 추출
   - Swing event dispatcher와 상호작용하는 헬퍼 코드로 시작
   - 결국 별도 프로젝트로 성장

---

### 7. 단언문과 기대값 작성

**이전 내용과의 관계**: [테스트 코드 간소화](#6-테스트-코드-간소화-기법)에서 테스트 구조를 간결하게 만들었다면, 이제 검증 부분을 명확하고 정확하게 작성하는 방법을 다룬다.

**관련 핵심 개념**: [명확한 단언문](#핵심-개념-목록)

**출처**: 279-280페이지, Lines 309-343

#### 원칙: 정확성과 최소성

테스트의 단언과 기대값은 대상 코드의 동작에서 **무엇이 중요한지** 정확하게 전달해야 한다.

**일반적인 문제**:
- 너무 많은 세부사항을 단언 → 읽기 어렵고 변경에 취약
- "Too Many Expectations" (242페이지) 참조

#### 기법 1: 최대한 좁게 정의하기

관련 있는 것만 검증하고 나머지는 무시한다.

```java
// "instrument with price" 단언 예시
assertThat(instruments, hasItem(instrumentWithPrice(greaterThan(81))));
// strike price만 검증, 나머지 값은 무시

// Chapter 19의 예: 일부 인자만 검증
oneOf(failureReporter).cannotTranslateMessage(
                         with(SNIPER_ID),              // 정확한 값 필요
                         with(badMessage),             // 정확한 값 필요
                         with(any(RuntimeException.class)));  // 아무 RuntimeException이나 OK
```

```python
# Python 예시: 선택적 검증

def test_reports_failure_with_correct_context(self):
    # 일부만 검증하는 matcher 사용
    self.failure_reporter.report_failure.assert_called_once()

    # 호출된 인자 중 중요한 것만 검증
    args = self.failure_reporter.report_failure.call_args[0]
    assert args[0] == SNIPER_ID  # 첫 번째 인자는 정확해야 함
    assert args[1] == bad_message  # 두 번째 인자도 정확해야 함
    assert isinstance(args[2], RuntimeException)  # 세 번째는 타입만 중요

# 더 나은 방법: 사용자 정의 matcher
def test_reports_failure_with_correct_context(self):
    self.failure_reporter.report_failure.assert_called_once_with(
        SNIPER_ID,
        bad_message,
        any_instance_of(RuntimeException)  # 헬퍼 matcher
    )

def any_instance_of(cls):
    """특정 클래스의 인스턴스면 통과하는 matcher"""
    class InstanceMatcher:
        def __eq__(self, other):
            return isinstance(other, cls)
        def __repr__(self):
            return f"<any {cls.__name__}>"
    return InstanceMatcher()
```

**대학에서 배운 사전조건/사후조건(pre/postcondition)이 유용할 때다.**

#### 기법 2: assertFalse 피하기

`assertFalse()`는 실패 메시지와 부정이 결합되어 읽기 어렵다.

```java
// 나쁜 예: 부정 로직이 혼란스러움
assertFalse("end date", first.endDate().equals(second.endDate()));
// "두 날짜가 다르지 않아야 한다"로 읽힐 수 있음

// 약간 나은 예: assertTrue + "!"
assertTrue("end date", !first.endDate().equals(second.endDate()));
// 하지만 "!" 한 글자는 놓치기 쉬움

// 좋은 예: matcher로 명시적으로 표현
assertThat("end date", first.endDate(), not(equalTo(second.endDate())));
```

```python
# Python 예시

# 나쁜 예: 부정 로직
assert not first.end_date() == second.end_date(), "end date"

# 좋은 예: 명시적 표현 (pytest)
assert first.end_date() != second.end_date(), "end dates should differ"

# 더 좋은 예: Hamcrest 스타일 (PyHamcrest)
assert_that(first.end_date(), is_not(equal_to(second.end_date())),
            "end date")
```

**matcher 사용의 장점**: 실패 보고서에 실제 받은 값도 표시된다.

```
java.lang.AssertionError: end date
Expected: not <Thu Jan 01 02:34:38 GMT 1970>
     but: was <Thu Jan 01 02:34:38 GMT 1970>
```

```python
# PyHamcrest 실패 메시지
"""
AssertionError: end date
Expected: not <datetime.datetime(1970, 1, 1, 2, 34, 38)>
     but: was <datetime.datetime(1970, 1, 1, 2, 34, 38)>
"""
```

#### 실전 적용 예시

```python
# 복잡한 객체 검증: 관련 있는 속성만

class TestOrderProcessor:
    def test_processes_order_and_updates_status(self):
        order = self.create_pending_order()

        result = self.processor.process(order)

        # 관련 있는 것만 검증
        assert result.status == "completed"  # 상태가 핵심
        assert result.processed_at is not None  # 시간 존재 여부만
        # result.id, result.customer 등은 이 테스트와 무관하므로 무시

    def test_sends_confirmation_email_with_order_details(self):
        order = self.create_order()

        self.processor.process(order)

        # 이메일 발송 확인 - 일부 인자만 검증
        self.email_service.send.assert_called_once()

        call_args = self.email_service.send.call_args
        email = call_args[0][0]

        # 중요한 것만 검증
        assert email.to == order.customer.email  # 수신자는 정확해야 함
        assert order.order_id in email.body  # 본문에 주문 번호 포함
        assert email.subject  # 제목 존재 여부만 확인 (정확한 내용은 무관)
```

---

### 8. 리터럴과 변수의 역할

**이전 내용과의 관계**: [단언문과 기대값 작성](#7-단언문과-기대값-작성)에서 무엇을 검증할지 명확히 했다면, 이제 테스트에 사용되는 값들이 어떤 의미를 갖는지 명확히 표현하는 방법을 다룬다.

**관련 핵심 개념**: [리터럴과 변수 사용](#핵심-개념-목록)

**출처**: 280-281페이지, Lines 344-369

#### 문제: 설명 없는 리터럴 값

이 장 서론에서 언급했듯이, 테스트 코드는 프로덕션 코드보다 구체적이므로 리터럴 값이 더 많다.

**리터럴 값의 이해 어려움**:
프로그래머는 특정 값이 다음 중 무엇인지 해석해야 한다:
- **중요한 값**: 허용 범위 바로 밖의 값
- **임의의 플레이스홀더**: 동작을 추적하기 위한 값 (예: 두 배가 되어 전달되어야 함)

리터럴 값은 그 역할을 설명하지 않는다.

```python
# 나쁜 예: 값의 의미 불명확
def test_validates_user_age(self):
    user = User(18)  # 18이 왜 중요한가?
    assert user.is_valid()

    user2 = User(17)  # 17이 왜 중요한가?
    assert not user2.is_valid()

def test_processes_transaction(self):
    # 이 숫자들의 의미는?
    transaction = Transaction(100, 50, 25)
    result = process(transaction)
    assert result == 175  # 왜 175?
```

#### 해결책 1: 의미 있는 변수/상수 이름

리터럴 값을 역할을 설명하는 이름을 가진 변수와 상수에 할당한다.

```python
# 좋은 예: 역할이 명확한 이름

def test_validates_user_age(self):
    MINIMUM_LEGAL_AGE = 18
    JUST_BELOW_LEGAL_AGE = 17

    adult = User(MINIMUM_LEGAL_AGE)
    assert adult.is_valid()

    minor = User(JUST_BELOW_LEGAL_AGE)
    assert not minor.is_valid()

def test_calculates_total_with_tax_and_tip(self):
    BASE_AMOUNT = 100
    TAX_AMOUNT = 50
    TIP_AMOUNT = 25
    EXPECTED_TOTAL = 175

    transaction = Transaction(BASE_AMOUNT, TAX_AMOUNT, TIP_AMOUNT)

    result = process(transaction)

    assert result == EXPECTED_TOTAL
```

#### Chapter 12의 예시

**출처**: 280-281페이지, Lines 354-362

```java
// "사용되지 않는" 것을 명시적으로 표현
public static final Chat UNUSED_CHAT = null;
```

```python
# Python 버전
UNUSED_CHAT = None  # 인자가 사용되지 않음을 명시

def test_connects_to_auction_without_chat(self):
    # null/None이 프로덕션에서 예상되는 것은 아님
    # 하지만 신경 쓰지 않으며, 테스트하기 쉽게 만듦
    sniper = AuctionSniper(auction, UNUSED_CHAT)

    sniper.connect()

    # chat 관련 동작은 검증하지 않음
```

**이 패턴의 의도**:
- 프로덕션에서 `null`을 받을 것으로 예상하는 것이 아니다
- 실제로 신경 쓰지 않으며 테스트를 더 쉽게 만든다
- `UNUSED_CHAT`이라는 이름이 의도를 명확히 한다

#### 팀 규칙: 공통 값에 대한 명명 규칙

팀이 일반적인 값에 대한 규칙을 개발할 수 있다:

```java
// 잘못된 ID를 나타내는 규칙
public final static INVALID_ID = 666;
```

```python
# Python 팀 규칙 예시

# 테스트 상수 모듈 (test_constants.py)
class TestConstants:
    # ID 관련
    INVALID_ID = -1
    NONEXISTENT_ID = 999999

    # 날짜 관련
    PAST_DATE = datetime(2000, 1, 1)
    FUTURE_DATE = datetime(2099, 12, 31)

    # 문자열 관련
    EMPTY_STRING = ""
    VERY_LONG_STRING = "x" * 10000

    # 금액 관련
    ZERO_AMOUNT = 0.0
    NEGATIVE_AMOUNT = -100.0
    VERY_LARGE_AMOUNT = 1_000_000_000.0

# 테스트에서 사용
from test_constants import TestConstants as TC

def test_rejects_invalid_user_id(self):
    with pytest.raises(ValueError):
        user_service.get_user(TC.INVALID_ID)

def test_handles_very_long_input(self):
    result = text_processor.process(TC.VERY_LONG_STRING)
    assert result is not None
```

#### 변수 명명의 목적

**출처**: 281페이지, Lines 365-366

> 변수를 명명하여 이 값이나 객체가 테스트에서 수행하는 역할과 대상 객체와의 관계를 보여준다.

```python
# 역할과 관계를 보여주는 명명

def test_transfers_money_between_accounts(self):
    # 역할을 명확히 하는 변수명
    sender_account = Account(initial_balance=1000)
    receiver_account = Account(initial_balance=500)
    transfer_amount = 300

    transfer_service.transfer(
        from_account=sender_account,
        to_account=receiver_account,
        amount=transfer_amount
    )

    # 역할이 명확하므로 단언도 읽기 쉬움
    assert sender_account.balance == 700  # 1000 - 300
    assert receiver_account.balance == 800  # 500 + 300

def test_notifies_observers_in_registration_order(self):
    # 순서 관계를 보여주는 명명
    first_observer = MockObserver()
    second_observer = MockObserver()
    third_observer = MockObserver()

    subject.register(first_observer)
    subject.register(second_observer)
    subject.register(third_observer)

    subject.notify_all()

    # 순서 관계 검증
    assert first_observer.notified_at < second_observer.notified_at
    assert second_observer.notified_at < third_observer.notified_at
```

#### 실전 종합 예시

```python
# 모든 기법 통합 예시

class TestPricingEngine:
    # 테스트 상수: 의미 명확
    BASE_PRICE = 100.0
    STANDARD_TAX_RATE = 0.10
    PREMIUM_TAX_RATE = 0.15
    DISCOUNT_THRESHOLD = 1000.0
    LARGE_ORDER_DISCOUNT = 0.05

    def test_applies_standard_tax_for_regular_customers(self):
        # 역할을 보여주는 변수명
        regular_customer = Customer(membership_level="standard")
        order_with_base_price = Order(
            items=[Item(price=self.BASE_PRICE)],
            customer=regular_customer
        )
        expected_total = self.BASE_PRICE * (1 + self.STANDARD_TAX_RATE)

        engine = PricingEngine()
        actual_total = engine.calculate_total(order_with_base_price)

        # 의미 있는 단언
        assert actual_total == expected_total

    def test_applies_bulk_discount_when_exceeding_threshold(self):
        # 시나리오를 설명하는 변수명
        LARGE_ORDER_AMOUNT = self.DISCOUNT_THRESHOLD + 100
        order_exceeding_threshold = Order(
            items=[Item(price=LARGE_ORDER_AMOUNT)]
        )

        # 기대값 계산 명시
        price_with_tax = LARGE_ORDER_AMOUNT * (1 + self.STANDARD_TAX_RATE)
        expected_with_discount = price_with_tax * (1 - self.LARGE_ORDER_DISCOUNT)

        engine = PricingEngine()
        actual_total = engine.calculate_total(order_exceeding_threshold)

        assert actual_total == expected_with_discount

    def test_uses_placeholder_values_for_unimportant_fields(self):
        # 관련 없는 필드는 명시적으로 표시
        UNUSED_CUSTOMER_NAME = "placeholder"
        UNUSED_ORDER_DATE = None
        IMPORTANT_ITEM_PRICE = 50.0

        order = Order(
            customer_name=UNUSED_CUSTOMER_NAME,  # 이 테스트와 무관
            order_date=UNUSED_ORDER_DATE,  # 이 테스트와 무관
            items=[Item(price=IMPORTANT_ITEM_PRICE)]  # 이것만 중요
        )

        result = engine.calculate_total(order)

        # IMPORTANT_ITEM_PRICE만 결과에 영향을 미침
        assert result > 0
```

---

## 요약

Chapter 21은 테스트 가독성을 향상시키는 8가지 핵심 원칙과 기법을 다룬다:

1. **테스트 가독성이 TDD 지속 가능성의 핵심**이며
2. **테스트와 프로덕션 코드는 상반된 특성**(구체성 vs 추상성)을 가지고
3. **5가지 일반적인 테스트 문제**를 피해야 하며
4. **TestDox 명명 규칙**으로 기능을 서술적으로 표현하고
5. **Setup-Execute-Verify-Teardown 구조**를 일관되게 사용하며
6. **간소화 기법**으로 노이즈를 제거하고
7. **정확하고 좁은 단언문**으로 중요한 것만 검증하며
8. **의미 있는 변수명**으로 값의 역할을 명확히 해야 한다

이 모든 원칙은 "무엇을 테스트하는가"를 명확히 표현하여 개발자가 테스트를 이해하는 시간을 줄이고 팀 생산성을 유지하는 것을 목표로 한다.

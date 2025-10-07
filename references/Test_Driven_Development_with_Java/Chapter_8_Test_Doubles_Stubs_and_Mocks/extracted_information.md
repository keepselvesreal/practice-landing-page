# Test_Driven_Development_with_Java_Chapter_8_Test_Doubles_Stubs_and_Mocks

## 압축 내용

Test Double(스텁과 목)은 테스트하기 어려운 협력 객체를 대체하는 특수 객체로, 스텁은 미리 정해진 데이터를 제공하고(pull 모델), 목은 상호작용을 기록하고 검증하며(push 모델), 의존성 역전 원칙을 통해 주입되어 테스트 가능성을 높인다.

## 핵심 내용

1. **협력 객체 테스트의 문제** → [상세 내용 섹션 1, 2]
   - 반복 불가능한 동작(랜덤 값, 시간 등)은 assertion 작성 불가
   - 오류 조건 트리거가 어렵거나 불가능한 경우(배터리 방전, 네트워크 오류 등)
   - 빠르고 반복 가능한 테스트를 위해 Test Double 필요

2. **Test Double의 종류와 역할** → [상세 내용 섹션 3-5]
   - 스텁(Stub): 미리 정해진 결과 반환 - 데이터를 가져오는 pull 모델에 사용
   - 목(Mock): 상호작용 기록 및 검증 - 명령을 전달하는 push 모델에 사용
   - DIP를 통해 프로덕션 객체를 Test Double로 교체 가능하도록 설계

3. **Mockito를 이용한 Test Double 생성** → [상세 내용 섹션 6, 7]
   - @Mock 애노테이션과 when-thenReturn으로 스텁 간단 생성
   - verify() 메서드로 목 검증
   - doThrow()로 예외 상황 테스트
   - Argument Matcher로 유연한 파라미터 처리

**관계도**: DIP가 Test Double 주입을 가능하게 하고, 스텁과 목은 각각 다른 협력 패턴(pull vs push)에 사용되며, Mockito는 이들의 생성과 검증을 자동화한다.

## 상세 내용

### 목차

1. 협력 객체가 제시하는 테스트 문제
2. Test Double의 목적과 개념
3. 스텁(Stub)을 이용한 미리 정해진 결과 제공
4. 목(Mock)을 이용한 상호작용 검증
5. Test Double 사용이 적절한 경우와 부적절한 경우
6. Mockito 라이브러리 활용
7. 스텁을 이용한 오류 처리 코드 구현
8. Wordz 애플리케이션의 오류 조건 테스트
9. Test Double 사용 시 주의사항

---

### 1. 협력 객체가 제시하는 테스트 문제 → [핵심 개념 1]

**이전 내용과의 관계**: 소프트웨어 시스템이 성장하면서 단일 클래스를 넘어 여러 객체로 분할되며, 협력 객체가 등장한다.

소프트웨어가 성장하면 단일 클래스로는 부족해지고, 여러 객체로 분할된다. 테스트 대상(SUT)이 의존하는 다른 객체가 협력자(collaborator)다. 일부 협력자는 테스트를 어렵거나 불가능하게 만든다 (Lines 32-44).

**협력 객체의 두 가지 문제**:
1. 반복 불가능한 동작 (Lines 45-67)
2. 오류 처리 테스트의 어려움 (Lines 68-90)

**문제 1: 반복 불가능한 동작** (Lines 45-67)

```java
// 랜덤 값으로 인한 테스트 어려움
package examples;
import java.util.random.RandomGenerator;

public class DiceRoll {
    private final int NUMBER_OF_SIDES = 6;
    private final RandomGenerator rnd = RandomGenerator.getDefault();

    public String asText() {
        int rolled = rnd.nextInt(NUMBER_OF_SIDES) + 1;  // 매번 다른 값
        return String.format("You rolled a %d", rolled);
    }
}
// 문제: assertion에서 어떤 값을 기대해야 할지 알 수 없음
// rolled는 1~6 사이의 랜덤 값 - 예측 불가능
```

**Python 버전**:
```python
# 랜덤 값으로 인한 테스트 어려움
import random

class DiceRoll:
    def __init__(self):
        self.NUMBER_OF_SIDES = 6

    def as_text(self):
        rolled = random.randint(1, self.NUMBER_OF_SIDES)  # 매번 다른 값
        return f"You rolled a {rolled}"
# 문제: assertion에서 어떤 값을 기대해야 할지 알 수 없음
# rolled는 1~6 사이의 랜덤 값 - 예측 불가능
```

**문제 2: 오류 처리 테스트의 어려움** (Lines 68-90):

```java
// 오류 조건 트리거의 어려움
public class BatteryMonitor {
    public void warnWhenBatteryPowerLow() {
        if (DeviceApi.getBatteryPercentage() < 10) {  // 배터리 API 호출
            System.out.println("Warning - Battery low");
        }
    }
}
// 문제:
// - getBatteryPercentage()가 10 미만을 반환하도록 어떻게 강제할까?
// - 배터리를 방전시켜야 하나? 어떻게?
// - 실제로 배터리가 방전될 때까지 기다려야 하나?
// - 반환값을 제어할 방법이 없음
```

**Python 버전**:
```python
# 오류 조건 트리거의 어려움
class BatteryMonitor:
    def warn_when_battery_power_low(self):
        if DeviceApi.get_battery_percentage() < 10:  # 배터리 API 호출
            print("Warning - Battery low")
# 문제:
# - get_battery_percentage()가 10 미만을 반환하도록 어떻게 강제할까?
# - 배터리를 방전시켜야 하나? 어떻게?
# - 실제로 배터리가 방전될 때까지 기다려야 하나?
# - 반환값을 제어할 방법이 없음
```

**문제의 핵심** (Lines 91-96):
- TDD는 빠르고 반복 가능한 테스트 필요
- 예측 불가능한 동작이나 제어 불가능한 상황은 TDD에 문제 발생
- 해결책: 어려움의 원인 제거 - DIP + Test Double

(출처: Lines 32-96)

### 2. Test Double의 목적과 개념 → [핵심 개념 2]

**이전 내용과의 관계**: Chapter 7에서 배운 DIP를 Test Double과 결합하여 테스트 문제를 해결한다.

Test Double은 영화의 스턴트 배우처럼 실제 협력 객체를 대신하여 테스트를 가능하게 만드는 특수 객체다 (Lines 101-111).

**Test Double의 정의** (Lines 105-111):
- 테스트에서 사용하기 쉽도록 특별히 작성된 객체
- 영화 스턴트 배우처럼 실제 객체를 안전하게 대체
- Arrange 단계에서 SUT에 주입
- 프로덕션 코드에서는 실제 객체 주입

**DiceRoll 예제: DIP 적용 과정** (Lines 112-202)

**1단계: 인터페이스 추상화 생성** (Lines 115-118):

```java
// 랜덤 숫자 소스를 추상화
interface RandomNumbers {
    int nextInt(int upperBoundExclusive);
}
```

**Python 버전**:
```python
# 랜덤 숫자 소스를 추상화
from abc import ABC, abstractmethod

class RandomNumbers(ABC):
    @abstractmethod
    def next_int(self, upper_bound_exclusive):
        pass
```

**2단계: DiceRoll에 DIP 적용** (Lines 120-138):

```java
// DIP 적용: 추상화에 의존하도록 리팩토링
package examples;
import java.util.random.RandomGenerator;

public class DiceRoll {
    private final int NUMBER_OF_SIDES = 6;
    private final RandomNumbers rnd;  // 인터페이스 타입으로 변경

    public DiceRoll(RandomNumbers r) {  // 생성자 주입
        this.rnd = r;
    }

    public String asText() {
        int rolled = rnd.nextInt(NUMBER_OF_SIDES) + 1;  // 인터페이스 메서드 호출
        return String.format("You rolled a %d", rolled);
    }
}
// 장점: 어떤 RandomNumbers 구현체든 주입 가능
```

**Python 버전**:
```python
# DIP 적용: 추상화에 의존하도록 리팩토링
class DiceRoll:
    def __init__(self, random_numbers: RandomNumbers):  # 생성자 주입
        self.NUMBER_OF_SIDES = 6
        self.rnd = random_numbers  # 인터페이스 타입

    def as_text(self):
        rolled = self.rnd.next_int(self.NUMBER_OF_SIDES) + 1  # 인터페이스 메서드 호출
        return f"You rolled a {rolled}"
# 장점: 어떤 RandomNumbers 구현체든 주입 가능
```

**3단계: Test Double(Stub) 작성** (Lines 144-179):

```java
// 테스트: Test Double 사용
package examples;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;

class DiceRollTest {
    @Test
    void producesMessage() {
        var stub = new StubRandomNumbers();  // Test Double 생성
        var roll = new DiceRoll(stub);       // SUT에 주입
        var actual = roll.asText();
        assertThat(actual).isEqualTo("You rolled a 5");  // 예측 가능한 assertion
    }
}

// Test Double 구현: 항상 같은 값 반환
package examples;

public class StubRandomNumbers implements RandomNumbers {
    @Override
    public int nextInt(int upperBoundExclusive) {
        return 4;  // 항상 4 반환 (4+1=5)
    }
}
// 핵심:
// - RandomNumbers 인터페이스 구현 (LSP 준수)
// - 모든 호출에 동일한 값 반환 - 예측 가능
// - 랜덤 값 문제 해결
```

**Python 버전**:
```python
# 테스트: Test Double 사용
import pytest

class TestDiceRoll:
    def test_produces_message(self):
        stub = StubRandomNumbers()  # Test Double 생성
        roll = DiceRoll(stub)        # SUT에 주입
        actual = roll.as_text()
        assert actual == "You rolled a 5"  # 예측 가능한 assertion

# Test Double 구현: 항상 같은 값 반환
class StubRandomNumbers(RandomNumbers):
    def next_int(self, upper_bound_exclusive):
        return 4  # 항상 4 반환 (4+1=5)
# 핵심:
# - RandomNumbers 인터페이스 구현 (LSP 준수)
# - 모든 호출에 동일한 값 반환 - 예측 가능
# - 랜덤 값 문제 해결
```

**프로덕션 버전 만들기** (Lines 180-202):

```java
// 프로덕션용 RandomNumbers 구현
public class RandomlyGeneratedNumbers implements RandomNumbers {
    private final RandomGenerator rnd = RandomGenerator.getDefault();

    @Override
    public int nextInt(int upperBoundExclusive) {
        return rnd.nextInt(upperBoundExclusive);  // 실제 랜덤 값 생성
    }
}

// 프로덕션 코드 사용
public class DiceRollApp {
    public static void main(String[] args) {
        new DiceRollApp().run();
    }

    private void run() {
        var rnd = new RandomlyGeneratedNumbers();  // 프로덕션 구현체
        var roll = new DiceRoll(rnd);               // 주입
        System.out.println(roll.asText());
    }
}
// 핵심:
// - DiceRoll 클래스는 변경 불필요
// - 테스트에는 StubRandomNumbers 주입
// - 프로덕션에는 RandomlyGeneratedNumbers 주입
// - DIP로 인해 OCP 달성: 새 동작 추가 가능, 클래스 수정 불필요
```

**Python 버전**:
```python
# 프로덕션용 RandomNumbers 구현
import random

class RandomlyGeneratedNumbers(RandomNumbers):
    def next_int(self, upper_bound_exclusive):
        return random.randint(0, upper_bound_exclusive - 1)  # 실제 랜덤 값 생성

# 프로덕션 코드 사용
class DiceRollApp:
    def run(self):
        rnd = RandomlyGeneratedNumbers()  # 프로덕션 구현체
        roll = DiceRoll(rnd)               # 주입
        print(roll.as_text())

if __name__ == "__main__":
    DiceRollApp().run()
# 핵심:
# - DiceRoll 클래스는 변경 불필요
# - 테스트에는 StubRandomNumbers 주입
# - 프로덕션에는 RandomlyGeneratedNumbers 주입
# - DIP로 인해 OCP 달성: 새 동작 추가 가능, 클래스 수정 불필요
```

**용어 정리** (Lines 207-213):
- **Dependency Inversion(의존성 역전)**: 코드에 추상화 생성하는 설계 기법
- **Dependency Injection(의존성 주입)**: 런타임에 추상화 구현체를 공급하는 기법
- **Inversion of Control(IoC)**: 위 두 개념의 결합
- **IoC Container**: Spring, Guice, CDI 등 의존성 관리 프레임워크

(출처: Lines 101-234)

### 3. 스텁(Stub)을 이용한 미리 정해진 결과 제공 → [핵심 개념 2]

**이전 내용과의 관계**: Test Double의 한 종류인 스텁에 대해 구체적으로 배운다.

스텁은 제어할 수 없는 객체를 제어 가능한 테스트 전용 버전으로 교체하며, 항상 알려진 데이터 값을 제공한다 (Lines 239-263).

**스텁의 정의** (Lines 248-250):
- 값을 공급하는 Test Double
- 제어할 수 없는 객체를 제어 가능한 버전으로 교체
- 테스트 대상 코드가 소비할 알려진 데이터 값 생성

**스텁의 작동 원리** (Lines 251-263):

```
┌─────────────┐
│  Test Class │
└─────┬───────┘
      │ Arrange: SUT에 stub 연결
      ▼
┌─────────────┐        ┌─────────────┐
│     SUT     │◀───────│    Stub     │
└─────┬───────┘        └─────────────┘
      │                Known data values
      │ Act: SUT 실행
      ▼
┌─────────────┐
│   Assert    │
└─────────────┘
Expected behavior based on known data
```

**스텁이 작동하는 이유** (Lines 256-263):
- SUT는 자신의 로직만 테스트
- 의존성 자체의 동작은 테스트하지 않음
- Test Double을 테스트하는 것은 안티패턴
- DIP로 SUT가 협력자로부터 완전히 격리됨
- SUT에게는 데이터 출처가 중요하지 않음

**스텁 사용 시나리오** (Lines 269-286):
- 저장소 인터페이스/데이터베이스 스텁
- 참조 데이터 소스 스텁 (properties 파일, 웹 서비스)
- HTML이나 JSON 변환 코드 테스트용 입력 데이터
- 시스템 시계 스텁 - 시간 의존 동작 테스트
- 랜덤 숫자 생성기 스텁 - 예측 가능성 확보
- 인증 시스템 스텁 - 테스트 사용자 로그인 허용
- 서드파티 웹 서비스 응답 스텁 (결제 제공자 등)
- OS 명령 호출 스텁 (디렉토리 목록 등)

**Pull 모델 vs Push 모델** (Lines 287-292):
- **Pull 모델**: SUT가 다른 곳에서 객체를 가져옴 - 스텁 사용
- **Push 모델**: SUT가 다른 객체의 메서드 호출 - 목(Mock) 필요
- 스텁은 메서드 호출 확인 불가 - 다음 섹션에서 목 다룸

(출처: Lines 239-292)

### 4. 목(Mock)을 이용한 상호작용 검증 → [핵심 개념 2]

**이전 내용과의 관계**: 스텁은 pull 모델에 적합하지만, push 모델에는 목이 필요하다.

목은 상호작용을 기록하는 Test Double로, "SUT가 메서드를 올바르게 호출했는가?"라는 질문에 답한다 (Lines 293-301).

**목의 정의** (Lines 296-301):
- 상호작용을 기록하는 Test Double
- 스텁과 달리 객체를 제공하지 않고 상호작용 기록
- Push 모델 상호작용 검증에 완벽
- SUT가 협력자에게 명령을 내렸는지 확인
- 메서드 호출과 필요한 파라미터 검증

**목의 작동 원리** (Lines 306-310):

```
┌─────────────┐
│  Test Class │
└─────┬───────┘
      │ Arrange: SUT에 mock 연결
      ▼
┌─────────────┐        ┌─────────────┐
│     SUT     │────────│    Mock     │
└─────┬───────┘        └─────────────┘
      │                Records method calls
      │ Act: SUT 실행
      │ Assert: Mock에서 호출 확인
      ▼
┌─────────────┐
│   Verify    │
└─────────────┘
```

**MailServer 예제** (Lines 311-368):

**인터페이스 정의** (Lines 314-317):
```java
// 메일 서버 추상화
public interface MailServer {
    void sendEmail(String recipient, String subject, String text);
}
```

**Python 버전**:
```python
# 메일 서버 추상화
from abc import ABC, abstractmethod

class MailServer(ABC):
    @abstractmethod
    def send_email(self, recipient, subject, text):
        pass
```

**Mock 구현** (Lines 321-338):

```java
// 수작업 Mock 구현
public class MockMailServer implements MailServer {
    boolean wasCalled;          // 호출 여부 기록
    String actualRecipient;     // 실제 받은 파라미터 기록
    String actualSubject;
    String actualText;

    @Override
    public void sendEmail(String recipient, String subject, String text) {
        wasCalled = true;       // 호출되었음을 기록
        actualRecipient = recipient;    // 파라미터 값 저장
        actualSubject = subject;
        actualText = text;
    }
}
// 핵심: sendEmail() 호출 사실과 파라미터 값을 필드에 기록
// 테스트 코드가 이 필드들을 사용하여 assertion 작성
```

**Python 버전**:
```python
# 수작업 Mock 구현
class MockMailServer(MailServer):
    def __init__(self):
        self.was_called = False      # 호출 여부 기록
        self.actual_recipient = None # 실제 받은 파라미터 기록
        self.actual_subject = None
        self.actual_text = None

    def send_email(self, recipient, subject, text):
        self.was_called = True       # 호출되었음을 기록
        self.actual_recipient = recipient    # 파라미터 값 저장
        self.actual_subject = subject
        self.actual_text = text
# 핵심: send_email() 호출 사실과 파라미터 값을 필드에 기록
# 테스트 코드가 이 필드들을 사용하여 assertion 작성
```

**Mock 사용 테스트** (Lines 345-368):

```java
// Mock을 사용한 테스트
@Test
public void sendsWelcomeEmail() {
    var mailServer = new MockMailServer();           // Mock 생성
    var notifications = new UserNotifications(mailServer);  // SUT에 주입

    notifications.welcomeNewUser();                  // Act: SUT 실행

    // Assert: Mock에 기록된 상호작용 검증
    assertThat(mailServer.wasCalled).isTrue();
    assertThat(mailServer.actualRecipient).isEqualTo("test@example.com");
    assertThat(mailServer.actualSubject).isEqualTo("Welcome!");
    assertThat(mailServer.actualText).contains("Welcome to your account");
}
// 논리적으로는 하나의 assert - "sendEmail()이 올바르게 호출되었는가?"
```

**Python 버전**:
```python
# Mock을 사용한 테스트
def test_sends_welcome_email():
    mail_server = MockMailServer()                    # Mock 생성
    notifications = UserNotifications(mail_server)    # SUT에 주입

    notifications.welcome_new_user()                  # Act: SUT 실행

    # Assert: Mock에 기록된 상호작용 검증
    assert mail_server.was_called is True
    assert mail_server.actual_recipient == "test@example.com"
    assert mail_server.actual_subject == "Welcome!"
    assert "Welcome to your account" in mail_server.actual_text
# 논리적으로는 하나의 assert - "send_email()이 올바르게 호출되었는가?"
```

**목의 장점** (Lines 363-368):
- 제어하기 어려운 객체와의 상호작용 기록
- 실제 이메일 전송 불필요 - 느리고 불안정
- 테스트 사용자의 메일함 모니터링 불필요
- SUT 책임 범위만 테스트 - sendEmail() 호출 확인
- 그 이후 일어나는 일은 SUT 범위 밖 - 테스트 범위 밖

**프로덕션 구현** (Lines 373-377):
- DIP 덕분에 프로덕션 코드 생성 용이
- SMTP 프로토콜로 실제 메일 서버와 통신하는 구현 필요
- 라이브러리 클래스 검색 후 간단한 어댑터 작성

(출처: Lines 293-380)

### 5. Test Double 사용이 적절한 경우와 부적절한 경우 → [핵심 개념 3]

**이전 내용과의 관계**: Test Double은 유용하지만 항상 적절한 것은 아니다. 올바른 사용법을 이해해야 한다.

목을 포함한 Test Double은 유용하지만 특정 상황에서는 피해야 한다 (Lines 381-472).

**피해야 할 상황**:

**1. Mock 과다 사용** (Lines 387-397)

```java
// 나쁜 예: 구현 세부사항을 목으로 만듦
// TDD 테스트의 정의: 동작 검증, 구현과 독립적
// 문제: 추상화가 아닌 구현 세부사항에 대한 Mock 생성

// Mock이 구현 세부사항과 결합되면:
// - 특정 구현과 코드 구조에 고정됨
// - 구현 변경 시 테스트도 변경 필요
// - 같은 결과를 내는 새 구현도 테스트 실패 가능
// - 리팩토링과 새 기능 추가를 적극적으로 방해

// 원칙: 진짜 추상화에 대해서만 Mock 사용
```

**Python 버전**:
```python
# 나쁜 예: 구현 세부사항을 목으로 만듦
# TDD 테스트의 정의: 동작 검증, 구현과 독립적
# 문제: 추상화가 아닌 구현 세부사항에 대한 Mock 생성

# Mock이 구현 세부사항과 결합되면:
# - 특정 구현과 코드 구조에 고정됨
# - 구현 변경 시 테스트도 변경 필요
# - 같은 결과를 내는 새 구현도 테스트 실패 가능
# - 리팩토링과 새 기능 추가를 적극적으로 방해

# 원칙: 진짜 추상화에 대해서만 Mock 사용
```

**2. 자신이 소유하지 않은 코드에 Mock 사용 금지** (Lines 398-414)

```java
// 나쁜 예: 외부 라이브러리 클래스에 대한 Mock
// 문제 시나리오:
// - PdfGenerator 외부 라이브러리 사용 중
// - PdfGenerator를 Mock으로 대체하여 테스트 작성
// - 미래에 라이브러리 업데이트 시 메서드 변경/삭제
// - 프로덕션 코드는 컴파일 실패
// - 하지만 Mock은 여전히 예전 메서드 가짐 - 테스트 통과
// - 미래 유지보수자를 위한 미묘한 함정

// 해결책:
// - 서드파티 라이브러리를 래핑
// - 인터페이스 뒤에 배치하여 의존성 역전
// - 완전히 격리
```

**Python 버전**:
```python
# 나쁜 예: 외부 라이브러리 클래스에 대한 Mock
# 문제 시나리오:
# - PdfGenerator 외부 라이브러리 사용 중
# - PdfGenerator를 Mock으로 대체하여 테스트 작성
# - 미래에 라이브러리 업데이트 시 메서드 변경/삭제
# - 프로덕션 코드는 실패
# - 하지만 Mock은 여전히 예전 메서드 가짐 - 테스트 통과
# - 미래 유지보수자를 위한 미묘한 함정

# 해결책:
# - 서드파티 라이브러리를 래핑
# - 인터페이스 뒤에 배치하여 의존성 역전
# - 완전히 격리
```

**3. 값 객체(Value Object)에 Mock 사용 금지** (Lines 415-427)

```java
// 값 객체: 특정 정체성이 없고 포함된 데이터로만 정의되는 객체
// 예시: Integer, String
// - 두 문자열이 같은 텍스트를 포함하면 동일하다고 간주
// - 메모리 상 다른 객체여도 값이 같으면 동일

// Java에서 값 객체 식별: equals()와 hashCode() 메서드 재정의
// - 기본: Java는 객체 정체성(identity)으로 동등성 비교
// - 값 객체: 내용 기반으로 equals()와 hashCode() 재정의

// 값 객체는 단순 - 생성하기 쉬움
// Mock 생성할 이유 없음 - 그냥 값 객체 생성하여 테스트에 사용
```

**Python 버전**:
```python
# 값 객체: 특정 정체성이 없고 포함된 데이터로만 정의되는 객체
# 예시: int, str
# - 두 문자열이 같은 텍스트를 포함하면 동일하다고 간주
# - 메모리 상 다른 객체여도 값이 같으면 동일

# Python에서 값 객체 식별: __eq__와 __hash__ 메서드 재정의
# - 기본: Python은 객체 정체성(identity)으로 동등성 비교
# - 값 객체: 내용 기반으로 __eq__와 __hash__ 재정의

# 값 객체는 단순 - 생성하기 쉬움
# Mock 생성할 이유 없음 - 그냥 값 객체 생성하여 테스트에 사용
```

**4. 의존성 주입 없이는 Mock 사용 불가** (Lines 428-450)

```java
// 나쁜 예: new 키워드로 구체 클래스 생성
package examples;

public class UserGreeting {
    private final UserProfiles profiles
        = new UserProfilesPostgres();  // 구체 클래스 직접 생성

    public String formatGreeting(UserId id) {
        return String.format("Hello and welcome, %s",
                profiles.fetchNicknameFor(id));
    }
}
// 문제:
// - profiles 필드가 구체 클래스로 초기화됨
// - Test Double 주입 방법 없음
// - Java Reflection으로 우회 시도 가능하지만 바람직하지 않음

// 해결책:
// - 의존성 주입 허용하도록 설계 변경
// - 이전 예제처럼 생성자 파라미터로 주입
// - 레거시 코드에서 흔한 문제
// - TDD 피드백: 설계 한계를 알려줌
```

**Python 버전**:
```python
# 나쁜 예: 구체 클래스 직접 생성
class UserGreeting:
    def __init__(self):
        self.profiles = UserProfilesPostgres()  # 구체 클래스 직접 생성

    def format_greeting(self, user_id):
        return f"Hello and welcome, {self.profiles.fetch_nickname_for(user_id)}"
# 문제:
# - profiles가 구체 클래스로 초기화됨
# - Test Double 주입 방법 없음
# - 우회 방법이 있지만 바람직하지 않음

# 해결책:
# - 의존성 주입 허용하도록 설계 변경
# - 이전 예제처럼 생성자 파라미터로 주입
# - 레거시 코드에서 흔한 문제
# - TDD 피드백: 설계 한계를 알려줌
```

**5. Mock을 테스트하지 말 것** (Lines 451-459)

```python
# "Mock을 테스트한다"는 표현: Test Double에 너무 많은 가정이 내장된 테스트
# 나쁜 예:
# - 데이터베이스 접근을 대체하는 스텁 작성
# - 스텁에 특정 쿼리를 에뮬레이트하는 수백 줄의 코드
# - 테스트 assertion이 모두 그 상세 쿼리 기반

# 문제:
# - SUT 로직이 쿼리에 응답하는지 증명
# - 하지만 스텁이 실제 데이터 접근 코드 동작에 대해 많은 가정
# - 스텁 코드와 실제 코드가 빠르게 불일치
# - 결과: 통과하지만 무효한 단위 테스트
# - 스텁 응답이 현실에서 더 이상 발생하지 않을 수 있음
```

**목 사용이 적절한 경우** (Lines 460-468):
- Push 모델 사용 시 - 명백한 응답이 없는 다른 컴포넌트에 액션 요청:
  - 원격 서비스에 액션 요청 (메일 서버에 이메일 전송)
  - 데이터베이스에 데이터 삽입/삭제
  - TCP 소켓이나 시리얼 인터페이스로 명령 전송
  - 캐시 무효화
  - 로그 파일이나 분산 로깅 엔드포인트에 로그 정보 작성

(출처: Lines 381-472)

### 6. Mockito 라이브러리 활용 → [핵심 개념 3]

**이전 내용과의 관계**: 수작업 Test Double 작성은 반복적이고 시간 소모적이다. Mockito가 이를 자동화한다.

Mockito는 Test Double 생성을 자동화하는 MIT 라이선스의 무료 오픈소스 라이브러리다 (Lines 477-485).

**Mockito 시작하기** (Lines 486-499):

```gradle
// build.gradle 의존성 추가
dependencies {
    testImplementation 'org.junit.jupiter:junit-jupiter-api:5.8.2'
    testRuntimeOnly 'org.junit.jupiter:junit-jupiter-engine:5.8.2'
    testImplementation 'org.assertj:assertj-core:3.22.0'
    testImplementation 'org.mockito:mockito-core:4.8.0'
    testImplementation 'org.mockito:mockito-junit-jupiter:4.8.0'  // JUnit5 통합
}
```

**Mockito로 스텁 작성 (TDD 단계별)** (Lines 500-715):

**1단계: 테스트 클래스에 Mockito 통합** (Lines 505-517):

```java
// Mockito와 JUnit5 통합
package examples;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)  // Mockito 활성화
public class UserGreetingTest {
}
// @ExtendWith 애노테이션이 JUnit5 테스트 실행 시 Mockito 라이브러리 실행
```

**Python 버전**:
```python
# Python에서는 pytest-mock 사용
# pip install pytest-mock
import pytest
from pytest_mock import MockerFixture

class TestUserGreeting:
    pass
# Pytest fixture를 통해 Mockito 유사 기능 제공
```

**2-9단계: TDD로 SUT 구현** (Lines 519-644)

```java
// 최종 테스트 코드 (단계 10: @Mock 추가 전)
@ExtendWith(MockitoExtension.class)
public class UserGreetingTest {
    private static final UserId USER_ID = new UserId("1234");
    private UserProfiles profiles;  // 아직 초기화 안됨

    @Test
    void formatsGreetingWithName() {
        var greeting = new UserGreeting(profiles);
        String actual = greeting.formatGreeting(USER_ID);
        assertThat(actual).isEqualTo("Hello and welcome, Alan");
    }
}

// SUT: UserGreeting 클래스
public class UserGreeting {
    private final UserProfiles profiles;

    public UserGreeting(UserProfiles profiles) {
        this.profiles = profiles;
    }

    public String formatGreeting(UserId id) {
        return String.format("Hello and Welcome, %s",
                profiles.fetchNicknameFor(id));
    }
}

// 인터페이스: UserProfiles
public interface UserProfiles {
    String fetchNicknameFor(UserId id);
}
```

**Python 버전**:
```python
# 최종 테스트 코드 (@Mock 추가 전)
from abc import ABC, abstractmethod

class TestUserGreeting:
    def test_formats_greeting_with_name(self, mocker):
        USER_ID = UserId("1234")
        profiles = None  # 아직 초기화 안됨

        greeting = UserGreeting(profiles)
        actual = greeting.format_greeting(USER_ID)
        assert actual == "Hello and welcome, Alan"

# SUT: UserGreeting 클래스
class UserGreeting:
    def __init__(self, profiles: 'UserProfiles'):
        self.profiles = profiles

    def format_greeting(self, user_id):
        return f"Hello and Welcome, {self.profiles.fetch_nickname_for(user_id)}"

# 인터페이스: UserProfiles
class UserProfiles(ABC):
    @abstractmethod
    def fetch_nickname_for(self, user_id):
        pass
```

**10-11단계: Mockito @Mock과 설정** (Lines 645-709):

```java
// @Mock 애노테이션 추가 및 설정
import org.mockito.Mock;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class UserGreetingTest {
    private static final UserId USER_ID = new UserId("1234");

    @Mock  // Mockito가 자동으로 Mock 객체 생성
    private UserProfiles profiles;

    @Test
    void formatsGreetingWithName() {
        // Stub 설정: when-thenReturn 패턴
        when(profiles.fetchNicknameFor(USER_ID))
           .thenReturn("Alan");

        var greeting = new UserGreeting(profiles);
        String actual = greeting.formatGreeting(USER_ID);
        assertThat(actual).isEqualTo("Hello and welcome, Alan");
    }
}
// 핵심:
// - @Mock으로 Mock 객체 자동 생성
// - when().thenReturn()으로 스텁 동작 설정
// - 수작업 스텁 작성 불필요
```

**Python 버전**:
```python
# pytest-mock을 사용한 Mock과 설정
class TestUserGreeting:
    def test_formats_greeting_with_name(self, mocker):
        USER_ID = UserId("1234")

        # Mock 객체 생성
        profiles = mocker.Mock(spec=UserProfiles)

        # Stub 설정
        profiles.fetch_nickname_for.return_value = "Alan"

        greeting = UserGreeting(profiles)
        actual = greeting.format_greeting(USER_ID)
        assert actual == "Hello and welcome, Alan"
# 핵심:
# - mocker.Mock()으로 Mock 객체 생성
# - return_value로 스텁 동작 설정
# - 수작업 스텁 작성 불필요
```

**Mockito로 Mock 작성** (Lines 716-748):

```java
// Mockito로 Mock 객체 사용
@ExtendWith(MockitoExtension.class)
class WelcomeEmailTest {
    @Mock  // 스텁과 동일하게 @Mock 사용
    private MailServer mailServer;

    @Test
    public void sendsWelcomeEmail() {
        var notifications = new UserNotifications(mailServer);
        notifications.welcomeNewUser("test@example.com");

        // verify() 메서드로 상호작용 검증
        verify(mailServer).sendEmail("test@example.com",
                "Welcome!",
                "Welcome to your account");
    }
}
// 핵심:
// - @Mock 애노테이션은 스텁과 목 모두 사용
// - verify()로 메서드 호출 확인
// - 파라미터 값도 함께 검증
// - Mockito가 코드 생성으로 모든 호출 가로채어 저장
```

**Python 버전**:
```python
# pytest-mock으로 Mock 객체 사용
class TestWelcomeEmail:
    def test_sends_welcome_email(self, mocker):
        mail_server = mocker.Mock(spec=MailServer)
        notifications = UserNotifications(mail_server)

        notifications.welcome_new_user("test@example.com")

        # assert_called_with()로 상호작용 검증
        mail_server.send_email.assert_called_with(
            "test@example.com",
            "Welcome!",
            "Welcome to your account"
        )
# 핵심:
# - mocker.Mock()은 스텁과 목 모두 사용
# - assert_called_with()로 메서드 호출 확인
# - 파라미터 값도 함께 검증
```

**Mockito 구문 주의사항** (Lines 749-752):
```java
// when()과 verify()의 미묘하게 다른 구문
when(object.method()).thenReturn(expected_value);  // when: method() 실행
verify(object).method();                            // verify: method 참조만
```

**Stub과 Mock 구분 흐림** (Lines 753-759):
- Mockito는 스텁과 목 구분을 흐림
- @Mock으로 생성된 Test Double을 스텁, 목, 또는 둘 다로 사용 가능
- 하나의 Test Double을 스텁과 목 둘 다로 설정하는 것은 테스트 코드 스멜
- 잘못된 것은 아니지만 멈춰서 생각해볼 가치 있음
- 협력자가 여러 책임을 섞었을 가능성 - 객체 분할 고려

**Argument Matcher - Test Double 동작 커스터마이징** (Lines 760-809):

```java
// Argument Matcher로 유연한 파라미터 처리
import static org.mockito.ArgumentMatchers.any;

@Test
void formatsGreetingWithName() {
    when(profiles.fetchNicknameFor(any()))  // any(): 모든 UserId 허용
       .thenReturn("Alan");

    var greeting = new UserGreeting(profiles);
    String actual = greeting.formatGreeting(new UserId(""));  // 빈 문자열도 OK
    assertThat(actual).isEqualTo("Hello and welcome, Alan");
}
// 장점:
// - 특정 파라미터 값에 구애받지 않음
// - 테스트에서 중요한 것과 중요하지 않은 것 명확히 구분
// - null, 알 수 없는 값 등 다양한 파라미터 처리
```

**Python 버전**:
```python
# Argument Matcher로 유연한 파라미터 처리
from unittest.mock import ANY

def test_formats_greeting_with_name(mocker):
    profiles = mocker.Mock(spec=UserProfiles)
    profiles.fetch_nickname_for.return_value = "Alan"  # 모든 인자에 대해 "Alan" 반환

    greeting = UserGreeting(profiles)
    actual = greeting.format_greeting(UserId(""))  # 빈 문자열도 OK
    assert actual == "Hello and welcome, Alan"

    # 호출 검증 시 ANY 사용 가능
    profiles.fetch_nickname_for.assert_called_with(ANY)
# 장점:
# - 특정 파라미터 값에 구애받지 않음
# - 테스트에서 중요한 것과 중요하지 않은 것 명확히 구분
```

(출처: Lines 477-809)

### 7. 스텁을 이용한 오류 처리 코드 구현 → [핵심 개념 3]

**이전 내용과의 관계**: 스텁의 훌륭한 활용 사례는 오류 조건 테스트다.

오류 조건을 잘 처리하는지 확인하려면 스텁을 사용하여 오류를 발생시켜야 한다 (Lines 810-862).

**오류 조건 테스트의 중요성** (Lines 813-823):
- 일부 오류 조건은 테스트하기 쉬움 (예: 입력 검증기 - 잘못된 데이터 제공)
- 하지만 SUT가 협력자가 발생시킨 오류에 응답하는 코드는 어려움
- 오류 보고 메커니즘에 따라 테스트 방법 다름:
  - 상태 코드: 스텁에서 오류 코드 반환
  - 예외: 스텁에서 예외 발생

**Mockito doThrow()로 예외 테스트** (Lines 824-862):

```java
// 예외 발생 스텁 테스트
@Test
public void rejectsInvalidEmailRecipient() {
    // doThrow()로 예외 발생 설정
    doThrow(new IllegalArgumentException())
        .when(mailServer).sendEmail(any(), any(), any());

    var notifications = new UserNotifications(mailServer);

    // assertThatExceptionOfType()로 예외 검증
    assertThatExceptionOfType(NotificationFailureException.class)
            .isThrownBy(() -> notifications
                    .welcomeNewUser("not-an-email-address"));
}
// 작동 방식:
// 1. doThrow(): sendEmail() 호출 시 IllegalArgumentException 발생 설정
// 2. any(): 어떤 파라미터든 예외 발생
// 3. SUT가 sendEmail() 호출하면 예외 발생
// 4. SUT는 예외를 잡아서 NotificationFailureException으로 재포장
// 5. assertThatExceptionOfType()이 올바른 예외가 발생했는지 검증
```

**Python 버전**:
```python
# 예외 발생 스텁 테스트
import pytest

def test_rejects_invalid_email_recipient(mocker):
    mail_server = mocker.Mock(spec=MailServer)
    # side_effect로 예외 발생 설정
    mail_server.send_email.side_effect = IllegalArgumentException()

    notifications = UserNotifications(mail_server)

    # pytest.raises()로 예외 검증
    with pytest.raises(NotificationFailureException):
        notifications.welcome_new_user("not-an-email-address")
# 작동 방식:
# 1. side_effect: send_email() 호출 시 IllegalArgumentException 발생 설정
# 2. SUT가 send_email() 호출하면 예외 발생
# 3. SUT는 예외를 잡아서 NotificationFailureException으로 재포장
# 4. pytest.raises()가 올바른 예외가 발생했는지 검증
```

**설계 결정 포착** (Lines 844-860):
- sendEmail()이 IllegalArgumentException을 던져 잘못된 이메일 주소 보고
- SUT는 이를 NotificationFailureException으로 래핑하여 재발생
- 새 예외는 사용자 알림 책임과 관련
- 시스템 계층화 고려사항: 원본 예외를 이 계층에 더 적합한 일반적 예외로 교체

**TDD로 예외 처리 구현**:
1. 테스트 작성: 예외 발생 확인
2. 코드 작성: InvalidArgumentException에 대한 catch 핸들러
3. NotificationFailureException 발생 (RuntimeException 확장)
4. 알림 전송 실패를 보고하는 새 계층 적합 예외

(출처: Lines 810-862)

### 8. Wordz 애플리케이션의 오류 조건 테스트

**이전 내용과의 관계**: 배운 내용을 Wordz 애플리케이션에 적용한다.

WordSelection 클래스가 랜덤으로 단어를 선택하되, 단어가 없을 때 오류를 처리하는 테스트를 작성한다 (Lines 863-927).

**설계 결정** (Lines 864-872):
- WordRepository 인터페이스: 저장된 단어에 접근
- fetchWordByNumber(wordNumber): 번호로 단어 가져오기
- 단어는 1부터 시작하는 순차 번호로 저장
- WordSelection 클래스: 랜덤 번호 선택하여 단어 가져오기
- RandomNumbers 인터페이스 재사용

**테스트 코드** (Lines 877-905):

```java
// Wordz의 오류 조건 테스트
@ExtendWith(MockitoExtension.class)
public class WordSelectionTest {
    @Mock
    private WordRepository repository;
    @Mock
    private RandomNumbers random;

    @Test
    public void reportsWordNotFound() {
        // doThrow()로 WordRepositoryException 발생 설정
        doThrow(new WordRepositoryException())
                .when(repository)
                  .fetchWordByNumber(anyInt());  // 어떤 번호든 예외 발생

        var selection = new WordSelection(repository, random);

        // WordSelectionException 발생 확인
        assertThatExceptionOfType(WordSelectionException.class)
                .isThrownBy(() -> selection.getRandomWord());
    }
}
// 설계 결정:
// - WordRepository.fetchWordByNumber()는 문제 발생 시 WordRepositoryException
// - WordSelection.getRandomWord()는 완료 불가 시 WordSelectionException
// - 계층별로 적절한 예외 사용
```

**Python 버전**:
```python
# Wordz의 오류 조건 테스트
import pytest

class TestWordSelection:
    def test_reports_word_not_found(self, mocker):
        repository = mocker.Mock(spec=WordRepository)
        random_gen = mocker.Mock(spec=RandomNumbers)

        # side_effect로 WordRepositoryException 발생 설정
        repository.fetch_word_by_number.side_effect = WordRepositoryException()

        selection = WordSelection(repository, random_gen)

        # WordSelectionException 발생 확인
        with pytest.raises(WordSelectionException):
            selection.get_random_word()
# 설계 결정:
# - WordRepository.fetch_word_by_number()는 문제 발생 시 WordRepositoryException
# - WordSelection.get_random_word()는 완료 불가 시 WordSelectionException
# - 계층별로 적절한 예외 사용
```

**테스트 단계 분석** (Lines 901-921):

1. **Arrange 단계**:
   - doThrow()로 repository가 예외를 던지도록 설정
   - anyInt(): 어떤 파라미터든 예외 발생
   - @Mock으로 repository와 random 스텁 생성
   - WordSelection SUT 생성 및 두 협력자 주입

2. **Act & Assert 단계 통합**:
   - assertThatExceptionOfType()로 예외 클래스 지정
   - isThrownBy()로 Act 단계 실행 (람다 함수)
   - getRandomWord() 호출 → 실패하여 예외 발생 예상
   - 올바른 예외 클래스가 던져졌는지 확인

3. **구현**:
   - 테스트 실행 → 실패 확인
   - 필요한 로직 추가하여 테스트 통과

**테스트의 결합도** (Lines 922-927):
- 테스트가 특정 구현에 많은 설계 결정 포함
- 어떤 예외가 발생하는지, 어디에 사용되는지
- 예외가 오류 보고에 사용된다는 사실까지
- 하지만 책임 분할과 컴포넌트 간 계약 정의로서는 합리적
- 모든 것이 테스트에 포착됨

(출처: Lines 863-927)

### 9. Test Double 사용 시 주의사항

**요약** (Lines 928-940):
- 문제 있는 협력자 테스트 문제 해결
- 협력자 대신 사용할 Test Double 사용법 학습
- Test Double로 테스트 코드에서 협력자 제어

**Test Double의 두 가지 종류**:
- **스텁(Stub)**: 데이터 반환
- **목(Mock)**: 메서드 호출 검증

**Mockito의 이점**:
- 스텁과 목을 자동 생성
- AssertJ와 함께 사용하여 다양한 조건 검증
- 예외를 던지는 오류 조건 테스트

**주요 교훈** (Lines 945-968):

**Q1: Stub과 Mock은 상호 교환 가능한가?** (Lines 947-952)
- 일상 대화에서는 혼용 가능
- 정확성보다 유창성을 위해
- 중요: 각 Test Double 종류의 다른 용도 이해
- 대화 시 지나치게 엄격할 필요 없음
- Test Double이 일반 용어, 특정 타입이 다른 역할을 가짐

**Q2: "Mock을 테스트한다"는 문제는 무엇인가?** (Lines 954-959)
- SUT에 실제 로직이 없는데 테스트 작성하려 할 때 발생
- Test Double을 연결하고 테스트 작성
- Assertion이 Test Double이 올바른 데이터를 반환했는지만 확인
- 잘못된 레벨에서 테스트했다는 지표
- 잘못된 코드 커버리지 목표나 메서드당 테스트 규칙에 의해 발생
- 이런 테스트는 가치 없음 - 제거해야 함

**Q3: Test Double은 어디서나 사용 가능한가?** (Lines 961-968)
- 아니오. DIP를 사용하여 설계해야만 가능
- Test Double을 프로덕션 객체 대신 교체할 수 있어야 함
- TDD는 이런 설계 이슈를 일찍 생각하도록 강제
- 나중에 테스트 작성 시 Test Double 주입 접근이 부족하면 어려움
- 레거시 코드는 특히 어려움
- 추천: Michael Feathers의 "Working Effectively with Legacy Code" 책 참고

**다음 장 예고** (Lines 938-940):
- 유용한 시스템 설계 기법
- 대부분 코드를 FIRST 단위 테스트 아래 두기
- 제어할 수 없는 외부 시스템과의 협력 테스트 문제 회피

(출처: Lines 928-968)

---

## 요약 (Lines 928-940)

이 장에서는 문제 있는 협력자를 테스트하는 문제를 해결하는 방법을 살펴보았다. 협력자 대신 사용할 Test Double이라는 대체 객체 사용법을 배웠다. Test Double이 테스트 코드 내에서 협력자가 하는 일을 간단하게 제어할 수 있게 해준다는 것을 학습했다.

특히 유용한 두 가지 종류의 Test Double은 스텁과 목이다. 스텁은 데이터를 반환하고, 목은 메서드가 호출되었는지 검증한다. Mockito 라이브러리를 사용하여 스텁과 목을 자동으로 생성하는 방법을 배웠다.

AssertJ를 사용하여 Test Double의 다양한 조건에서 SUT가 올바르게 동작했는지 검증하는 방법을 배웠다. 예외를 던지는 오류 조건을 테스트하는 방법도 학습했다.

이러한 기술들은 테스트 작성을 위한 도구 상자를 확장했다.

다음 장에서는 대부분의 코드를 FIRST 단위 테스트 아래 두면서 동시에 제어할 수 없는 외부 시스템과의 협력 테스트 문제를 피할 수 있는 매우 유용한 시스템 설계 기법을 다룬다.

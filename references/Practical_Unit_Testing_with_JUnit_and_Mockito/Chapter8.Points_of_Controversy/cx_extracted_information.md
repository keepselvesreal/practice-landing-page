## 압축 내용
테스트 가시성, 데이터 생성, 캡슐화 우회, 인수 검증, 파일·DB 사용 같은 논쟁거리를 맥락별 선택 기준과 실전 기법으로 정리한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:9; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:660; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:718; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1174; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1386).

## 핵심 내용
**핵심 개념**
- 테스트 코드의 가시성과 구성은 접근 제한자 선택, 픽스처 배치, 단언 구조, 소프트 단언 사용 여부로 균형 잡는다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:10; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:238; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:312; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:454).
- 난수·속성 기반·인수 캡처는 테스트 데이터 다양성과 재현성을 높이되 제약·한계를 명확히 제어해야 한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:20; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:67; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:134; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1305).
- 프라이빗 메서드·람다·new 연산자·정적 호출은 리팩터링, 서브클래싱, 부분 모킹, 파워모킹 등으로 제어하며 설계 품질과 테스트 용이성을 저울질한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:479; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:660; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:718; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:808; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:883; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:940; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1016).

**압축 설명**
- 가시성·구성 선택: 테스트 클래스는 필요 시 private을 생략하고, 픽스처는 선언부·테스트·setUp에서 혼합 구성하며, 단언 개수는 SRP 준수 범위에서 조정하고 소프트 단언은 장기 실행 시나리오에만 제한적으로 활용한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:10; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:238; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:435; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:454).
- 난수·속성 기반·인수 캡처: 랜덤 입력은 경계·가독성·재현성 전략과 병행하고, ArgumentCaptor·Hamcrest 등으로 전달 인수를 검증해 설계 냄새를 드러낸다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:65; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:134; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1305; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1355).
- 캡슐화·생성 우회 전략: 프라이빗 메서드는 리팩터링·리플렉션·접근 완화·PowerMock 중 상황에 맞춰 선택하고, 람다나 new는 메서드 추출·DI·서브클래스·spy로 seam을 만든다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:545; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:622; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:660; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:718; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:940; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1045).

**개념 관계**
- DRY·가독성·일관성 같은 테스트 설계 원칙 위에 난수 제어와 seam 추출을 결합하면, 설계 냄새를 경고로 활용하며 도구적 해결(파워모킹)보다 구조적 개선을 우선하게 된다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:271; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:435; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:853; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1158).

## 상세 핵심 내용
**중요 개념**
- 테스트 가시성과 픽스처 구성의 유연성 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:10; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:238)
- 난수·속성 기반 테스트의 가치와 주의사항 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:65; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:134)
- 캡슐화 우회 전략: 프라이빗·람다·new·정적 호출 대응 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:545; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:660; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:808)
- 인수 캡처와 파일·DB 사용에 대한 현대적 시각 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1174; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1386)

**상세 설명**
- 테스트 가시성과 픽스처 구성의 유연성: 테스트 클래스는 private 생략을 통해 가독성을 확보하거나, 선언부·setUp·테스트 본문을 적절히 섞어 픽스처 DRY와 시나리오별 구성을 조화시킨다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:14; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:238; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:271).
- 난수·속성 기반 테스트의 가치와 주의사항: 랜덤 값은 다양한 입력을 탐색하지만 경계 값 통제, 재현 가능한 시드 기록, 실패 데이터의 고정 등이 필수이며, property-based 테스트는 알고리즘적 제약을 기술할 때 진가를 발휘한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:65; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:134; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:178).
- 캡슐화 우회 전략: 프라이빗 메서드·람다·new·정적 호출은 리팩터링, ReflectionUtils, 접근 완화, PowerMock, DI, 서브클래싱, spy 등을 활용하며 설계 개선과 테스트 비용 사이의 절충이 필요하다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:545; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:622; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:660; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:808; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1045).
- 인수 캡처와 파일·DB 사용에 대한 현대적 시각: ArgumentCaptor·Hamcrest로 전달 객체를 조사하고 equals 기반 비교의 한계를 보완하며, 파일은 속도가 충분히 빠르면 단위 테스트에 포함하고 DB는 맥락에 맞춰 경량 대안을 검토한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1305; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1355; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1386).

**개념 관계**
- 가시성과 픽스처 전략으로 읽기 좋은 테스트 틀을 만들면, 난수·캡슐화 우회·인수 캡처 같은 고급 기법을 적용할 때도 재현성과 설계 개선 원칙을 지키기 쉬워진다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:271; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:435; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:853; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1350).

## 상세 내용
### 화제 1. 테스트 접근 제한자와 가시성
테스트 클래스는 외부에서 재사용되지 않기 때문에 필요하다면 private 한정자를 생략해도 가독성과 유지보수성에 영향을 주지 않는다는 점을 환기한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:10).

### 화제 2. 앞선 가시성 논의를 토대로 난수 기반 테스트 전략을 평가
사용자 이름을 랜덤하게 조합하는 예제는 UserToPersonConverter가 단순 문자열 결합임을 보여 주며, 무작위 값이 테스트의 본질을 강화하지 않는 경우도 있음을 지적한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:42). 이는 난수 사용이 테스트 목적과 직접 연관되어야 한다는 메시지를 전달한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:65).

```java
// Listing 8.1 — Converts user name and surname into a person nickname by concatenation.
public class UserToPersonConverter {
    public static Person convert(User user) {
        return new Person(user.getName() + " " + user.getSurname()); // join name parts for nickname
    }
}
```

```python
class UserToPersonConverter:
    """Mirror of Listing 8.1: combine name and surname into a nickname string."""

    @staticmethod
    def convert(user: "User") -> "Person":
        return Person(f"{user.name} {user.surname}")  # mimic Java concatenation rule
```

단일 랜덤 값으로는 테스트 강도가 크게 달라지지 않으며, 실패 시에도 의도를 파악하기 어렵다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:49).

```java
// Listing 8.2 — Uses random alphabetic strings to build a user and check nickname mapping.
public class UserToPersonConverterTest {
    @Test
    void shouldConvertUserNamesIntoPersonNick() {
        String name = RandomStringUtils.randomAlphabetic(8); // random but unconstrained word
        String surname = RandomStringUtils.randomAlphabetic(12);
        User user = new User(name, surname);
        Person person = UserToPersonConverter.convert(user);
        assertThat(person.getNick()).isEqualTo(name + " " + surname); // expect concatenation
    }
}
```

```python
class TestUserToPersonConverter:
    """Python equivalent of Listing 8.2 using random strings."""

    def test_should_convert_user_names_into_person_nick(self) -> None:
        name = random_string(8)  # helper mimicking RandomStringUtils.randomAlphabetic
        surname = random_string(12)
        user = User(name, surname)
        person = UserToPersonConverter.convert(user)
        assert person.nick == f"{name} {surname}"  # assert concatenation result
```

난수+파라미터화 조합은 수량을 늘릴 뿐 경계 검증을 보장하지 못하므로, 의미 있는 사례를 의도적으로 포함해야 한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:67; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:98).

```java
// Listing 8.3 — Parameterized test feeding 100 randomly generated name pairs via Faker.
import com.github.javafaker.Faker;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import java.util.stream.Stream;

public class UserToPersonConverterDataProvidersTest {
    private static final Faker faker = new Faker(); // reusable generator for realistic names

    private static Stream<Arguments> getRandomNames() {
        return Stream.generate(() -> Arguments.of(
                faker.name().firstName(), // human-readable first name
                faker.name().lastName()   // human-readable last name
        )).limit(100); // cap random stream for deterministic test length
    }

    @ParameterizedTest
    @MethodSource("getRandomNames")
    void shouldConvertUserNamesIntoPersonNick(String name, String surname) {
        User user = new User(name, surname);
        Person person = UserToPersonConverter.convert(user);
        assertThat(person.getNick()).isEqualTo(name + " " + surname); // reuse concatenation rule
    }
}
```

```python
from collections.abc import Iterable
from faker import Faker
import pytest

class TestUserToPersonConverterDataProviders:
    """Python mirror of Listing 8.3 using Faker and pytest parametrize-like generator."""

    faker = Faker()

    @staticmethod
    def _random_names() -> Iterable[tuple[str, str]]:
        for _ in range(100):
            yield TestUserToPersonConverterDataProviders.faker.first_name(), \
                  TestUserToPersonConverterDataProviders.faker.last_name()

    @pytest.mark.parametrize("name,surname", list(_random_names()))
    def test_should_convert_user_names_into_person_nick(self, name: str, surname: str) -> None:
        user = User(name, surname)
        person = UserToPersonConverter.convert(user)
        assert person.nick == f"{name} {surname}"  # expect same concatenation rule
```

표 8.1은 난수 사용 시 입력 분포 통제, 경계값 보장, 실패 재현, 로그 가독성 문제를 대비해야 한다고 정리한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:143; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:195).

### 화제 3. 난수 전략의 한계를 보완하는 픽스처 구성
난수 테스트의 한계를 인지한 뒤에는 고정 픽스처와 DRY 원칙을 어떻게 조율할지 결정해야 한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:206).

```java
// Listing 8.4 — Declares collaborators as instance fields for simple fixtures.
public class DeclarationTest {
    Collaborator collaborator = mock(Collaborator.class); // eager mock creation
    OtherCollaborator otherCollaborator = mock(OtherCollaborator.class);
    SUT sut = new SUT(collaborator, otherCollaborator); // inlined construction with mocks

    @Test
    void testA() {
        // test logic using shared fixture
    }

    @Test
    void testB() {
        // another scenario reusing the same fixture
    }
}
```

```python
from unittest.mock import Mock

class TestDeclaration:
    """Python translation of Listing 8.4 using unittest.mock."""

    collaborator = Mock(spec=Collaborator)  # eager fixture
    other_collaborator = Mock(spec=OtherCollaborator)
    sut = SUT(collaborator, other_collaborator)

    def test_a(self) -> None:
        pass  # replace with assertions leveraging shared sut

    def test_b(self) -> None:
        pass
```

```java
// Listing 8.5 — Uses @BeforeEach to build the default fixture and customizes per test if needed.
public class SetUpTest {
    private Collaborator collaborator;
    private OtherCollaborator otherCollaborator;
    private SUT sut;

    @BeforeEach
    void setUp() {
        collaborator = mock(Collaborator.class); // fresh mocks per test
        otherCollaborator = mock(OtherCollaborator.class);
        sut = new SUT(collaborator, otherCollaborator); // default wiring
        // perform shared configuration tweaks here when necessary
    }

    @Test
    void testA() {
        // assertions for baseline scenario
    }

    @Test
    void testB() {
        sut.someConfigurationMethod(); // scenario-specific customization
        // assertions for altered configuration
    }
}
```

```python
from unittest.mock import Mock

class TestSetUp:
    """Python equivalent of Listing 8.5 using pytest fixtures for fresh objects."""

    def setup_method(self) -> None:
        self.collaborator = Mock(spec=Collaborator)
        self.other_collaborator = Mock(spec=OtherCollaborator)
        self.sut = SUT(self.collaborator, self.other_collaborator)

    def test_a(self) -> None:
        pass  # baseline assertions go here

    def test_b(self) -> None:
        self.sut.some_configuration_method()
        pass
```

### 화제 4. 픽스처 논의를 잇는 단언 개수와 테스트 크기 조절
픽스처 구조를 정했다면 각 테스트가 다루는 책임 범위와 단언 개수를 어떻게 설계할지 고려해야 하며, OAPTM(one assert per test method) 논의가 이를 촉발한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:291).

```java
// Listing 8.6 — One assert per test method; each method covers a single field.
public class AddressParsingOneAssertTest {
    private Address anAddress = new Address("ADDR1$CITY IL 60563$COUNTRY"); // shared fixture

    @Test
    void testAddr1() {
        assertEquals("ADDR1", anAddress.getAddr1()); // check first line only
    }

    @Test
    void testCsp() {
        assertEquals("CITY IL 60563", anAddress.getCsp()); // check city/state/postal
    }

    @Test
    void testCountry() {
        assertEquals("COUNTRY", anAddress.getCountry()); // check country part
    }
}
```

```python
class TestAddressParsingOneAssert:
    """Python counterpart of Listing 8.6 with one assertion per test."""

    def setup_method(self) -> None:
        self.address = Address("ADDR1$CITY IL 60563$COUNTRY")

    def test_addr1(self) -> None:
        assert self.address.addr1 == "ADDR1"

    def test_csp(self) -> None:
        assert self.address.csp == "CITY IL 60563"

    def test_country(self) -> None:
        assert self.address.country == "COUNTRY"
```

```java
// Listing 8.7 — Groups related assertions to describe the whole parsing behaviour at once.
public class AddressParsingManyAsserts {
    @Test
    void testAddressParsing() {
        Address anAddress = new Address("ADDR1$CITY IL 60563$COUNTRY");
        assertEquals("ADDR1", anAddress.getAddr1()); // first line check
        assertEquals("CITY IL 60563", anAddress.getCsp()); // second line check
        assertEquals("COUNTRY", anAddress.getCountry()); // third line check
    }
}
```

```python
class TestAddressParsingManyAsserts:
    """Python translation of Listing 8.7 combining related assertions."""

    def test_address_parsing(self) -> None:
        address = Address("ADDR1$CITY IL 60563$COUNTRY")
        assert address.addr1 == "ADDR1"
        assert address.csp == "CITY IL 60563"
        assert address.country == "COUNTRY"
```

저자는 작은 메서드를 선호하지만, 테스트가 단 하나의 기능을 다루는 한 필요한 만큼 단언을 허용하라고 조언한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:435).

### 화제 5. 단언 전략을 보완하는 소프트 단언의 제한적 활용
다수의 단언을 실행하는 SoftAssertions는 장시간 실행되는 시나리오에서 모든 실패 정보를 한 번에 얻고자 할 때만 고려하라고 조언한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:446).

```java
// Listing 8.8 — AssertJ soft assertions execute every check inside the lambda before reporting.
import org.assertj.core.api.SoftAssertions;

SoftAssertions.assertSoftly(softly -> {
    softly.assertThat(something).someAssertHere();      // first check executed lazily
    softly.assertThat(something).anotherAssert();       // continues even if previous failed
    softly.assertThat(something).yetAnotherAssert();    // gathers all failures
});
```

```python
with soft_assertions() as softly:  # hypothetical helper mimicking AssertJ soft assertions
    softly.assert_that(something).is_true()
    softly.assert_that(other_thing).equals(expected)
    softly.assert_that(third).is_not_none()
```

### 화제 6. 소프트 단언 논의를 잇는 프라이빗 메서드 테스트 선택지
캡슐화 위반 우려에도 불구하고, 레거시 상황에서는 프라이빗 메서드 검증을 위해 리플렉션이나 접근 완화를 사용할 수밖에 없는 경우가 있다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:545).

```java
// Listing 8.9 — Simple class exposing only a private method that always returns true.
public class SomeClass {
    private boolean privateMethod(Long param) {
        return true; // placeholder logic to be verified in tests
    }
}
```

```python
class SomeClass:
    """Python version of Listing 8.9 with a private-like method."""

    def _private_method(self, param: int) -> bool:
        return True
```

```java
// Listing 8.10 — Uses reflection to invoke the private method by name.
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class PrivateMethodReflectionTest {
    @Test
    void testingPrivateMethodWithReflection()
            throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        SomeClass sut = new SomeClass();
        Method m = sut.getClass().getDeclaredMethod("privateMethod", Long.class); // locate method
        m.setAccessible(true); // bypass private access
        Boolean result = (Boolean) m.invoke(sut, 5569L); // call with sample argument
        assertThat(result).isTrue(); // expect true outcome
    }
}
```

```python
class TestPrivateMethodReflection:
    """Python equivalent using getattr and name mangling bypass."""

    def test_private_method_with_reflection(self) -> None:
        sut = SomeClass()
        private = getattr(sut, "_SomeClass__private_method", sut._private_method)  # handle name mangling
        result = private(5569)
        assert result is True
```

```java
// Listing 8.11 — Relies on JUnit's ReflectionUtils helper to simplify access.
import org.junit.platform.commons.util.ReflectionUtils;
import java.lang.reflect.Method;

public class PrivateMethodReflectionUtilsTest {
    @Test
    void testingPrivateMethodWithReflection() throws Exception {
        SomeClass sut = new SomeClass();
        Method privateMethod = sut.getClass().getDeclaredMethod("privateMethod", Long.class);
        ReflectionUtils.makeAccessible(privateMethod); // simplify accessibility handling
        assertThat((boolean) privateMethod.invoke(sut, 2348973L)).isTrue();
    }
}
```

```python
class TestPrivateMethodReflectionUtils:
    """Python analogue using inspect to bypass attribute access restrictions."""

    def test_private_method_with_helper(self) -> None:
        sut = SomeClass()
        private = getattr(sut, "_private_method")
        assert private(2348973) is True
```

```java
// Listing 8.12 — Relaxes access modifier to package-private so tests can call method directly.
public class SomeClass {
    boolean privateMethod(Long param) { // package-private for test visibility
        return true;
    }
}

public class PrivateMethodAccessModifierTest {
    @Test
    void testingPrivateMethodWithReflection() {
        SomeClass sut = new SomeClass();
        assertThat(sut.privateMethod(9238423L)).isTrue(); // direct invocation now possible
    }
}
```

```python
class SomeClassAccessible(SomeClass):
    """Python version exposing the method directly for tests."""

    def private_method(self, param: int) -> bool:  # no underscore mimics relaxed access
        return True


def test_private_method_access_modifier() -> None:
    sut = SomeClassAccessible()
    assert sut.private_method(9238423) is True
```

저자는 새 코드를 작성할 때는 공용 API만 테스트하고 TDD로 프라이빗 메서드 필요성 자체를 줄이되, 레거시에서는 위 기술을 마지막 수단으로 준비하라고 강조한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:650).

### 화제 7. 프라이빗 논의에서 확장한 람다 테스트 지침
복잡한 람다는 메서드 참조로 추출해 개별 메서드를 테스트하고, 단순 람다는 결과만 확인하면 된다고 정리한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:670; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:688).

```java
// Refactor complex lambda into a named method so it can be unit tested separately.
public static List<String> someMethod(List<String> input) {
    return input.stream()
        .map(MyClass::complexLambda) // extracted method reference acts as seam
        .collect(Collectors.toList());
}

static String complexLambda(String s) {
    // complex processing omitted for brevity
    return s.trim().toUpperCase();
}
```

```python
def some_method(values: list[str]) -> list[str]:
    """Python equivalent: map values through a named helper to ease testing."""

    return [complex_lambda(value) for value in values]


def complex_lambda(value: str) -> str:
    return value.strip().upper()
```

### 화제 8. 람다에서 이어지는 new 연산자·정적 호출 처리 전략
복잡한 람다를 분리한 다음에는 new 연산자 또는 정적 팩토리가 테스트 seam을 차단하는 문제를 해결해야 한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:718).

```java
// Listing 8.13 — SUT directly instantiates its collaborator, hindering dependency injection.
public class MySut {
    public void myMethod() {
        MyCollaborator collaborator = new MyCollaborator(); // hard-wired dependency
        // behaviour interacting with collaborator
    }
}
```

```python
class MySut:
    """Python analogue of Listing 8.13 creating a collaborator inline."""

    def my_method(self) -> None:
        collaborator = MyCollaborator()
        collaborator.do_work()
```

```java
// Listing 8.14 — Skeleton highlighting the need to replace the in-method new call.
public class MySutTest {
    @Test
    void testMyMethod() {
        MySut sut = new MySut();
        MyCollaborator collaborator = mock(MyCollaborator.class); // desired double
        // inject collaborator somehow, exercise sut, verify collaborator usage
    }
}
```

```python
class TestMySut:
    """Python skeleton mirroring Listing 8.14."""

    def test_my_method(self) -> None:
        sut = MySut()
        collaborator = Mock(spec=MyCollaborator)
        # need seam to inject collaborator before verifying interactions
```

PowerMock는 JUnit4 환경에서 new를 가장 간단히 대체하지만 설계 개선을 가로막을 수 있다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:808).

```java
// Listing 8.15 — PowerMock stubs out new MyCollaborator() calls for legacy code.
import org.powermock.api.mockito.PowerMockito;
import org.powermock.core.classloader.annotations.PrepareForTest;
import org.powermock.modules.junit4.PowerMockRunner;

@PrepareForTest(MySut.class)
@RunWith(PowerMockRunner.class)
public class MySutTest {
    @Test
    void testMyMethod() throws Exception {
        MySut sut = new MySut();
        MyCollaborator collaborator = mock(MyCollaborator.class); // test double
        PowerMockito.whenNew(MyCollaborator.class).withNoArguments().thenReturn(collaborator); // intercept new
        // normal Mockito stubbing & verification follow here
    }
}
```

```python
import pytest

@pytest.mark.skip("PowerMock concept has no direct Python equivalent; illustrate with monkeypatching.")
def test_my_method_with_monkeypatch(monkeypatch):
    monkeypatch.setattr(MySutModule, "MyCollaborator", lambda: collaborator_double)
    sut = MySut()
    sut.my_method()
```

리팩터링을 통해 생성자를 주입받게 만들면 PowerMock 없이도 테스트가 단순해진다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:883).

```java
// Listing 8.16 — Constructor injection removes the hard dependency on new.
public class MySut {
    private final MyCollaborator collab;

    public MySut(MyCollaborator collab) {
        this.collab = collab; // dependency provided externally
    }

    public void myMethod() {
        // behaviour using collab
    }
}
```

```python
class MySutInjected:
    """Python translation of Listing 8.16 injecting the collaborator."""

    def __init__(self, collaborator: MyCollaborator) -> None:
        self._collaborator = collaborator

    def my_method(self) -> None:
        self._collaborator.do_work()
```

```java
// Listing 8.17 — Standard Mockito test once constructor injection is in place.
public class MySutTest {
    @Test
    void testMyMethod() {
        MyCollaborator collaborator = mock(MyCollaborator.class);
        MySut sut = new MySut(collaborator);
        // perform behaviour verification with Mockito
    }
}
```

```python
def test_my_sut_with_injected_dependency() -> None:
    collaborator = Mock(spec=MyCollaborator)
    sut = MySutInjected(collaborator)
    sut.my_method()
    collaborator.do_work.assert_called()
```

API를 바꾸기 어렵다면 createCollaborator 메서드 추출과 서브클래싱·spy로 seam을 만든다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:940; refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1016).

```java
// Listing 8.18 — Extract factory method to override in tests.
public class MyRefactoredSut {
    void myMethod() {
        MyCollaborator collaborator = createCollaborator(); // delegate creation
        // behaviour using collaborator
    }

    MyCollaborator createCollaborator() {
        return new MyCollaborator(); // default production creation
    }
}
```

```python
class MyRefactoredSut:
    """Python mirror of Listing 8.18 with overridable factory."""

    def my_method(self) -> bool:
        collaborator = self.create_collaborator()
        return collaborator.do_work()

    def create_collaborator(self) -> MyCollaborator:
        return MyCollaborator()
```

```java
// Listing 8.19 — Test uses a subclass overriding the factory method.
public class MySutRefactoredTest {
    private MyCollaborator collaborator;

    class MyRefactoredSutSubclassed extends MyRefactoredSut {
        @Override
        protected MyCollaborator createCollaborator() {
            return collaborator; // return injected test double
        }
    }

    @Test
    void testMyMethod() {
        MyRefactoredSut sut = new MyRefactoredSutSubclassed();
        collaborator = mock(MyCollaborator.class);
        when(collaborator.someMethod()).thenReturn(true);
        assertThat(sut.myMethod()).isTrue();
    }
}
```

```python
class MyRefactoredSutSubclassed(MyRefactoredSut):
    """Python subclass overriding collaborator creation for tests."""

    def __init__(self, collaborator: MyCollaborator):
        self._collaborator = collaborator

    def create_collaborator(self) -> MyCollaborator:
        return self._collaborator


def test_my_refactored_sut_subclassed() -> None:
    collaborator = Mock(spec=MyCollaborator)
    collaborator.do_work.return_value = True
    sut = MyRefactoredSutSubclassed(collaborator)
    assert sut.my_method() is True
```

```java
// Listing 8.20 — Same factory extraction reused for partial mocking with spies.
public class MyPartialSut {
    public boolean myMethod() {
        MyCollaborator collaborator = createCollaborator();
        // business logic using collaborator
        return collaborator.someMethod();
    }

    MyCollaborator createCollaborator() {
        return new MyCollaborator();
    }
}
```

```python
class MyPartialSut(MyRefactoredSut):
    """Python version of Listing 8.20 returning a collaborator in the same way."""

    def create_collaborator(self) -> MyCollaborator:
        return MyCollaborator()
```

```java
// Listing 8.21 — Mockito spy intercepts only the factory method to supply a mock.
public class MySutPartialTest {
    @Test
    void testMyMethod() {
        MyPartialSut sut = spy(new MyPartialSut()); // real object with overridable seams
        MyCollaborator collaborator = mock(MyCollaborator.class);
        doReturn(collaborator).when(sut).createCollaborator(); // intercept factory
        // continue with Mockito behaviour verification
    }
}
```

```python
def test_my_partial_sut(monkeypatch) -> None:
    collaborator = Mock(spec=MyCollaborator)

    class SpyMyPartialSut(MyPartialSut):
        def create_collaborator(self) -> MyCollaborator:
            return collaborator

    sut = SpyMyPartialSut()
    sut.my_method()
    collaborator.some_method.assert_called()
```

### 화제 9. 생성자 시나리오에서 파생된 인수 캡처와 비교 전략
new·정적 호출을 제어한 뒤에는 협력자에게 전달되는 객체를 검증해야 하며, PIM 예제가 대표적이다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1174).

```java
// Listing 8.22 — Calendar collaborator interface that accepts events.
public interface Calendar {
    void addEvent(Event event); // collaborator API to verify
}
```

```python
class Calendar(Protocol):
    """Python protocol mirroring Listing 8.22."""

    def add_event(self, event: "Event") -> None:
        ...
```

```java
// Listing 8.23 — Meeting value object capturing start/end dates defensively.
public class Meeting implements Event {
    private final Date startDate;
    private final Date endDate;

    public Meeting(Date startDate, Date endDate) {
        this.startDate = new Date(startDate.getTime()); // defensive copy
        this.endDate = new Date(endDate.getTime());
    }

    public Date getStartDate() {
        return startDate;
    }

    public Date getEndDate() {
        return endDate;
    }
}
```

```python
@dataclass(frozen=True)
class Meeting(Event):
    """Python equivalent of Listing 8.23 with immutable datetime copies."""

    start_date: datetime
    end_date: datetime
```

```java
// Listing 8.24 — PIM creates Meeting and forwards it to Calendar.
public class PIM {
    private static final int MILLIS_IN_MINUTE = 60 * 1000;
    private Calendar calendar;

    public PIM(Calendar calendar) {
        this.calendar = calendar; // inject collaborator
    }

    public void addMeeting(Date startDate, int durationInMinutes) {
        Date endDate = new Date(startDate.getTime() + MILLIS_IN_MINUTE * durationInMinutes);
        Meeting meeting = new Meeting(startDate, endDate);
        calendar.addEvent(meeting); // forward constructed event
    }
}
```

```python
class PIM:
    """Python translation of Listing 8.24 scheduling meetings."""

    MILLIS_IN_MINUTE = 60 * 1000

    def __init__(self, calendar: Calendar) -> None:
        self._calendar = calendar

    def add_meeting(self, start_date: datetime, duration_minutes: int) -> None:
        end_date = start_date + timedelta(minutes=duration_minutes)
        meeting = Meeting(start_date, end_date)
        self._calendar.add_event(meeting)
```

```java
// Listing 8.25 — First attempt: create an identical Meeting and rely on equals.
public class PIMTest {
    private static final int ONE_HOUR = 60;
    private static final Date START_DATE = new Date();
    private static final int MILLIS_IN_MINUTE = 1000 * 60;
    private static final Date END_DATE = new Date(START_DATE.getTime() + ONE_HOUR * MILLIS_IN_MINUTE);

    @Test
    void shouldAddNewEventToCalendar() {
        Calendar calendar = mock(Calendar.class);
        PIM pim = new PIM(calendar);
        Meeting expectedMeeting = new Meeting(START_DATE, END_DATE);
        pim.addMeeting(START_DATE, ONE_HOUR);
        verify(calendar).addEvent(expectedMeeting); // fails without equals override
    }
}
```

```python
class TestPIMEquality:
    """Python analogue of Listing 8.25 expecting equality comparison."""

    def test_should_add_new_event_to_calendar(self) -> None:
        calendar = Mock(spec=Calendar)
        pim = PIM(calendar)
        start = datetime.now()
        end = start + timedelta(hours=1)
        expected = Meeting(start, end)
        pim.add_meeting(start, 60)
        calendar.add_event.assert_called_with(expected)
```

```text
# Listing 8.26 — Failure output when equals/hashCode are missing.
Argument(s) are different! Wanted:
calendar.addEvent(
    com.practicalunittesting.Meeting@1242b11
);
Actual invocation has different arguments:
calendar.addEvent(
    com.practicalunittesting.Meeting@1878144
);
```

```java
// Listing 8.27 — Generated equals/hashCode to enable value comparison.
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    Meeting meeting = (Meeting) o;
    if (endDate != null ? !endDate.equals(meeting.endDate) : meeting.endDate != null) return false;
    return !(startDate != null ? !startDate.equals(meeting.startDate) : meeting.startDate != null);
}

@Override
public int hashCode() {
    // hashCode implementation omitted in book but must align with equals
    return Objects.hash(startDate, endDate);
}
```

```python
@dataclass(frozen=True)
class MeetingComparable(Meeting):
    """Python version overriding equality via dataclass semantics."""
    pass
```

ArgumentCaptor는 equals 의존성을 제거하고 전달된 속성을 직접 검증할 수 있게 해준다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1305).

```java
// Listing 8.28 — Capture Meeting argument and assert on its fields.
public class PIMTest {
    private static final int ONE_HOUR = 60;
    private static final Date START_DATE = new Date();
    private static final int MILLIS_IN_MINUTE = 1000 * 60;
    private static final Date END_DATE = new Date(START_DATE.getTime() + ONE_HOUR * MILLIS_IN_MINUTE);

    @Test
    void shouldAddNewEventToCalendar() {
        Calendar calendar = mock(Calendar.class);
        PIM pim = new PIM(calendar);
        ArgumentCaptor<Meeting> argument = ArgumentCaptor.forClass(Meeting.class);
        pim.addMeeting(START_DATE, ONE_HOUR);
        verify(calendar).addEvent(argument.capture());
        Meeting meeting = argument.getValue();
        assertThat(meeting.getStartDate()).isEqualTo(START_DATE);
        assertThat(meeting.getEndDate()).isEqualTo(END_DATE);
    }
}
```

```python
def test_pim_with_argument_captor() -> None:
    calendar = Mock(spec=Calendar)
    pim = PIM(calendar)
    start = datetime.now()
    pim.add_meeting(start, 60)
    captured = calendar.add_event.call_args[0][0]
    assert captured.start_date == start
    assert captured.end_date == start + timedelta(minutes=60)
```

Hamcrest/람다 matcher는 더 짧지만 실패 메시지가 모호해질 수 있다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1355).

```java
// Listing 8.29 — Inline predicate matching the captured event.
import static org.mockito.ArgumentMatchers.argThat;

verify(calendar).addEvent(argThat(event ->
    event.getStartDate().equals(START_DATE) &&
    event.getEndDate().equals(END_DATE)
));
```

```python
calendar.add_event.assert_called_with(mock.ANY)
arg = calendar.add_event.call_args[0][0]
assert arg.start_date == START_DATE and arg.end_date == END_DATE
```

### 화제 10. 인수 검증에서 확장된 파일·DB 접근 논쟁
파일 시스템과 DB를 만지는 테스트는 원칙적으로 피했지만, 현대 환경에서는 저비용 파일 입출력 정도는 단위 테스트에 포함해도 괜찮다고 작가는 입장을 완화한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1386).

### 화제 11. 실습 과제로 이어지는 정적 호출 테스트
마지막으로 정적 메서드와 new 조합을 다루는 MailClient 예제를 연습 문제로 제시함으로써 앞선 기법을 적용해 보도록 권장한다 (refactoring/tests/data/Practical_Unit_Testing_with_JUnit_and_Mockito/Chapter8.Points_of_Controversy/content.md:1439).

```java
// Listing 8.30 — MailClient creates Email and sends it through a static EmailServer.
public class MailClient {
    public void sendEmail(String address, String title, String body) {
        Email email = new Email(address, title, body); // direct instantiation
        EmailServer.sendEmail(email); // static call hard to stub without seams
    }
}
```

```python
class MailClient:
    """Python translation of Listing 8.30 forming an Email and calling a static-like server."""

    def send_email(self, address: str, title: str, body: str) -> None:
        email = Email(address, title, body)
        EmailServer.send_email(email)
```

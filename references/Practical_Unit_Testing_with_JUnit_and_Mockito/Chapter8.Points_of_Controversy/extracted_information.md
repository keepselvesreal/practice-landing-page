# 정보 추출 결과
- 생성 시간: 2025년 9월 29일 21시 16분
- 핵심 내용: Chapter 8. Points of Controversy 정보 추출
- 상세 내용:
  - 압축 내용 (Line 1-3): 단위 테스트 작성 시 논란이 되는 여러 주제들에 대한 가이드
  - 핵심 내용 (Line 1-50): 테스트 작성의 주요 논란점들과 해결 방안
  - 상세 핵심 내용 (Line 1-200): 핵심 개념들의 상세 설명 및 추가 중요 개념들
  - 상세 내용 (Line 1-1449): 각 화제별 상세 설명과 코드 예제
- 상태: active
- 참조: content.md

## 압축 내용
단위 테스트 작성 시 개발자 커뮤니티에서 논란이 되는 주제들(접근 제어자, 랜덤 값, Setup 메서드, 어설션 수, 프라이빗 메서드 테스트, new 연산자, 협력자 인수 캡처 등)에 대한 다양한 해결 방안과 장단점을 제시하는 실용적 가이드.

## 핵심 내용

### 핵심 개념들
1. **접근 제어자 (Access Modifiers)**
2. **랜덤 값 테스트 (Random Values in Tests)**
3. **Setup 메서드 활용**
4. **어설션 수 논란**
5. **프라이빗 메서드 테스트**
6. **new 연산자 테스트**
7. **협력자 인수 캡처**

### 압축적 설명
- **접근 제어자**: 테스트 클래스에서는 프로덕션 코드와 달리 캡슐화가 덜 중요하므로 private 키워드 사용이 선택사항
- **랜덤 값 테스트**: 테스트 강도보다는 품질이 중요하며, 의도적으로 선택한 경계값이 랜덤 값보다 효과적
- **Setup 메서드**: 테스트 가독성과 유지보수성을 위해 적절한 초기화 방법 선택 필요
- **어설션 수**: 테스트당 하나의 어설션 vs 여러 어설션의 장단점 비교
- **프라이빗 메서드**: 설계 관점과 검증 관점의 균형, 리팩터링을 통한 해결 권장
- **new 연산자**: 의존성 주입, 리팩터링, PowerMock 등 다양한 해결 방안 제시
- **협력자 인수**: ArgumentCaptor, Hamcrest Matchers 등을 통한 인수 검증 방법

### 개념 간 관계
이들 논란점들은 모두 테스트 격리성, 가독성, 유지보수성이라는 공통 목표를 달성하기 위한 다양한 접근법을 다루며, 설계 개선을 통한 근본적 해결과 도구를 활용한 기술적 해결 사이의 균형을 추구한다.

## 상세 핵심 내용

### 중요 개념들
1. **접근 제어자 (Access Modifiers)**
2. **랜덤 값 테스트 (Random Values in Tests)**
3. **속성 기반 테스트 (Property-based Testing)**
4. **Setup 메서드 활용**
5. **어설션 수 논란**
6. **Soft Assertions**
7. **프라이빗 메서드 테스트**
8. **람다 표현식 테스트**
9. **new 연산자 테스트**
10. **협력자 인수 캡처**
11. **파일 시스템과 데이터베이스**

### 자세한 설명

**접근 제어자**: 테스트 클래스는 다른 클래스에서 거의 사용되지 않으므로 private 키워드가 코드 품질을 실질적으로 향상시키지 않음. 가독성을 위해 생략해도 무방함.

**랜덤 값 테스트**: 100개의 랜덤 값보다 의도적으로 선택한 경계값(빈 문자열, 극도로 긴 문자열 등)이 더 효과적. 속성 기반 테스트에서는 유용하지만 일반적인 단위 테스트에서는 제한적.

**속성 기반 테스트**: 알고리즘 검증에 유용하며, 대량의 랜덤 입력값으로 예상 속성이 유지되는지 검증. jqwik, junit-quickcheck 등 전용 라이브러리 활용.

**Setup 메서드**: 테스트 메서드 내 직접 생성 vs @BeforeEach 사용의 장단점. 가독성과 유지보수성 고려하여 선택.

**어설션 수**: 테스트당 하나의 어설션은 실패 지점 명확화에 유리하지만 코드 중복 증가. 여러 어설션은 효율적이지만 실패 시 디버깅 어려움.

**Soft Assertions**: 모든 어설션을 실행한 후 종합적으로 실패 보고하는 방식으로 두 접근법의 장점 결합.

**프라이빗 메서드**: 리플렉션 활용, 접근 제어자 완화, 서브클래스 생성 등의 기술적 해결책보다 설계 개선을 통한 근본적 해결 권장.

**람다 표현식**: 복잡한 람다는 별도 메서드로 추출하여 테스트. 스트림 파이프라인과 비즈니스 로직 분리.

**new 연산자**: PowerMock(마지막 수단), 의존성 주입 설계 변경(권장), 리팩터링 후 서브클래싱, 부분 모킹의 4가지 접근법 비교.

**협력자 인수**: equals() 메서드 구현, ArgumentCaptor 활용, Hamcrest Matchers 사용 등 다양한 인수 검증 방법.

**파일 시스템과 데이터베이스**: 현대적 관점에서 빠르고 안정적인 파일 시스템 사용은 단위 테스트 범위에 포함 가능. 데이터베이스는 여전히 신중한 접근 필요.

### 개념 간 관계
이들 개념들은 테스트의 격리성, 신뢰성, 유지보수성이라는 핵심 원칙을 중심으로 연결됨. 기술적 해결책과 설계 개선 사이의 선택에서 항상 설계 개선을 우선시하되, 레거시 코드 등 제약 상황에서는 적절한 기술적 도구 활용을 권장함.

## 상세 내용

### 8.1. 접근 제어자 (Access Modifiers)
**이전 화제와의 관계**: 장 도입부로서 테스트 작성의 첫 번째 논란점 제시

테스트 클래스에서 private 키워드 사용의 필요성에 대한 논의. 프로덕션 코드와 달리 테스트 클래스는 다른 클래스에서 거의 사용되지 않으므로 캡슐화의 이점이 제한적임. 개발자의 습관과 가독성 선호도에 따라 선택할 것을 권장.

### 8.2. 랜덤 값 테스트 (Random Values in Tests)
**이전 화제와의 관계**: 접근 제어자보다 더 복잡한 설계 결정 문제로 진전

#### 8.2.1. 랜덤 객체 속성
랜덤 값 생성의 다양한 방법(커스텀 유틸리티, Java Faker, Apache Commons Lang 등) 소개.

```java
// 기본 랜덤 값 테스트 예제
public class UserToPersonConverter {
    public static Person convert(User user) {
        return new Person(user.getName() + " " + user.getSurname());
    }
}

// 파이썬 버전
class UserToPersonConverter:
    @staticmethod
    def convert(user):
        return Person(user.get_name() + " " + user.get_surname())
```

```java
public class UserToPersonConverterTest {
    @Test
    void shouldConvertUserNamesIntoPersonNick() {
        String name = RandomStringUtils.randomAlphabetic(8);  // 8자 랜덤 문자열 생성
        String surname = RandomStringUtils.randomAlphabetic(12);  // 12자 랜덤 문자열 생성
        User user = new User(name, surname);
        Person person = UserToPersonConverter.convert(user);
        assertThat(person.getNick())
            .isEqualTo(name + " " + surname);  // 이름과 성이 올바르게 결합되었는지 검증
    }
}

// 파이썬 버전
class TestUserToPersonConverter:
    def test_should_convert_user_names_into_person_nick(self):
        import string
        import random
        name = ''.join(random.choices(string.ascii_letters, k=8))  # 8자 랜덤 문자열
        surname = ''.join(random.choices(string.ascii_letters, k=12))  # 12자 랜덤 문자열
        user = User(name, surname)
        person = UserToPersonConverter.convert(user)
        assert person.get_nick() == name + " " + surname
```

다중 랜덤 테스트 케이스:

```java
import com.github.javafaker.Faker;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import java.util.stream.Stream;

public class UserToPersonConverterDataProvidersTest {
    private static Stream<Arguments> getRandomNames() {
        return Stream.generate(() -> {
            return Arguments.of(
                    faker.name().firstName(),  // Faker를 통한 실제적인 이름 생성
                    faker.name().lastName()   // Faker를 통한 실제적인 성 생성
            );
        }).limit(100);  // 100개의 테스트 케이스 생성
    }

    @ParameterizedTest
    @MethodSource(value = "getRandomNames")
    void shouldConvertUserNamesIntoPersonNick(String name, String surname) {
        User user = new User(name, surname);
        Person person = UserToPersonConverter.convert(user);
        assertThat(person.getNick())
            .isEqualTo(name + " " + surname);
    }
}

// 파이썬 버전
import pytest
from faker import Faker

class TestUserToPersonConverterDataProviders:
    @pytest.mark.parametrize("name,surname",
        [(Faker().first_name(), Faker().last_name()) for _ in range(100)])
    def test_should_convert_user_names_into_person_nick(self, name, surname):
        user = User(name, surname)
        person = UserToPersonConverter.convert(user)
        assert person.get_nick() == name + " " + surname
```

**참조**: content.md Lines 48-114

#### 8.2.2. 문제점들 (The Gotchas)
랜덤 값 사용 시 발생할 수 있는 문제점들과 해결책:

| 문제점 | 해결책 |
|--------|--------|
| 무의미한 값 테스트 | RandomStringUtils.randomAlphabetic() 같은 제어된 랜덤 값 사용 |
| 경계값 누락 | 랜덤 값과 별도로 경계값 테스트 필수 |
| 재현 불가능성 | 시드 값 저장, JUnit XML 리포트 활용 |
| 깜빡이는 테스트 | 실패 시 해당 값을 고정 테스트에 추가 |
| 모호한 오류 메시지 | "ANY_NAME", "ANY_SURNAME" 같은 의미 있는 값 사용 |

**참조**: content.md Lines 142-197

### 8.3. Setup 메서드의 적절성
**이전 화제와의 관계**: 랜덤 값 논의에서 테스트 구조화로 논의 확장

테스트 객체 초기화 방법에 대한 비교:

```java
// 선언과 동시에 생성
public class ClientTest {
    private Client client = new Client();  // 필드 레벨에서 직접 초기화

    @Test
    void shouldCalculateTotal() {
        // 테스트 로직
    }
}

// 파이썬 버전
class TestClient:
    def setUp(self):
        self.client = Client()  # setUp 메서드에서 초기화

    def test_should_calculate_total(self):
        # 테스트 로직
        pass
```

```java
// SetUp 메서드와 추가 설정 조합
public class ClientTest {
    private Client client;

    @BeforeEach
    void setUp() {
        client = new Client();  // 매 테스트마다 새로운 인스턴스 생성
    }

    @Test
    void shouldReturnProperProducts() {
        client.addProduct(new Product("TV"));  // 테스트별 추가 설정
        client.addProduct(new Product("Camera"));
        assertThat(client.getProducts()).hasSize(2);
    }
}

// 파이썬 버전
class TestClient:
    def setUp(self):
        self.client = Client()

    def test_should_return_proper_products(self):
        self.client.add_product(Product("TV"))
        self.client.add_product(Product("Camera"))
        assert len(self.client.get_products()) == 2
```

**참조**: content.md Lines 198-286

### 8.4. 테스트당 어설션 수
**이전 화제와의 관계**: Setup에서 테스트 내용 구성으로 논의 심화

#### 8.4.1. 코드 예제
주소 파싱 예제를 통한 어설션 수 비교:

```java
// 하나의 어설션per 테스트 메서드
public class AddressTest {
    @Test
    void shouldParseStreet() {
        Address address = new Address("123 Main Street, Springfield");
        assertThat(address.getStreet()).isEqualTo("123 Main Street");  // 거리만 검증
    }

    @Test
    void shouldParseCity() {
        Address address = new Address("123 Main Street, Springfield");
        assertThat(address.getCity()).isEqualTo("Springfield");  // 도시만 검증
    }
}

// 파이썬 버전
class TestAddress:
    def test_should_parse_street(self):
        address = Address("123 Main Street, Springfield")
        assert address.get_street() == "123 Main Street"

    def test_should_parse_city(self):
        address = Address("123 Main Street, Springfield")
        assert address.get_city() == "Springfield"
```

```java
// 여러 어설션 per 테스트 메서드
public class AddressTest {
    @Test
    void shouldParseAddress() {
        Address address = new Address("123 Main Street, Springfield");
        assertThat(address.getStreet()).isEqualTo("123 Main Street");  // 거리 검증
        assertThat(address.getCity()).isEqualTo("Springfield");        // 도시 검증
        // 모든 속성을 한 번에 검증
    }
}

// 파이썬 버전
class TestAddress:
    def test_should_parse_address(self):
        address = Address("123 Main Street, Springfield")
        assert address.get_street() == "123 Main Street"
        assert address.get_city() == "Springfield"
```

**참조**: content.md Lines 300-349

#### 8.4.2. 장단점 비교
**하나의 어설션 접근법 장점**:
- 실패 지점 명확화
- 테스트 이름의 명확성
- 독립성 보장

**여러 어설션 접근법 장점**:
- 코드 효율성
- 관련된 검증의 논리적 그룹화
- 테스트 실행 속도

**참조**: content.md Lines 366-422

#### 8.4.3. Soft Assertions
두 접근법의 장점을 결합한 해결책:

```java
// Soft Assertions 의사코드
@Test
void shouldParseAddressSoftAssertions() {
    Address address = new Address("123 Main Street, Springfield");

    SoftAssertions softly = new SoftAssertions();
    softly.assertThat(address.getStreet()).isEqualTo("123 Main Street");
    softly.assertThat(address.getCity()).isEqualTo("Springfield");
    softly.assertAll();  // 모든 어설션 실행 후 종합 결과 보고
}

// 파이썬 버전
def test_should_parse_address_soft_assertions(self):
    address = Address("123 Main Street, Springfield")

    with soft_assertions():  # pytest-soft-assertions 플러그인 사용
        assert address.get_street() == "123 Main Street"
        assert address.get_city() == "Springfield"
    # 모든 어설션이 실행된 후 결과 종합
```

**참조**: content.md Lines 454-478

### 8.5. 프라이빗 메서드 테스트
**이전 화제와의 관계**: 어설션 구성에서 테스트 접근성 문제로 확장

#### 8.5.1. 설계 vs 검증 관점
프라이빗 메서드 테스트 필요성에 대한 두 관점:
- **설계 관점**: 프라이빗 메서드는 구현 세부사항이므로 직접 테스트 불필요
- **검증 관점**: 모든 코드는 테스트되어야 하므로 방법을 찾아서라도 테스트 필요

#### 8.5.2. 옵션들
프라이빗 메서드 테스트를 위한 선택지:
1. 테스트하지 않기 (설계 개선 권장)
2. 접근 제어자 변경 (package-private 또는 protected)
3. 리플렉션 사용
4. 클래스 설계 변경

#### 8.5.3. 기술적 해결책들

**리플렉션 사용**:
```java
public class ClassWithPrivateMethod {
    private boolean privateMethod(int x) {
        return x > 0;  // 양수인지 확인하는 프라이빗 메서드
    }
}

// 파이썬 버전
class ClassWithPrivateMethod:
    def __private_method(self, x):
        return x > 0
```

```java
// 리플렉션을 통한 프라이빗 메서드 테스트
public class ClassWithPrivateMethodTest {
    @Test
    void testPrivateMethod() throws Exception {
        ClassWithPrivateMethod sut = new ClassWithPrivateMethod();
        Method method = sut.getClass().getDeclaredMethod("privateMethod", int.class);
        method.setAccessible(true);  // 접근 제한 해제

        Boolean result = (Boolean) method.invoke(sut, 1);  // 메서드 호출
        assertThat(result).isTrue();
    }
}

// 파이썬 버전
class TestClassWithPrivateMethod:
    def test_private_method(self):
        sut = ClassWithPrivateMethod()
        # 파이썬에서는 name mangling으로 접근
        result = sut._ClassWithPrivateMethod__private_method(1)
        assert result is True
```

**ReflectionUtils 활용**:
```java
import org.springframework.util.ReflectionUtils;

@Test
void testPrivateMethodWithReflectionUtils() {
    ClassWithPrivateMethod sut = new ClassWithPrivateMethod();
    Method method = ReflectionUtils.findMethod(
        ClassWithPrivateMethod.class, "privateMethod", int.class);
    ReflectionUtils.makeAccessible(method);  // 접근 가능하게 설정

    Boolean result = (Boolean) ReflectionUtils.invokeMethod(method, sut, 1);
    assertThat(result).isTrue();
}

// 파이썬 버전 (getattr 사용)
def test_private_method_with_getattr(self):
    sut = ClassWithPrivateMethod()
    method = getattr(sut, '_ClassWithPrivateMethod__private_method')
    result = method(1)
    assert result is True
```

**접근 제어자 완화**:
```java
public class ClassWithPackagePrivateMethod {
    boolean packagePrivateMethod(int x) {  // package-private으로 변경
        return x > 0;
    }
}

@Test
void testPackagePrivateMethod() {
    ClassWithPackagePrivateMethod sut = new ClassWithPackagePrivateMethod();
    boolean result = sut.packagePrivateMethod(1);  // 직접 호출 가능
    assertThat(result).isTrue();
}

// 파이썬 버전 (언더스코어 하나만 사용)
class ClassWithPackagePrivateMethod:
    def _package_private_method(self, x):  # 관례상 내부 사용 메서드
        return x > 0

def test_package_private_method(self):
    sut = ClassWithPackagePrivateMethod()
    result = sut._package_private_method(1)
    assert result is True
```

**참조**: content.md Lines 479-641

### 8.6. 람다 표현식 테스트
**이전 화제와의 관계**: 프라이빗 메서드에서 현대적 Java 구문으로 확장

람다 표현식 테스트의 두 가지 접근법:
1. **별도 메서드 추출**: 복잡한 람다를 독립적인 메서드로 분리하여 테스트
2. **전체 메서드 테스트**: 람다를 포함한 전체 메서드의 동작 검증

**참조**: content.md Lines 658-708

### 8.7. new 연산자 테스트
**이전 화제와의 관계**: 람다에서 객체 생성과 의존성 관리 문제로 진전

의존성 주입이 어려운 상황에서의 테스트 방법들:

#### 8.7.1. PowerMock 활용
```java
// 테스트하기 어려운 코드
public class MySut {
    public void myMethod() {
        MyCollaborator collaborator = new MyCollaborator();  // 직접 객체 생성
        // collaborator를 사용하는 로직
    }
}

// 파이썬 버전
class MySut:
    def my_method(self):
        collaborator = MyCollaborator()  # 직접 객체 생성
        # collaborator를 사용하는 로직
```

```java
// PowerMock을 사용한 테스트 (JUnit4)
@PrepareForTest(MySut.class)
@RunWith(PowerMockRunner.class)
public class MySutTest {
    @Test
    void testMyMethod() throws Exception {
        MySut sut = new MySut();
        MyCollaborator collaborator = mock(MyCollaborator.class);
        PowerMockito.whenNew(MyCollaborator.class)
            .withNoArguments().thenReturn(collaborator);  // new 연산자 가로채기

        // 일반적인 Mockito 문법으로 테스트 진행
    }
}

// 파이썬 버전 (mock.patch 사용)
from unittest.mock import patch, Mock

class TestMySut:
    @patch('__main__.MyCollaborator')
    def test_my_method(self, mock_collaborator_class):
        mock_collaborator = Mock()
        mock_collaborator_class.return_value = mock_collaborator

        sut = MySut()
        sut.my_method()

        mock_collaborator_class.assert_called_once()
```

**참조**: content.md Lines 781-865

#### 8.7.2. 설계 변경과 의존성 주입
```java
// 개선된 설계 - 생성자 주입
public class MySut {
    private final MyCollaborator collab;

    public MySut(MyCollaborator collab) {  // 생성자를 통한 의존성 주입
        this.collab = collab;
    }

    public void myMethod() {
        // collab 객체 사용, new 연산자 사용하지 않음
    }
}

// 파이썬 버전
class MySut:
    def __init__(self, collab):
        self.collab = collab

    def my_method(self):
        # self.collab 사용
        pass
```

```java
// 개선된 테스트
public class MySutTest {
    @Test
    void testMyMethod() {
        MyCollaborator collaborator = mock(MyCollaborator.class);
        MySut sut = new MySut(collaborator);  // 테스트 더블 주입

        // 일반적인 Mockito 상호작용 테스트
    }
}

// 파이썬 버전
class TestMySut:
    def test_my_method(self):
        collaborator = Mock()
        sut = MySut(collaborator)

        # 일반적인 mock 테스트
```

**참조**: content.md Lines 866-932

#### 8.7.3. 리팩터링과 서브클래싱
```java
// 리팩터링된 버전
public class MyRefactoredSut {
    void myMethod() {
        MyCollaborator collaborator = createCollaborator();  // 메서드로 추출
        // collaborator 사용 로직
    }

    // 테스트 지원을 위해 추출된 메서드
    MyCollaborator createCollaborator() {
        return new MyCollaborator();
    }
}

// 파이썬 버전
class MyRefactoredSut:
    def my_method(self):
        collaborator = self.create_collaborator()
        # collaborator 사용 로직

    def create_collaborator(self):
        return MyCollaborator()
```

```java
// 서브클래스를 통한 테스트
public class MySutRefactoredTest {
    private MyCollaborator collaborator;

    class MyRefactoredSutSubclassed extends MyRefactoredSut {
        @Override
        protected MyCollaborator createCollaborator() {
            return collaborator;  // 테스트 더블 반환
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

// 파이썬 버전
class TestMyRefactoredSut:
    def test_my_method(self):
        collaborator = Mock()

        class MyRefactoredSutSubclassed(MyRefactoredSut):
            def create_collaborator(self):
                return collaborator

        sut = MyRefactoredSutSubclassed()
        collaborator.some_method.return_value = True
        assert sut.my_method() is True
```

**참조**: content.md Lines 933-1008

#### 8.7.4. 부분 모킹 (Partial Mocking)
```java
public class MyPartialSut {
    public boolean myMethod() {
        MyCollaborator collaborator = createCollaborator();
        // collaborator 사용 로직
    }

    MyCollaborator createCollaborator() {
        return new MyCollaborator();
    }
}

// 파이썬 버전
class MyPartialSut:
    def my_method(self):
        collaborator = self.create_collaborator()
        # collaborator 사용 로직
        return True

    def create_collaborator(self):
        return MyCollaborator()
```

```java
// Mockito spy를 사용한 부분 모킹
public class MySutPartialTest {
    @Test
    void testMyMethod() {
        MyPartialSut sut = spy(new MyPartialSut());  // 실제 객체를 spy로 생성
        MyCollaborator collaborator = mock(MyCollaborator.class);
        doReturn(collaborator).when(sut).createCollaborator();  // 특정 메서드만 스텁

        // 일반적인 Mockito 테스트
    }
}

// 파이썬 버전 (patch.object 사용)
class TestMyPartialSut:
    @patch.object(MyPartialSut, 'create_collaborator')
    def test_my_method(self, mock_create_collaborator):
        collaborator = Mock()
        mock_create_collaborator.return_value = collaborator

        sut = MyPartialSut()
        result = sut.my_method()

        mock_create_collaborator.assert_called_once()
        assert result is True
```

**참조**: content.md Lines 1009-1089

#### 8.7.5. 접근법 비교표
| 접근법 | SUT 변경 | 설계 품질 | 테스트 복잡도 | 작업량 |
|--------|----------|-----------|---------------|--------|
| PowerMock | 없음 | 변화없음 | 다름 | 최소 |
| 설계변경 | API변경 | 개선 | 단순 | 많음 |
| 리팩터링+서브클래스 | 메서드추출 | 약간나빠짐 | 복잡 | 중간 |
| 부분모킹 | 메서드추출 | 약간나빠짐 | 복잡 | 중간 |

**참조**: content.md Lines 1090-1161

### 8.8. 협력자 인수 캡처
**이전 화제와의 관계**: new 연산자 해결에서 협력자와의 상호작용 검증으로 심화

협력자에게 전달되는 인수를 검증하는 방법들:

#### 8.8.1. 동일 객체 생성
```java
// 테스트 대상 클래스들
public interface Calendar {
    public void addEvent(Event event);
}

public class Meeting implements Event {
    private final Date startDate;
    private final Date endDate;

    public Meeting(Date startDate, Date endDate) {
        this.startDate = new Date(startDate.getTime());
        this.endDate = new Date(endDate.getTime());
    }

    // getter 메서드들...
}

public class PIM {
    private final static int MILLIS_IN_MINUTE = 60 * 1000;
    private Calendar calendar;

    public PIM(Calendar calendar) {
        this.calendar = calendar;
    }

    public void addMeeting(Date startDate, int durationInMinutes) {
        Date endDate = new Date(startDate.getTime() + MILLIS_IN_MINUTE * durationInMinutes);
        Meeting meeting = new Meeting(startDate, endDate);  // 새 Meeting 객체 생성
        calendar.addEvent(meeting);  // 협력자에게 전달
    }
}

// 파이썬 버전
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Calendar(ABC):
    @abstractmethod
    def add_event(self, event):
        pass

class Meeting:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

class PIM:
    def __init__(self, calendar):
        self.calendar = calendar

    def add_meeting(self, start_date, duration_in_minutes):
        end_date = start_date + timedelta(minutes=duration_in_minutes)
        meeting = Meeting(start_date, end_date)
        self.calendar.add_event(meeting)
```

```java
// 동일 객체를 통한 검증 (equals() 구현 필요)
public class PIMTest {
    private static final int ONE_HOUR = 60;
    private static final Date START_DATE = new Date();
    private static final int MILLIS_IN_MINUTE = 1000 * 60;
    private static final Date END_DATE = new Date(START_DATE.getTime() + ONE_HOUR * MILLIS_IN_MINUTE);

    @Test
    void shouldAddNewEventToCalendar() {
        Calendar calendar = mock(Calendar.class);
        PIM pim = new PIM(calendar);
        Meeting expectedMeeting = new Meeting(START_DATE, END_DATE);  // 예상되는 객체 생성

        pim.addMeeting(START_DATE, ONE_HOUR);

        verify(calendar).addEvent(expectedMeeting);  // 동일한 객체로 호출되었는지 검증
    }
}

// 파이썬 버전
class TestPIM:
    def test_should_add_new_event_to_calendar(self):
        from unittest.mock import Mock

        calendar = Mock()
        pim = PIM(calendar)
        start_date = datetime.now()
        end_date = start_date + timedelta(hours=1)
        expected_meeting = Meeting(start_date, end_date)

        pim.add_meeting(start_date, 60)

        calendar.add_event.assert_called_once_with(expected_meeting)
```

```java
// equals() 메서드 구현
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    Meeting meeting = (Meeting) o;
    if (endDate != null ? !endDate.equals(meeting.endDate) : meeting.endDate != null) return false;
    if (startDate != null ? !startDate.equals(meeting.startDate) : meeting.startDate != null) return false;
    return true;
}

@Override
public int hashCode() {
    int result = startDate != null ? startDate.hashCode() : 0;
    result = 31 * result + (endDate != null ? endDate.hashCode() : 0);
    return result;
}

// 파이썬 버전
def __eq__(self, other):
    if not isinstance(other, Meeting):
        return False
    return self.start_date == other.start_date and self.end_date == other.end_date

def __hash__(self):
    return hash((self.start_date, self.end_date))
```

**참조**: content.md Lines 1224-1303

#### 8.8.2. ArgumentCaptor 활용
```java
// ArgumentCaptor를 사용한 인수 캡처
@Test
void shouldAddNewEventToCalendar() {
    Calendar calendar = mock(Calendar.class);
    PIM pim = new PIM(calendar);
    ArgumentCaptor<Meeting> argument = ArgumentCaptor.forClass(Meeting.class);  // 캡처기 생성

    pim.addMeeting(START_DATE, ONE_HOUR);

    verify(calendar).addEvent(argument.capture());  // 인수 캡처
    Meeting meeting = argument.getValue();  // 캡처된 값 추출
    assertThat(meeting.getStartDate()).isEqualTo(START_DATE);  // 개별 속성 검증
    assertThat(meeting.getEndDate()).isEqualTo(END_DATE);
}

// 파이썬 버전
def test_should_add_new_event_to_calendar(self):
    from unittest.mock import Mock, call

    calendar = Mock()
    pim = PIM(calendar)
    start_date = datetime.now()

    pim.add_meeting(start_date, 60)

    # 호출된 인수 확인
    call_args = calendar.add_event.call_args[0][0]  # 첫 번째 인수 추출
    assert call_args.start_date == start_date
    assert call_args.end_date == start_date + timedelta(hours=1)
```

**참조**: content.md Lines 1304-1349

#### 8.8.3. Hamcrest Matchers 활용
```java
// Hamcrest Matchers를 사용한 인수 검증
import static org.mockito.ArgumentMatchers.argThat;

@Test
void shouldAddNewEventToCalendarLambda() {
    Calendar calendar = mock(Calendar.class);
    PIM pim = new PIM(calendar);

    pim.addMeeting(START_DATE, ONE_HOUR);

    verify(calendar).addEvent(argThat(event ->  // 람다 표현식으로 조건 검증
        event.getStartDate().equals(START_DATE) &&
        event.getEndDate().equals(END_DATE)
    ));
}

// 파이썬 버전
def test_should_add_new_event_to_calendar_lambda(self):
    from unittest.mock import Mock, ANY

    calendar = Mock()
    pim = PIM(calendar)
    start_date = datetime.now()
    end_date = start_date + timedelta(hours=1)

    pim.add_meeting(start_date, 60)

    # 커스텀 매처 함수
    def meeting_matcher(meeting):
        return (meeting.start_date == start_date and
                meeting.end_date == end_date)

    calendar.add_event.assert_called_once()
    called_meeting = calendar.add_event.call_args[0][0]
    assert meeting_matcher(called_meeting)
```

**참조**: content.md Lines 1350-1384

### 8.9. 파일과 데이터베이스
**이전 화제와의 관계**: 협력자 상호작용에서 외부 시스템과의 상호작용으로 확장

Michael Feathers의 2005년 원칙에 대한 현대적 재고찰:
- **파일 시스템**: 현대 파일 시스템의 신뢰성과 속도 향상으로 단위 테스트 범위에 포함 가능
- **데이터베이스**: 여전히 신중한 접근 필요, 인메모리 데이터베이스 고려 가능

"규칙은 훌륭하지만 돌에 새겨진 것이 아니며, 법의 정신을 지키는 한 괜찮다" - 테스트의 빠른 속도, 신뢰성, 독립성, 반복 가능성, 단일 클래스 집중이 핵심.

**참조**: content.md Lines 1385-1408

### 8.10. 결론
**이전 화제와의 관계**: 모든 논란점들을 종합한 실용적 조언

이 장에서 다룬 논란점들은 실제 현장에서 마주치는 문제들로, 특히 레거시 코드 작업 시 빈번히 발생. 상황에 따른 적절한 해결책 선택이 중요하며, 가능하면 설계 개선을 통한 근본적 해결을 권장.

**참조**: content.md Lines 1409-1423

### 8.11. 연습문제
**이전 화제와의 관계**: 이론 학습을 실습으로 강화

#### 8.11.1. 속성 기반 테스트
문자열 역순 메서드의 속성 기반 테스트 구현 과제.

#### 8.11.2. 레거시 코드 테스트
```java
// 테스트하기 어려운 레거시 코드 예제
public class MailClient {
    public void sendEmail(String address, String title, String body) {
        Email email = new Email(address, title, body);  // 직접 객체 생성
        EmailServer.sendEmail(email);  // 정적 메서드 호출
    }
}

// 파이썬 버전
class MailClient:
    def send_email(self, address, title, body):
        email = Email(address, title, body)
        EmailServer.send_email(email)  # 클래스 메서드 호출
```

8.7과 8.8절의 다양한 기법들을 적용하여 테스트 작성, 특히 "재설계" 접근법을 한 번은 적용할 것.

**참조**: content.md Lines 1427-1449

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"content": "content.md \ud30c\uc77c \uad6c\uc870 \ubd84\uc11d (\uc139\uc158\ubcc4 \ubd84\uc11d)", "status": "completed", "activeForm": "content.md \ud30c\uc77c \uad6c\uc870 \ubd84\uc11d \uc644\ub8cc"}, {"content": "\uc555\ucd95 \ub0b4\uc6a9 \ucd94\ucd9c (\ud55c \ubb38\uc7a5 \uc694\uc57d)", "status": "completed", "activeForm": "\uc555\ucd95 \ub0b4\uc6a9 \ucd94\ucd9c \uc644\ub8cc"}, {"content": "\ud575\uc2ec \ub0b4\uc6a9 \ucd94\ucd9c (\ud575\uc2ec \uac1c\ub150 + \uc555\ucd95 \uc124\uba85 + \uad00\uacc4 \uc124\uba85)", "status": "completed", "activeForm": "\ud575\uc2ec \ub0b4\uc6a9 \ucd94\ucd9c \uc644\ub8cc"}, {"content": "\uc0c1\uc138 \ud575\uc2ec \ub0b4\uc6a9 \ucd94\ucd9c (\uc911\uc694 \uac1c\ub150 + \uc790\uc138\ud55c \uc124\uba85 + \uad00\uacc4 \uc124\uba85)", "status": "completed", "activeForm": "\uc0c1\uc138 \ud575\uc2ec \ub0b4\uc6a9 \ucd94\ucd9c \uc644\ub8cc"}, {"content": "\uc0c1\uc138 \ub0b4\uc6a9 \ucd94\ucd9c (\ud654\uc81c\ubcc4 \uc124\uba85 + \ucf54\ub4dc + \uc8fc\uc11d)", "status": "completed", "activeForm": "\uc0c1\uc138 \ub0b4\uc6a9 \ucd94\ucd9c \uc644\ub8cc"}, {"content": "extracted_information.md \ud30c\uc77c \uc0dd\uc131", "status": "completed", "activeForm": "extracted_information.md \ud30c\uc77c \uc0dd\uc131 \uc644\ub8cc"}]
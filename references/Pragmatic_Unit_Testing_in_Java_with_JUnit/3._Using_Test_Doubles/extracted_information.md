# 생성 시간: 2025-09-29 20:42:27 KST

# 핵심 내용: Pragmatic Unit Testing - Chapter 3. Using Test Doubles

## 핵심 개념들
1. **Test Double (테스트 더블)**
2. **Stub (스텁)**
3. **Mock (모크)**
4. **Dependency Injection (의존성 주입)**
5. **Mockito 라이브러리**

## 핵심 개념들에 대한 압축적 설명
- **Test Double**: 테스트하기 어려운 종속성을 대체하는 대역 객체 (content.md:11-13)
- **Stub**: 하드코딩된 값을 반환하는 간단한 테스트 더블 (content.md:109-110)
- **Mock**: 스텁과 유사하지만 예상된 상호작용 검증 기능을 추가로 제공하는 테스트 더블 (content.md:274-276)
- **Dependency Injection**: 테스트 더블을 프로덕션 코드에 전달하는 기법 (content.md:135-136)
- **Mockito**: Java용 표준 모킹 라이브러리로 테스트 더블 생성과 관리를 단순화 (content.md:299-302)

## 핵심 개념들 간의 관계
Test Double은 상위 개념으로 Stub과 Mock을 포함한다. Stub은 가장 단순한 형태의 테스트 더블이며, Mock은 Stub의 기능에 검증 기능을 추가한 발전된 형태다. Dependency Injection은 이러한 테스트 더블들을 실제 코드에 삽입하는 방법이며, Mockito는 이 모든 과정을 쉽게 만들어주는 도구다.

# 상세 핵심 내용

## 중요 개념들
1. **Test Double (테스트 더블)**
2. **Stub (스텁)**
3. **Mock (모크)**
4. **Dependency Injection (의존성 주입)**
5. **Mockito 라이브러리**
6. **Constructor Injection (생성자 주입)**
7. **Field Injection (필드 주입)**
8. **Mock Verification (모크 검증)**
9. **Exception Handling Testing (예외 처리 테스트)**
10. **Fast vs Slow Tests (빠른 테스트 vs 느린 테스트)**

## 중요 개념들에 대한 자세한 설명
- **Test Double**: 스턴트 더블과 같은 개념으로, 테스트를 어렵게 만드는 문제가 있는 협력자를 대체하는 대역 객체다. 실제 종속성과의 상호작용 없이 코드의 로직을 테스트할 수 있게 해준다 (content.md:11-15)
- **Stub**: 실제 동작을 하드코딩된 값을 반환하는 메서드로 대체하는 테스트 더블이다. 가장 단순한 형태로 특정 입력에 대해 항상 동일한 출력을 제공한다 (content.md:109-110)
- **Mock**: Stub과 유사하지만 예상된 상호작용이 발생했는지 자체 검증할 수 있는 기능을 추가로 제공한다. 메서드가 올바른 인자로 호출되었는지 확인할 수 있다 (content.md:274-276, 288-289)
- **Dependency Injection**: 테스트 더블을 프로덕션 코드에 전달하는 기법으로, 생성자 주입이 가장 일반적인 방법이다. 코드의 설계를 변경하여 테스트 가능하게 만든다 (content.md:135-137)
- **Mockito**: Java의 사실상 표준 모킹 라이브러리로, 테스트 더블 생성과 관리를 크게 단순화한다. when().thenReturn() 패턴으로 쉽게 모크를 설정할 수 있다 (content.md:299-302)
- **Constructor Injection**: 생성자를 통해 의존성을 주입하는 방법으로, 클래스의 인터페이스 변경이 필요하지만 명시적이고 안전하다 (content.md:144-148)
- **Field Injection**: Mockito의 @InjectMocks와 @Mock 어노테이션을 사용하여 필드에 직접 모크를 주입하는 방법이다. 편리하지만 성능이 느리고 설계상 문제가 있을 수 있다 (content.md:439-468)
- **Mock Verification**: verify() 메서드를 사용하여 특정 메서드가 예상된 인자로 호출되었는지 검증하는 기능이다. 부작용만 있고 반환값이 없는 메서드 테스트에 유용하다 (content.md:470-474)
- **Exception Handling Testing**: thenThrow()를 사용하여 예외 상황을 시뮬레이션하고 코드가 적절히 처리하는지 테스트하는 방법이다 (content.md:562-565)
- **Fast vs Slow Tests**: 외부 종속성과 상호작용하는 테스트는 느리고(수백-수천 밀리초), 순수 Java 코드만 실행하는 테스트는 빠르다(수 밀리초). 빠른 테스트는 증분적 개발과 지속적인 피드백을 가능하게 한다 (content.md:620-631, 644-647)

## 중요 개념들 간의 관계
Test Double은 포괄적 개념으로 Stub과 Mock을 모두 포함한다. Stub은 가장 기본적인 테스트 더블로 단순히 하드코딩된 값을 반환하며, Mock은 Stub의 기능에 상호작용 검증 기능을 추가한 발전된 형태다. Dependency Injection은 이러한 테스트 더블들을 실제 코드에 삽입하는 메커니즘으로, Constructor Injection과 Field Injection 등의 구체적인 방법들이 있다. Mockito는 이 모든 과정을 자동화하고 단순화하는 도구로, Mock Verification과 Exception Handling Testing 등의 고급 기능도 제공한다. Fast Tests는 Test Double 사용의 주요 이점 중 하나로, 외부 종속성을 제거함으로써 달성된다.

# 상세 내용

## 1. 테스팅 도전과제 - 외부 종속성 문제
**주제**: AddressRetriever 클래스의 테스트 어려움 (content.md:16-103)

### 다뤄지는 내용
AddressRetriever는 위도와 경도를 받아 Address 객체를 반환하는 클래스다. 겉보기에는 단순해 보이지만 실제로는 HTTP 요청을 수행하는 코드가 포함되어 있어 테스트가 어렵다.

```java
// AddressRetriever 클래스 - 핵심 메서드
public Address retrieve(double latitude, double longitude) {
    var locationParams = "lon=%.6f&lat=%.6f".formatted(latitude, longitude);  // 위경도 매개변수 포맷팅
    var url = "%s/reverse?%s&format=json".formatted(SERVER, locationParams);  // URL 생성
    var jsonResponse = new HttpImpl().get(url);  // 실제 HTTP 호출 - 문제 지점
    var response = parseResponse(jsonResponse);  // JSON 파싱
    var address = response.address();
    var country = address.country_code();
    if (!country.equals("us"))  // 미국 주소만 지원
        throw new UnsupportedOperationException("intl addresses unsupported");
    return address;
}
```

HttpImpl 클래스는 실제 HTTP 클라이언트를 사용하여 외부 API를 호출한다:

```java
// HttpImpl 클래스 - 실제 HTTP 호출 구현
public class HttpImpl implements Http {
    @Override
    public String get(String url) {
        try (var client = HttpClient.newHttpClient()) {  // HTTP 클라이언트 생성
            var request = HttpRequest.newBuilder().uri(URI.create(url)).build();  // 요청 생성
            try {
                var httpResponse = client.send(request, BodyHandlers.ofString());  // 실제 네트워크 호출
                return httpResponse.body();  // 응답 반환
            } catch (IOException | InterruptedException e) {
                throw new RuntimeException(e);  // 예외 처리
            }
        }
    }
}
```

이러한 설계는 두 가지 큰 문제를 야기한다:
1. **성능 문제**: 실제 HTTP 호출로 인한 느린 테스트 실행
2. **신뢰성 문제**: 외부 API 가용성과 일관성에 대한 의존

## 2. Stub을 사용한 문제 해결
**주제**: 문제가 되는 동작을 Stub으로 대체하기 (content.md:104-131)
**이전 화제와의 관계**: 위에서 제기된 HTTP 종속성 문제를 해결하는 첫 번째 방법

### 다뤄지는 내용
Stub은 실제 동작을 하드코딩된 값을 반환하는 간단한 메서드로 대체하는 테스트 더블이다. Http는 함수형 인터페이스이므로 람다를 사용해 간결하게 구현할 수 있다:

```java
// HTTP Stub 구현 - 하드코딩된 JSON 반환
Http http = url ->
    """
    {"address":{
        "house_number":"324",
        "road":"Main St",
        "city":"Anywhere",
        "state":"Colorado",
        "postcode":"81234",
        "country_code":"us"}}
    """;
```

이 스텁은 AddressRetriever의 파싱 코드에서 역공학으로 만든 하드코딩된 JSON 문자열을 반환한다. 실제 HTTP 호출 대신 테스트에서만 사용할 수 있는 대체 구현이다.

## 3. 의존성 주입으로 프로덕션 코드 수정
**주제**: 테스트를 지원하기 위한 설계 변경 (content.md:132-162)
**이전 화제와의 관계**: Stub을 만들었지만 이를 AddressRetriever에 전달하는 방법이 필요

### 다뤄지는 내용
Stub을 사용하려면 AddressRetriever가 실제 HttpImpl 대신 스텁을 사용하도록 해야 한다. 이는 의존성 주입을 통해 달성할 수 있다. 생성자 주입을 사용한 수정된 코드:

```java
// 의존성 주입을 지원하도록 수정된 AddressRetriever
public class AddressRetriever {
    private static final String SERVER = "https://nominatim.openstreetmap.org";
    private final Http http;  // Http 인터페이스 필드

    public AddressRetriever(Http http) {  // 생성자를 통한 의존성 주입
        this.http = http;
    }

    public Address retrieve(double latitude, double longitude) {
        var locationParams = "lon=%.6f&lat=%.6f".formatted(latitude, longitude);
        var url = "%s/reverse?%s&format=json".formatted(SERVER, locationParams);
        var jsonResponse = http.get(url);  // 주입된 http 인스턴스 사용
        var response = parseResponse(jsonResponse);
        // ... 나머지 코드
    }
}
```

이제 테스트에서는 스텁을, 프로덕션에서는 실제 HttpImpl을 주입할 수 있다:

```java
// 테스트 코드 - 스텁 주입 및 검증
@Test
void answersAppropriateAddressForValidCoordinates() {
    Http http = url -> "하드코딩된 JSON...";  // 스텁 생성
    var retriever = new AddressRetriever(http);  // 스텁 주입
    var address = retriever.retrieve(38, -104);  // 메서드 실행

    // 결과 검증
    assertEquals("324", address.house_number());
    assertEquals("Main St", address.road());
    assertEquals("Anywhere", address.city());
    assertEquals("Colorado", address.state());
    assertEquals("81234", address.postcode());
}
```

## 4. 스마트 스텁으로 매개변수 검증
**주제**: 스텁에 검증 로직 추가하기 (content.md:235-289)
**이전 화제와의 관계**: 기본 스텁은 매개변수를 검증하지 않아 추가적인 보안이 필요

### 다뤄지는 내용
기본 스텁은 입력 매개변수와 관계없이 항상 같은 값을 반환한다. 이는 AddressRetriever가 매개변수를 올바르게 전달하지 않는 결함을 놓칠 수 있다. 가드 절을 추가한 "스마트 스텁":

```java
// 매개변수 검증 기능이 있는 스마트 스텁
@Test
void answersAppropriateAddressForValidCoordinates() {
    Http http = url -> {
        // URL에 예상 매개변수가 포함되어 있는지 검증
        if (!url.contains("lat=38") || !url.contains("lon=-104"))
            fail("url " + url + " does not contain correct params");

        return """
            {"address":{
                "house_number":"324",
                "road":"Main St",
                "city":"Anywhere",
                "state":"Colorado",
                "postcode":"81234",
                "country_code":"us"}}
            """;
    };
    var retriever = new AddressRetriever(http);
    var address = retriever.retrieve(38, -104);
    // ... 검증 코드
}
```

이 스마트 스텁은 실제로 버그를 발견했다. 원래 코드에서 위도와 경도의 순서가 바뀌어 있었던 것이다:

```java
// 버그가 있는 원본 코드
var locationParams = "lon=%.6f&lat=%.6f".formatted(latitude, longitude);
// 수정된 코드
var locationParams = "lat=%.6f&lon=%.6f".formatted(latitude, longitude);
```

스마트 스텁은 더 이상 단순한 스텁이 아니라 모크에 가깝다. 모크는 스텁과 같이 테스트별 동작을 제공하지만 예상되는 상호작용이 발생했는지 자체 검증할 수 있다.

## 5. Mockito를 사용한 테스트 단순화
**주제**: 모킹 도구로 테스트 더블 관리 개선 (content.md:290-373)
**이전 화제와의 관계**: 수동으로 만든 스마트 스텁의 복잡성을 해결하는 도구적 접근

### 다뤄지는 내용
수동으로 작성한 스마트 스텁은 로직이 복잡해지고 오류가 발생하기 쉽다. Mockito는 Java의 사실상 표준 모킹 라이브러리로 이러한 문제를 해결한다.

Mockito를 사용한 테스트:

```java
// Mockito 임포트
import static org.mockito.ArgumentMatchers.contains;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

class AnAddressRetriever {
    Http http = mock(Http.class);  // Http 인터페이스의 모크 객체 생성

    @Test
    void answersAppropriateAddressForValidCoordinates() {
        // 모크 설정: 특정 매개변수로 호출되면 JSON 반환
        when(http.get(contains("lat=38.000000&lon=-104.000000"))).thenReturn(
            """
            {"address":{
                "house_number":"324",
                "road":"Main St",
                "city":"Anywhere",
                "state":"Colorado",
                "postcode":"81234",
                "country_code":"us"}}
            """);

        var retriever = new AddressRetriever(http);  // 모크 주입
        var address = retriever.retrieve(38, -104);  // 실행
        // ... 검증 코드
    }
}
```

Mockito의 장점:
- **안전성**: 수동 로직 작성 시 발생할 수 있는 오류 방지
- **단순성**: when().thenReturn() 패턴으로 한 줄에 모크 설정
- **유연성**: contains, and 등의 매처를 통한 정교한 매개변수 검증

더 유연한 매개변수 검증:

```java
// 순서에 관계없이 두 매개변수 모두 확인
when(http.get(
    and(contains("lat=38.000000"), contains("lon=-104.000000"))))
    .thenReturn(/* JSON 응답 */);
```

## 6. Mockito를 통한 의존성 주입
**주제**: Mockito의 내장 의존성 주입 기능 (content.md:400-468)
**이전 화제와의 관계**: 생성자 주입의 한계를 극복하는 자동화된 접근

### 다뤄지는 내용
생성자 주입은 클래스 인터페이스 변경이 필요할 수 있다. Mockito는 어노테이션 기반의 자동 의존성 주입을 제공한다:

```java
// Mockito 어노테이션을 사용한 자동 의존성 주입
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)  // Mockito 확장 활성화
class AnAddressRetriever {
    @InjectMocks  // Mockito가 자동으로 인스턴스 생성 및 모크 주입
    AddressRetriever retriever;

    @Mock  // 자동으로 모크 객체 생성
    Http http;

    @Test
    void answersAppropriateAddressForValidCoordinates() {
        when(http.get(and(contains("lat=38.000000"), contains("lon=-104.000000"))))
            .thenReturn(/* JSON 응답 */);
        // retriever는 이미 http 모크가 주입된 상태
        var address = retriever.retrieve(38, -104);
        // ... 검증
    }
}
```

Mockito 주입 메커니즘:
1. **생성자 주입**: 적절한 생성자를 찾아 모크 주입
2. **세터 주입**: 생성자가 없으면 세터 메서드 사용
3. **필드 주입**: 마지막으로 필드에 직접 주입

필드 주입을 위한 프로덕션 코드 수정:

```java
// 필드 주입을 지원하는 AddressRetriever
public class AddressRetriever {
    private static final String SERVER = "https://nominatim.openstreetmap.org";
    private Http http = new HttpImpl();  // final 제거 필요

    // 생성자 불필요!

    public Address retrieve(double latitude, double longitude) {
        // ... 기존 로직
    }
}
```

프로덕션 클라이언트는 더 이상 Http 인스턴스를 전달할 필요가 없다. 하지만 단점도 있다:
- **설계 문제**: private 필드 조작이 설계 원칙에 위배
- **성능 저하**: 테스트 실행 시간이 거의 1초 증가

## 7. 메서드 호출 검증
**주제**: verify() 메서드를 통한 상호작용 검증 (content.md:469-549)
**이전 화제와의 관계**: 반환값 검증에서 더 나아가 메서드 호출 자체를 검증하는 고급 기능

### 다뤄지는 내용
때로는 메서드가 호출되었는지, 올바른 인자로 호출되었는지 검증해야 한다. 특히 부작용만 있고 반환값이 없는 소비자 메서드의 경우 verify() 기능이 유용하다.

AddressRetriever에 감사 기능 추가:

```java
// 감사 기능이 추가된 AddressRetriever
public class AddressRetriever {
    private Auditor auditor = new ApplicationAuditor();  // 감사자 의존성
    // ...

    public Address retrieve(double latitude, double longitude) {
        // ... 기존 로직
        var country = address.country_code();
        if (!country.equals("us")) {
            auditor.audit("request for country code: %s".formatted(country));  // 감사 기록
            throw new UnsupportedOperationException("intl addresses unsupported");
        }
        return address;
    }
}
```

Auditor 인터페이스:

```java
// 감사 인터페이스 정의
public interface Auditor {
    void audit(String message);  // 반환값이 없는 소비자 메서드
}
```

audit 메서드 호출 검증 테스트:

```java
// verify()를 사용한 메서드 호출 검증
@Test
void auditsWhenNonUSAddressRetrieved() {
    when(http.get(anyString())).thenReturn("""
        {"address":{ "country_code":"not us"}}""");

    assertThrows(UnsupportedOperationException.class,
        () -> retriever.retrieve(1.0, -1.0));

    verify(auditor).audit("request for country code: not us");  // 정확한 메시지로 호출되었는지 검증
}
```

호출되지 않았음을 검증하는 테스트:

```java
// 메서드가 호출되지 않았음을 검증
@Test
void doesNotOccurWhenUSAddressRetrieved() {
    when(http.get(anyString())).thenReturn("""
        {"address":{ "country_code":"us"}}""");

    retriever.retrieve(1.0, -1.0);

    verify(auditor, never()).audit(any());  // 어떤 인자로도 호출되지 않았음을 검증
}
```

verify와 when의 구문 차이:
- `verify(someObject).method();` - 검증 시
- `when(someObject.method()).thenReturn(...);` - 설정 시

## 8. 예외 처리 테스트
**주제**: thenThrow()를 사용한 예외 상황 시뮬레이션 (content.md:553-615)
**이전 화제와의 관계**: 정상 경로 외에 예외 상황에서의 동작을 검증하는 확장

### 다뤄지는 내용
예외 처리는 종종 후순위로 밀리지만 중요한 테스트 영역이다. 현재 AddressRetriever는 HTTP get 메서드에서 발생할 수 있는 오류를 처리하지 않는다. retrieve 메서드가 예외를 전파하지 않고 null을 반환하도록 결정했다.

Mockito를 사용한 예외 시뮬레이션:

```java
// thenThrow()를 사용한 예외 상황 테스트
@Test
void returnsNullWhenHttpGetThrows() {
    when(http.get(anyString())).thenThrow(RuntimeException.class);  // 예외 발생 설정

    var address = retriever.retrieve(38, -104);
    assertNull(address);  // null 반환 검증
}
```

이를 위한 프로덕션 코드 수정 - 예외 처리 로직 추가:

```java
// 예외 처리가 추가된 AddressRetriever
public Address retrieve(double latitude, double longitude) {
    // ... URL 생성 로직
    var jsonResponse = get(url);  // 별도 메서드로 추출
    if (jsonResponse == null) return null;  // null 체크 추가
    // ... 나머지 로직
}

private String get(String url) {  // 예외 처리를 위한 별도 메서드
    try {
        return http.get(url);  // 실제 HTTP 호출
    } catch (Exception e) {
        return null;  // 예외 발생 시 null 반환
    }
}
```

예외 처리 추출의 이점:
- **가독성**: 6줄의 try-catch 블록을 별도 메서드로 분리
- **재사용성**: 예외 처리 로직의 중복 방지
- **테스트 용이성**: 예외 상황과 정상 상황의 명확한 분리

## 9. 빠른 테스트의 중요성
**주제**: 모크 객체를 통한 테스트 성능 향상 (content.md:616-647)
**이전 화제와의 관계**: 모크 사용의 궁극적인 목적 중 하나인 성능 개선에 대한 심화 논의

### 다뤄지는 내용
모크 객체는 외부 종속성으로부터의 격리뿐만 아니라 엄청난 성능 향상도 제공한다.

테스트 속도 정의:
- **빠른 테스트**: 순수 Java 코드만 실행, 최대 수 밀리초
- **느린 테스트**: 외부 종속성(데이터베이스, 파일, 네트워크) 상호작용, 수십-수천 밀리초

성능 차이의 현실적 영향:

```
// 성능 비교 시나리오
2500개 단위 테스트 스위트:
- 느린 테스트 (평균 200ms): 8분 이상
- 빠른 테스트 (평균 5ms): 15초 미만
```

개발 패턴에 미치는 영향:
- **8분 스위트**: 하루 2-3회 실행, 부분 테스트로 타협
- **15초 스위트**: 시간당 여러 번 실행, 완전한 테스트 가능

빠른 테스트의 전략적 중요성:
- **증분적 개발**: 각 변경 후 즉시 검증 가능
- **지속적 통합**: 코드 변경의 빈번하고 자신 있는 통합
- **개발자 생산성**: 빠른 피드백 루프로 인한 효율성 향상

모크의 핵심 가치: 외부 종속성을 제거하여 빠른 테스트를 가능하게 하고, 이를 통해 효과적인 소프트웨어 개발 방식을 지원한다.

## 10. 중요한 테스트 더블 팁들
**주제**: 테스트 더블 사용 시 주의사항과 베스트 프랙티스 (content.md:648-697)
**이전 화제와의 관계**: 앞서 배운 모든 기법들을 올바르게 적용하기 위한 실용적 가이드

### 다뤄지는 내용

### 좋은 모크 기반 테스트 구조:
- **3줄 테스트**: arrange(1줄) + act(1줄) + assert(1줄)
- **가독성**: 매개변수 문자열이 실행 인자와 명확히 연관되어야 함
- **이해도**: 다른 개발자가 빠르게 읽고 이해할 수 있어야 함

### 모크 안전성 고려사항:
```java
// 실제 동작과 모크 동작의 일치성 확인
// 프로덕션 코드가 다른 형식을 반환할 수 있나?
// 예외를 던질 수 있나?
// null을 반환할 수 있나?
// 각 조건마다 별도 테스트 필요
```

### 모크 검증 방법:
- **모크 비활성화**: 실제 프로덕션 코드와 상호작용시켜 차이점 확인
- **예외 삽입**: 프로덕션 코드에서 일시적으로 예외를 던져 모크 사용 확인
- **단계별 디버깅**: 모크가 실제로 호출되는지 확인

### 테스트 데이터 전략:
- **비현실적 데이터**: 프로덕션에서 나올 수 없는 데이터 사용
- **명백한 가짜**: "Anywhere", 깔끔한 정수 등으로 테스트임을 명확히 표시
- **실패 유도**: 실제 클래스 사용 시 테스트가 실패하도록 설계

### 테스트 커버리지 고려사항:
모크는 테스트 커버리지에 구멍을 만든다. 모크로 대체된 코드는 테스트되지 않으므로 적절한 상위 레벨 테스트(통합 테스트)로 실제 클래스의 end-to-end 사용을 검증해야 한다.

### 성능 고려사항:
DI 프레임워크는 테스트 실행을 상당히 느리게 할 수 있다. 수동 의존성 주입이 더 간단하고 빠를 수 있다.

### 인터페이스 노출 원칙:
DI 프레임워크 사용 시 실제 노출된 인터페이스 지점(일반적으로 생성자)을 통한 주입을 선호한다. 교묘함은 복잡성을 만들고 경멸을 키운다.

### 모크 회피 정책:
- **설계 재고**: 많은 테스트에서 테스트 더블이 필요하다면 문제가 있는 종속성이 너무 확산되었을 수 있음
- **책임 이동**: 클래스가 지속성 레이어에 의존하지 않고, 클라이언트가 관련 데이터를 검색해서 주입하도록 설계
- **실제 코드 사용**: 협력자 클래스에 문제가 있는 종속성이 없다면 모킹하지 말고 실제 코드와 상호작용

핵심 원칙: 모크는 훌륭한 도구이지만 큰 골칫거리도 될 수 있다. 신중하게 사용해야 한다.

# 상태: active
# 참조: 원본 content.md 파일에서 추출
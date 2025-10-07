# 3장: 단위 테스트의 해부 - 추출된 정보

## 핵심 내용
- AAA(Arrange, Act, Assert) 패턴을 통한 단위 테스트 구조화
- 단위 테스트 네이밍 모범 사례와 가독성 개선 방법
- 매개변수화된 테스트를 통한 테스트 코드 최적화
- 플루언트 어설션을 활용한 테스트 가독성 향상

## 상세 핵심 내용

### AAA 패턴 (Arrange, Act, Assert)
- **Arrange**: SUT(System Under Test)와 의존성을 원하는 상태로 준비
- **Act**: SUT의 메서드를 호출하고 출력값 캡처
- **Assert**: 결과를 검증 (반환값, 최종 상태, 협력자 호출 등)
- **3A 패턴**이라고도 불리며, 모든 테스트에 균일한 구조 제공

### 테스트 구조화 원칙

#### AAA 섹션의 크기 가이드라인
- **Arrange 섹션**: 일반적으로 가장 큼 (Act + Assert 섹션 합보다 클 수 있음)
- **Act 섹션**: 보통 한 줄의 코드 (두 줄 이상이면 SUT API 문제 신호)
- **Assert 섹션**: 단일 동작 단위의 여러 결과를 모두 평가 가능

#### 캡슐화와 불변식 보호
- **불변식 위반**: 비즈니스 규칙이 깨지는 상태
- **캡슐화**: 불변식 위반으로부터 코드를 보호하는 행위
- **예시**: 구매 성공 시 제품 획득과 재고 감소가 함께 일어나야 함

## 상세 내용

### 피해야 할 안티패턴

#### 1. 여러 개의 AAA 섹션
- 여러 개의 Act 섹션 = 여러 동작 단위 검증 = 통합 테스트
- **해결책**: 각 Act를 개별 테스트로 분리
- **예외**: 느린 통합 테스트에서만 속도 최적화 목적으로 허용

#### 2. 테스트 내 if 문
- 테스트가 한 번에 너무 많은 것을 검증한다는 신호
- **원칙**: 테스트는 분기 없는 단순한 단계 순서여야 함

#### 3. 생성자를 통한 테스트 픽스처 재사용
```csharp
// 잘못된 방법 - 높은 결합도, 가독성 저하
public class CustomerTests
{
    private readonly Store _store;
    private readonly Customer _sut;

    public CustomerTests()
    {
        _store = new Store();
        _sut = new Customer();
    }
}
```

#### 4. 올바른 테스트 픽스처 재사용
```csharp
// 올바른 방법 - 팩토리 메서드 사용
private Store CreateStoreWithInventory(Product product, int quantity)
{
    Store store = new Store();
    store.AddInventory(product, quantity);
    return store;
}
```

### xUnit 테스트 프레임워크 특징
- **[Fact] 특성**: 개별 테스트를 나타내는 깔끔한 표현
- **생성자/Dispose**: SetUp/TearDown 대신 사용
- **규칙 기반**: [TestFixture] 같은 추가 특성 불필요
- **명명 철학**: "Fact"는 각 테스트가 시스템에 대한 사실을 나타낸다는 강조

### 테스트 네이밍 모범 사례

#### 피해야 할 네이밍 규칙
```
[MethodUnderTest]_[Scenario]_[ExpectedResult]
```
- **문제점**: 구현 세부사항에 집중, 동작 대신 코드에 집중
- **예시**: `Sum_TwoNumbers_ReturnsSum` (암호 같고 의미 불분명)

#### 권장하는 네이밍 가이드라인
1. **경직된 네이밍 정책 지양**: 복잡한 동작을 좁은 틀에 맞출 수 없음
2. **도메인 전문가 관점**: 비개발자도 이해할 수 있는 설명
3. **밑줄로 단어 분리**: 가독성 향상, 특히 긴 이름에서
4. **메서드명 포함 금지**: 동작을 테스트하는 것이지 코드를 테스트하는 것이 아님

#### 네이밍 개선 예시
```csharp
// 개선 과정
IsDeliveryValid_InvalidDate_ReturnsFalse               // 경직된 규칙
↓
Delivery_with_invalid_date_should_be_considered_invalid // 자연어화
↓
Delivery_with_past_date_should_be_considered_invalid    // 구체화
↓
Delivery_with_past_date_should_be_invalid              // 간소화
↓
Delivery_with_past_date_is_invalid                     // 사실 진술
↓
Delivery_with_a_past_date_is_invalid                   // 문법 개선
```

### SUT 구분과 섹션 분리
- **SUT 네이밍**: 항상 `sut` 변수명 사용으로 의존성과 구분
- **섹션 분리 방법**:
  - 주석 사용: `// Arrange`, `// Act`, `// Assert`
  - 빈 줄 사용: 간단한 테스트에서 권장
  - **권장사항**: AAA 패턴이 명확하고 섹션 내 추가 빈 줄이 불필요한 경우 주석 생략

## 주요 화제

### 1. 매개변수화된 테스트 (Parameterized Tests)

#### Theory와 Fact의 차이
- **[Fact]**: 단일 사실에 대한 테스트
- **[Theory]**: 여러 사실을 다루는 테스트의 묶음

#### InlineData 사용 예시
```csharp
[InlineData(-1, false)]   // 과거 날짜
[InlineData(0, false)]    // 오늘
[InlineData(1, false)]    // 내일
[InlineData(2, true)]     // 모레
[Theory]
public void Can_detect_an_invalid_delivery_date(int daysFromNow, bool expected)
```

#### 트레이드오프
- **장점**: 테스트 코드량 감소
- **단점**: 테스트가 나타내는 사실들을 파악하기 어려움
- **권장사항**: 입력 매개변수만으로 케이스 구분이 명확할 때만 사용

### 2. MemberData를 통한 복잡한 데이터 생성
```csharp
[Theory]
[MemberData(nameof(Data))]
public void Can_detect_an_invalid_delivery_date(DateTime deliveryDate, bool expected)

public static List<object[]> Data()
{
    return new List<object[]>
    {
        new object[] { DateTime.Now.AddDays(-1), false },
        new object[] { DateTime.Now.AddDays(2), true }
    };
}
```

### 3. Given-When-Then 패턴
- **Given**: Arrange에 해당
- **When**: Act에 해당
- **Then**: Assert에 해당
- **차이점**: 비개발자에게 더 읽기 쉬움
- **적용**: 비기술적 이해관계자와 공유하는 테스트에 적합

## 부차 화제

### 1. 테스트 픽스처 정의
두 가지 의미:
1. **일반적 정의**: 테스트가 실행되는 객체 (의존성, 데이터베이스 데이터, 파일)
2. **NUnit 정의**: 테스트를 포함하는 클래스를 표시하는 특성

### 2. 팩토리 메서드 vs 생성자 재사용
- **팩토리 메서드**: 제네릭하고 읽기 쉬우며 테스트 간 결합도 낮음
- **생성자 재사용**: 모든/거의 모든 테스트에서 사용되는 경우만 예외적 허용
- **통합 테스트**: 베이스 클래스 생성자에서 데이터베이스 연결 초기화

### 3. Teardown 단계
- **단위 테스트**: 대부분 불필요 (프로세스 외부 의존성과 통신하지 않음)
- **통합 테스트**: 파일 정리, 데이터베이스 연결 해제 등에 필요
- **구현**: 별도 메서드로 클래스의 모든 테스트에서 재사용

### 4. 플루언트 어설션 (Fluent Assertions)
```csharp
// 기존 방식
Assert.Equal(30, result);

// 플루언트 어설션
result.Should().Be(30);
```

#### 장점
- **자연어 패턴**: [주어] [동작] [목적어] 구조
- **가독성**: 일반 영어처럼 읽힘
- **풍부한 헬퍼 메서드**: 숫자, 문자열, 컬렉션, 날짜 등

#### 단점
- **추가 의존성**: 개발용이지만 프로젝트에 의존성 추가

### 5. 객체지향 프로그래밍과 가독성
- **OOP 성공 요인**: 코드를 스토리처럼 구조화할 수 있는 가독성 이점
- **인간의 정보 흡수**: 스토리 형태를 선호
- **패턴 적용**: 코드도 동일한 스토리 패턴을 따를 때 더 읽기 쉬움

### 6. C# 특성 제한사항
- **컴파일 타임 평가**: 특성 내용은 컴파일 시점에 평가
- **허용 값**: 상수, 리터럴, typeof() 표현식만 가능
- **DateTime.Now**: 런타임에 의존하므로 InlineData에서 사용 불가
# 11장: 단위 테스트 안티패턴 - 추출된 정보

## 핵심 내용
- 프라이빗 메서드 테스트와 그 문제점
- 코드 오염과 도메인 지식 누출
- 구체 클래스 목킹의 문제점
- 시간 처리와 테스트에서 피해야 할 안티패턴들

## 상세 핵심 내용

### 프라이빗 메서드 테스트 안티패턴
**기본 원칙**: 프라이빗 메서드를 직접 테스트하지 말고, 공개 동작의 일부로 간접 테스트

#### 프라이빗 메서드가 복잡한 경우 해결책
1. **죽은 코드**: 사용되지 않는 코드라면 삭제
2. **누락된 추상화**: 별도 클래스로 추출하여 독립적 테스트

```csharp
// Before: 복잡한 프라이빗 메서드
public class Order
{
    private decimal GetPrice()
    {
        // 복잡한 비즈니스 로직
        decimal basePrice = /* 계산 */;
        decimal discounts = /* 계산 */;
        decimal taxes = /* 계산 */;
        return basePrice - discounts + taxes;
    }
}

// After: 추상화 추출
public class PriceCalculator
{
    public decimal Calculate(Customer customer, List<Product> products)
    {
        // 동일한 로직이지만 독립적으로 테스트 가능
        // 출력 기반 테스트 스타일 적용 가능
    }
}
```

### 코드의 공개성과 목적 관계

| | 구현 세부사항 | 관찰 가능한 동작 |
|---|---|---|
| **Public** | 코드 오염 | 잘 설계된 API |
| **Private** | 잘 설계된 API | N/A* |

*예외: Inquiry 클래스의 private 생성자같은 특수한 경우

### 주요 안티패턴들
1. **프라이빗 메서드 테스트**: 구현 세부사항 결합으로 취약한 테스트
2. **코드 오염**: 테스트만을 위한 프로덕션 코드 추가
3. **구체 클래스 목킹**: 캡슐화 위반과 취약성 증가
4. **과도한 시간 처리**: 복잡한 시간 관련 테스트 로직

## 상세 내용

### 프라이빗 메서드 테스트 예외 케이스
```csharp
public class Inquiry
{
    public bool IsApproved { get; private set; }
    public DateTime? TimeApproved { get; private set; }

    private Inquiry(bool isApproved, DateTime? timeApproved)  // 불변 조건 보장
    {
        if (isApproved && !timeApproved.HasValue)
            throw new Exception();

        IsApproved = isApproved;
        TimeApproved = timeApproved;
    }

    public static Inquiry Approved(DateTime approvedTime) => new Inquiry(true, approvedTime);
    public static Inquiry Rejected() => new Inquiry(false, null);
}

// 프라이빗 생성자를 통한 불변 조건 테스트
[Fact]
public void Creating_an_approved_inquiry_without_approval_time_is_invalid()
{
    Action action = () => (Inquiry)Activator.CreateInstance(
        typeof(Inquiry),
        BindingFlags.Instance | BindingFlags.NonPublic,
        null,
        new object[] { true, null },
        null);

    action.Should().Throw<TargetInvocationException>();
}
```

### 코드 오염 안티패턴
**정의**: 테스트만을 위해 프로덕션 코드에 추가되는 불필요한 코드

#### 일반적인 코드 오염 사례
1. **테스트용 생성자 추가**
2. **테스트용 프로퍼티 노출**
3. **테스트용 메서드 추가**
4. **내부 구현을 위한 public 멤버**

```csharp
// 코드 오염 예시
public class Customer
{
    public string Name { get; private set; }

    // 코드 오염: 테스트만을 위한 기본 생성자
    public Customer() { }  // ❌

    // 코드 오염: 테스트만을 위한 setter
    public string Name { get; set; }  // ❌
}
```

### 구체 클래스 목킹 안티패턴
**문제점**:
- 캡슐화 위반
- 취약한 테스트 (구현 세부사항 결합)
- 복잡성 증가

```csharp
// 잘못된 예: 구체 클래스 목킹
var mock = new Mock<OrderService>(); // ❌
mock.Setup(x => x.CalculateTotal(It.IsAny<List<Item>>())).Returns(100);

// 올바른 예: 인터페이스 사용
public interface IOrderService
{
    decimal CalculateTotal(List<Item> items);
}
var mock = new Mock<IOrderService>(); // ✅
```

## 주요 화제

### 1. 시간 처리 모범 사례
#### Ambient Context 패턴
```csharp
public static class DateTimeServer
{
    private static Func<DateTime> _func = () => DateTime.Now;
    public static DateTime Now => _func();

    public static void Init(Func<DateTime> func) => _func = func;
}

// 테스트에서 사용
[Fact]
public void Some_test()
{
    DateTimeServer.Init(() => new DateTime(2020, 1, 1));

    // 테스트 로직

    // 정리는 필요시 또는 기본값으로 복원
}
```

#### 명시적 의존성 주입의 문제점
- 모든 클래스에 시간 의존성 추가 필요
- 도메인 로직과 인프라 관심사 혼재
- 코드 복잡성 불필요 증가

### 2. 누락된 추상화 식별법
- **단일 책임 원칙 위반**: 여러 일을 하는 메서드
- **높은 복잡도**: 순환 복잡도가 높은 프라이빗 메서드
- **테스트 어려움**: 공개 API를 통한 테스트가 복잡함

### 3. 팩토리 메서드를 통한 불변 조건 보장
```csharp
// 불변 조건을 보장하는 설계
public class Money
{
    public decimal Amount { get; private set; }
    public string Currency { get; private set; }

    private Money(decimal amount, string currency)
    {
        if (amount < 0) throw new ArgumentException("Amount cannot be negative");
        if (string.IsNullOrEmpty(currency)) throw new ArgumentException("Currency is required");

        Amount = amount;
        Currency = currency;
    }

    public static Money Create(decimal amount, string currency) => new Money(amount, currency);
}
```

### 4. 테스트 가능성과 설계 품질
- **좋은 설계 = 테스트하기 쉬운 설계**
- **캡슐화가 잘 된 코드 = 테스트 코드도 간단**
- **단일 책임 원칙을 따르는 클래스 = 독립적 테스트 가능**

## 부차 화제

### 1. 리플렉션을 사용한 프라이빗 멤버 접근
```csharp
// 정말 필요한 경우에만 (예: 불변 조건 검증)
var constructor = typeof(Inquiry).GetConstructors(
    BindingFlags.Instance | BindingFlags.NonPublic)[0];

var inquiry = (Inquiry)constructor.Invoke(new object[] { true, null });
```

**주의사항**:
- 성능 오버헤드
- 컴파일 타임 안전성 상실
- 리팩터링 시 깨지기 쉬움

### 2. 값 객체를 통한 테스트 단순화
```csharp
// 값 객체로 변환하여 비교 단순화
public class Comment
{
    public string Text { get; }
    public string Author { get; }
    public DateTime DateCreated { get; }

    // Equals, GetHashCode 구현
    public override bool Equals(object obj) { /* ... */ }
    public override int GetHashCode() { /* ... */ }
}

// 테스트에서 간단한 비교
Assert.Equal(expectedComment, actualComment); // 객체 전체 비교
```

### 3. 인터페이스 도입 시점
- **실제 필요할 때까지 지연**: YAGNI 원칙
- **두 번째 구현체가 필요할 때**
- **테스트를 위해서만 인터페이스 만들지 않기**

### 4. 테스트 작성 순서와 설계
1. 테스트 작성 (TDD)
2. 최소한의 코드로 통과시키기
3. 리팩터링으로 설계 개선
4. 반복

**장점**: 자연스럽게 테스트 가능한 설계 유도

### 5. 복잡성 지표와 대응
- **순환 복잡도 > 10**: 메서드 분해 고려
- **매개변수 수 > 5**: 객체로 그룹핑 고려
- **라인 수 > 50**: 단일 책임 원칙 위반 의심

### 6. 도메인 지식 누출 방지
```csharp
// 나쁜 예: 테스트에 비즈니스 로직 누출
Assert.Equal(product.Price * 0.9m, order.Total); // ❌ 할인율이 테스트에 하드코딩

// 좋은 예: 결과만 검증
Assert.Equal(expectedTotal, order.Total); // ✅ 비즈니스 로직은 프로덕션 코드에
```
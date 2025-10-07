# 9장: 목킹 모범 사례 - 추출된 정보

## 핵심 내용
- 시스템 가장자리에서 상호작용 검증하기
- 목을 스파이로 교체하여 과도한 명세 문제 해결
- 목킹 시 시간 처리와 단위 테스트에서 목 사용 가이드라인
- 관리되지 않는 종속성에만 목 사용하기

## 상세 핵심 내용

### 목 가치 극대화를 위한 핵심 원칙
1. **관리되지 않는 종속성에만 목 사용** (기본 전제)
2. **시스템 가장자리에서 상호작용 검증**
3. **목을 스파이로 교체하여 결합도 감소**
4. **단위 테스트에서는 목 사용 최소화**

### 시스템 가장자리 검증
**문제점**: 시스템 내부의 추상화 레이어를 목으로 검증
```csharp
// 잘못된 예: 내부 인터페이스 목킹
messageBusMock.Verify(
    x => x.SendEmailChangedMessage(userId, "new@gmail.com"),
    Times.Once);

// 올바른 예: 실제 외부 버스 목킹
busMock.Verify(
    x => x.Send("Type: USER EMAIL CHANGED; Id: 1; NewEmail: new@gmail.com"),
    Times.Once);
```

**해결책**: 실제 외부 시스템과의 통신을 직접 검증

### 목을 스파이로 교체
**목의 문제점**:
- 과도한 명세(Overspecification): 구현 세부사항에 결합
- 취약한 테스트: 내부 구조 변경 시 테스트 실패

**스파이의 장점**:
```csharp
// 스파이 구현 예제
public class MessageBusSpy : IMessageBus
{
    private List<string> _sentMessages = new List<string>();

    public void SendEmailChangedMessage(int userId, string newEmail)
    {
        _sentMessages.Add($"Type: USER EMAIL CHANGED; Id: {userId}; NewEmail: {newEmail}");
    }

    public bool ShouldSendEmailChangedMessage(int userId, string newEmail)
    {
        string expectedMessage = $"Type: USER EMAIL CHANGED; Id: {userId}; NewEmail: {newEmail}";
        return _sentMessages.Contains(expectedMessage);
    }
}
```

## 상세 내용

### 과도한 명세 문제 해결
**과도한 명세**: 최종 결과가 아닌 구현 방식을 검증하는 문제
- **일반적 원인**: 목을 통한 상세한 상호작용 검증
- **해결책**: 최종 결과에 집중한 스파이 사용

### 단위 테스트에서의 목 사용 지침
**일반적 실수**: 도메인 모델 테스트에서 목 남용
```csharp
// 잘못된 예: 단위 테스트에서 목 사용
var factoryMock = new Mock<IUserFactory>();
factoryMock.Setup(x => x.Create(userData)).Returns(user);

// 올바른 예: 실제 팩토리 사용
User user = UserFactory.Create(userData);
```

**핵심 원칙**:
- 단위 테스트에서는 프로세스 외부 종속성만 목 사용
- 관리되지 않는 종속성만 목킹

### 시간 처리 베스트 프랙티스
**앰비언트 컨텍스트 패턴** 사용:
```csharp
public static class DateTimeServer
{
    private static Func<DateTime> _func = () => DateTime.Now;

    public static DateTime Now => _func();

    public static void Init(Func<DateTime> func)
    {
        _func = func;
    }
}

// 테스트에서 사용
DateTimeServer.Init(() => new DateTime(2020, 1, 1));
```

**명시적 시간 인터페이스 문제점**:
- 모든 클래스에 시간 의존성 주입 필요
- 코드 복잡성 증가
- 도메인 로직과 인프라 관심사 혼재

## 주요 화제

### 1. EventDispatcher 도입의 가치
- **관심사 분리**: 도메인 이벤트 → 외부 시스템 호출 변환
- **단일 책임**: 컨트롤러에서 외부 통신 로직 분리
- **테스트 용이성**: 이벤트 검증으로 충분

### 2. 목 vs 스파이 비교
| 측면 | 목 | 스파이 |
|------|----|----|
| 구현 방식 | 프레임워크 자동 생성 | 수동 작성 |
| 검증 방식 | 세부 상호작용 검증 | 최종 결과 검증 |
| 결합도 | 높음 (구현 세부사항) | 낮음 (결과 중심) |
| 유지보수성 | 취약함 | 안정적 |

### 3. 로깅 테스트 전략
**구조적 로깅** (테스트 필요):
- 비즈니스 요구사항과 직결
- 도메인 이벤트 기반
- 감사(Audit) 목적

**지원 로깅** (테스트 불필요):
- 디버깅 목적
- 기술적 세부사항
- 운영 편의성

### 4. 인터페이스 설계 원칙
**잘못된 인터페이스**:
```csharp
// 단일 구현체만 가진 인터페이스
interface IUserFactory
{
    User Create(object[] userData);
}
```

**올바른 설계**:
- 실제 추상화 필요성이 있을 때만 인터페이스 생성
- YAGNI(You Ain't Gonna Need It) 원칙 준수

## 부차 화제

### 1. CRM 시스템 진화 과정
- **초기**: 단순한 이메일 변경
- **개선**: 도메인 이벤트 도입
- **최적화**: EventDispatcher를 통한 관심사 분리

### 2. 도메인 이벤트 활용
```csharp
public class User
{
    private readonly List<IDomainEvent> _domainEvents = new List<IDomainEvent>();

    public void ChangeEmail(string newEmail, Company company)
    {
        // 비즈니스 로직 실행
        if (/* 타입 변경 조건 */)
        {
            _domainEvents.Add(new UserTypeChangedEvent(UserId, oldType, newType));
        }

        _domainEvents.Add(new EmailChangedEvent(UserId, newEmail));
    }
}
```

### 3. 테스트 더블 선택 가이드
- **Dummy**: 매개변수 채우기용
- **Stub**: 간접 입력 제공
- **Spy**: 간접 출력 캡처 (수동 작성)
- **Mock**: 간접 출력 검증 (프레임워크)
- **Fake**: 단순한 작동 구현체

### 4. 통합 테스트 구조화
```csharp
[Fact]
public void Changing_email_from_corporate_to_non_corporate()
{
    // Arrange: 관리되는 종속성은 실제 사용
    var database = new Database(ConnectionString);

    // 관리되지 않는 종속성은 목/스파이 사용
    var messageBusSpy = new MessageBusSpy();

    // Act: 전체 시스템 동작 실행

    // Assert: 상태 변경과 부작용 모두 검증
}
```

### 5. 아키텍처 개선의 단계별 접근
1. **단일 컨트롤러**: 모든 로직 포함
2. **도메인 분리**: 비즈니스 로직을 도메인으로 이동
3. **이벤트 도입**: 도메인 이벤트를 통한 부작용 표현
4. **Dispatcher 분리**: 이벤트 처리 로직 분리

### 6. 성능 고려사항
- **스파이 구현 비용**: 목보다 높지만 장기적 가치
- **테스트 실행 속도**: 실제 종속성 사용 시 느려질 수 있음
- **유지보수 시간**: 스파이가 목보다 안정적
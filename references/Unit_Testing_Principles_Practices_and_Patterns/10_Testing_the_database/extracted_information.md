# 10장: 데이터베이스 테스트 - 추출된 정보

## 핵심 내용
- 데이터베이스 테스트의 전제 조건과 스키마 관리
- 상태 기반 vs 마이그레이션 기반 데이터베이스 배포 방식
- 데이터베이스 트랜잭션 관리와 테스트 데이터 정리
- 데이터베이스 테스트 모범 사례와 성능 최적화

## 상세 핵심 내용

### 데이터베이스 테스트 전제 조건
1. **소스 제어 시스템에 데이터베이스 보관**
   - 스키마를 일반 코드처럼 취급
   - 단일 진실 공급원 유지
   - 변경 이력 추적 가능

2. **개발자별 별도 데이터베이스 인스턴스**
   - 테스트 격리 보장
   - 병렬 개발 지원

3. **마이그레이션 기반 데이터베이스 배포**
   - 상태 기반 접근법보다 우수
   - 순차적 스크립트 실행
   - 모든 환경에서 일관성 보장

### 참조 데이터(Reference Data)
- **정의**: 애플리케이션이 정상 작동하기 위해 미리 채워져 있어야 하는 데이터
- **예**: UserType 테이블의 Customer, Employee 타입 정보
- **관리**: 데이터베이스 스키마의 일부로 취급하여 소스 제어에 포함

### 데이터베이스 배포 방식 비교

#### 상태 기반 접근법 (State-based)
- 현재 상태와 원하는 상태 비교
- 자동 도구가 차이점 스크립트 생성
- **문제점**: 데이터 손실 위험, 복잡한 변경 처리 어려움

#### 마이그레이션 기반 접근법 (Migration-based)
- 순차적인 마이그레이션 스크립트 작성
- 각 스크립트는 특정 버전에서 다음 버전으로 전환
- **장점**: 안전성, 명시성, 완전한 제어

## 상세 내용

### 데이터베이스 트랜잭션 관리
```csharp
[Fact]
public void Changing_email_from_corporate_to_non_corporate()
{
    using var context = new CrmContext(ConnectionString);
    using var transaction = context.Database.BeginTransaction();

    try
    {
        // Arrange
        User user = CreateUser("user@mycorp.com", UserType.Employee, context);

        // Act
        string result = sut.ChangeEmail(user.UserId, "new@gmail.com");

        // Assert
        // 검증 로직

        transaction.Commit();
    }
    finally
    {
        // 자동으로 트랜잭션 롤백 (using 블록)
    }
}
```

### 테스트 데이터 정리 전략
1. **데이터베이스 백업/복원**: 각 테스트 전 깨끗한 상태로 복원
2. **트랜잭션 롤백**: 각 테스트를 트랜잭션으로 감싸고 롤백
3. **데이터 정리**: 테스트 후 생성된 데이터 수동 삭제
4. **인메모리 데이터베이스**: SQLite 등 경량 데이터베이스 사용

### 통합 테스트 구조 최적화
```csharp
[Fact]
public void Changing_email_from_corporate_to_non_corporate()
{
    // Arrange: 핵심 테스트 데이터만 생성
    User user = CreateUser("user@mycorp.com", UserType.Employee);

    // Act: 실제 비즈니스 시나리오 실행
    string result = sut.ChangeEmail(user.UserId, "new@gmail.com");

    // Assert: 핵심 결과만 검증
    Assert.Equal("OK", result);
    User userFromDb = GetUserById(user.UserId);
    Assert.Equal("new@gmail.com", userFromDb.Email);
    Assert.Equal(UserType.Customer, userFromDb.Type);
}
```

## 주요 화제

### 1. 모델 데이터베이스의 문제점
**안티패턴**: 전용 데이터베이스 인스턴스를 참조점으로 사용
- **문제점**: 변경 이력 없음, 복수 진실 공급원
- **해결책**: 소스 제어 시스템에 스키마 저장

### 2. 테스트 데이터 생성자(Test Data Builder)
```csharp
public class UserBuilder
{
    private string _email = "user@company.com";
    private UserType _type = UserType.Employee;

    public UserBuilder WithEmail(string email)
    {
        _email = email;
        return this;
    }

    public UserBuilder WithType(UserType type)
    {
        _type = type;
        return this;
    }

    public User Build() => new User(_email, _type);
}

// 사용법
User user = new UserBuilder()
    .WithEmail("test@example.com")
    .WithType(UserType.Customer)
    .Build();
```

### 3. 읽기 전용 테스트 최적화
```csharp
public class DatabaseTests : IClassFixture<DatabaseFixture>
{
    // 클래스 수준에서 데이터 한 번 생성
    // 여러 읽기 전용 테스트에서 공유
}
```

### 4. 테스트 범주화와 실행 전략
- **단위 테스트**: 빠른 피드백, 개발 중 지속 실행
- **통합 테스트**: 더 느림, 커밋 전이나 CI 파이프라인에서 실행
- **테스트 필터링**: 카테고리별 선택적 실행

## 부차 화제

### 1. Entity Framework를 사용한 테스트
```csharp
// DbContext 설정
public class TestCrmContext : CrmContext
{
    public TestCrmContext() : base(GetConnectionString()) { }

    private static string GetConnectionString()
    {
        return "Server=(localdb)\\mssqllocaldb;Database=CrmTest;Integrated Security=true";
    }
}
```

### 2. 병렬 테스트 실행 고려사항
- **데이터베이스 격리**: 각 테스트 클래스별 별도 데이터베이스
- **테스트 컬렉션**: xUnit의 Collection 특성 사용
- **리소스 경합**: 공유 리소스 접근 시 동기화

### 3. 테스트 성능 최적화
- **연결 풀링**: 데이터베이스 연결 재사용
- **배치 작업**: 여러 SQL 문을 한 번에 실행
- **인덱스 최적화**: 테스트 데이터베이스에도 적절한 인덱스

### 4. Docker를 활용한 테스트 환경
```yaml
# docker-compose.test.yml
services:
  testdb:
    image: mcr.microsoft.com/mssql/server:2019-latest
    environment:
      - SA_PASSWORD=YourPassword123
      - ACCEPT_EULA=Y
    ports:
      - "1433:1433"
```

### 5. 스키마 버전 관리
```sql
-- Migration 001: Create Users table
CREATE TABLE Users (
    Id INT PRIMARY KEY IDENTITY,
    Email VARCHAR(255) NOT NULL,
    Type INT NOT NULL
);

-- Migration 002: Add Companies table
CREATE TABLE Companies (
    Id INT PRIMARY KEY IDENTITY,
    DomainName VARCHAR(255) NOT NULL,
    NumberOfEmployees INT NOT NULL
);
```

### 6. 테스트 데이터의 실제성 vs 단순성
- **실제 데이터**: 프로덕션과 유사한 복잡성
- **단순 데이터**: 테스트 의도가 명확하고 유지보수 쉬움
- **권장사항**: 테스트 목적에 맞는 최소한의 데이터 사용

### 7. 데이터베이스 종속성이 있는 단위 테스트
```csharp
// Repository 패턴을 통한 데이터 접근 추상화
public interface IUserRepository
{
    User GetById(int id);
    void Save(User user);
}

// 테스트에서는 Fake Repository 사용
public class FakeUserRepository : IUserRepository
{
    private readonly List<User> _users = new List<User>();

    public User GetById(int id) => _users.FirstOrDefault(u => u.Id == id);

    public void Save(User user) => _users.Add(user);
}
```
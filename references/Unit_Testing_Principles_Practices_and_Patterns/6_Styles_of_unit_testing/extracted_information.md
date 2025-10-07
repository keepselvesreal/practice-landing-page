# 6장: 단위 테스트의 스타일 - 추출된 정보

## 핵심 내용
- 단위 테스트의 3가지 스타일과 각각의 특성
- 출력 기반 테스트가 최고 품질이지만 제한적 적용 가능성
- 함수형 프로그래밍과 함수형 아키텍처의 기본 개념
- 출력 기반 테스트로의 전환을 위한 코드 구조 개선

## 상세 핵심 내용

### 3가지 단위 테스트 스타일
1. **출력 기반 테스트 (Output-based testing)**
   - 입력을 제공하고 출력을 검증
   - 부작용 없는 순수 함수에만 적용 가능
   - 최고의 품질 보장 (함수형 테스트라고도 함)

2. **상태 기반 테스트 (State-based testing)**
   - 작업 완료 후 시스템 상태 검증
   - SUT, 협력 객체, 또는 프로세스 외부 종속성의 상태 확인

3. **통신 기반 테스트 (Communication-based testing)**
   - SUT와 협력 객체 간의 상호작용 검증
   - 목(Mock)을 사용한 호출 패턴 확인

### 4가지 속성으로 본 스타일 비교

| 스타일 | 리팩터링 저항성 주의도 | 유지보수 비용 |
|--------|---------------------|--------------|
| 출력 기반 | 낮음 | 낮음 |
| 상태 기반 | 중간 | 중간 |
| 통신 기반 | 중간 | 높음 |

*주: 회귀 방지와 빠른 피드백은 스타일과 무관하게 비슷함*

### 함수형 프로그래밍의 핵심
- **수학적 함수**: 숨겨진 입출력이 없는 함수
- **순수성**: 같은 입력에 대해 항상 같은 출력
- **명시적 시그니처**: 모든 입출력이 메서드 시그니처에 표현

## 상세 내용

### 출력 기반 테스트의 장점
```csharp
// 완벽한 출력 기반 테스트 예제
public class PriceEngine
{
    public decimal CalculateDiscount(params Product[] products)
    {
        decimal discount = products.Length * 0.01m;
        return Math.Min(discount, 0.2m);
    }
}

[Fact]
public void Discount_of_two_products()
{
    var sut = new PriceEngine();
    decimal discount = sut.CalculateDiscount(product1, product2);
    Assert.Equal(0.02m, discount);
}
```

### 상태 기반 테스트의 복잡성
```csharp
// 상태 검증은 더 많은 코드 필요
[Fact]
public void Adding_a_comment_to_an_article()
{
    var sut = new Article();
    sut.AddComment("Comment text", "John Doe", new DateTime(2019, 4, 1));

    Assert.Equal(1, sut.Comments.Count);
    Assert.Equal("Comment text", sut.Comments[0].Text);
    Assert.Equal("John Doe", sut.Comments[0].Author);
    Assert.Equal(new DateTime(2019, 4, 1), sut.Comments[0].DateCreated);
}
```

### 상태 기반 테스트 개선 기법
1. **도우미 메서드 사용**
```csharp
sut.ShouldContainNumberOfComments(1)
   .WithComment(text, author, now);
```

2. **값 객체 변환**
```csharp
sut.Comments.Should().BeEquivalentTo(comment);
```

### 통신 기반 테스트의 한계
- 목 설정과 상호작용 검증으로 인한 높은 유지보수 비용
- 목 체인(Mock chains) 사용 시 복잡성 증가
- 구현 세부사항 결합 위험성

## 주요 화제

### 1. 스타일과 학파의 관계
- **고전 학파**: 상태 기반 > 통신 기반 선호, 둘 다 출력 기반 사용
- **런던 학파**: 통신 기반 > 상태 기반 선호, 둘 다 출력 기반 사용

### 2. 리팩터링 저항성 분석
- **출력 기반**: 메서드만 결합, 최고의 저항성
- **상태 기반**: 더 큰 API 표면으로 인한 구현 세부사항 누출 가능성
- **통신 기반**: 목 오용 시 취약한 테스트 발생 (5장 참조)

### 3. 유지보수성 세부 분석
- **테스트 이해 난이도**: 테스트 크기에 따라 결정
- **테스트 실행 난이도**: 프로세스 외부 종속성 수에 따라 결정
- **출력 기반**: 보통 2-3줄의 간결한 코드
- **통신 기반**: 목 설정과 검증으로 인한 긴 코드

### 4. 함수형 아키텍처와 육각형 아키텍처 비교
- **공통점**: 비즈니스 로직과 외부 통신 분리
- **차이점**: 함수형은 모든 협력 객체로부터 분리, 육각형은 프로세스 외부 종속성만 분리
- **함수형 코어**: 불변 종속성만 사용, 수직 축(복잡성)에 가까움
- **가변 셸**: 함수형 코어와 외부 세계 연결

## 부차 화제

### 1. 수학적 함수의 정의
- 수학에서 함수: 첫 번째 집합의 각 원소를 두 번째 집합의 정확히 하나의 원소와 연결
- 프로그래밍에서: 숨겨진 입출력이 없는 메서드
- 예: `f(x) = x + 1`은 완벽한 수학적 함수

### 2. 코드 오염(Code Pollution) 경고
- 테스트 목적으로만 프로덕션 코드에 추가되는 코드
- 값 객체 변환은 클래스가 본질적으로 값일 때만 적용
- 11장에서 단위 테스트 안티패턴으로 자세히 다룸

### 3. Fluent Assertions 활용
```csharp
// 컬렉션 전체 비교로 개별 속성 검증 불필요
sut.Comments.Should().BeEquivalentTo(expectedComments);
```

### 4. 통신 기반 테스트 성능
- 목 사용으로 인한 약간의 런타임 지연
- 수만 개의 테스트가 아닌 이상 무시할 수 있는 차이
- 유지보수성 문제가 더 중요

### 5. 얕은 테스트(Shallow Tests) 경고
- 통신 기반 테스트의 극단적 오용 사례
- 모든 것을 목으로 대체해 실제 코드를 거의 검증하지 않음
- 스타일 자체의 문제가 아닌 오용의 결과

### 6. 도우미 메서드 사용 지침
- 여러 테스트에서 재사용될 때만 작성 비용 정당화
- 단일 테스트를 위한 도우미 메서드는 비효율적
- 3부에서 도우미 메서드에 대해 자세히 다룸
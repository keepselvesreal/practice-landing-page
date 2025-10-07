# Test_Driven_Development_with_Java_Chapter_9_Hexagonal_Architecture_Decoupling_External_Systems

## 압축 내용

Hexagonal Architecture(육각형 아키텍처)는 **Dependency Inversion Principle**을 적용하여 **도메인 모델**을 외부 시스템으로부터 완전히 격리시키고, **포트(Ports)**와 **어댑터(Adapters)**를 통해 외부 시스템과 통신함으로써 **FIRST 단위 테스트**로 전체 사용자 스토리를 테스트할 수 있게 하고, 외부 시스템 변경에 대한 복원력을 제공한다.

---

## 핵심 내용

### 핵심 개념
1. **외부 시스템의 테스트 어려움** → 상세 내용 1
2. **Hexagonal Architecture 구조** → 상세 내용 2
3. **포트(Ports)와 어댑터(Adapters)** → 상세 내용 3
4. **Dependency Inversion 적용** → 상세 내용 4
5. **도메인 모델 격리** → 상세 내용 5
6. **테스트 더블로 전체 도메인 테스트** → 상세 내용 6

### 핵심 개념 설명

#### 1. 외부 시스템의 테스트 어려움 → [상세 내용 섹션 1]
외부 시스템(데이터베이스, 웹 서비스, OS 호출 등)에 직접 의존하는 코드는 테스트하기 어렵다.
- **환경 문제**: 네트워크 연결 끊김, 전원 장애, 장비 한계
- **데이터 불확실성**: 프로덕션 데이터를 미리 알 수 없음
- **실제 트랜잭션 위험**: 테스트가 실제 결과를 유발 (하와이 미사일 경보 사례)
- **느린 실행**: 데이터베이스 정리 등으로 테스트가 느림

**관계**: 이 문제들이 Hexagonal Architecture의 필요성을 만들고, 포트와 어댑터 패턴으로 해결된다.

#### 2. Hexagonal Architecture 구조 → [상세 내용 섹션 2]
애플리케이션을 4개 계층으로 나누어 도메인 로직을 외부 시스템으로부터 격리한다.
- **도메인 모델(Domain Model)**: 핵심 애플리케이션 로직
- **포트(Ports)**: 외부 시스템이 필요한 이유를 추상화
- **어댑터(Adapters)**: 외부 시스템의 구체적 API 구현
- **외부 시스템(External Systems)**: 웹 브라우저, 데이터베이스, 서비스 등

**관계**: Dependency Inversion을 적용한 구조로, 도메인 모델 격리를 실현하는 구체적 방법이다.

#### 3. 포트(Ports)와 어댑터(Adapters) → [상세 내용 섹션 3]
**포트**: 도메인 모델이 외부 시스템을 필요로 하는 이유를 기술 독립적으로 표현
- 인터페이스로 정의
- 도메인 용어로만 작성
- HTTP, JSON, SQL 등의 기술 세부사항 없음

**어댑터**: 외부 시스템의 구체적 API를 포트 인터페이스로 구현
- 외부 시스템과 통신하는 모든 지식 캡슐화
- 단일 책임: 특정 외부 시스템과의 통신만 담당

**관계**: 포트는 Dependency Inversion의 추상화이고, 어댑터는 구체적 구현이다.

#### 4. Dependency Inversion 적용 → [상세 내용 섹션 4]
도메인 모델이 포트 인터페이스에 의존하고, 어댑터가 포트를 구현함으로써 의존성을 역전시킨다.
- 도메인 모델 → 포트 인터페이스 (추상)
- 어댑터 → 포트 인터페이스 구현 (구체)
- 도메인 모델은 어댑터를 직접 알지 못함

**관계**: SOLID 원칙의 적용으로 Hexagonal Architecture의 핵심 메커니즘이며, 테스트 더블 사용을 가능하게 한다.

#### 5. 도메인 모델 격리 → [상세 내용 섹션 5]
도메인 모델은 외부 시스템의 세부사항 없이 순수 비즈니스 로직만 포함한다.
- 사용자 문제 영역의 언어 사용
- 사용자 스토리의 용어 직접 반영
- 기술 세부사항이 아닌 문제 해결에 집중

**관계**: Hexagonal Architecture의 목적이자 결과로, 포트와 어댑터를 통해 실현된다.

#### 6. 테스트 더블로 전체 도메인 테스트 → [상세 내용 섹션 6]
모든 어댑터를 테스트 더블로 교체하여 FIRST 단위 테스트로 전체 도메인 모델을 테스트할 수 있다.
- **빠른 실행**: 초 단위로 전체 도메인 테스트
- **반복 가능**: 외부 환경 독립적
- **더 큰 단위 테스트**: 전체 사용자 스토리를 단위 테스트로 커버

**관계**: Hexagonal Architecture의 가장 큰 TDD 장점으로, 도메인 모델 격리와 포트/어댑터 분리의 결과이다.

### 핵심 개념 간 관계
**외부 시스템의 테스트 어려움** → **Dependency Inversion 적용** → **Hexagonal Architecture 구조** 설계 → **포트와 어댑터 분리** → **도메인 모델 격리** 달성 → **테스트 더블로 전체 도메인 테스트** 가능

---

## 상세 내용

### 목차
1. 외부 시스템이 어려운 이유
2. Dependency Inversion이 구원하다
3. 외부 시스템 추상화하기
4. 도메인 코드 작성하기
5. 외부 시스템을 테스트 더블로 대체하기
6. 더 큰 단위 테스트하기
7. Wordz - 데이터베이스 추상화

---

### 1. 외부 시스템이 어려운 이유 → [핵심 개념 1]

**출처**: Lines 32-139

#### 1.1 단순한 접근의 문제점 (Lines 32-50)

**단일 코드 조각 설계**:
- 사용자가 데이터베이스에서 월간 판매 리포트를 가져오는 작업
- 하나의 코드가 모든 것을 수행: 데이터베이스 연결 → 쿼리 → 처리 → 포맷팅

**문제점**:
- 3가지 책임 혼합: 데이터베이스 접근, 로직 수행, 리포트 포맷팅
- SQL 문과 HTML5 태그가 섞임
- 한 영역의 변경이 다른 영역으로 파급
- 테스트를 위해 리포트 포맷 파싱 필요
- 데이터베이스와 직접 작업 필요

#### 1.2 환경 문제 (Lines 58-85)

**출처**: Lines 58-71

**네트워크 및 인프라 문제**:
- **네트워크 연결 끊김**: 케이블 분리, ISP 연결 끊김
- **전원 장애**: 데이터베이스 서버, 네트워크 스위치 전원 장애
- **장비 한계**: 디스크 공간 부족, 느린 쿼리 (인덱스 누락)

**데이터 관리 문제** (Lines 72-85):
- 프로덕션 데이터를 미리 알 수 없음 → 테스트에서 예상 결과 예측 불가
- 테스트 데이터 추가 → 실제 사용자가 상호작용할 수 있는 가짜 사용자 생성
- 데이터 저장 → 중복 항목 에러 발생
- 테스트 정리 필요 → 실패 시 정리 코드 실행 안 됨 → 느린 테스트

#### 1.3 실제 트랜잭션 위험 (Lines 86-101)

**출처**: Lines 86-101

**하와이 미사일 경보 사례**:
- 시스템 테스트가 실제 문자 메시지 발송
- "하와이가 미사일 공격 받고 있음" (실제로는 아님)

**실제 결과**:
- 결제 프로세서가 실제 청구
- 실제 은행 계좌에서 인출
- 알람 활성화로 실제 대피
- **3R 손실**: Revenue(수익), Reputation(평판), Retention(유지율)

#### 1.4 데이터 불확실성 (Lines 102-108)

**순환 의존성 문제**:
- 판매 리포트의 정답을 미리 알아야 테스트 가능
- 프로덕션 시스템 연결 시 정답은 리포트가 말하는 것
- 판매 리포트 코드가 작동해야 판매 리포트 코드 테스트 가능 (순환 의존)

#### 1.5 OS 호출과 시스템 시간 (Lines 109-117)

**로그 파일 정리 유틸리티 예제**:
- 매주 월요일 02:00 A.M.에 `/logfiles/` 디렉토리의 모든 파일 삭제

**테스트 어려움**:
- 월요일 02:00 A.M.까지 대기 필요
- 모든 로그 파일이 삭제되었는지 확인
- 효과적이지 않음
- 원하는 시간에 파일 삭제 없이 테스트하는 더 나은 접근 필요

#### 1.6 타사 서비스 문제 (Lines 118-135)

**출처**: Lines 118-135

**결제 프로세서 (PayPal, Stripe) 예제**:

**추가 문제**:
- **서비스 다운타임**: 정기 유지보수 기간 → 테스트 실패
- **API 변경**:
  - 코드는 API v1 사용
  - API v2 배포 → v1 호출이 작동하지 않을 수 있음
  - Breaking published interface (나쁜 관행이지만 발생)
  - 단일 코드 조각 → v2 변경이 코드 전체에 영향
- **느린 응답**: API 호출이 예상보다 늦게 응답 → 코드 및 테스트 실패

---

### 2. Dependency Inversion이 구원하다 → [핵심 개념 2, 4]

**출처**: Lines 140-342

#### 2.1 SOLID 원칙 적용 (Lines 140-182)

**이전 학습 내용** (Lines 144-147):
- **Dependency Inversion Principle**: 테스트 대상 코드를 협력자 세부사항으로부터 격리
- **Single Responsibility Principle**: 소프트웨어를 작은 집중된 작업으로 분할

**개선된 설계** (Lines 148-182):

**3가지 별도 작업으로 분할**:
1. 리포트 포맷팅
2. 판매 총계 계산
3. 데이터베이스에서 판매 데이터 읽기

**Dependency Inversion 적용 장점**:
- 계산 코드가 데이터베이스와 포맷팅으로부터 완전히 격리
- 모든 데이터베이스에 접근할 수 있는 코드로 교체 가능
- 모든 리포트 포맷팅 코드로 교체 가능
- 포맷팅 및 데이터베이스 접근 코드 대신 테스트 더블 사용 가능

**주요 장점**:
- 계산 코드 변경 없이 Postgres SQL → Mongo NoSQL 전환 가능
- FIRST 단위 테스트를 위해 데이터베이스용 테스트 더블 사용 가능
- 순수 코드 작성에서 소프트웨어 엔지니어링으로 이동

#### 2.2 Hexagonal Architecture로 일반화 (Lines 183-211)

**출처**: Lines 183-199

**질문**: 이 접근을 전체 애플리케이션으로 확장 가능한가?

**답변**: 가능하며, 이것이 **Hexagonal Architecture**

**구조** (Lines 194-199):
- 또한 **Ports and Adapters**라고도 함 (Alastair Cockburn의 원래 용어)
- 애플리케이션의 핵심 로직을 외부 시스템 세부사항으로부터 완전히 격리
- 핵심 로직 테스트에 도움
- 잘 설계된 코드의 합리적 템플릿 제공

#### 2.3 4개 공간으로 분할 (Lines 200-210)

**출처**: Lines 200-210

1. **External Systems**: 웹 브라우저, 데이터베이스, 컴퓨팅 서비스
2. **Adapters**: 외부 시스템이 요구하는 구체적 API 구현
3. **Ports**: 애플리케이션이 외부 시스템으로부터 필요로 하는 것의 추상화
4. **Domain Model**: 외부 시스템 세부사항 없는 애플리케이션 로직

**중심**: 도메인 모델이 중심, 외부 시스템의 지원으로 둘러싸임

#### 2.4 외부 시스템과 어댑터 (Lines 215-239)

**출처**: Lines 215-239

**외부 시스템 예시**:
- 사용자와 직접 상호작용: 웹 브라우저, 콘솔 애플리케이션
- 데이터 저장소: SQL 데이터베이스, NoSQL 데이터베이스
- 기타: 데스크톱 GUI, 파일시스템, 다운스트림 웹 서비스, 하드웨어 드라이버

**어댑터의 역할**:
- 외부 시스템과 통신하는 책임
- 핵심 애플리케이션 코드는 외부 시스템과 상호작용하는 방법을 알지 못함

**REST 어댑터 예제** (Lines 225-239):
- 웹 브라우저 → REST 어댑터 연결
- HTTP 요청/응답 이해
- JSON 데이터 포맷 이해
- 애플리케이션의 REST API 프로토콜 이해
- **단일 책임**: 외부 시스템과 상호작용하는 방법만 알고 있음

**핵심 원칙**: "어댑터는 외부 시스템과 상호작용하는 데 필요한 모든 지식을 캡슐화하며, 그 외 아무것도 아님"

#### 2.5 어댑터와 포트 연결 (Lines 244-282)

**출처**: Lines 244-282

**포트 정의**:
- 도메인 모델의 일부
- 어댑터의 복잡한 외부 시스템 지식을 추상화
- 질문: "외부 시스템이 왜 필요한가?"
- Dependency Inversion Principle 사용하여 도메인 코드 격리

**Commands 포트 예제** (Lines 256-261):

```java
package com.sales.domain;
import java.time.LocalDate;

public interface Commands {
    SalesReport calculateForPeriod(LocalDate start,
                                   LocalDate end);
}
```

```python
# Python 버전
from datetime import date
from typing import Protocol

class Commands(Protocol):
    """판매 리포트 명령 포트"""
    def calculate_for_period(self, start: date, end: date) -> SalesReport:
        """기간에 대한 판매 리포트 계산"""
        ...
```

**포트의 특징** (Lines 262-270):
- `HttpServletRequest`나 HTTP 관련 참조 없음
- JSON 포맷 참조 없음
- 도메인 모델 참조: `SalesReport`, `java.time.LocalDate`
- `public` 접근 제어자로 REST 어댑터에서 호출 가능

**다중 어댑터 지원** (Lines 272-277):
- REST 어댑터와 콘솔 어댑터가 동일한 포트에 연결
- 외부 시스템(웹, 커맨드 라인)이 다르지만 애플리케이션은 동일한 작업 수행
- 하나의 명령 세트만 지원, 요청 소스와 무관

**핵심 원칙**: "포트는 애플리케이션이 외부 시스템으로부터 필요로 하는 것의 논리적 관점을 제공하며, 기술적으로 어떻게 충족되어야 하는지 제약하지 않음"

#### 2.6 포트와 도메인 모델 연결 (Lines 283-308)

**출처**: Lines 283-308

**도메인 모델 역할**:
- 애플리케이션 로직이 사는 곳
- 애플리케이션이 해결하는 문제를 위한 순수 로직
- 포트와 어댑터로 인해 외부 시스템 세부사항으로부터 자유로움

**도메인 모델의 내용** (Lines 288-292):
- 사용자가 하고 싶은 일을 코드로 표현
- 모든 사용자 스토리가 여기 코드로 기술됨
- 이상적으로 기술 세부사항 대신 문제 영역의 언어 사용
- **스토리텔링**: 사용자가 관심 있는 행동을 사용자 용어로 기술

**프로그래밍 패러다임 자유** (Lines 293-303):
- Functional Programming (FP) 아이디어 사용 가능
- Object-Oriented Programming (OOP) 아이디어 사용 가능
- 절차적 프로그래밍 가능
- 기성 라이브러리를 선언적으로 구성 가능
- Hexagonal Architecture나 TDD에 상관없음
- 저자의 현재 스타일: OOP로 전체 구조 조직, FP 아이디어로 객체 메서드 구현

**핵심 원칙**: "도메인 모델은 사용자 문제가 어떻게 해결되는지 기술하는 코드를 포함. 이것이 비즈니스 가치를 창출하는 애플리케이션의 본질적 로직"

#### 2.7 황금 규칙 (Lines 309-327)

**출처**: Lines 309-327

**주요 규칙**: 도메인 모델은 어댑터에 절대 직접 연결하지 않음. 항상 포트를 통해 수행.

**검증 방법** (Lines 313-319):
- 도메인 모델: `domain` 패키지 (및 하위 패키지)
- 어댑터: `adapters` 패키지 (및 하위 패키지)
- `domain` 패키지의 코드는 `adapters` 패키지로부터 import 문 없음
- 코드 리뷰, 페어링/모빙에서 시각적 검사 가능
- SonarQube 같은 정적 분석 도구로 빌드 파이프라인에서 자동 검사

**Hexagonal Architecture의 황금 규칙들** (Lines 320-327):
1. 도메인 모델은 어댑터 레이어의 어떤 것과도 직접 연결하지 않음 → 애플리케이션 로직이 외부 시스템 세부사항에 의존하지 않음
2. 어댑터는 포트에 연결 → 외부 시스템에 연결하는 코드가 격리됨
3. 포트는 도메인 모델의 일부 → 외부 시스템의 추상화 생성
4. 도메인 모델과 어댑터는 포트에만 의존 → Dependency Inversion 작동 중

#### 2.8 왜 육각형 모양인가? (Lines 332-339)

**출처**: Lines 332-339

**육각형 의미**:
- 각 면이 하나의 외부 시스템 표현
- 설계의 그래픽 표현으로 최대 6개 외부 시스템이면 충분
- 내부/외부 육각형: 도메인 모델이 핵심이며 포트/어댑터 레이어로 격리됨을 그래픽으로 표현

**핵심 아이디어**:
- Ports and Adapters 기술이 중요
- 실제 면의 수는 외부 시스템 수에 따라 다름
- 면의 수는 중요하지 않음

---

### 3. 외부 시스템 추상화하기 → [핵심 개념 3]

**출처**: Lines 343-488

#### 3.1 도메인 모델이 필요로 하는 것 결정 (Lines 348-365)

**출처**: Lines 348-365

**설계 시작점**: 도메인 모델부터 시작

**포트 설계 요구사항**:
- 외부 시스템의 세부사항 없음
- 애플리케이션이 이 시스템을 필요로 하는 이유에 답
- 추상화 생성

**추상화 사고 방법** (Lines 353-356):
- 작업 수행 방법을 변경해도 동일하게 유지되는 것
- 예: 따뜻한 수프 먹기 원함 → 스토브 또는 전자레인지로 데움 → "수프를 데운다"가 추상화

**일반적인 추상화** (Lines 357-365):
- 웹 연결
- 데이터 저장소 (타사 데이터베이스)
- 다른 웹 서비스 호출 (내부 서비스 플릿 또는 타사 서비스)
- 신용카드 결제 프로세서 예

#### 3.2 웹 요청과 응답 추상화 (Lines 370-410)

**출처**: Lines 370-410

**목표**: HTTP 요청/응답을 도메인 모델 용어로 표현, 웹 기술 제거

**RequestSalesReport 도메인 객체** (Lines 374-388):

```java
package com.sales.domain;
import java.time.LocalDate;

public class RequestSalesReport {
    private final LocalDate start;  // 시작 날짜
    private final LocalDate end;    // 종료 날짜

    public RequestSalesReport(LocalDate start, LocalDate end){
        this.start = start;
        this.end = end;
    }

    public SalesReport produce(SalesReporting reporting) {
        return reporting.reportForPeriod(start, end);
    }
}
```

```python
# Python 버전
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class RequestSalesReport:
    """판매 리포트 요청을 표현하는 도메인 객체"""
    start: date  # 시작 날짜
    end: date    # 종료 날짜

    def produce(self, reporting: SalesReporting) -> SalesReport:
        """리포트 생성 (Tell, Don't Ask 패턴)"""
        return reporting.report_for_period(self.start, self.end)
```

**존재하는 것** (Lines 389-393):
- 요청 내용: 판매 리포트 (클래스명에서 캡처)
- 요청 매개변수: 리포팅 기간의 시작/종료 날짜
- 응답: `SalesReport` 클래스가 요청된 원시 정보 포함

**존재하지 않는 것** (Lines 394-397):
- 웹 요청의 데이터 포맷
- HTTP 상태 코드 (예: 200 OK)
- `HttpServletRequest`, `HttpServletResponse` 또는 동등 프레임워크 객체

**장점** (Lines 402-410):
- 순수 도메인 모델 표현
- 웹에서 온 것이라는 힌트 없음
- 다른 입력 소스(데스크톱 GUI, 커맨드 라인)에서 요청 가능
- 단위 테스트에서 쉽게 생성 가능
- OOP의 Tell-Don't-Ask 접근 또는 FP 접근 가능
- Java 17 record로 순수 데이터 구조 표현 가능

#### 3.3 데이터베이스 추상화 (Lines 411-457)

**출처**: Lines 411-457

**중요성**: 데이터 없는 애플리케이션은 유용하지 않고, 데이터 저장 없으면 건망증

**데이터베이스 포트 2가지 구성요소** (Lines 418-426):

1. **인터페이스** - 데이터베이스에 대한 의존성 역전
   - Repository 또는 Data Access Object로 알려짐
   - 도메인 모델을 데이터베이스와 접근 기술의 모든 부분으로부터 격리

2. **Value Objects** - 도메인 모델 용어로 데이터 자체 표현
   - 데이터를 장소 간에 전송하기 위해 존재
   - 동일한 데이터 값을 가진 두 value object는 동등으로 간주
   - 데이터베이스와 코드 간 데이터 전송에 이상적

**SalesRepository 설계 예제** (Lines 427-432):

```java
package com.sales.domain;

public interface SalesRepository {
    List<Sale> allWithinDateRange(LocalDate start,
                                  LocalDate end);
}
```

```python
# Python 버전
from datetime import date
from typing import Protocol, List

class SalesRepository(Protocol):
    """판매 데이터 저장소 포트"""
    def all_within_date_range(self, start: date, end: date) -> List[Sale]:
        """날짜 범위 내의 모든 판매 데이터 조회"""
        ...
```

**특징** (Lines 437-442):
- `allWithinDateRange()` 메서드: 날짜 범위 내의 개별 판매 트랜잭션 가져오기
- `java.util.List`의 간단한 `Sale` value object 반환
- 완전한 도메인 모델 객체
- 핵심 애플리케이션 로직을 수행하는 메서드 포함 가능
- 기본 데이터 구조일 수도 (Java 17 record 사용 가능)

**존재하지 않는 것** (Lines 443-448):
- 데이터베이스 연결 문자열
- JDBC 또는 JPA API 세부사항
- SQL 쿼리 (또는 NoSQL 쿼리)
- 데이터베이스 스키마와 테이블명
- 데이터베이스 저장 프로시저 세부사항

**설계 트레이드오프** (Lines 449-457):
- 데이터베이스와 도메인 모델 간 작업 분배 결정 필요
- 복잡한 쿼리를 데이터베이스 어댑터에 작성할지, 단순한 쿼리로 도메인 모델에서 추가 작업할지
- 저장 프로시저 사용 여부
- 모든 결정이 데이터베이스 어댑터에 상주
- 어댑터가 데이터 스키마와 데이터베이스 기술의 설계 세부사항 캡슐화

#### 3.4 웹 서비스 호출 추상화 (Lines 458-485)

**출처**: Lines 458-485

**일반적 작업**: 다른 웹 서비스 호출 (결제 프로세서, 주소 조회 서비스)

**추상화 구성요소**:
- 호출하는 웹 서비스에 대한 의존성을 역전시키는 인터페이스
- 데이터 전송을 위한 value object

**MappingService 예제** (Lines 466-476):

```java
package com.sales.domain;

public interface MappingService {
    void addReview(GeographicLocation location,
                   Review review);
}
```

```python
# Python 버전
from typing import Protocol

class MappingService(Protocol):
    """지도 서비스 포트"""
    def add_review(self, location: GeographicLocation, review: Review) -> None:
        """특정 위치에 리뷰 추가"""
        ...
```

**특징** (Lines 477-482):
- `MappingService` 인터페이스로 전체 표현
- 특정 위치에 리뷰 추가 메서드
- `GeographicLocation`으로 장소 표현 (우리 용어로)
  - 위도/경도 쌍 또는 우편번호 기반 가능 (설계 결정)
- 기본 지도 서비스나 API 세부사항의 징후 없음
- 실제 코드는 어댑터에 존재

**장점** (Lines 483-485):
- 외부 서비스용 테스트 더블 사용 가능
- 미래에 서비스 제공자 변경 가능
- 외부 서비스 종료 또는 비용 증가 대비
- Hexagonal Architecture로 옵션 열어두기

---

### 4. 도메인 코드 작성하기 → [핵심 개념 5]

**출처**: Lines 489-544

#### 4.1 도메인 모델에 포함할 내용 결정 (Lines 494-518)

**출처**: Lines 494-518

**도메인 모델의 본질** (Lines 494-499):
- 애플리케이션의 핵심
- Hexagonal Architecture가 전면 중앙에 배치
- 사용자 문제 영역의 언어 사용 (Domain에서 이름 유래)
- 사용자가 인식할 수 있는 프로그램 요소 이름
- 해결 메커니즘보다 해결되는 문제 인식
- 사용자 스토리의 용어 사용

**독립성 선택** (Lines 500-505):
- 문제 해결에 필수적이지 않은 것들로부터 독립
- 외부 시스템이 격리되는 이유
- 예: 판매 리포트
  - 초기 생각: 파일 읽기와 HTML 문서 생성 필수
  - 본질: 어딘가에서 판매 데이터 가져오기, 총계 계산, 어떤 방식으로든 포맷팅
  - "어딘가"와 "어떤 방식"은 변경 가능, 솔루션의 본질에 영향 없음

**설계 접근** (Lines 510-518):
- 표준 분석 및 설계 접근 사용 가능
- 객체 선택 또는 함수로 분해 자유
- 문제의 본질과 구현 세부사항 간 구분만 보존

**판단 필요 예제**:
- 판매 리포트: 판매 데이터 소스 무관 (추상화 적절)
- Java 파일 린터: 파일 개념을 도메인 모델에 직접 표현 (문제 영역이 Java 파일 작업이므로 명확히 해야 함)
  - OS별 파일 읽기/쓰기 세부사항에서 파일의 도메인 모델 분리 가능

#### 4.2 도메인 모델에서 라이브러리와 프레임워크 사용 (Lines 519-526)

**출처**: Lines 519-526

**사용 가능 라이브러리**:
- Apache Commons, Java Standard Runtime library 같은 일반 라이브러리는 문제 없음

**주의 필요 프레임워크**:
- 외부 시스템과 어댑터 레이어 세계에 우리를 묶는 프레임워크
- 의존성 역전 필요, 어댑터 레이어의 구현 세부사항으로 남겨둠

**예**: Spring Boot의 `@RestController` 어노테이션
- 처음에는 순수 도메인 코드처럼 보임
- 실제로는 웹 어댑터 특정 생성 코드에 클래스를 강하게 결합

#### 4.3 프로그래밍 접근 결정 (Lines 527-540)

**출처**: Lines 527-540

**고려 사항**:

1. **기존 팀 기술과 선호** (Lines 531-532):
   - 팀이 가장 잘 아는 패러다임은?
   - 기회가 주어지면 사용하고 싶은 패러다임은?

2. **기존 라이브러리, 프레임워크, 코드베이스** (Lines 533-534):
   - 사전 작성 코드 사용 시 어떤 패러다임이 적합한가?

3. **스타일 가이드와 코드 규칙** (Lines 535-537):
   - 기존 스타일 가이드나 패러다임 사용 중인가?
   - 유료 작업 또는 기존 오픈소스 프로젝트 기여 시 설정된 패러다임 채택 필요

**결론** (Lines 538-540):
- 선택한 패러다임과 관계없이 도메인 모델 작성 성공 가능
- 코드가 달라 보일 수 있지만 동등한 기능을 모든 패러다임으로 작성 가능

---

### 5. 외부 시스템을 테스트 더블로 대체하기 → [핵심 개념 6]

**출처**: Lines 545-573

#### 5.1 어댑터를 테스트 더블로 교체 (Lines 548-566)

**출처**: Lines 548-566

**주요 장점**: 모든 어댑터를 테스트 더블로 교체하여 FIRST 단위 테스트로 전체 도메인 모델 테스트 가능

**테스트 환경 불필요**:
- 테스트 데이터베이스 불필요
- HTTP 도구 (Postman, curl) 불필요
- 빠르고 반복 가능한 단위 테스트만으로 충분

**장점** (Lines 557-565):

1. **테스트 퍼스트 작성 용이** (Lines 558-559):
   - 메모리에만 존재하는 간단한 테스트 더블 작성
   - 테스트 환경에 의존성 없음

2. **FIRST 단위 테스트 장점** (Lines 560-563):
   - 매우 빠른 실행 (시간 단위가 아닌 초 단위)
   - 반복 가능
   - 불안정한 통합 테스트 실패로 인한 빌드 실패 고민 불필요

3. **팀 잠금 해제** (Lines 564-565):
   - 테스트 환경 설계 및 구축 대기 없이 유용한 작업 수행 가능
   - 시스템의 핵심 로직 구축 가능

**기술 참조** (Lines 570-571):
- Chapter 8(Test Doubles - Stubs and Mocks)에서 테스트 더블 생성 기술 개요
- 새로운 구현 필요 없음

---

### 6. 더 큰 단위 테스트하기 → [핵심 개념 6]

**출처**: Lines 574-624

#### 6.1 사용자 스토리 전체를 단위 테스트 (Lines 574-599)

**출처**: Lines 574-599

**전통적 단위 테스트 오해** (Lines 578-582):
- 단위 테스트는 작은 것만 테스트
- 하나의 함수만 테스트해야 함
- 모든 클래스에 모든 메서드에 대해 하나의 단위 테스트
- 이런 테스트는 일부 장점 놓침
- **더 나은 접근**: 구현 세부사항 대신 행동 커버

**새로운 시스템 레이어링** (Lines 583-587):
- Hexagonal Architecture 설계 + 행동 대신 구현 세부사항 테스트 → 흥미로운 시스템 레이어링
- 3계층 아키텍처의 전통적 레이어 대신 점점 높은 수준 행동의 원들
- 도메인 모델 내부: 작은 테스트
- 어댑터 레이어 방향: 더 큰 행동 단위

**포트의 높은 수준 경계** (Lines 589-599):

포트의 구성 (Lines 590-594):
- 사용자 요청의 본질
- 애플리케이션 응답의 본질
- 데이터 저장 및 접근 필요의 본질
- 모두 기술 독립적 코드 사용

**의미** (Lines 595-599):
- 이 레이어는 애플리케이션이 하는 일의 본질 (어떻게 하는지의 세부사항 제외)
- 원래 사용자 스토리 그 자체
- **중요**: FIRST 단위 테스트 작성 가능
- 어려운 외부 시스템을 간단한 테스트 더블로 교체할 수 있는 모든 것 보유
- 전체 사용자 스토리를 커버하는 단위 테스트 작성 가능, 핵심 로직 정확성 확인

#### 6.2 더 빠르고 신뢰할 수 있는 테스트 (Lines 604-622)

**출처**: Lines 604-622

**전통적 접근**:
- 사용자 스토리 테스트 = 테스트 환경의 느린 통합 테스트
- Hexagonal Architecture = 일부 통합 테스트를 단위 테스트로 교체 가능 → 빌드 속도 향상, 테스트 반복 가능성 향상

**3가지 세분성에서 테스트 주도** (Lines 608-611):
1. 단일 메서드 또는 함수
2. 클래스의 공개 행동과 협력자들
3. 전체 사용자 스토리의 핵심 로직

**주요 장점** (Lines 612-622):
- 외부 서비스로부터의 격리 → 사용자 스토리의 본질적 로직을 도메인 모델로 푸시
- 도메인 모델이 포트와 상호작용
- 포트는 설계상 테스트 더블 작성이 매우 쉬움
- **FIRST 단위 테스트 장점 재확인**:
  - 매우 빠름 → 사용자 스토리 테스트가 매우 빠름
  - 높은 반복 가능성 → 테스트 통과/실패 신뢰 가능

**통합 테스트와 단위 테스트 경계 흐림** (Lines 618-622):
- 단위 테스트로 넓은 기능 영역 커버 → 통합 테스트와 단위 테스트 경계 모호
- 더 많은 사용자 스토리 테스트 → 개발자 마찰 제거 (테스트가 쉬워짐)
- 단위 테스트 증가 → 빌드 시간 개선 (빠르고 신뢰할 수 있는 통과/실패)
- 통합 테스트 감소 → 좋음 (더 느리고 잘못된 결과 발생 가능성 높음)

---

### 7. Wordz - 데이터베이스 추상화 → [핵심 개념 3, 6]

**출처**: Lines 625-780

#### 7.1 Repository 인터페이스 설계 (Lines 629-664)

**출처**: Lines 629-664

**첫 번째 작업**: 포트가 무엇을 해야 하는지 결정

**3가지 지침 원칙** (Lines 637-646):

1. **도메인 모델이 필요로 하는 것 고려** (Lines 638):
   - 왜 이 데이터가 필요한가?
   - 무엇을 위해 사용될 것인가?

2. **가정된 데이터베이스 구현을 단순히 반영하지 말 것** (Lines 639-643):
   - 이 단계에서 테이블과 외래 키로 생각하지 말 것
   - 저장소 구현 결정 시 나중에 등장
   - 데이터베이스 성능 고려로 여기서 생성한 추상화 재검토 필요할 수 있음
   - 더 나은 데이터베이스 기능을 위해 일부 데이터베이스 구현 세부사항 누출을 트레이드오프
   - 가능한 한 늦게 결정 연기

3. **데이터베이스 엔진을 더 활용할 시기 고려** (Lines 644-646):
   - 데이터베이스 엔진에서 복잡한 저장 프로시저 사용 의도 가능
   - Repository 인터페이스에서 행동 분할 반영
   - Repository 인터페이스에서 더 높은 수준의 추상화 제안 가능

**단어 가져오기 작업 예제** (Lines 647-664):

**2가지 옵션**:
1. 데이터베이스가 무작위로 단어 선택
2. 도메인 모델이 무작위 숫자 생성, 데이터베이스가 번호가 매겨진 단어 제공

**옵션 1 분석** (Lines 651-655):
- 데이터베이스가 더 많은 작업 수행 → 더 빠른 데이터 처리
- 데이터베이스 코드가 데이터에 더 가까움
- 네트워크 연결을 통해 도메인 모델로 데이터 끌어오지 않음
- 문제: 데이터베이스가 무작위로 선택하도록 설득하는 방법?
  - 관계형 데이터베이스: 보장되지 않은 순서로 결과 반환하는 쿼리 → "일종의" 무작위
  - 충분히 무작위한가? 모든 가능한 구현에서? 가능성 낮음

**옵션 2 선택** (Lines 656-664):
- 도메인 모델 코드가 어떤 단어를 선택할지 결정 (무작위 숫자 생성)
- 해당 숫자와 연결된 단어를 가져오는 쿼리 발행
- 각 단어에 관련 숫자 필요 → 나중에 데이터베이스 스키마 설계 시 제공

**추가 설계 결정** (Lines 660-664):
- 도메인 모델이 모든 단어와 연결된 전체 숫자 집합에서 무작위 숫자 선택
- 도메인 모델이 선택할 전체 숫자 집합 알아야 함
- 단어 식별 숫자: 1부터 시작, 각 단어마다 1씩 증가
- 포트에 이 숫자들의 상한선 반환하는 메서드 제공

#### 7.2 테스트 작성 (Lines 665-732)

**출처**: Lines 665-732

**테스트 클래스 시작** (Lines 665-681):

```java
package com.wordz.domain;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import static org.assertj.core.api.Assertions.*;
import static org.mockito.Mockito.when;

// Mockito 통합 활성화
@ExtendWith(MockitoExtension.class)
public class WordSelectionTest {
```

```python
# Python 버전
import pytest
from unittest.mock import Mock
from wordz.domain import WordSelection, WordRepository, RandomNumbers

class TestWordSelection:
    """단어 선택 테스트"""
```

**테스트 상수와 필드** (Lines 683-692):

```java
    private static final int HIGHEST_WORD_NUMBER = 3;  // 가장 높은 단어 번호
    private static final int WORD_NUMBER_SHINE = 2;    // "SHINE" 단어의 번호

    @Mock
    private WordRepository repository;  // 단어 저장소 스텁

    @Mock
    private RandomNumbers random;  // 무작위 숫자 생성기 스텁
```

```python
# Python 버전 (pytest fixture 사용)
    @pytest.fixture
    def repository(self):
        """단어 저장소 Mock"""
        return Mock(spec=WordRepository)

    @pytest.fixture
    def random(self):
        """무작위 숫자 생성기 Mock"""
        return Mock(spec=RandomNumbers)
```

**테스트 메서드** (Lines 696-714):

```java
    @Test
    void selectsWordAtRandom() {
        // 저장소 스텁 설정: 가장 높은 단어 번호 반환
        when(repository.highestWordNumber())
            .thenReturn(HIGHEST_WORD_NUMBER);

        // 저장소 스텁 설정: 번호 2로 "SHINE" 반환
        when(repository.fetchWordByNumber(WORD_NUMBER_SHINE))
            .thenReturn("SHINE");

        // 무작위 생성기 스텁 설정: 번호 2 반환
        when(random.next(HIGHEST_WORD_NUMBER))
            .thenReturn(WORD_NUMBER_SHINE);

        // 단어 선택기 생성
        var selector = new WordSelection(repository, random);

        // 무작위 단어 선택 실행
        String actual = selector.chooseRandomWord();

        // 검증: "SHINE" 반환
        assertThat(actual).isEqualTo("SHINE");
    }
}
```

```python
# Python 버전
    def test_selects_word_at_random(self, repository, random):
        """무작위로 단어 선택 테스트"""
        HIGHEST_WORD_NUMBER = 3
        WORD_NUMBER_SHINE = 2

        # 저장소 스텁 설정
        repository.highest_word_number.return_value = HIGHEST_WORD_NUMBER
        repository.fetch_word_by_number.return_value = "SHINE"

        # 무작위 생성기 스텁 설정
        random.next.return_value = WORD_NUMBER_SHINE

        # 단어 선택기 생성 및 실행
        selector = WordSelection(repository, random)
        actual = selector.choose_random_word()

        # 검증
        assert actual == "SHINE"
```

**설계 결정 캡처** (Lines 716-731):

1. `WordSelection` 클래스가 단어 선택 알고리즘 캡슐화
2. `WordSelection` 생성자가 2가지 의존성 받음:
   - `WordRepository`: 저장된 단어용 포트
   - `RandomNumbers`: 무작위 숫자 생성용 포트
3. `chooseRandomWord()` 메서드가 무작위 선택 단어를 `String`으로 반환
4. Arrange 섹션을 `beforeEachTest()` 메서드로 이동:

```java
@BeforeEach
void beforeEachTest() {
    when(repository.highestWordNumber())
                  .thenReturn(HIGHEST_WORD_NUMBER);
    when(repository.fetchWordByNumber(WORD_NUMBER_SHINE))
                  .thenReturn("SHINE");
}
```

```python
# Python 버전
    @pytest.fixture(autouse=True)
    def setup(self, repository):
        """각 테스트 전 실행 (자동)"""
        repository.highest_word_number.return_value = 3
        repository.fetch_word_by_number.return_value = "SHINE"
```

#### 7.3 포트 인터페이스 정의 (Lines 736-751)

**출처**: Lines 736-751

**WordRepository 인터페이스** (Lines 737-741):

```java
package com.wordz.domain;

public interface WordRepository {
    String fetchWordByNumber(int number);  // 번호로 단어 가져오기
    int highestWordNumber();               // 가장 높은 단어 번호
}
```

```python
# Python 버전
from typing import Protocol

class WordRepository(Protocol):
    """단어 저장소 포트"""

    def fetch_word_by_number(self, number: int) -> str:
        """번호로 단어 가져오기"""
        ...

    def highest_word_number(self) -> int:
        """가장 높은 단어 번호 반환"""
        ...
```

**설명** (Lines 742-745):
- 애플리케이션의 데이터베이스 관점 정의
- 현재 필요를 위한 2가지 기능:
  - `fetchWordByNumber()`: 식별 번호로 단어 가져오기
  - `highestWordNumber()`: 가장 높은 단어 번호 반환

**RandomNumbers 인터페이스** (Lines 746-751):

```java
package com.wordz.domain;

public interface RandomNumbers {
    int next(int upperBoundInclusive);  // 상한선 포함 범위의 무작위 숫자
}
```

```python
# Python 버전
class RandomNumbers(Protocol):
    """무작위 숫자 생성기 포트"""

    def next(self, upper_bound_inclusive: int) -> int:
        """1부터 상한선(포함)까지의 무작위 숫자 반환"""
        ...
```

**설명** (Lines 751):
- `next()` 메서드: 1부터 `upperBoundInclusive` 숫자까지 범위의 `int` 반환

#### 7.4 도메인 모델 코드 작성 (Lines 752-774)

**출처**: Lines 752-774

**WordSelection 클래스** (Lines 753-771):

```java
package com.wordz.domain;

public class WordSelection {
    private final WordRepository repository;  // 단어 저장소
    private final RandomNumbers random;       // 무작위 숫자 생성기

    public WordSelection(WordRepository repository,
                         RandomNumbers random) {
        this.repository = repository;
        this.random = random;
    }

    public String chooseRandomWord() {
        // 무작위 단어 번호 생성
        int wordNumber = random.next(repository.highestWordNumber());
        // 해당 번호의 단어 반환
        return repository.fetchWordByNumber(wordNumber);
    }
}
```

```python
# Python 버전
class WordSelection:
    """무작위 단어 선택 로직"""

    def __init__(self, repository: WordRepository, random: RandomNumbers):
        """의존성 주입"""
        self.repository = repository
        self.random = random

    def choose_random_word(self) -> str:
        """무작위 단어 선택"""
        # 무작위 단어 번호 생성
        word_number = self.random.next(self.repository.highest_word_number())
        # 해당 번호의 단어 반환
        return self.repository.fetch_word_by_number(word_number)
```

**핵심 특징** (Lines 772-774):
- `com.wordz.domain` 패키지 외부에서 아무것도 import하지 않음
- 순수 애플리케이션 로직
- 저장된 단어와 무작위 숫자 접근을 위해 포트 인터페이스에만 의존
- `WordSelection`의 도메인 모델 프로덕션 코드 완성

#### 7.5 어댑터 설계 (Lines 775-780)

**출처**: Lines 775-780

**다음 작업**:
1. `RandomNumbers` 포트 구현
2. `WordRepository` 인터페이스를 구현하는 데이터베이스 접근 코드

**개요**:
- 데이터베이스 제품 선택
- 데이터베이스 연결 및 쿼리 실행 방법 연구
- 통합 테스트로 해당 코드 테스트 주도

**연기**: Part 3에서 수행
- Chapter 13: Driving the Domain Layer
- Chapter 14: Driving the Database Layer

---

## 요약 및 다음 단계

**출처**: Lines 781-792

### 이 장에서 배운 내용

1. **SOLID 원칙 적용**: 외부 시스템 완전 분리 → Hexagonal Architecture
2. **테스트 더블 사용**: 외부 시스템 대신 사용 → 테스트 단순화, 반복 가능한 결과
3. **전체 사용자 스토리 테스트**: FIRST 단위 테스트로 가능
4. **보너스**: 외부 시스템의 미래 변경으로부터 격리 → 새 기술 지원을 위한 재작업량 제한
5. **다중 외부 시스템 지원**: Hexagonal Architecture + Dependency Injection → 런타임 구성으로 선택

### 다음 장 예고 (Chapter 10)

- Hexagonal Architecture 애플리케이션의 다른 섹션에 적용되는 다양한 자동화 테스트 스타일
- **Test Pyramid**로 요약되는 접근

---

## Q&A

**출처**: Lines 797-822

### Q1: Hexagonal Architecture를 나중에 추가할 수 있나?

**출처**: Lines 800-804

**답변**: 항상은 아님. 리팩토링 가능하지만 도전적일 수 있음
- **문제**: 외부 시스템 세부사항에 직접 의존하는 코드가 너무 많으면 리팩토링이 어려움
- **결과**: 많은 재작업 필요
- **시사점**: 작업 시작 전에 어느 정도의 사전 설계 및 아키텍처 논의 필요

### Q2: Hexagonal Architecture는 OOP에 특정한가?

**출처**: Lines 806-808

**답변**: 아니오
- 코드에서 의존성을 조직하는 방법
- OOP, FP, 절차적 프로그래밍 또는 기타 모든 것에 적용 가능
- 의존성이 올바르게 관리되기만 하면 됨

### Q3: Hexagonal Architecture를 사용하지 말아야 할 때는?

**출처**: Lines 810-814

**답변**: 도메인 모델에 실제 로직이 없을 때
- **예**: 데이터베이스 테이블을 프론트엔드하는 매우 작은 CRUD 마이크로서비스
- 격리할 로직 없음 → 이 모든 코드를 넣어도 이점 없음
- 통합 테스트만으로 TDD 수행, FIRST 단위 테스트 사용 불가 수용

### Q4: 외부 시스템에 대해 하나의 포트만 가질 수 있나?

**출처**: Lines 816-822

**답변**: 아니오. 더 많은 포트가 더 나은 경우가 많음

**예**: 단일 Postgres 데이터베이스 (사용자, 판매, 제품 재고 데이터)
- **나쁜 접근**: 3가지 데이터셋 작업 메서드를 가진 단일 Repository 인터페이스
- **더 나은 접근**: ISP 준수하여 인터페이스 분할
  - `UserRepository`
  - `SalesRepository`
  - `InventoryRepository`

**포트의 역할**:
- 도메인 모델이 외부 시스템으로부터 원하는 것의 관점 제공
- 포트는 하드웨어에 일대일 매핑이 아님

---

## 추가 읽기 자료

**출처**: Lines 823-833

1. **Hexagonal Architecture, Alastair Cockburn**: https://alistair.cockburn.us/hexagonal-architecture/
   - Ports and Adapters로서의 Hexagonal Architecture 원래 설명

2. **FIRST 단위 테스트**: https://medium.com/pragmatic-programmers/unit-tests-are-first-fast-isolated-repeatable-self-verifying-and-timely-a83e8070698e
   - FIRST 용어의 원래 발명자 Tim Ottinger와 Brett Schuchert 크레딧

3. **프로덕션 테스팅**: https://launchdarkly.com/blog/testing-in-production-for-safety-and-sanity/
   - 의도하지 않은 결과를 실수로 트리거하지 않고 프로덕션 시스템에 배포된 코드 테스트 가이드

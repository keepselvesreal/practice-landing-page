# 걸어다니는 뼈대 (The Walking Skeleton)

## 압축 내용
초기 개발 환경 구축과 첫 end-to-end 테스트 작성을 통해 시스템 전체 구조를 검증하고, 실제 배포 가능한 최소한의 기능을 갖춘 "걸어다니는 뼈대"를 만드는 과정은 예상보다 많은 노력이 필요하지만 프로젝트의 기술적·조직적 의문사항을 조기에 해결하고 이후 변경을 자신감 있게 수행할 수 있는 토대를 마련한다.

## 핵심 내용

### 핵심 개념

1. **걸어다니는 뼈대 (Walking Skeleton)**: 시스템의 모든 주요 컴포넌트를 연결하고 배포 가능한 최소한의 기능을 갖춘 초기 구현체 → [상세: 걸어다니는 뼈대의 목적]

2. **반복 0 (Iteration Zero)**: 실제 기능 개발(반복 1)을 시작하기 전 개발 환경 구축과 초기 아키텍처를 검증하는 초기 단계 → [상세: 반복 0의 역할]

3. **희망적 사고에 의한 프로그래밍 (Programming by Wishful Thinking)**: 구현이 이미 존재한다고 가정하고 테스트를 먼저 작성한 후 필요한 인프라를 채워나가는 방식 → [상세: 첫 테스트 작성 방법]

4. **End-to-End 테스트**: UI부터 외부 서비스 통신까지 시스템 전체를 아우르는 테스트로, 비동기 환경에서 폴링(polling) 기법을 활용 → [상세: End-to-End 테스트의 특성]

5. **가짜 서비스 (Fake Service/Stub)**: 외부 의존성(경매 서버)을 실제 서비스 대신 테스트에서 제어 가능한 가짜 구현체로 대체 → [상세: 테스트 인프라 구성]

6. **도메인 언어 (Domain Language)**: 테스트 코드를 기술적 세부사항이 아닌 도메인(경매, 스나이퍼) 관점의 언어로 작성 → [상세: 테스트 코드 작성 원칙]

### 핵심 개념 간 관계

- **걸어다니는 뼈대**는 **반복 0**에서 구현되며, **End-to-End 테스트**를 통해 검증된다
- **희망적 사고에 의한 프로그래밍**은 **도메인 언어**로 작성된 테스트를 먼저 만들고, 이를 지원할 인프라(가짜 서비스)를 구축하는 방식이다
- **End-to-End 테스트**는 실제 서비스 대신 **가짜 서비스**를 사용하여 전체 시스템을 검증하며, 이는 초기 개발 단계에서 외부 의존성의 불확실성을 관리하는 전략이다

## 상세 내용

### 화제 목차
1. 걸어다니는 뼈대의 목적
2. 반복 0의 역할
3. 첫 테스트 작성 방법
4. 테스트 코드 작성 원칙
5. 테스트 인프라 구성
6. End-to-End 테스트의 특성
7. 실전 시작 전 고려사항

---

### 1. 걸어다니는 뼈대의 목적
**참조**: content.md 13-25행
**관계**: 이 섹션은 전체 장의 기초가 되며, 다음 섹션인 "반복 0의 역할"에서 구체적인 구현 시점을 다룬다.

걸어다니는 뼈대는 요구사항을 충분히 이해하여 시스템의 넓은 범위 구조를 제안하고 검증하는 데 도움을 준다. 나중에 더 많이 배우면 언제든지 마음을 바꿀 수 있지만, 솔루션의 지형을 매핑하는 것으로 시작하는 것이 중요하다.

**핵심 개념 참조**: [걸어다니는 뼈대]

**주요 특징**:
- 선택한 접근 방식을 평가하고 결정을 테스트할 수 있게 함
- 나중에 자신감 있게 변경할 수 있는 기반 마련
- 예상보다 많은 노력 필요:
  - 애플리케이션과 그 위치에 대한 모든 종류의 질문 해결
  - 프로덕션과 유사한 환경으로의 빌드, 패키징, 배포 자동화
  - 기술적·조직적 질문들 해결

---

### 2. 반복 0의 역할
**참조**: content.md 26-35행
**이전 화제와의 관계**: "걸어다니는 뼈대의 목적"에서 제시한 개념을 실제로 구현하는 시점과 방법을 설명한다.

반복 0(Iteration Zero)는 대부분의 애자일 프로젝트에서 팀이 초기 분석을 수행하고, 물리적·기술적 환경을 설정하며, 프로젝트를 시작하는 첫 단계다.

**핵심 개념 참조**: [반복 0]

**특징**:
- 거의 모든 작업이 인프라이므로 가시적인 기능을 많이 추가하지 않음
- 일정 관리를 위해 기존 반복으로 계산하지 않을 수 있음
- "반복(iteration)": 팀이 여전히 활동을 시간 제한해야 하기 때문
- "0": 반복 1에서 기능 개발이 시작되기 전이기 때문
- **중요 작업**: 걸어다니는 뼈대를 사용하여 초기 아키텍처를 테스트 주도로 개발

**테스트 우선 원칙**:
```python
# 반복 0에서도 테스트로 시작한다
# "Of course, we start our walking skeleton by writing a test."
# (content.md 35행)
```

---

### 3. 첫 테스트 작성 방법
**참조**: content.md 39-100행
**이전 화제와의 관계**: "반복 0의 역할"에서 테스트로 시작한다는 원칙을 구체적인 테스트 코드로 구현한다.

**핵심 개념 참조**: [희망적 사고에 의한 프로그래밍], [End-to-End 테스트], [도메인 언어]

#### 최소 기능 정의
경매 스나이퍼 시스템의 모든 컴포넌트(UI, 스나이핑 컴포넌트, 경매 서버 통신)를 커버하는 가장 얇은 슬라이스:
- 경매 스나이퍼가 경매에 참여(join)하고 종료를 기다림
- 입찰 전송은 고려하지 않음
- 클라이언트 GUI와 외부 경매 서버에서 이벤트를 주입하여 시스템을 외부에서 테스트

#### 희망적 사고에 의한 프로그래밍
```python
# 구현이 이미 존재한다고 가정하고 테스트를 먼저 작성
# "programming by wishful thinking" (Abelson and Sussman)
# (content.md 49-59행)

# 1. 시스템이 무엇을 해야 하는지에 집중
# 2. 어떻게 작동하게 할지의 복잡성에 빠지지 않음
# 3. 테스트를 기존 인프라에 맞추는 대신, 원하는 테스트 방식을 지원하는 인프라 구축
```

#### 테스트 개요
```python
# 원본 코드 (content.md 61-71행)
"""
1. When an auction is selling an item,
2. And an Auction Sniper has started to bid in that auction,
3. Then the auction will receive a Join request from the Auction Sniper.
4. When an auction announces that it is Closed,
5. Then the Auction Sniper will show that it lost the auction.
"""

# 이것은 상태 머신의 한 전환을 설명한다 (Figure 10.1 참조)
# 경매 참여 → 경매 종료 → 스나이퍼가 낙찰 실패 표시
```

#### 실제 테스트 코드
```java
// 원본 Java 코드 (content.md 101-118행)
public class AuctionSniperEndToEndTest {
  private final FakeAuctionServer auction = new FakeAuctionServer("item-54321");
  private final ApplicationRunner application = new ApplicationRunner();

  @Test public void sniperJoinsAuctionUntilAuctionCloses() throws Exception {
    auction.startSellingItem();                 // Step 1: 경매 시작
    application.startBiddingIn(auction);        // Step 2: 스나이퍼 입찰 시작
    auction.hasReceivedJoinRequestFromSniper(); // Step 3: 참여 요청 확인
    auction.announceClosed();                   // Step 4: 경매 종료 알림
    application.showsSniperHasLostAuction();    // Step 5: 낙찰 실패 표시 확인
  }

  // Additional cleanup
  @After public void stopAuction() {
    auction.stop();
  }

  @After public void stopApplication() {
    application.stop();
  }
}
```

```python
# Python 버전
import unittest

class AuctionSniperEndToEndTest(unittest.TestCase):
    """경매 스나이퍼 End-to-End 테스트

    경매 참여부터 종료까지의 전체 시나리오를 테스트한다.
    """

    def setUp(self):
        """테스트 환경 설정"""
        self.auction = FakeAuctionServer("item-54321")
        self.application = ApplicationRunner()

    def test_sniper_joins_auction_until_auction_closes(self):
        """스나이퍼가 경매에 참여하고 종료될 때까지 대기하는 시나리오"""
        # Step 1: 경매 시작
        self.auction.start_selling_item()

        # Step 2: 스나이퍼가 경매에서 입찰 시작
        self.application.start_bidding_in(self.auction)

        # Step 3: 경매가 스나이퍼로부터 참여 요청을 받았는지 확인
        self.auction.has_received_join_request_from_sniper()

        # Step 4: 경매 종료 알림
        self.auction.announce_closed()

        # Step 5: 애플리케이션이 스나이퍼가 낙찰 실패했음을 표시하는지 확인
        self.application.shows_sniper_has_lost_auction()

    def tearDown(self):
        """테스트 환경 정리"""
        self.auction.stop()
        self.application.stop()
```

#### 설계 가정
FakeAuctionServer는 주어진 아이템에 연결된다는 가정:
- Southabee's On-Line이 여러 경매를 호스팅하며, 각각 단일 아이템 판매
- 의도된 아키텍처 구조와 일치

---

### 4. 테스트 코드 작성 원칙
**참조**: content.md 123-139행
**이전 화제와의 관계**: "첫 테스트 작성 방법"에서 작성한 코드의 명명 규칙과 언어적 일관성을 설명한다.

**핵심 개념 참조**: [도메인 언어]

#### 명명 규칙
```python
# Helper 객체의 메서드 명명 규칙 (content.md 123-129행)

# 1. 이벤트를 트리거하는 메서드: 명령형 (imperative mood)
def start_bidding_in(auction):
    """입찰을 시작한다 - 동작을 유발"""
    pass

# 2. 어떤 일이 발생했는지 검증하는 메서드: 서술형 (indicative mood)
def shows_sniper_has_lost_auction():
    """
    스나이퍼가 낙찰에 실패했음을 표시하는지 확인
    애플리케이션이 경매 상태를 "lost"로 표시하지 않으면 예외 발생
    """
    pass

# 정리 메서드
# JUnit의 @After가 테스트 실행 후 호출하여 런타임 환경 정리
def stop():
    """테스트 후 환경 정리"""
    pass
```

#### 도메인 언어의 중요성
```python
# 테스트 언어는 경매(auctions)와 스나이퍼(Snipers)에 관한 것
# 메시징 레이어나 UI 컴포넌트에 대한 내용은 없음
# (content.md 135-139행)

# 장점:
# 1. 테스트에서 중요한 것이 무엇인지 이해하는 데 도움
# 2. 구현이 불가피하게 변경될 때 보호
# 3. 부수 효과: 코드 유지보수성 향상
```

---

### 5. 테스트 인프라 구성
**참조**: content.md 140-168행
**이전 화제와의 관계**: "테스트 코드 작성 원칙"에 따라 작성된 테스트를 실행하기 위한 기술적 인프라를 선택하고 구성한다.

**핵심 개념 참조**: [가짜 서비스]

#### 필요한 컴포넌트
```python
# 테스트를 통과시키기 위해 필요한 4가지 컴포넌트 (content.md 142-149행)
"""
1. XMPP 메시지 브로커
2. XMPP를 통해 통신할 수 있는 stub 경매
3. GUI 테스팅 프레임워크
4. 멀티스레드, 비동기 아키텍처를 다룰 수 있는 테스트 하네스
"""

# 추가로 필요한 작업:
# - 버전 관리 시스템 설정
# - 자동화된 빌드/배포/테스트 프로세스 구축
```

#### 선택한 기술 스택
```python
# 패키지 선택 (content.md 150-162행)

# 1. XMPP 메시지 브로커: Openfire (오픈소스)
# 2. 클라이언트 라이브러리: Smack
# 3. GUI 테스트 프레임워크: WindowLicker (오픈소스)
#    - Swing과 Smack 모두 멀티스레드이고 이벤트 주도형
#    - WindowLicker가 Swing의 멀티스레드, 이벤트 주도 아키텍처를 다루는 방식이
#      XMPP 메시징에도 잘 작동함
#    - 테스트에 필요한 비동기 접근 방식 지원

class FakeAuctionServer:
    """
    가짜 경매 서버 (Stub)

    - XMPP 메시지 브로커에 연결
    - 스나이퍼로부터 명령을 받아 테스트가 검증
    - 테스트가 이벤트를 다시 보낼 수 있도록 허용
    - Southabee's On-Line 전체를 재구현하는 것이 아니라
      테스트 시나리오를 지원하기에 충분한 정도만 구현
    """
    pass
```

#### 인프라 구조
```
# Figure 10.2: End-to-end 테스트 장비 (content.md 166-168행)

┌─────────────────────────────────────────┐
│    AuctionSniperEndToEndTest (JUnit)   │
│  ┌─────────────────┐ ┌───────────────┐ │
│  │ ApplicationRunner│ │FakeAuctionServ│ │
│  └────────┬────────┘ └───────┬───────┘ │
└───────────┼──────────────────┼─────────┘
            │                  │
            │ WindowLicker     │ Smack
            │ (GUI Testing)    │ (XMPP Client)
            ↓                  ↓
    ┌──────────────┐    ┌─────────────┐
    │ Auction      │←──→│  Openfire   │
    │ Sniper App   │    │ (XMPP Broker)│
    │ (Swing UI)   │    │             │
    └──────────────┘    └─────────────┘
```

---

### 6. End-to-End 테스트의 특성
**참조**: content.md 169-194행
**이전 화제와의 관계**: "테스트 인프라 구성"에서 선택한 비동기 기술들(Swing, XMPP)을 다루는 테스트 전략을 설명한다.

**핵심 개념 참조**: [End-to-End 테스트]

#### 비동기성 처리
```python
# End-to-End 테스트는 비동기성을 다뤄야 함 (content.md 170-184행)

class AsyncEndToEndTest:
    """
    비동기 이벤트 기반 시스템의 End-to-End 테스트

    단위 테스트와의 차이:
    - 단위 테스트: 같은 스레드에서 객체를 직접 구동, 상태와 동작을 직접 검증
    - E2E 테스트: 애플리케이션과 병렬로 실행, 언제 준비되는지 정확히 알 수 없음
    """

    def wait_for_ui_change(self, timeout_seconds=5):
        """
        폴링(polling) 기법으로 가시적인 효과 감지

        - 대상 애플리케이션 내부를 들여다볼 수 없음
        - UI 변경이나 로그 항목 같은 가시적인 효과를 감지해야 함
        - 효과를 폴링하고 주어진 시간 제한 내에 발생하지 않으면 실패

        추가 복잡성:
        - 대상 애플리케이션이 트리거 이벤트 후 충분히 안정화되어야 함
        - 테스트가 결과를 포착할 수 있을 만큼 충분히 오래 유지되어야 함
        - 화면에 잠깐만 나타나는 값을 기다리는 테스트는 자동 빌드에 너무 불안정
        """
        pass

    def step_through_scenario(self):
        """
        일반적인 기법: 애플리케이션을 제어하고 시나리오를 단계별로 진행

        각 단계에서:
        1. 테스트가 검증(assertion)이 통과할 때까지 대기
        2. 다음 단계를 위해 애플리케이션을 깨우는 이벤트 전송
        """
        pass
```

#### WindowLicker의 역할
```python
# WindowLicker와 비동기성 (content.md 189-191행)
"""
Swing과 메시징 인프라 모두 비동기적
WindowLicker(값을 폴링)를 사용하여 스나이퍼를 구동하면
End-to-End 테스팅의 자연스러운 비동기성을 커버함
"""

class WindowLickerDriver:
    """
    WindowLicker를 사용한 비동기 테스트

    장점:
    - Swing의 이벤트 디스패치 스레드 자동 처리
    - 폴링 메커니즘 내장
    - XMPP 메시징의 비동기성도 함께 처리
    """

    def poll_for_value(self, getter, expected, timeout_ms=5000):
        """값이 나타날 때까지 폴링"""
        pass
```

#### End-to-End 테스트의 특징
```python
# 느리고 취약한 특성 (content.md 185-188행)
"""
End-to-End 테스팅의 한계:

1. 속도: 단위 테스트보다 느림
2. 취약성: 타이밍 관련 문제 (예: 네트워크가 오늘 바쁠 수 있음)
3. 실패 해석 필요: 타이밍 관련 테스트가 연속으로 여러 번 실패해야 보고되는 팀도 있음
4. 단위 테스트와의 차이: 단위 테스트는 매번 모두 통과해야 함

주의사항:
- 실패가 해석이 필요할 수 있음
- 환경적 요인을 고려해야 함
- 재현 가능성 확보가 중요
"""
```

---

### 7. 실전 시작 전 고려사항
**참조**: content.md 196-211행
**이전 화제와의 관계**: "End-to-End 테스트의 특성"에서 다룬 테스트의 한계를 인정하고, 실전에서의 위험 관리 전략을 제시한다.

**핵심 개념 참조**: [가짜 서비스], [걸어다니는 뼈대]

#### 테스트 범위의 한계 인식
```python
# 진짜 End-to-End가 아님 (content.md 197-203행)
"""
첫 번째 테스트는 실제로는 완전한 end-to-end가 아니다:
- 실제 경매 서비스를 포함하지 않음 (쉽게 사용할 수 없기 때문)
- Southabee's On-Line 문서를 기반으로 한 가짜 경매 서비스 사용

TDD 기술의 중요한 부분:
1. 무엇을 테스트할지 경계를 설정하는 판단
2. 결국 모든 것을 어떻게 커버할지 계획
"""

class RiskManagement:
    """위험 관리 전략"""

    def identify_known_risks(self):
        """
        알려진 위험을 프로젝트 계획에 기록

        위험:
        - Southabee's On-Line 문서가 정확하지 않을 수 있음
        - 가짜 서비스와 실제 서비스 간 불일치 가능성
        """
        pass

    def schedule_real_service_testing(self):
        """
        실제 서버 테스트 일정 수립

        시점:
        - 의미 있는 거래를 완료할 수 있을 만큼 충분한 기능 구현 후
        - 실제 경매에서 (못생겼지만 저렴한) 촛대 한 쌍을 구매하게 되더라도

        이유:
        - 불일치를 빨리 발견할수록 더 적은 코드가 오해를 기반으로 함
        - 수정할 시간이 더 많음
        """
        pass
```

#### 실전 검증 전략
```python
# 조기 검증의 중요성 (content.md 206-207행)
"""
The sooner we find a discrepancy, the less code we will have
based on that misunderstanding and the more time to fix it.

불일치를 더 빨리 발견할수록:
- 오해를 기반으로 한 코드가 더 적음
- 수정할 시간이 더 많음

행동 원칙:
"We'd better get on with it." (208행)
- 지체하지 말고 시작하라
- 문제를 조기에 발견하고 해결하라
"""
```

#### 걸어다니는 뼈대의 가치 재확인
```python
# 전체 흐름 요약
"""
1. 걸어다니는 뼈대 구축 시작
   └─> 테스트로 시작 (반복 0)

2. 희망적 사고로 테스트 작성
   └─> 도메인 언어 사용
       └─> 구현 세부사항 숨김

3. 인프라 선택 및 구축
   └─> XMPP (Openfire, Smack)
   └─> GUI 테스팅 (WindowLicker)
   └─> 가짜 서비스 (FakeAuctionServer)

4. End-to-End 테스트 실행
   └─> 비동기성 처리 (폴링)
   └─> 전체 시스템 검증

5. 위험 관리
   └─> 알려진 한계 인식
   └─> 실제 서비스 테스트 계획

결과:
- 변경에 자신감을 갖고 대응할 수 있는 토대
- 기술적·조직적 의문사항 조기 해결
- 이후 기능 개발을 위한 견고한 기반
"""
```

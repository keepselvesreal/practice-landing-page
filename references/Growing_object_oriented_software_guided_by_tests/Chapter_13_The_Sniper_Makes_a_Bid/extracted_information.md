# Chapter 13: 스나이퍼가 입찰하다 (The Sniper Makes a Bid)

## 압축 내용

단일 책임 원칙(SRP)에 따라 Main 클래스에서 AuctionSniper 클래스를 추출하고, Auction 및 SniperListener 인터페이스를 도입하여 도메인을 분리하며, XMPPAuction과 SniperStateDisplayer로 각 책임을 분산시켜 테스트 가능하고 유지보수 가능한 구조로 설계를 진화시키는 과정.

## 핵심 내용

### 핵심 개념

1. **단일 책임 원칙(Single Responsibility Principle)** (→ 상세 내용 1.1)
   - Main 클래스의 복잡도를 인식하고 새로운 개념 추출
   - 각 클래스는 하나의 책임만 가져야 함
   - 타입 생성에 두려워하지 말아야 함

2. **AuctionSniper 클래스 추출** (→ 상세 내용 1.2)
   - 경매 입찰 정책과 상태 알림에 집중하는 핵심 도메인 객체
   - AuctionEventListener 구현으로 이벤트 처리
   - Main에서 분리되어 단위 테스트 가능

3. **의존성 분리와 인터페이스 도입** (→ 상세 내용 2.1, 2.2)
   - **SniperListener**: 알림(notification) 관계 - Sniper 상태 변경 추적
   - **Auction**: 의존성(dependency) 관계 - 금융 거래 도메인
   - 두 인터페이스는 서로 다른 도메인을 나타냄

4. **Null Implementation 패턴** (→ 상세 내용 2.3)
   - 임시 빈 구현을 통해 점진적 개발 가능
   - Null Object와는 의도가 다름 (임시성 vs 영구성)
   - 컴파일 유지하며 다음 단계로 진행

5. **XMPPAuction 추출** (→ 상세 내용 3.1)
   - 경매 명령 전송 책임을 캡슐화
   - 메시징 인프라 기반 Auction 구현
   - 도메인 의도를 명확히 표현 (auction.join())

6. **SniperStateDisplayer 추출** (→ 상세 내용 3.2)
   - Sniper 이벤트를 Swing UI 표현으로 변환
   - Swing 스레딩 처리 포함
   - Main의 책임 분리

7. **Value Type 패턴** (→ 상세 내용 3.3)
   - AuctionEvent 내부 클래스로 메시지 파싱 캡슐화
   - 불변(immutable) 값 객체
   - 도메인 개념 추출로 중복 제거

8. **점진적 설계(Emergent Design)** (→ 상세 내용 4.1)
   - 기능 추가와 리팩토링 반복
   - 작은 증분 단위로 진행
   - 코드가 말하는 것을 따름

### 핵심 개념 간 관계

```
단일 책임 원칙
    ↓ 적용
AuctionSniper 추출 → 의존성 분리 필요
    ↓                      ↓
    ↓              SniperListener (알림)
    ↓              Auction (의존성)
    ↓                      ↓
Null Implementation ← 점진적 구현
    ↓
XMPPAuction 추출 → 도메인 의도 명확화
    ↓
SniperStateDisplayer 추출 → UI 책임 분리
    ↓
AuctionEvent (Value Type) → 파싱 캡슐화
    ↓
점진적 설계 → 테스트 가능한 구조
```

**설계 진화 흐름**:
1. Main의 복잡도 인식 → SRP 적용 동기
2. AuctionSniper 추출 → 새로운 의존성 필요
3. Auction/SniperListener 도입 → 도메인 분리
4. Null Implementation → 점진적 개발
5. XMPPAuction 추출 → 메시징 캡슐화
6. SniperStateDisplayer 추출 → UI 분리
7. AuctionEvent 추출 → 파싱 로직 캡슐화
8. Main은 조립자(Assembler) 역할만 수행

## 상세 내용

### 화제 목차

1. AuctionSniper 도입 (Introducing AuctionSniper)
   1.1. 새 클래스와 의존성 (A New Class, with Dependencies)
   1.2. 집중, 집중, 집중 (Focus, Focus, Focus)

2. 입찰 보내기 (Sending a Bid)
   2.1. Auction 인터페이스 (An Auction Interface)
   2.2. AuctionSniper가 입찰하다 (The AuctionSniper Bids)
   2.3. AuctionSniper로 성공적인 입찰 (Successfully Bidding with the AuctionSniper)

3. 구현 정리 (Tidying Up the Implementation)
   3.1. XMPPAuction 추출 (Extracting XMPPAuction)
   3.2. 사용자 인터페이스 추출 (Extracting the User Interface)
   3.3. Translator 정리 (Tidying Up the Translator)

4. 설계 원칙
   4.1. 점진적 설계 (Emergent Design)
   4.2. 결정 연기 (Defer Decisions)
   4.3. 코드 컴파일 유지 (Keep the Code Compiling)

---

### 1. AuctionSniper 도입 (Introducing AuctionSniper)

**이전 화제와의 관계**: 없음 (챕터 시작)

#### 1.1. 새 클래스와 의존성 (A New Class, with Dependencies)

**참조**: 페이지 148-150, 줄 10-103

**설명**:

Main 클래스가 이미 너무 많은 일을 하고 있어 복잡해짐. Price 이벤트를 받으면 더 높은 입찰을 보내고 UI 상태를 업데이트해야 하는데, Main을 확장하기보다 **AuctionSniper**라는 새 클래스를 도입.

**핵심 개념**: [단일 책임 원칙 ✓], [AuctionSniper 클래스 추출 ✓]

**설계 결정**:
1. AuctionSniper가 AuctionEventListener 구현
2. UI 구현 세부사항(Swing 스레드)을 AuctionSniper가 알아야 하는가? → **아니오**
3. **SniperListener** 인터페이스 도입으로 책임 분리

**의존성 관계**:
- SniperListener = 알림(notification): Sniper 상태 변경 추적
- Auction = 의존성(dependency): Sniper는 Auction 없이 동작 불가

**코드 예시**:

```java
// SniperListener 인터페이스 정의
// 참조: 페이지 149, 줄 42-44
public interface SniperListener extends EventListener {
    void sniperLost();
}
```

```python
# 파이썬 버전
from abc import ABC, abstractmethod
from typing import Protocol

class SniperListener(Protocol):
    """Sniper 상태 변경을 추적하는 리스너"""

    @abstractmethod
    def sniper_lost(self) -> None:
        """경매에서 졌을 때 호출"""
        pass
```

**첫 번째 단위 테스트**:

```java
// AuctionSniper 단위 테스트
// 참조: 페이지 149, 줄 45-58
@RunWith(JMock.class)
public class AuctionSniperTest {
    private final Mockery context = new Mockery();
    private final SniperListener sniperListener =
                                        context.mock(SniperListener.class);
    private final AuctionSniper sniper = new AuctionSniper(sniperListener);

    @Test public void reportsLostWhenAuctionCloses() {
        context.checking(new Expectations() {{
            one(sniperListener).sniperLost();
        }});
        sniper.auctionClosed();
    }
}
```

```python
# 파이썬 버전 (pytest + unittest.mock)
import pytest
from unittest.mock import Mock, call

class TestAuctionSniper:
    """AuctionSniper 단위 테스트"""

    def test_reports_lost_when_auction_closes(self):
        """경매가 종료되면 패배를 보고해야 함"""
        # Given
        sniper_listener = Mock(spec=SniperListener)
        sniper = AuctionSniper(sniper_listener)

        # When
        sniper.auction_closed()

        # Then
        sniper_listener.sniper_lost.assert_called_once()
```

**구현**:

```java
// AuctionSniper 구현
// 참조: 페이지 149, 줄 66-77
public class AuctionSniper implements AuctionEventListener {
    private final SniperListener sniperListener;

    public AuctionSniper(SniperListener sniperListener) {
        this.sniperListener = sniperListener;
    }

    public void auctionClosed() {
        sniperListener.sniperLost();
    }

    public void currentPrice(int price, int increment) {
        // TODO Auto-generated method stub
    }
}
```

```python
# 파이썬 버전
class AuctionSniper:
    """경매 스나이퍼 - 경매 이벤트에 반응하여 입찰"""

    def __init__(self, sniper_listener: SniperListener):
        self._sniper_listener = sniper_listener

    def auction_closed(self) -> None:
        """경매 종료 시 리스너에게 패배 알림"""
        self._sniper_listener.sniper_lost()

    def current_price(self, price: int, increment: int) -> None:
        """현재 가격 업데이트 (미구현)"""
        pass  # TODO: 구현 필요
```

**Main에 통합**:

```java
// Main이 SniperListener 구현
// 참조: 페이지 150, 줄 85-102
public class Main implements SniperListener {
    // ...

    private void joinAuction(XMPPConnection connection, String itemId)
        throws XMPPException
    {
        disconnectWhenUICloses(connection);
        Chat chat = connection.getChatManager().createChat(
            auctionId(itemId, connection),
            new AuctionMessageTranslator(new AuctionSniper(this)));
        this.notToBeGCd = chat;
        chat.sendMessage(JOIN_COMMAND_FORMAT);
    }

    public void sniperLost() {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                ui.showStatus(MainWindow.STATUS_LOST);
            }
        });
    }
}
```

```python
# 파이썬 버전
class Main(SniperListener):
    """애플리케이션 메인 - SniperListener 구현"""

    def __init__(self):
        self._ui: MainWindow = None
        self._not_to_be_gcd = None

    def join_auction(self, connection: XMPPConnection, item_id: str) -> None:
        """경매 참여"""
        self._disconnect_when_ui_closes(connection)

        chat = connection.get_chat_manager().create_chat(
            self._auction_id(item_id, connection),
            AuctionMessageTranslator(AuctionSniper(self))
        )
        self._not_to_be_gcd = chat
        chat.send_message(JOIN_COMMAND_FORMAT)

    def sniper_lost(self) -> None:
        """스나이퍼가 경매에서 졌을 때"""
        def update_ui():
            self._ui.show_status(MainWindow.STATUS_LOST)

        # Swing 스레드에서 UI 업데이트
        threading.Thread(target=update_ui).start()
```

#### 1.2. 집중, 집중, 집중 (Focus, Focus, Focus)

**참조**: 페이지 150-151, 줄 109-129

**이전 화제와의 관계**: 1.1에서 추출한 AuctionSniper의 가치 설명

**설명**:

**핵심 개념**: [단일 책임 원칙 ✓]

복잡성을 인식하고 새 개념을 추출하는 것이 낭비인가? → **아니오**

**이점**:
1. 코드 표현력 향상
2. 단위 테스트 용이
3. `sniperLost()` 메서드가 이전 `auctionClosed()`보다 명확 - 이름과 동작이 일치

**팀의 관찰**:
- 대부분의 팀은 코드 명확화에 너무 적은 시간을 씀
- 유지보수 오버헤드로 나중에 대가를 치름
- "단일 책임" 원칙은 복잡성 분해에 매우 효과적
- 새로운 타입 생성을 두려워하지 말 것

**아직 남은 문제**:
- Main이 여전히 너무 많은 일을 함
- 아직 어떻게 분해할지 확실하지 않음
- → 계속 진행하며 코드가 우리를 어디로 이끄는지 관찰

---

### 2. 입찰 보내기 (Sending a Bid)

**이전 화제와의 관계**: 1장에서 AuctionSniper 추출 완료, 이제 입찰 기능 구현

#### 2.1. Auction 인터페이스 (An Auction Interface)

**참조**: 페이지 151, 줄 130-146

**설명**:

Sniper가 경매에 입찰을 보내려면 누구와 대화해야 하는가?

**핵심 개념**: [의존성 분리와 인터페이스 도입 ✓]

**잘못된 접근**:
- SniperListener 확장? → **아니오**
- SniperListener는 Sniper의 일어나는 일 추적, 외부 약속(commitment)이 아님
- Object Peer Stereotypes 용어: SniperListener는 **알림(notification)**, **의존성(dependency)** 아님

**올바른 접근**:
- 새 협력자 도입: **Auction**
- **Auction**: 금융 거래 도메인 - 시장의 아이템에 대한 입찰 수락
- **SniperListener**: 애플리케이션 피드백 도메인 - Sniper 현재 상태 변경 보고

**관계 정의**:
- **Auction** = 의존성: Sniper는 Auction 없이 동작 불가
- **SniperListener** = 알림: Sniper 상태 추적만 담당

**설계 다이어그램**: Figure 13.2 - Introducing Auction

#### 2.2. AuctionSniper가 입찰하다 (The AuctionSniper Bids)

**참조**: 페이지 151-153, 줄 147-207

**이전 화제와의 관계**: 2.1에서 Auction 인터페이스 도입, 이제 입찰 로직 구현

**설명**:

Price 이벤트에 반응하는 구현 시작.

**핵심 개념**: [AuctionSniper 클래스 추출 ✓]

**단위 테스트**:

```java
// 입찰 테스트
// 참조: 페이지 152, 줄 160-175
public class AuctionSniperTest {
    private final Auction auction = context.mock(Auction.class);
    private final AuctionSniper sniper =
                        new AuctionSniper(auction, sniperListener);
    // ...

    @Test public void bidsHigherAndReportsBiddingWhenNewPriceArrives() {
        final int price = 1001;
        final int increment = 25;

        context.checking(new Expectations() {{
            one(auction).bid(price + increment);
            atLeast(1).of(sniperListener).sniperBidding();
        }});

        sniper.currentPrice(price, increment);
    }
}
```

```python
# 파이썬 버전
class TestAuctionSniper:
    def test_bids_higher_and_reports_bidding_when_new_price_arrives(self):
        """새 가격 도착 시 더 높게 입찰하고 입찰 중 상태 보고"""
        # Given
        auction = Mock(spec=Auction)
        sniper_listener = Mock(spec=SniperListener)
        sniper = AuctionSniper(auction, sniper_listener)

        price = 1001
        increment = 25

        # When
        sniper.current_price(price, increment)

        # Then
        auction.bid.assert_called_once_with(price + increment)
        sniper_listener.sniper_bidding.assert_called()
```

**테스트 설계 결정**:
1. `sniperListener.sniperBidding()` - `atLeast(1)`: 상태 업데이트, 여러 번 호출 허용
2. `auction.bid()` - `one()`: 정확히 한 번, 중복 입찰 방지
3. → listener는 더 관대한 협력자, Auction은 엄격

**기대값 표현 방법**:
- `price + increment` 계산식 사용
- 리터럴 vs 계산: 계산이 너무 간단하면 테스트에 직접 작성
- 재구현 위험 vs 가독성 균형

**jMock 기대값 순서**:
- 선언 순서 ≠ 호출 순서
- 순서가 중요하면 sequence 절 사용 (Appendix A 참조)

**구현**:

```java
// Auction 인터페이스와 AuctionSniper 구현
// 참조: 페이지 153, 줄 209-223
public interface Auction {
    void bid(int amount);
}

public class AuctionSniper implements AuctionEventListener {
    private final SniperListener sniperListener;
    private final Auction auction;

    public AuctionSniper(Auction auction, SniperListener sniperListener) {
        this.auction = auction;
        this.sniperListener = sniperListener;
    }

    public void currentPrice(int price, int increment) {
        auction.bid(price + increment);
        sniperListener.sniperBidding();
    }
}
```

```python
# 파이썬 버전
from abc import ABC, abstractmethod

class Auction(ABC):
    """경매 인터페이스"""

    @abstractmethod
    def bid(self, amount: int) -> None:
        """입찰"""
        pass

class AuctionSniper:
    """경매 스나이퍼 - 입찰 로직 포함"""

    def __init__(self, auction: Auction, sniper_listener: SniperListener):
        self._auction = auction
        self._sniper_listener = sniper_listener

    def auction_closed(self) -> None:
        """경매 종료"""
        self._sniper_listener.sniper_lost()

    def current_price(self, price: int, increment: int) -> None:
        """현재 가격 업데이트 - 더 높게 입찰"""
        self._auction.bid(price + increment)
        self._sniper_listener.sniper_bidding()
```

#### 2.3. AuctionSniper로 성공적인 입찰 (Successfully Bidding with the AuctionSniper)

**참조**: 페이지 153-156, 줄 224-318

**이전 화제와의 관계**: 2.2에서 단위 테스트 완료, 이제 애플리케이션에 통합

**설명**:

**핵심 개념**: [Null Implementation 패턴 ✓]

**통합 단계**:

1. **UI 상태 표시** (쉬움)
2. **경매에 입찰 전송** (약간 어려움)

**컴파일 통과를 위한 Null Implementation**:

```java
// Null Auction 구현
// 참조: 페이지 154, 줄 236-256
public class Main implements SniperListener {
    // ...

    private void joinAuction(XMPPConnection connection, String itemId)
        throws XMPPException
    {
        Auction nullAuction = new Auction() {
            public void bid(int amount) {}  // 아무 동작 안 함
        };

        disconnectWhenUICloses(connection);
        Chat chat = connection.getChatManager().createChat(
            auctionId(itemId, connection),
            new AuctionMessageTranslator(new AuctionSniper(nullAuction, this)));
        this.notToBeGCd = chat;
        chat.sendMessage(JOIN_COMMAND_FORMAT);
    }

    public void sniperBidding() {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                ui.showStatus(MainWindow.STATUS_BIDDING);
            }
        });
    }
}
```

```python
# 파이썬 버전
class Main(SniperListener):
    """메인 - Null Auction 사용"""

    def join_auction(self, connection: XMPPConnection, item_id: str) -> None:
        """경매 참여 - Null Auction으로 임시 구현"""

        # Null Implementation
        class NullAuction(Auction):
            def bid(self, amount: int) -> None:
                pass  # 아무 동작 안 함

        null_auction = NullAuction()

        self._disconnect_when_ui_closes(connection)
        chat = connection.get_chat_manager().create_chat(
            self._auction_id(item_id, connection),
            AuctionMessageTranslator(AuctionSniper(null_auction, self))
        )
        self._not_to_be_gcd = chat
        chat.send_message(JOIN_COMMAND_FORMAT)

    def sniper_bidding(self) -> None:
        """입찰 중 상태 UI 업데이트"""
        def update():
            self._ui.show_status(MainWindow.STATUS_BIDDING)

        threading.Thread(target=update).start()
```

**의존성 순환 문제**:
- Chat 생성 → Translator 필요
- Translator → Sniper 필요
- Sniper → Auction 필요
- Auction → Chat 필요 (입찰 메시지 전송)
- → **의존성 순환!**

**해결책**:
ChatManager API가 오해의 소지 있음. MessageListener는 **알림(notification)**이므로:
- Chat 생성 시 null 전달 가능
- 나중에 MessageListener 추가

**API 의도 표현**:
- Smack 라이브러리 소스 코드 확인으로 발견
- API만으로는 불명확
- 대안: listener 없는 생성 메서드 제공 (API 비대화 문제)
- → 소스 코드 포함 배포가 라이브러리 사용성 향상

**재구조화된 연결 코드**:

```java
// Chat를 먼저 생성하고 Auction 구현
// 참조: 페이지 155, 줄 282-303
public class Main implements SniperListener {
    // ...

    private void joinAuction(XMPPConnection connection, String itemId)
        throws XMPPException
    {
        disconnectWhenUICloses(connection);

        // 1. Chat 먼저 생성 (listener null)
        final Chat chat =
            connection.getChatManager().createChat(
                auctionId(itemId, connection), null);
        this.notToBeGCd = chat;

        // 2. Auction 구현 (Chat 사용)
        Auction auction = new Auction() {
            public void bid(int amount) {
                try {
                    chat.sendMessage(
                        String.format(BID_COMMAND_FORMAT, amount));
                } catch (XMPPException e) {
                    e.printStackTrace();  // TODO: 개선 필요
                }
            }
        };

        // 3. MessageListener 나중에 추가
        chat.addMessageListener(
            new AuctionMessageTranslator(new AuctionSniper(auction, this)));
        chat.sendMessage(JOIN_COMMAND_FORMAT);
    }
}
```

```python
# 파이썬 버전
class Main(SniperListener):
    """메인 - 의존성 순환 해결"""

    def join_auction(self, connection: XMPPConnection, item_id: str) -> None:
        """경매 참여 - 의존성 순환 해결"""
        self._disconnect_when_ui_closes(connection)

        # 1. Chat 먼저 생성 (listener 없이)
        chat = connection.get_chat_manager().create_chat(
            self._auction_id(item_id, connection),
            None  # listener는 나중에 추가
        )
        self._not_to_be_gcd = chat

        # 2. Auction 구현 (Chat 캡처)
        class ChatAuction(Auction):
            def bid(self, amount: int) -> None:
                try:
                    chat.send_message(
                        BID_COMMAND_FORMAT.format(amount))
                except XMPPException as e:
                    print(e)  # TODO: 더 나은 에러 처리 필요

        auction = ChatAuction()

        # 3. MessageListener 나중에 추가
        chat.add_message_listener(
            AuctionMessageTranslator(AuctionSniper(auction, self)))
        chat.send_message(JOIN_COMMAND_FORMAT)
```

**Null Implementation vs Null Object**:
- **Null Object**: 프로토콜에 아무것도 하지 않는 여러 구현 중 하나, 호출 코드 복잡성 감소
- **Null Implementation**: 임시 빈 구현, 진행을 위해 노력 연기, 교체 예정

**End-to-End 테스트 통과**:
- 입찰 없이 패배
- 입찰 후 패배
- ✓ 항목 체크

**남은 문제**:
- XMPPException 단순 출력 - 나쁜 관행
- End-to-End 테스트가 실패 감지하므로 일단 진행
- TODO 항목 추가: 더 나은 해결책 찾기 (Figure 13.3)

---

### 3. 구현 정리 (Tidying Up the Implementation)

**이전 화제와의 관계**: 2장에서 End-to-End 테스트 통과, 이제 코드 정리

#### 3.1. XMPPAuction 추출 (Extracting XMPPAuction)

**참조**: 페이지 156-158, 줄 326-388

**설명**:

**핵심 개념**: [XMPPAuction 추출 ✓]

End-to-End 테스트는 통과했지만 새 구현이 지저분함.

**문제점**:
- `joinAuction()`이 여러 도메인에 걸쳐 있음:
  - Chat 관리
  - 입찰 전송
  - Sniper 생성
  - 등등

**관찰**:
- 경매 명령을 두 레벨에서 전송:
  1. 최상위 (`chat.sendMessage(JOIN_COMMAND_FORMAT)`)
  2. Auction 내부 (`bid()` 메서드)
- → 경매 명령 전송은 **Auction 객체가 할 일**

**리팩토링**:
1. Auction 인터페이스에 `join()` 메서드 추가
2. 익명 구현 확장
3. 중첩 클래스로 추출
4. 이름 지정: **XMPPAuction** (메시징 인프라 기반)

**XMPPAuction 구현**:

```java
// XMPPAuction 중첩 클래스
// 참조: 페이지 157, 줄 343-374
public class Main implements SniperListener {
    // ...

    private void joinAuction(XMPPConnection connection, String itemId) {
        disconnectWhenUICloses(connection);

        final Chat chat =
            connection.getChatManager().createChat(
                auctionId(itemId, connection), null);
        this.notToBeGCd = chat;

        Auction auction = new XMPPAuction(chat);
        chat.addMessageListener(
            new AuctionMessageTranslator(new AuctionSniper(auction, this)));
        auction.join();  // 명확한 의도 표현
    }

    public static class XMPPAuction implements Auction {
        private final Chat chat;

        public XMPPAuction(Chat chat) {
            this.chat = chat;
        }

        public void bid(int amount) {
            sendMessage(format(BID_COMMAND_FORMAT, amount));
        }

        public void join() {
            sendMessage(JOIN_COMMAND_FORMAT);
        }

        private void sendMessage(final String message) {
            try {
                chat.sendMessage(message);
            } catch (XMPPException e) {
                e.printStackTrace();  // TODO: 개선 필요
            }
        }
    }
}
```

```python
# 파이썬 버전
class XMPPAuction(Auction):
    """XMPP 메시징 기반 Auction 구현"""

    def __init__(self, chat):
        self._chat = chat

    def bid(self, amount: int) -> None:
        """입찰"""
        self._send_message(BID_COMMAND_FORMAT.format(amount))

    def join(self) -> None:
        """경매 참여"""
        self._send_message(JOIN_COMMAND_FORMAT)

    def _send_message(self, message: str) -> None:
        """메시지 전송 (에러 처리 포함)"""
        try:
            self._chat.send_message(message)
        except XMPPException as e:
            print(e)  # TODO: 더 나은 에러 처리

class Main(SniperListener):
    """메인 - XMPPAuction 사용"""

    def join_auction(self, connection: XMPPConnection, item_id: str) -> None:
        """경매 참여 - XMPPAuction으로 정리"""
        self._disconnect_when_ui_closes(connection)

        chat = connection.get_chat_manager().create_chat(
            self._auction_id(item_id, connection), None)
        self._not_to_be_gcd = chat

        auction = XMPPAuction(chat)
        chat.add_message_listener(
            AuctionMessageTranslator(AuctionSniper(auction, self)))
        auction.join()  # 명확한 의도 표현
```

**개선점**:
- `auction.join()` - 의도를 명확히 표현
- Chat에 문자열 전송하는 상세 구현 숨김
- 도메인 모델이 명확해짐

**설계 다이어그램**: Figure 13.4 - Closing the loop with an XMPPAuction

**다음 단계**:
- XMPPAuction을 최상위 클래스로 승격
- `joinAuction()`은 여전히 불명확 - XMPP 상세 내용을 Main에서 제거하고 싶음
- → 아직 준비되지 않음, 나중에

#### 3.2. 사용자 인터페이스 추출 (Extracting the User Interface)

**참조**: 페이지 158-159, 줄 389-444

**이전 화제와의 관계**: 3.1에서 XMPPAuction 추출, 이제 UI 책임 분리

**설명**:

**핵심 개념**: [SniperStateDisplayer 추출 ✓]

**문제점**:
- Main이 SniperListener 구현 - 서로 다른 책임 혼합
  - 애플리케이션 시작
  - 이벤트 응답

**해결책**:
- SniperListener 동작을 중첩 헬퍼 클래스로 추출
- 이름: **SniperStateDisplayer**
- 역할: 두 도메인 간 브리지
  - Sniper 이벤트 → Swing 표현으로 변환
  - Swing 스레딩 처리 포함

**SniperStateDisplayer 구현**:

```java
// SniperStateDisplayer 추출
// 참조: 페이지 159, 줄 399-434
public class Main {  // SniperListener 구현 제거
    private MainWindow ui;

    private void joinAuction(XMPPConnection connection, String itemId) {
        disconnectWhenUICloses(connection);

        final Chat chat =
            connection.getChatManager().createChat(
                auctionId(itemId, connection), null);
        this.notToBeGCd = chat;

        Auction auction = new XMPPAuction(chat);
        chat.addMessageListener(
            new AuctionMessageTranslator(
                connection.getUser(),
                new AuctionSniper(auction, new SniperStateDisplayer())));
        auction.join();
    }

    // 중첩 클래스: Sniper 이벤트를 UI로 변환
    public class SniperStateDisplayer implements SniperListener {
        public void sniperBidding() {
            showStatus(MainWindow.STATUS_BIDDING);
        }

        public void sniperLost() {
            showStatus(MainWindow.STATUS_LOST);
        }

        public void sniperWinning() {
            showStatus(MainWindow.STATUS_WINNING);
        }

        private void showStatus(final String status) {
            SwingUtilities.invokeLater(new Runnable() {
                public void run() {
                    ui.showStatus(status);
                }
            });
        }
    }
}
```

```python
# 파이썬 버전
class SniperStateDisplayer(SniperListener):
    """Sniper 이벤트를 UI 표현으로 변환하는 브리지"""

    def __init__(self, ui: MainWindow):
        self._ui = ui

    def sniper_bidding(self) -> None:
        """입찰 중 상태 표시"""
        self._show_status(MainWindow.STATUS_BIDDING)

    def sniper_lost(self) -> None:
        """패배 상태 표시"""
        self._show_status(MainWindow.STATUS_LOST)

    def sniper_winning(self) -> None:
        """승리 중 상태 표시"""
        self._show_status(MainWindow.STATUS_WINNING)

    def _show_status(self, status: str) -> None:
        """Swing 스레드에서 UI 업데이트"""
        def update():
            self._ui.show_status(status)

        # UI 스레드에서 실행
        threading.Thread(target=update).start()

class Main:
    """메인 - 이제 SniperListener 구현 안 함"""

    def __init__(self):
        self._ui: MainWindow = None
        self._not_to_be_gcd = None

    def join_auction(self, connection: XMPPConnection, item_id: str) -> None:
        """경매 참여 - SniperStateDisplayer 사용"""
        self._disconnect_when_ui_closes(connection)

        chat = connection.get_chat_manager().create_chat(
            self._auction_id(item_id, connection), None)
        self._not_to_be_gcd = chat

        auction = XMPPAuction(chat)
        chat.add_message_listener(
            AuctionMessageTranslator(
                connection.get_user(),
                AuctionSniper(auction, SniperStateDisplayer(self._ui))))
        auction.join()
```

**설계 개선**:
- Main이 더 이상 실행 중인 애플리케이션에 참여하지 않음
- Main의 역할: 컴포넌트 생성 & 서로 연결
- MainWindow는 external로 표시 (Swing 프레임워크)

**설계 다이어그램**: Figure 13.5 - Extracting SniperStateDisplayer

#### 3.3. Translator 정리 (Tidying Up the Translator)

**참조**: 페이지 160-161, 줄 447-527

**이전 화제와의 관계**: 3.2에서 UI 추출 완료, 이제 AuctionMessageTranslator 리팩토링

**설명**:

**핵심 개념**: [Value Type 패턴 ✓]

**문제점**:
- AuctionMessageTranslator 코드가 노이즈 많음
- name/value 쌍 맵 조작이 절차적(procedural)

**리팩토링 단계**:
1. 상수 추가 및 static import로 노이즈 감소
2. 헬퍼 메서드로 중복 제거
3. 내부 클래스 **AuctionEvent** 추출 - 메시지 파싱 캡슐화

**최종 코드**:

```java
// AuctionMessageTranslator with AuctionEvent
// 참조: 페이지 160-161, 줄 466-504
public class AuctionMessageTranslator implements MessageListener {
    private final AuctionEventListener listener;

    public AuctionMessageTranslator(AuctionEventListener listener) {
        this.listener = listener;
    }

    public void processMessage(Chat chat, Message message) {
        AuctionEvent event = AuctionEvent.from(message.getBody());
        String eventType = event.type();

        if ("CLOSE".equals(eventType)) {
            listener.auctionClosed();
        } if ("PRICE".equals(eventType)) {
            listener.currentPrice(event.currentPrice(), event.increment());
        }
    }

    // 내부 Value Type 클래스
    private static class AuctionEvent {
        private final Map<String, String> fields = new HashMap<String, String>();

        public String type() { return get("Event"); }
        public int currentPrice() { return getInt("CurrentPrice"); }
        public int increment() { return getInt("Increment"); }

        private int getInt(String fieldName) {
            return Integer.parseInt(get(fieldName));
        }

        private String get(String fieldName) {
            return fields.get(fieldName);
        }

        private void addField(String field) {
            String[] pair = field.split(":");
            fields.put(pair[0].trim(), pair[1].trim());
        }

        static AuctionEvent from(String messageBody) {
            AuctionEvent event = new AuctionEvent();
            for (String field : fieldsIn(messageBody)) {
                event.addField(field);
            }
            return event;
        }

        static String[] fieldsIn(String messageBody) {
            return messageBody.split(";");
        }
    }
}
```

```python
# 파이썬 버전
from typing import Dict
from dataclasses import dataclass, field

@dataclass
class AuctionEvent:
    """경매 이벤트 값 객체 - 메시지 파싱 캡슐화"""

    _fields: Dict[str, str] = field(default_factory=dict)

    def type(self) -> str:
        """이벤트 타입"""
        return self._get("Event")

    def current_price(self) -> int:
        """현재 가격"""
        return self._get_int("CurrentPrice")

    def increment(self) -> int:
        """증분"""
        return self._get_int("Increment")

    def _get_int(self, field_name: str) -> int:
        """정수 필드 가져오기"""
        return int(self._get(field_name))

    def _get(self, field_name: str) -> str:
        """문자열 필드 가져오기"""
        return self._fields[field_name]

    def _add_field(self, field: str) -> None:
        """필드 추가 (파싱)"""
        key, value = field.split(":")
        self._fields[key.strip()] = value.strip()

    @staticmethod
    def from_message(message_body: str) -> 'AuctionEvent':
        """메시지 본문에서 AuctionEvent 생성"""
        event = AuctionEvent()
        for field in AuctionEvent._fields_in(message_body):
            event._add_field(field)
        return event

    @staticmethod
    def _fields_in(message_body: str) -> list[str]:
        """메시지 본문을 필드로 분할"""
        return message_body.split(";")

class AuctionMessageTranslator:
    """경매 메시지를 이벤트로 변환"""

    def __init__(self, listener: AuctionEventListener):
        self._listener = listener

    def process_message(self, chat, message) -> None:
        """메시지 처리 - 이벤트로 변환"""
        event = AuctionEvent.from_message(message.get_body())
        event_type = event.type()

        if event_type == "CLOSE":
            self._listener.auction_closed()
        elif event_type == "PRICE":
            self._listener.current_price(
                event.current_price(),
                event.increment())
```

**Value Type 특징**:
- 불변(immutable)
- 같은 내용의 두 인스턴스는 구별 불가
- "Breaking Out" 패턴 (Value Types, page 59)

**관심사 분리**:
- 최상위: 이벤트와 리스너 처리
- 내부 객체: 문자열 파싱

**컬렉션 캡슐화 원칙**:
- Java 제네릭으로 캐스팅 불필요해졌지만 여전히 자체 클래스로 감쌈
- 문제 도메인 언어 사용 vs Java 구조 언어
- 제네릭 타입(`<>`)은 중복의 한 형태
- → 도메인 개념을 타입으로 추출하라는 힌트

---

### 4. 설계 원칙

#### 4.1. 점진적 설계 (Emergent Design)

**참조**: 페이지 162, 줄 549-568

**이전 화제와의 관계**: 3장 전체 리팩토링 과정 회고

**설명**:

**핵심 개념**: [점진적 설계 ✓]

**설계 성장 방식**:
1. 기능 추가
2. 반성 및 정리
3. 반복

**정리 단계의 중요성**:
- 정리하지 않으면 유지보수 불가능한 혼란
- 아직 명확하지 않으면 리팩토링 연기 가능
- 준비되면 시간을 가짐

**기법**:
- 가능한 한 깨끗한 코드 유지
- 작은 증분 단위로 이동
- Null Implementation으로 중단 시간 최소화

**레이어 구축**:
- Figure 13.5: 외부 의존성으로부터 핵심 구현을 "보호"하는 레이어
- 좋은 관행이지만 흥미로운 점은 **점진적으로 도달**
- 클래스의 기능이 함께 가는지 안 가는지 찾아봄

**경험의 영향**:
- 비슷한 코드베이스 경험에 영향 받음
- 하지만 선입견 강요보다 **코드가 말하는 것을 따름**
- 때때로 도메인이 놀라운 방향으로 이끔

#### 4.2. 결정 연기 (Defer Decisions)

**참조**: 페이지 161, 줄 527-536

**이전 화제와의 관계**: 전체 챕터에서 사용한 기법 설명

**설명**:

**핵심 개념**: [Null Implementation 패턴 ✓]

**기법**:
- 메서드(또는 타입)의 Null Implementation 도입
- 다음 단계를 통과하게 해줌
- 다음 중요 기능 덩어리에 대한 생각을 미룸

**예시**:
- Null Auction: 단위 테스트에서 발견한 새 관계를 메시징 문제 없이 연결
- → 의존성에 대해 생각할 수 있었음, 컴파일 중단 압박 없이

**이점**:
- 즉시 작업에 집중
- 기능 구현으로 끌려가지 않음
- 객체 간 의존성 설계에 집중

#### 4.3. 코드 컴파일 유지 (Keep the Code Compiling)

**참조**: 페이지 161-162, 줄 536-547

**이전 화제와의 관계**: 4.2 결정 연기 기법의 이점 설명

**설명**:

**원칙**:
컴파일되지 않는 시간 최소화, 변경을 점진적으로 유지

**컴파일 실패 시 문제**:
- 변경 경계가 확실하지 않음
- 컴파일러가 알려줄 수 없음
- 소스 저장소에 체크인 불가 (자주 하고 싶음)
- 더 많은 코드 = 머리에 더 많이 담아야 함 = 느려짐

**TDD의 위대한 발견**:
- 개발 단계가 얼마나 세밀할 수 있는지
- 작은 증분으로 진행 가능

**이점**:
- 명확한 경계
- 빈번한 체크인
- 인지 부하 감소
- 실제로 더 빠른 개발

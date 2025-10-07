# Chapter 17: Main 클래스 분리하기 (Teasing Apart Main)

## 압축 내용
Main 클래스에 과도하게 집중된 책임들(XMPP 통신, UI 관리, 스니핑 로직)을 점진적 리팩토링을 통해 독립적인 컴포넌트들로 분리하여 "포트와 어댑터" 아키텍처를 달성하고, 도메인 코드를 외부 인프라로부터 격리시키는 과정

## 핵심 내용

### 핵심 개념

1. **매치메이커 역할 (Matchmaker Role)** - 상세 내용 1 참조
   - Main 클래스의 적절한 역할 정의: 컴포넌트를 찾아서 서로 연결해주고 백그라운드로 물러남
   - 현재 Main의 문제: 매치메이커 역할과 동시에 일부 컴포넌트를 직접 구현하여 너무 많은 책임을 가짐
   - 패키지 순환 의존성 문제 발견 (top-level과 UI 패키지 간)

2. **Chat 추출 (Extracting the Chat)** - 상세 내용 2, 3 참조
   - XMPP 관련 기능을 Main에서 분리하는 첫 단계
   - Announcer를 사용하여 의존성 루프 해결
   - XMPPAuction으로 Chat 관련 모든 로직 캡슐화
   - 새로운 통합 테스트 작성으로 검증

3. **Connection 추출 (Extracting the Connection)** - 상세 내용 4 참조
   - XMPPConnection 직접 참조 제거
   - AuctionHouse 인터페이스와 XMPPAuctionHouse 구현으로 팩토리 패턴 도입
   - 도메인 언어 사용: "auction house"가 경매를 관리하는 개념
   - Main의 XMPP 관련 import를 하나로 통합

4. **SniperLauncher 추출 (Extracting SniperLauncher)** - 상세 내용 5 참조
   - 익명 UserRequestListener 구현을 독립 클래스로 전환
   - notToBeGCd를 로컬 필드로 이동
   - SniperCollector 역할 도입으로 책임 분리
   - Swing 관련 기능을 SniperLauncher에서 제거

5. **SniperPortfolio 추출 (Extracting SniperPortfolio)** - 상세 내용 6 참조
   - 모든 스나이핑 활동을 나타내는 포트폴리오 개념 도입
   - SnipersTableModel의 이중 책임 분리: 데이터 유지 vs 표시
   - PortfolioListener 패턴으로 느슨한 결합 달성
   - notToBeGCd 완전 제거

6. **포트와 어댑터 아키텍처 (Ports and Adapters Architecture)** - 상세 내용 7 참조
   - 핵심 도메인 코드, 브리징 코드, 기술 코드의 3계층 분리
   - 도메인 코드가 외부 인프라로부터 완전히 독립
   - auctionsniper 패키지가 자체 완결적 언어로 비즈니스 모델 정의

7. **점진적 리팩토링 (Incremental Refactoring)** - 상세 내용 8 참조
   - "삼점 접촉" 원칙: 한 번에 하나의 작은 변경만 수행
   - 항상 몇 분 이내에 작동하는 코드로 돌아갈 수 있도록 유지
   - 경험적 규칙(heuristics)을 반복 적용하여 자동적으로 좋은 설계에 도달

### 핵심 개념 간 관계

```
Matchmaker 역할 문제
    ↓ (분석)
패키지 루프 & 책임 과다 발견
    ↓ (전략 수립)
점진적 추출 전략 (XMPP → UI)
    ↓ (1단계: Chat 처리)
Announcer 패턴으로 순환 의존성 해결
    ↓
XMPPAuction 캡슐화 (Chat 숨김)
    ↓ (2단계: Connection 처리)
AuctionHouse 추상화 (도메인 언어 반영)
    ↓ (3단계: UI 모델 처리)
SniperLauncher 분리 (명확한 책임)
    ↓
SniperCollector 역할 도입 (관심사 분리)
    ↓
SniperPortfolio (notToBeGCd 제거, 포트폴리오 개념)
    ↓ (최종 결과)
포트와 어댑터 아키텍처 완성
    ↑ (지원 원칙)
Three-Point Contact (안전한 점진적 변경)
```

**관계 설명:**
- **Matchmaker 역할**은 리팩토링의 목표를 제시하고, 각 추출 단계의 방향성을 제공
- **패키지 루프 & 책임 과다**는 구체적인 문제점을 식별하여 개선 영역을 명확히 함
- **점진적 추출 전략**은 XMPP → UI 순서로 단계별 접근 방식 설정
- **Announcer 패턴**은 XMPPAuction, Chat, AuctionSniper 간 순환 의존성을 깨뜨림
- **XMPPAuction 캡슐화**는 Chat 관련 모든 로직을 하나의 클래스로 응집
- **AuctionHouse 추상화**는 도메인 언어(경매장)를 반영하여 XMPP 의존성을 완전히 격리
- **SniperLauncher 분리**는 익명 클래스를 독립 클래스로 추출하여 책임을 명확히 함
- **SniperCollector 역할**은 Sniper 생성과 수용을 분리하여 단일 책임 원칙 준수
- **SniperPortfolio**는 스니핑 활동 전체를 대표하는 개념으로 notToBeGCd 완전 제거
- **포트와 어댑터 아키텍처**는 자연스럽게 나타난 최종 구조
- **Three-Point Contact**는 전 과정에서 안전한 점진적 변경을 보장하는 핵심 원칙

## 상세 내용

### 화제 목차
1. Main 클래스의 역할 찾기 (Finding a Role) - 라인 10-41
2. Chat 격리하기 (Isolating the Chat) - 라인 42-111
3. Chat 캡슐화하기 (Encapsulating the Chat) - 라인 112-196
4. Connection 추출하기 (Extracting the Connection) - 라인 197-251
5. SnipersTableModel 추출하기 - SniperLauncher (Sniper Launcher) - 라인 252-356
6. SnipersTableModel 추출하기 - SniperPortfolio (Sniper Portfolio) - 라인 357-413
7. 관찰과 성찰 (Observations) - 라인 414-489

---

### 1. Main 클래스의 역할 찾기 (Finding a Role)
**참조:** content.md 라인 10-41
**관련 핵심 개념:** 매치메이커 역할

**이전 화제와의 관계:** 이 장의 시작점으로, Main 클래스 리팩토링의 필요성과 목표를 설정

**설명:**

Main 클래스의 적절한 역할을 정의하는 것부터 시작한다. 사소하지 않은 프로그램의 경우, 최상위 클래스를 "매치메이커(matchmaker)"로 생각하는 것이 좋다. 컴포넌트들을 찾아서 서로 소개시켜주고, 그 작업이 끝나면 백그라운드로 물러나 애플리케이션이 종료될 때까지 기다린다.

현재 Main 클래스의 문제점:
- 매치메이커 역할을 수행하면서 동시에 일부 컴포넌트를 직접 구현
- 너무 많은 책임을 가지고 있음
- import 문을 보면 세 개의 관련 없는 패키지에서 코드를 가져옴
- 패키지 순환 의존성 존재: top-level과 UI 패키지가 서로 의존

```python
# Java 원본 (라인 21-31)
# import java.awt.event.WindowAdapter;
# import java.awt.event.WindowEvent;
# import java.util.ArrayList;
# import javax.swing.SwingUtilities;
# import org.jivesoftware.smack.Chat;
# import org.jivesoftware.smack.XMPPConnection;
# import org.jivesoftware.smack.XMPPException;
# import auctionsniper.ui.MainWindow;
# import auctionsniper.ui.SnipersTableModel;
# import auctionsniper.AuctionMessageTranslator;
# import auctionsniper.XMPPAuction;

# Python 버전
# from java.awt.event import WindowAdapter, WindowEvent
# from java.util import ArrayList
# from javax.swing import SwingUtilities
# from org.jivesoftware.smack import Chat, XMPPConnection, XMPPException
# from auctionsniper.ui import MainWindow, SnipersTableModel
# from auctionsniper import AuctionMessageTranslator, XMPPAuction

# 세 개의 관련 없는 패키지에서 import:
# 1. java.awt/javax.swing (UI)
# 2. org.jivesoftware.smack (XMPP)
# 3. auctionsniper (도메인)
```

**개선 방향:** Smack 사용은 애플리케이션의 나머지 부분과 무관한 구현 세부사항이어야 하므로, XMPP 기능을 Main에서 추출하는 것이 좋은 첫 번째 후보가 된다.

---

### 2. Chat 격리하기 (Isolating the Chat)
**참조:** content.md 라인 42-111
**관련 핵심 개념:** Chat 추출

**이전 화제와의 관계:** 1장에서 식별한 XMPP 기능 분리를 실제로 구현하기 시작

**설명:**

Main 클래스의 `UserRequestListener.joinAuction()` 메서드에서 대부분의 작업이 이루어지는데, 여기서 경매 스나이핑(auction sniping)과 채팅(chatting)이라는 서로 다른 도메인 수준이 섞여 있다.

**문제 분석:**
- Chat 객체가 코드를 Smack에 묶어두고 있음
- Chat을 여러 곳에서 참조: 가비지 컬렉션 방지, Auction 구현에 연결, 메시지 리스너 연결
- XMPPAuction, Chat, AuctionSniper 간의 의존성 루프 존재

**해결책:** Announcer를 사용하여 두 컴포넌트를 연결함으로써 필요한 유연성 확보

```python
# Java 원본 - 리팩토링 전 (라인 56-73)
# public class Main { […]
#   private void addUserRequestListenerFor(final XMPPConnection connection) {
#     ui.addUserRequestListener(new UserRequestListener() {
#     public void joinAuction(String itemId) {
#       snipers.addSniper(SniperSnapshot.joining(itemId));
#         Chat chat = connection.getChatManager()
#                                  .createChat(auctionId(itemId, connection), null);
#         notToBeGCd.add(chat);
#         Auction auction = new XMPPAuction(chat);
# chat.addMessageListener(
#                new AuctionMessageTranslator(connection.getUser(),
#                      new AuctionSniper(itemId, auction,
#                            new SwingThreadSniperListener(snipers))));
#         auction.join();
#       }
#     });
#   }
# }

# Python 버전 - 리팩토링 전
class Main:
    def add_user_request_listener_for(self, connection):
        """XMPP 연결에 대한 사용자 요청 리스너 추가"""
        def join_auction(item_id):
            # 스나이퍼 추가
            self.snipers.add_sniper(SniperSnapshot.joining(item_id))

            # Chat 생성 (Smack 라이브러리 사용)
            chat = connection.get_chat_manager().create_chat(
                self.auction_id(item_id, connection),
                None
            )

            # 가비지 컬렉션 방지
            self.not_to_be_gcd.add(chat)

            # Auction 생성
            auction = XMPPAuction(chat)

            # 메시지 리스너 연결
            chat.add_message_listener(
                AuctionMessageTranslator(
                    connection.get_user(),
                    AuctionSniper(
                        item_id,
                        auction,
                        SwingThreadSniperListener(self.snipers)
                    )
                )
            )

            # 경매 참여
            auction.join()

        self.ui.add_user_request_listener(join_auction)


# Java 원본 - Announcer 적용 후 (라인 89-108)
# public class Main { […]
#   private void addUserRequestListenerFor(final XMPPConnection connection) {
#     ui.addUserRequestListener(new UserRequestListener() {
#       public void joinAuction(String itemId) {
#         Chat chat = connection.[…]
#         Announcer<AuctionEventListener> auctionEventListeners =
#             Announcer.to(AuctionEventListener.class);
#         chat.addMessageListener(
#             new AuctionMessageTranslator(
#                 connection.getUser(),
# auctionEventListeners.announce()));
#         notToBeGCd.add(chat);
#         Auction auction = new XMPPAuction(chat);
# auctionEventListeners.addListener(
#            new AuctionSniper(itemId, auction, new SwingThreadSniperListener(snipers)));
#         auction.join();
#       }
#     }
#   }
# }

# Python 버전 - Announcer 적용 후
class Main:
    def add_user_request_listener_for(self, connection):
        """Announcer를 사용하여 의존성 분리"""
        def join_auction(item_id):
            # Chat 생성
            chat = connection.get_chat_manager().create_chat(
                self.auction_id(item_id, connection),
                None
            )

            # Announcer 패턴으로 리스너 관리
            auction_event_listeners = Announcer(AuctionEventListener)

            # 메시지 변환기 연결 (Announcer 사용)
            chat.add_message_listener(
                AuctionMessageTranslator(
                    connection.get_user(),
                    auction_event_listeners.announce()
                )
            )

            # 가비지 컬렉션 방지
            self.not_to_be_gcd.add(chat)

            # Auction 생성
            auction = XMPPAuction(chat)

            # AuctionSniper를 리스너로 추가
            auction_event_listeners.add_listener(
                AuctionSniper(
                    item_id,
                    auction,
                    SwingThreadSniperListener(self.snipers)
                )
            )

            # 경매 참여
            auction.join()

        self.ui.add_user_request_listener(join_auction)
```

**효과:** 마지막 세 줄을 보면 Auction과 Sniper 관점에서 모든 것이 설명되고 있다 (Swing 스레드 문제는 아직 남아있지만).

---

### 3. Chat 캡슐화하기 (Encapsulating the Chat)
**참조:** content.md 라인 112-196
**관련 핵심 개념:** Chat 추출

**이전 화제와의 관계:** 2장에서 Announcer로 의존성을 분리한 후, 이제 Chat 관련 모든 것을 XMPPAuction으로 이동

**설명:**

Chat 설정 및 Announcer 사용과 관련된 모든 것을 XMPPAuction으로 밀어 넣고, Auction 인터페이스에 AuctionEventListener 관리 메서드를 추가한다. 코드는 점진적으로 변경하여 몇 분 이상 깨지지 않도록 유지했다.

```python
# Java 원본 - XMPPAuction 최종 형태 (라인 118-130)
# public final class XMPPAuction implements Auction { […]
#   private final Announcer<AuctionEventListener> auctionEventListeners = […]
#   private final Chat chat;
#   public XMPPAuction(XMPPConnection connection, String itemId) {
#     chat = connection.getChatManager().createChat(
#              auctionId(itemId, connection),
#              new AuctionMessageTranslator(connection.getUser(),
#                                           auctionEventListeners.announce()));
#   }
#   private static String auctionId(String itemId, XMPPConnection connection) {
#     return String.format(AUCTION_ID_FORMAT, itemId, connection.getServiceName());
#   }
# }

# Python 버전 - XMPPAuction 최종 형태
class XMPPAuction:
    """XMPP를 사용한 경매 구현 - Chat 완전 캡슐화"""

    AUCTION_ID_FORMAT = "auction-{0}@{1}/auction"

    def __init__(self, connection, item_id):
        """
        XMPPConnection과 item_id를 받아 경매 초기화

        Args:
            connection: XMPP 연결 객체
            item_id: 경매 아이템 식별자
        """
        # Announcer 초기화 (AuctionEventListener 관리)
        self.auction_event_listeners = Announcer(AuctionEventListener)

        # Chat 생성 및 메시지 변환기 연결
        # Chat 관련 모든 로직이 XMPPAuction 내부로 캡슐화됨
        self.chat = connection.get_chat_manager().create_chat(
            self._auction_id(item_id, connection),
            AuctionMessageTranslator(
                connection.get_user(),
                self.auction_event_listeners.announce()
            )
        )

    @staticmethod
    def _auction_id(item_id, connection):
        """경매 ID 생성"""
        return XMPPAuction.AUCTION_ID_FORMAT.format(
            item_id,
            connection.get_service_name()
        )

    def add_auction_event_listener(self, listener):
        """경매 이벤트 리스너 추가"""
        self.auction_event_listeners.add_listener(listener)

    def join(self):
        """경매 참여"""
        # 구현...
        pass


# Java 원본 - Main에서 Chat 참조 제거 (라인 137-151)
# public class Main { […]
#   private void addUserRequestListenerFor(final XMPPConnection connection) {
#     ui.addUserRequestListener(new UserRequestListener() {
#       public void joinAuction(String itemId) {
#           snipers.addSniper(SniperSnapshot.joining(itemId));
#           Auction auction = new XMPPAuction(connection, itemId);
#           notToBeGCd.add(auction);
# auction.addAuctionEventListener(
#                   new AuctionSniper(itemId, auction,
#                                     new SwingThreadSniperListener(snipers)));
# auction.join();
#       }
#     });
#   }
# }

# Python 버전 - Main에서 Chat 참조 제거
class Main:
    def add_user_request_listener_for(self, connection):
        """Chat 참조 완전 제거 - Auction 추상화만 사용"""
        def join_auction(item_id):
            # 스나이퍼 추가
            self.snipers.add_sniper(SniperSnapshot.joining(item_id))

            # XMPPAuction 생성 (Chat은 내부에 캡슐화됨)
            auction = XMPPAuction(connection, item_id)

            # 가비지 컬렉션 방지 (아직 남아있음)
            self.not_to_be_gcd.add(auction)

            # 이벤트 리스너 추가
            auction.add_auction_event_listener(
                AuctionSniper(
                    item_id,
                    auction,
                    SwingThreadSniperListener(self.snipers)
                )
            )

            # 경매 참여
            auction.join()

        self.ui.add_user_request_listener(join_auction)
```

**통합 테스트 작성:**

```python
# Java 원본 - 통합 테스트 (라인 164-182)
# @Test public void
# receivesEventsFromAuctionServerAfterJoining() throws Exception {
#   CountDownLatch auctionWasClosed = new CountDownLatch(1);
#   Auction auction =  new XMPPAuction(connection, auctionServer.getItemId());
#   auction.addAuctionEventListener(auctionClosedListener(auctionWasClosed));
#   auction.join();
#   server.hasReceivedJoinRequestFrom(ApplicationRunner.SNIPER_XMPP_ID);
#   server.announceClosed();
#   assertTrue("should have been closed", auctionWasClosed.await(2, SECONDS));
# }
# private AuctionEventListener
# auctionClosedListener(final CountDownLatch auctionWasClosed) {
#   return new AuctionEventListener() {
#     public void auctionClosed() { auctionWasClosed.countDown(); }
#     public void currentPrice(int price, int increment, PriceSource priceSource) {
# // not implemented
#     }
#   };
# }

# Python 버전 - 통합 테스트
import unittest
from threading import Event
from datetime import timedelta

class XMPPAuctionTest(unittest.TestCase):
    """XMPPAuction 통합 테스트"""

    def test_receives_events_from_auction_server_after_joining(self):
        """경매 참여 후 서버로부터 이벤트를 받는지 확인"""
        # CountDownLatch 대신 Event 사용
        auction_was_closed = Event()

        # XMPPAuction 생성
        auction = XMPPAuction(
            self.connection,
            self.auction_server.get_item_id()
        )

        # 경매 종료 리스너 추가
        auction.add_auction_event_listener(
            self._auction_closed_listener(auction_was_closed)
        )

        # 경매 참여
        auction.join()

        # 서버가 참여 요청을 받았는지 확인
        self.server.has_received_join_request_from(
            ApplicationRunner.SNIPER_XMPP_ID
        )

        # 서버가 종료 알림
        self.server.announce_closed()

        # 2초 내에 종료 이벤트를 받았는지 확인
        self.assertTrue(
            auction_was_closed.wait(timeout=2),
            "should have been closed"
        )

    def _auction_closed_listener(self, auction_was_closed):
        """경매 종료 리스너 생성"""
        class AuctionClosedListener:
            def auction_closed(self):
                """경매 종료 시 호출"""
                auction_was_closed.set()

            def current_price(self, price, increment, price_source):
                """현재 가격 업데이트 (미구현)"""
                pass

        return AuctionClosedListener()
```

**패키지 재구성:**
- XMPPAuction과 AuctionMessageTranslator를 새로운 `auctionsniper.xmpp` 패키지로 이동
- 테스트도 동등한 xmpp 테스트 패키지로 이동

**생성자에 대한 타협:**
- 생성자에 실제 동작이 포함되는 것에 대한 의구심
- 경험상 복잡한 생성자는 나중에 깨고 싶어지는 가정을 강제함
- 현재는 외부 라이브러리와의 "베니어(veneer)" 코드로 받아들임
- Smack 클래스들이 우리가 피하려는 복잡한 생성자를 가지고 있어 통합 테스트만 가능

---

### 4. Connection 추출하기 (Extracting the Connection)
**참조:** content.md 라인 197-251
**관련 핵심 개념:** Connection 추출

**이전 화제와의 관계:** Chat을 캡슐화한 후, 이제 XMPPConnection 직접 참조를 제거하여 XMPP 의존성을 완전히 격리

**설명:**

Main에서 XMPPConnection에 대한 직접 참조를 제거하고, 주어진 아이템에 대한 Auction 인스턴스를 생성하는 팩토리 클래스로 래핑한다.

**개념 모델링:**
- 경매(auctions)를 관리하는 개념은 "경매장(auction house)"
- 이 도메인 언어를 반영하여 새로운 타입 이름을 AuctionHouse로 결정

```python
# Java 원본 - AuctionHouse 인터페이스 (라인 209-211)
# public interface AuctionHouse {
#   Auction auctionFor(String itemId);
# }

# Python 버전 - AuctionHouse 인터페이스
from abc import ABC, abstractmethod

class AuctionHouse(ABC):
    """경매장 인터페이스 - 경매를 생성하고 관리"""

    @abstractmethod
    def auction_for(self, item_id):
        """
        주어진 아이템 ID에 대한 경매 생성

        Args:
            item_id: 경매 아이템 식별자

        Returns:
            Auction: 생성된 경매 객체
        """
        pass


# Java 원본 - Main 리팩토링 후 (라인 213-232)
# public class Main { […]
#   public static void main(String... args) throws Exception {
#     Main main = new Main();
# XMPPAuctionHouse auctionHouse =
#       XMPPAuctionHouse.connect(
#         args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]);
#     main.disconnectWhenUICloses(auctionHouse);
#     main.addUserRequestListenerFor(auctionHouse);
#   }
#   private void addUserRequestListenerFor(final AuctionHouse auctionHouse) {
#     ui.addUserRequestListener(new UserRequestListener() {
#       public void joinAuction(String itemId) {
#         snipers.addSniper(SniperSnapshot.joining(itemId));
# Auction auction = auctionHouse.auctionFor(itemId);
#         notToBeGCd.add(auction);
# […]
#       }
#     }
#   }
# }

# Python 버전 - Main 리팩토링 후
class Main:
    """애플리케이션 진입점 - XMPP 의존성 제거됨"""

    ARG_HOSTNAME = 0
    ARG_USERNAME = 1
    ARG_PASSWORD = 2

    @staticmethod
    def main(*args):
        """애플리케이션 메인 진입점"""
        main = Main()

        # XMPPAuctionHouse 연결 (팩토리 메서드 사용)
        auction_house = XMPPAuctionHouse.connect(
            args[Main.ARG_HOSTNAME],
            args[Main.ARG_USERNAME],
            args[Main.ARG_PASSWORD]
        )

        # UI 종료 시 연결 해제
        main.disconnect_when_ui_closes(auction_house)

        # 사용자 요청 리스너 추가
        main.add_user_request_listener_for(auction_house)

    def add_user_request_listener_for(self, auction_house):
        """
        AuctionHouse를 사용한 사용자 요청 처리
        XMPPConnection 직접 참조 완전 제거
        """
        def join_auction(item_id):
            # 스나이퍼 추가
            self.snipers.add_sniper(SniperSnapshot.joining(item_id))

            # 팩토리 메서드로 경매 생성
            auction = auction_house.auction_for(item_id)

            # 가비지 컬렉션 방지
            self.not_to_be_gcd.add(auction)

            # 리스너 추가 및 참여
            # [...]

        self.ui.add_user_request_listener(join_auction)


# XMPPAuctionHouse 구현 예시 (본문에 상세 코드는 없지만 구조는 명확함)
class XMPPAuctionHouse:
    """XMPP 기반 경매장 구현"""

    def __init__(self, connection):
        """XMPP 연결을 받아 초기화"""
        self.connection = connection

    @classmethod
    def connect(cls, hostname, username, password):
        """
        XMPP 서버에 연결하여 AuctionHouse 인스턴스 생성

        Args:
            hostname: XMPP 서버 호스트명
            username: 사용자 이름
            password: 비밀번호

        Returns:
            XMPPAuctionHouse: 연결된 경매장 인스턴스
        """
        # XMPP 연결 생성
        connection = # ... XMPP 연결 로직
        return cls(connection)

    def auction_for(self, item_id):
        """
        아이템 ID에 대한 경매 생성

        Args:
            item_id: 경매 아이템 식별자

        Returns:
            XMPPAuction: 생성된 경매 객체
        """
        return XMPPAuction(self.connection, item_id)

    def disconnect(self):
        """XMPP 연결 해제"""
        self.connection.disconnect()
```

**효과:**
- Main이 더욱 단순해짐
- XMPP 관련 모든 import가 하나로 통합: `auctionsniper.xmpp.XMPPAuctionHouse`
- 통합 테스트도 XMPPAuctionHouse를 사용하도록 개선
- 관련 상수들을 적절한 위치로 이동:
  - 메시지 포맷 → XMPPAuction
  - 연결 식별자 포맷 → XMPPAuctionHouse
- 상수의 사용 범위가 좁아져 올바른 방향으로 가고 있음을 확인

---

### 5. SnipersTableModel 추출하기 - SniperLauncher (Sniper Launcher)
**참조:** content.md 라인 252-356
**관련 핵심 개념:** SniperLauncher 추출

**이전 화제와의 관계:** XMPP 의존성을 제거한 후, 이제 UI(SnipersTableModel, SwingThreadSniperListener) 직접 참조와 notToBeGCd 문제 해결

**설명:**

SnipersTableModel에 대한 직접 참조와 관련된 SwingThreadSniperListener, 그리고 끔찍한 notToBeGCd를 제거하기 위해 여러 단계를 거친다.

**첫 번째 단계: 익명 클래스를 SniperLauncher로 추출**

```python
# Java 원본 - SniperLauncher (라인 262-279)
# public class SniperLauncher implements UserRequestListener {
#   private final ArrayList<Auction> notToBeGCd = new ArrayList<Auction>();
#   private final AuctionHouse auctionHouse;
#   private final SnipersTableModel snipers;
#   public SniperLauncher(AuctionHouse auctionHouse, SnipersTableModel snipers) {
# // set the fields
#   }
#   public void joinAuction(String itemId) {
# snipers.addSniper(SniperSnapshot.joining(itemId));
#       Auction auction = auctionHouse.auctionFor(itemId);
#       notToBeGCd.add(auction);
#       AuctionSniper sniper =
#         new AuctionSniper(itemId, auction,
#                           new SwingThreadSniperListener(snipers));
#       auction.addAuctionEventListener(snipers);
#       auction.join();
#   }
# }

# Python 버전 - SniperLauncher 첫 번째 버전
class SniperLauncher:
    """
    경매 참여 요청에 응답하여 Sniper를 '론칭'하는 클래스
    notToBeGCd를 클래스 로컬로 이동
    """

    def __init__(self, auction_house, snipers):
        """
        Args:
            auction_house: 경매장 인터페이스
            snipers: SnipersTableModel (아직 직접 의존)
        """
        self.not_to_be_gcd = []  # 가비지 컬렉션 방지 리스트
        self.auction_house = auction_house
        self.snipers = snipers

    def join_auction(self, item_id):
        """
        경매 참여 처리

        문제점:
        - snipers 사용이 어색함 (초기 스냅샷 추가, Sniper와 auction 모두에 연결)
        - 초기 SniperSnapshot 중복 생성 (여기와 AuctionSniper 생성자에서)
        """
        # 초기 스냅샷으로 스나이퍼 추가
        self.snipers.add_sniper(SniperSnapshot.joining(item_id))

        # 경매 생성
        auction = self.auction_house.auction_for(item_id)

        # 가비지 컬렉션 방지
        self.not_to_be_gcd.add(auction)

        # AuctionSniper 생성 (Swing 리스너 포함)
        sniper = AuctionSniper(
            item_id,
            auction,
            SwingThreadSniperListener(self.snipers)
        )

        # 이벤트 리스너로 등록
        auction.add_auction_event_listener(sniper)

        # 경매 참여
        auction.join()
```

**문제점 분석:**
- `snipers` (SnipersTableModel) 사용이 어색함
  - 초기 SniperSnapshot을 제공하여 새 Sniper를 알림
  - Sniper와 auction 모두에 연결
- 초기 SniperSnapshot 생성의 숨겨진 중복
  - 여기서 한 번, AuctionSniper 생성자에서 한 번

**두 번째 단계: SniperCollector 도입**

```python
# Java 원본 - SniperCollector 도입 후 (라인 294-305)
# public static class SniperLauncher implements UserRequestListener {
#   private final AuctionHouse auctionHouse;
#   private final SniperCollector collector;
# […]
#   public void joinAuction(String itemId) {
#       Auction auction = auctionHouse.auctionFor(itemId);
# AuctionSniper sniper = new AuctionSniper(itemId, auction);
#       auction.addAuctionEventListener(sniper);
# collector.addSniper(sniper);
#       auction.join();
#   }
# }

# Python 버전 - SniperCollector 도입 후
from abc import ABC, abstractmethod

class SniperCollector(ABC):
    """Sniper를 애플리케이션에 수용하는 역할"""

    @abstractmethod
    def add_sniper(self, sniper):
        """새로운 Sniper를 컬렉션에 추가"""
        pass


class SniperLauncher:
    """
    경매 참여 요청에 응답하여 Sniper를 '론칭'하는 클래스
    SniperCollector로 책임 분리
    """

    def __init__(self, auction_house, collector):
        """
        Args:
            auction_house: 경매장 인터페이스
            collector: SniperCollector 구현체
        """
        self.auction_house = auction_house
        self.collector = collector

    def join_auction(self, item_id):
        """
        경매 참여 처리 - 단순화됨

        개선점:
        - AuctionSniper 생성에만 집중
        - Swing 관련 로직 제거
        - SniperCollector에게 수용 프로세스 위임
        """
        # 경매 생성
        auction = self.auction_house.auction_for(item_id)

        # AuctionSniper 생성 (Swing 리스너 제거됨)
        sniper = AuctionSniper(item_id, auction)

        # 이벤트 리스너로 등록
        auction.add_auction_event_listener(sniper)

        # SniperCollector에게 추가 위임
        self.collector.add_sniper(sniper)

        # 경매 참여
        auction.join()
```

**테스트 작성:**

```python
# Java 원본 - SniperLauncherTest (라인 309-326)
# public class SniperLauncherTest {
#   private final States auctionState = context.states("auction state")
# .startsAs("not joined");
# […]
#   @Test public void
# addsNewSniperToCollectorAndThenJoinsAuction() {
#     final String itemId = "item 123";
#     context.checking(new Expectations() {{
#       allowing(auctionHouse).auctionFor(itemId); will(returnValue(auction));
#       oneOf(auction).addAuctionEventListener(with(sniperForItem(itemId)));
# when(auctionState.is("not joined"));
#       oneOf(sniperCollector).addSniper(with(sniperForItem(item)));
# when(auctionState.is("not joined"));
#       one(auction).join(); then(auctionState.is("joined"));
#     }});
#     launcher.joinAuction(itemId);
#   }
# }

# Python 버전 - SniperLauncherTest
import unittest
from unittest.mock import Mock, call

class SniperLauncherTest(unittest.TestCase):
    """SniperLauncher 테스트 - 순서 검증 포함"""

    def setUp(self):
        """테스트 설정"""
        self.auction_house = Mock()
        self.auction = Mock()
        self.sniper_collector = Mock()

        # auction_house.auction_for()가 auction을 반환하도록 설정
        self.auction_house.auction_for.return_value = self.auction

        self.launcher = SniperLauncher(
            self.auction_house,
            self.sniper_collector
        )

    def test_adds_new_sniper_to_collector_and_then_joins_auction(self):
        """
        새 Sniper를 컬렉터에 추가한 후 경매에 참여하는지 확인

        중요: 모든 것이 설정된 후에만 경매에 참여해야 함
        """
        item_id = "item 123"

        # 경매 참여 실행
        self.launcher.join_auction(item_id)

        # 호출 순서 검증
        # 1. auction_house.auction_for() 호출
        self.auction_house.auction_for.assert_called_with(item_id)

        # 2. auction.add_auction_event_listener() 호출
        #    (Sniper가 해당 item_id를 가지는지 확인)
        listener_call = self.auction.add_auction_event_listener.call_args
        self.assertEqual(listener_call[0][0].item_id, item_id)

        # 3. collector.add_sniper() 호출
        collector_call = self.sniper_collector.add_sniper.call_args
        self.assertEqual(collector_call[0][0].item_id, item_id)

        # 4. 마지막으로 auction.join() 호출
        self.auction.join.assert_called_once()

        # 호출 순서 확인 (Python mock의 mock_calls 사용)
        expected_calls = [
            ('auction_for', (item_id,), {}),
            # add_auction_event_listener와 add_sniper의 상대 순서는
            # 실제로는 중요하지 않을 수 있지만, join()은 마지막이어야 함
        ]
```

**SnipersTableModel 확장:**

```python
# Java 원본 - SnipersTableModel 확장 (라인 339-353)
# public class SnipersTableModel extends AbstractTableModel
#     implements SniperListener, SniperCollector
# {
#   private final ArrayList<AuctionSniper> notToBeGCd = […]
#   public void addSniper(AuctionSniper sniper) {
#     notToBeGCd.add(sniper);
#     addSniperSnapshot(sniper.getSnapshot());
#     sniper.addSniperListener(new SwingThreadSniperListener(this));
#   }
#   private void addSniperSnapshot(SniperSnapshot sniperSnapshot) {
#     snapshots.add(sniperSnapshot);
#     int row = snapshots.size() - 1;
#     fireTableRowsInserted(row, row);
#    }
# }

# Python 버전 - SnipersTableModel 확장
from javax.swing.table import AbstractTableModel

class SnipersTableModel(AbstractTableModel, SniperCollector):
    """
    Sniper 테이블 모델 - SniperCollector 역할 추가

    변경사항:
    - SniperSnapshot 대신 AuctionSniper를 받음
    - Sniper의 리스너를 의존성에서 알림으로 변경
    - SwingThreadSniperListener를 내부로 캡슐화
    """

    def __init__(self):
        super().__init__()
        self.not_to_be_gcd = []  # Sniper 참조 유지
        self.snapshots = []

    def add_sniper(self, sniper):
        """
        새로운 AuctionSniper 추가 (SniperCollector 구현)

        Args:
            sniper: AuctionSniper 인스턴스
        """
        # 가비지 컬렉션 방지
        self.not_to_be_gcd.append(sniper)

        # 스냅샷 추가
        self._add_sniper_snapshot(sniper.get_snapshot())

        # Swing 스레드 리스너 추가 (내부 캡슐화)
        sniper.add_sniper_listener(SwingThreadSniperListener(self))

    def _add_sniper_snapshot(self, sniper_snapshot):
        """
        SniperSnapshot을 내부 리스트에 추가하고 테이블 업데이트

        Args:
            sniper_snapshot: 추가할 스냅샷
        """
        self.snapshots.append(sniper_snapshot)
        row = len(self.snapshots) - 1
        self.fire_table_rows_inserted(row, row)

    # AbstractTableModel 메서드들...
    def get_row_count(self):
        return len(self.snapshots)

    # 기타 테이블 모델 메서드들...
```

**개선점:**
- SwingThreadSniperListener가 이제 Swing 부분의 코드로 패키징됨
- 일반적인 SniperLauncher에 포함되지 않음
- 올바른 방향으로 가고 있다는 신호

---

### 6. SnipersTableModel 추출하기 - SniperPortfolio (Sniper Portfolio)
**참조:** content.md 라인 357-413
**관련 핵심 개념:** SniperPortfolio 추출

**이전 화제와의 관계:** SniperLauncher를 추출한 후, 이제 모든 스나이핑 활동을 나타내는 포트폴리오 개념 도입

**설명:**

현재 SnipersTableModel이 암시적으로 두 가지 책임을 가지고 있다:
1. 스나이핑 기록 유지
2. 그 기록 표시

또한 Swing 구현 세부사항을 Main으로 끌어들인다.

**해결책: SniperPortfolio 추출**

```python
# Java 원본 - PortfolioListener 인터페이스 (라인 368-370)
# public interface PortfolioListener extends EventListener {
#   void sniperAdded(AuctionSniper sniper);
# }

# Python 버전 - PortfolioListener 인터페이스
from abc import ABC, abstractmethod

class PortfolioListener(ABC):
    """
    포트폴리오 변경 이벤트를 수신하는 리스너
    Sniper 추가/제거 시 알림 받음
    """

    @abstractmethod
    def sniper_added(self, sniper):
        """
        새로운 Sniper가 포트폴리오에 추가될 때 호출

        Args:
            sniper: 추가된 AuctionSniper
        """
        pass


# Java 원본 - MainWindow 수정 (라인 371-379)
# public class MainWindow extends JFrame {
#   private JTable makeSnipersTable(SniperPortfolio portfolio) {
# SnipersTableModel model = new SnipersTableModel();
#     portfolio.addPortfolioListener(model);
#     JTable snipersTable = new JTable(model);
#     snipersTable.setName(SNIPERS_TABLE_NAME);
#     return snipersTable;
#   }
# }

# Python 버전 - MainWindow 수정
from javax.swing import JFrame, JTable

class MainWindow(JFrame):
    """
    메인 윈도우 - SnipersTableModel 생성을 내부로 이동
    SniperPortfolio를 통해 느슨하게 결합
    """

    SNIPERS_TABLE_NAME = "Snipers Table"

    def __init__(self, portfolio):
        """
        Args:
            portfolio: SniperPortfolio 인스턴스
        """
        super().__init__()
        self.snipers_table = self._make_snipers_table(portfolio)
        # UI 구성...

    def _make_snipers_table(self, portfolio):
        """
        스나이퍼 테이블 생성

        Args:
            portfolio: SniperPortfolio (이벤트 소스)

        Returns:
            JTable: 생성된 테이블
        """
        # SnipersTableModel 생성 (MainWindow 내부에서)
        model = SnipersTableModel()

        # 포트폴리오의 리스너로 등록
        portfolio.add_portfolio_listener(model)

        # JTable 생성 및 설정
        snipers_table = JTable(model)
        snipers_table.set_name(self.SNIPERS_TABLE_NAME)

        return snipers_table


# SniperPortfolio 구현 (본문에 완전한 코드는 없지만 구조 추론 가능)
class SniperPortfolio:
    """
    모든 스나이핑 활동을 나타내는 포트폴리오
    SniperCollector 구현
    """

    def __init__(self):
        """포트폴리오 초기화"""
        self.snipers = []
        self.listeners = []

    def add_portfolio_listener(self, listener):
        """
        포트폴리오 리스너 추가

        Args:
            listener: PortfolioListener 구현체
        """
        self.listeners.append(listener)

    def add_sniper(self, sniper):
        """
        새로운 Sniper를 포트폴리오에 추가 (SniperCollector 구현)

        Args:
            sniper: AuctionSniper 인스턴스
        """
        # Sniper 저장 (notToBeGCd 역할도 함)
        self.snipers.append(sniper)

        # 모든 리스너에게 알림
        for listener in self.listeners:
            listener.sniper_added(sniper)


# Java 원본 - Main 최종 형태 (라인 386-398)
# public class Main {  […]
#   private final SniperPortfolio portfolio = new SniperPortfolio();
#   public Main() throws Exception {
#     SwingUtilities.invokeAndWait(new Runnable() {
#       public void run() {
#         ui = new MainWindow(portfolio);
#       }
#     });
#   }
#   private void addUserRequestListenerFor(final AuctionHouse auctionHouse) {
#     ui.addUserRequestListener(new SniperLauncher(auctionHouse, portfolio));
#   }
# }

# Python 버전 - Main 최종 형태
from javax.swing import SwingUtilities

class Main:
    """
    애플리케이션 최상위 클래스 - 매우 단순해짐

    역할:
    - UI와 Sniper 생성을 포트폴리오를 통해 연결
    - 더 이상 XMPP나 Swing 세부사항을 직접 다루지 않음
    """

    def __init__(self):
        """Main 초기화 - Swing 스레드에서 UI 생성"""
        self.portfolio = SniperPortfolio()

        # Swing EDT에서 UI 생성
        def create_ui():
            self.ui = MainWindow(self.portfolio)

        SwingUtilities.invoke_and_wait(create_ui)

    def add_user_request_listener_for(self, auction_house):
        """
        사용자 요청 리스너 추가

        Args:
            auction_house: AuctionHouse 인터페이스
        """
        # SniperLauncher를 리스너로 등록
        # 포트폴리오가 SniperCollector 역할 수행
        self.ui.add_user_request_listener(
            SniperLauncher(auction_house, self.portfolio)
        )

    @staticmethod
    def main(*args):
        """애플리케이션 진입점"""
        main = Main()

        # XMPPAuctionHouse 연결
        auction_house = XMPPAuctionHouse.connect(
            args[Main.ARG_HOSTNAME],
            args[Main.ARG_USERNAME],
            args[Main.ARG_PASSWORD]
        )

        main.disconnect_when_ui_closes(auction_house)
        main.add_user_request_listener_for(auction_house)
```

**주요 개선사항:**
1. SniperPortfolio가 모든 Sniper 목록을 유지하므로 **notToBeGCd를 완전히 제거**
2. 최상위 코드가 매우 단순해짐: UI와 Sniper 생성을 포트폴리오를 통해 연결
3. 세 개의 컴포넌트로 코드 분리:
   - 핵심 애플리케이션 (auctionsniper 패키지)
   - XMPP 통신 (auctionsniper.xmpp 패키지)
   - Swing 표시 (auctionsniper.ui 패키지)

**최종 아키텍처:** Figure 17.3 - SniperPortfolio를 포함한 구조

---

### 7. 관찰과 성찰 (Observations)
**참조:** content.md 라인 414-489
**관련 핵심 개념:** 포트와 어댑터 아키텍처, 점진적 리팩토링

**이전 화제와의 관계:** 전체 리팩토링 과정의 의미와 교훈을 정리

**설명:**

#### 점진적 아키텍처 (Incremental Architecture)

Main의 재구조화는 애플리케이션 개발의 핵심 순간이다. Figure 17.5에서 보듯이, 이제 "포트와 어댑터" 아키텍처와 일치하는 구조를 가지게 되었다.

**아키텍처 계층:**
1. **핵심 도메인 코드** (예: AuctionSniper)
2. **브리징 코드** (예: SnipersTableModel) - 기술 코드를 구동하거나 응답
3. **기술 코드** (예: JTable)

**핵심 특징:**
- 도메인 코드는 외부 인프라에 대한 참조가 전혀 없음
- auctionsniper 패키지가 자체 완결적 언어를 사용하여 경매 스나이핑 비즈니스 모델 정의
- Main은 진입점이자 도메인 모델과 인프라를 연결하는 유일한 예외

**중요한 점:**
- 이 설계에 **점진적으로** 도달했다는 것
- 기능을 추가하고 경험적 규칙(heuristics)을 반복 적용하여 도달
- 경험을 바탕으로 결정을 내리지만, 코드를 따라가고 깔끔하게 유지하는 것만으로 거의 자동적으로 해결책에 도달

```
포트와 어댑터 아키텍처 구조:

┌─────────────────────────────────────────────────────┐
│                     Main                             │ 진입점
│  (도메인 모델 ↔ 인프라 연결)                          │
└───────────────┬─────────────────────┬───────────────┘
                │                     │
    ┌───────────▼──────────┐  ┌──────▼──────────────┐
    │  XMPP 어댑터         │  │  Swing 어댑터        │ 어댑터 계층
    │  (XMPPAuctionHouse)  │  │  (MainWindow)        │
    │  (XMPPAuction)       │  │  (SnipersTableModel) │
    └───────────┬──────────┘  └──────┬──────────────┘
                │                     │
    ┌───────────▼─────────────────────▼───────────────┐
    │            핵심 도메인 모델                       │ 도메인 계층
    │  (AuctionSniper, SniperPortfolio,               │
    │   SniperLauncher, Auction 인터페이스)            │
    └──────────────────────────────────────────────────┘
                │                     │
    ┌───────────▼──────────┐  ┌──────▼──────────────┐
    │  XMPP 기술           │  │  Swing 기술          │ 외부 인프라
    │  (Smack)             │  │  (JTable, JFrame)    │
    └──────────────────────┘  └──────────────────────┘
```

#### 삼점 접촉 (Three-Point Contact)

리팩토링을 상세히 기술한 이유:
1. 과정 중 핵심 포인트를 보여주기 위해
2. 중요한 리팩토링을 점진적으로 수행할 수 있음을 보여주기 위해

**전략:**
- 다음에 무엇을 해야 할지 또는 어떻게 도달할지 확신이 없을 때
- **개별 변경의 규모를 축소**하는 것이 한 가지 대처 방법
- 코드의 로컬 문제를 반복적으로 수정
- 작동하는 코드에서 몇 분 이상 벗어나지 않으면서 설계를 안전하게 탐색
- 일반적으로 이것만으로도 더 나은 설계로 이끌기에 충분
- 잘 되지 않으면 언제든 되돌아가서 다른 경로를 선택 가능

**암벽 등반 규칙: "삼점 접촉"**
- 훈련된 등반가는 한 번에 하나의 팔다리만 움직임 (손 또는 발)
- 추락 위험을 최소화
- 각 이동은 최소한이고 안전하지만, 충분히 조합하면 루트의 정상에 도달

```python
# 삼점 접촉 리팩토링 예시

# 상태 1: 안정 (세 점 고정)
class Main:
    def join_auction(self, connection, item_id):
        chat = connection.create_chat()  # 고정점 1
        auction = XMPPAuction(chat)      # 고정점 2
        sniper = AuctionSniper()          # 고정점 3
        # 모든 것이 안정적

# 상태 2: 한 점 이동 (Announcer 도입)
class Main:
    def join_auction(self, connection, item_id):
        chat = connection.create_chat()       # 고정점 1
        announcer = Announcer()               # 이동 중 (새로운 점)
        auction = XMPPAuction(chat)           # 고정점 2
        sniper = AuctionSniper()              # 고정점 3
        # 다시 안정화

# 상태 3: 다른 점 이동 (Chat을 XMPPAuction으로)
class XMPPAuction:
    def __init__(self, connection, item_id):
        self.chat = connection.create_chat()  # 이동 중 (내부로)
        self.announcer = Announcer()          # 이동 중 (내부로)
        # Main에서 Chat 참조 제거됨
        # 다시 안정화

# 각 단계마다:
# - 하나의 작은 변경만 수행
# - 테스트 실행하여 안정성 확인
# - 다음 변경으로 이동
```

**실제 소요 시간:**
- 이 리팩토링은 읽는 시간보다 크게 오래 걸리지 않음
- 관심사의 명확한 분리를 위한 좋은 투자 수익
- 경험을 쌓으면 코드의 결함선(fault lines)을 인식하여 더 직접적인 경로를 택할 수 있음

#### 동적 설계와 정적 설계 (Dynamic as Well as Static Design)

**작은 실수 사례:**
- Steve가 SniperPortfolio를 추출하는 중 막힘
- `sniperAdded()` 메서드가 Swing 스레드 내에서 호출되도록 보장하려 함
- 결국 이벤트가 버튼 클릭으로 트리거되므로 이미 커버되어 있음을 깨달음

**교훈:**
- 리팩토링할 때 여러 관점을 고려해야 함
- 리팩토링은 설계 활동이므로 배운 모든 기술이 필요
- 예전에는 주기적으로 필요했지만 이제는 항상 필요
- 리팩토링은 정적 구조(클래스와 인터페이스)에 집중하지만
- 애플리케이션의 동적 구조(인스턴스와 스레드)를 잊기 쉬움
- 때로는 뒤로 물러나서 상호작용 다이어그램 등을 그려야 함

```
상호작용 다이어그램 예시 (Figure 17.6):

사용자 → UI → SniperLauncher → AuctionHouse → XMPPAuction
                      ↓              ↓              ↓
                SniperPortfolio    Auction      Chat (Smack)
                      ↓
               SnipersTableModel
                      ↓
                   JTable (Swing 스레드에서 실행)

스레드 분석:
1. 사용자 클릭 → Swing EDT (Event Dispatch Thread)
2. SniperLauncher.joinAuction() → 이미 Swing EDT 내부
3. SniperPortfolio.addSniper() → Swing EDT 내부
4. SnipersTableModel 업데이트 → Swing EDT 내부 (안전함)
```

#### notToBeGCd의 대안 수정 방법

**우리의 선택:**
- SniperPortfolio가 참조를 보유하는 것에 의존
- 실제로는 그럴 가능성이 높지만, 변경되면 추적하기 어려운 일시적 실패 발생 가능
- XMPP 코드의 문제를 애플리케이션의 부수 효과에 의존하여 해결

**대안:**
- Smack 문제이므로 XMPP 계층에서 처리해야 한다고 볼 수 있음
- XMPPAuctionHouse가 생성한 XMPPAuction을 보유
- Auction이 완료되었음을 알려주는 수명주기 리스너 추가 필요
- 그러면 해당 Auction을 해제 가능

**결론:**
- 명확한 선택은 없음
- 상황을 살펴보고 판단력을 발휘해야 함

```python
# 대안 1: 우리의 선택 (SniperPortfolio가 보유)
class SniperPortfolio:
    def __init__(self):
        self.snipers = []  # Sniper와 간접적으로 Auction 참조 유지

    def add_sniper(self, sniper):
        self.snipers.append(sniper)  # GC 방지

# 장점: 단순함
# 단점: XMPP 문제를 애플리케이션 로직에 의존하여 해결


# 대안 2: XMPPAuctionHouse가 보유
class XMPPAuctionHouse:
    def __init__(self, connection):
        self.connection = connection
        self.active_auctions = []  # Auction 참조 명시적 유지

    def auction_for(self, item_id):
        auction = XMPPAuction(self.connection, item_id)
        auction.add_lifecycle_listener(self)  # 수명주기 추적
        self.active_auctions.append(auction)
        return auction

    def auction_completed(self, auction):
        """Auction 완료 시 호출되는 리스너"""
        self.active_auctions.remove(auction)  # 참조 해제

# 장점: XMPP 계층에서 XMPP 문제 해결
# 단점: 수명주기 관리 복잡성 증가
```

**판단 기준:**
- 각 접근법의 장단점 평가
- 프로젝트의 특성과 요구사항 고려
- 팀의 경험과 선호도 반영
- 유지보수성과 명확성 사이의 균형

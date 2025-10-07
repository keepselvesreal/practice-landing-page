# 첫 번째 테스트 통과시키기

## 압축 내용

테스트 인프라(ApplicationRunner, FakeAuctionServer)를 먼저 구축하고, 최소 기능만 가진 애플리케이션을 점진적으로 만들어가며 첫 번째 종단간 테스트를 통과시키는 과정을 통해 워킹 스켈레톤의 핵심인 '필요한 최소한'의 원칙을 실천한다.

## 핵심 내용

### 핵심 개념들

1. **테스트 인프라 우선 구축** (→ 상세 내용 1, 2, 3 참조)
   - 실제 애플리케이션보다 테스트를 먼저 작성하여 시스템 구조 검증
   - ApplicationRunner로 GUI 애플리케이션 제어
   - FakeAuctionServer로 XMPP 메시지 통신 시뮬레이션

2. **점진적 실패 수정** (→ 상세 내용 4 참조)
   - 각 테스트 실패마다 최소한의 코드만 추가
   - 증상을 하나씩 수정하며 앞으로 전진
   - 작은 단계들이 예측 가능한 진행을 만듦

3. **필요한 최소한(Necessary Minimum)** (→ 상세 내용 5 참조)
   - 종단간 시스템 구조를 설계하고 검증하는 것이 목표
   - 메시지 내용보다 통신과 이벤트 처리가 작동하는지 확인
   - 배포 환경까지 포함한 초기 구조 검증

### 핵심 개념 간 관계

```
테스트 인프라 우선 구축
    ↓
점진적 실패 수정 (테스트 주도)
    ↓
필요한 최소한의 기능 구현
    ↓
워킹 스켈레톤 완성
```

- **테스트 인프라**는 **점진적 실패 수정**의 기반을 제공
- **점진적 실패 수정**은 **필요한 최소한** 원칙을 실천하는 방법
- 세 개념 모두 첫 번째 종단간 테스트를 통과시키는 목표에 수렴

## 상세 내용

### 화제 목차

1. 테스트 리그 구축 (Building the Test Rig)
2. 애플리케이션 러너 (The Application Runner)
3. 가짜 경매 서버 (The Fake Auction)
4. 테스트 실패와 통과 (Failing and Passing the Test)
5. 필요한 최소한 (The Necessary Minimum)

---

### 1. 테스트 리그 구축

**참조**: content.md 10-42행

**설명**: 테스트 시작 시 Openfire 서버를 시작하고 Sniper와 경매용 계정을 생성한 후 테스트를 실행하는 구조 설명 (→ **핵심 개념 1: 테스트 인프라 우선 구축** 참조)

**주요 구성 요소**:
- ApplicationRunner: Swing 애플리케이션 관리 및 제어
- FakeAuctionServer: XMPP 메시지 테스트를 위한 대체 서버

**Openfire 서버 설정**:
```python
# 테스트용 계정 설정 예시 (원본: 22-27행)
accounts = {
    "sniper": "sniper",
    "auction-item-54321": "auction",
    "auction-item-65432": "auction"
}

# 서버 설정
system_name = "localhost"
resource_policy = "Never kick"  # 충돌 시 새 리소스 로그인 불허
offline_messages = False  # 영구 상태 없음
```

---

### 2. 애플리케이션 러너

**참조**: content.md 36-135행

**이전 화제와의 관계**: 테스트 리그의 첫 번째 구성 요소인 ApplicationRunner 상세 구현

**설명**: WindowLicker 프레임워크를 활용해 Swing GUI를 제어하고 애플리케이션 상태를 쿼리하는 래퍼 객체 (→ **핵심 개념 1: 테스트 인프라 우선 구축** 참조)

**ApplicationRunner 구현**:
```java
// 원본: 51-78행
public class ApplicationRunner {
    public static final String SNIPER_ID = "sniper";
    public static final String SNIPER_PASSWORD = "sniper";
    private AuctionSniperDriver driver;

    public void startBiddingIn(final FakeAuctionServer auction) {
        // 1. 새 스레드에서 애플리케이션 시작
        Thread thread = new Thread("Test Application") {
            @Override public void run() {
                try {
                    // main() 함수 호출로 조립 확인
                    Main.main(XMPP_HOSTNAME, SNIPER_ID, SNIPER_PASSWORD,
                             auction.getItemId());
                } catch (Exception e) {
                    // 예외 출력, 테스트는 실패하고 스택 추적 확인 가능
                    e.printStackTrace();
                }
            }
        };
        thread.setDaemon(true);
        thread.start();

        // 4. 타임아웃 기간 축소 (1초)
        driver = new AuctionSniperDriver(1000);

        // 5. Joining 상태 대기 - 연결 시도 확인
        driver.showsSniperStatus(STATUS_JOINING);
    }

    // 6. Lost 상태 표시 확인
    public void showsSniperHasLostAuction() {
        driver.showsSniperStatus(STATUS_LOST);
    }

    // 7. 윈도우 정리
    public void stop() {
        if (driver != null) {
            driver.dispose();
        }
    }
}
```

**Python 버전**:
```python
# ApplicationRunner의 Python 버전
import threading
from typing import Optional

class ApplicationRunner:
    SNIPER_ID = "sniper"
    SNIPER_PASSWORD = "sniper"

    def __init__(self):
        self.driver: Optional[AuctionSniperDriver] = None

    def start_bidding_in(self, auction: 'FakeAuctionServer') -> None:
        """경매 입찰 시작"""
        def run_application():
            try:
                # main() 함수 호출로 애플리케이션 시작
                main(XMPP_HOSTNAME, self.SNIPER_ID, self.SNIPER_PASSWORD,
                     auction.get_item_id())
            except Exception as e:
                print(f"Error in application: {e}")

        # 데몬 스레드로 시작
        thread = threading.Thread(target=run_application,
                                 name="Test Application",
                                 daemon=True)
        thread.start()

        # 드라이버 생성 (1초 타임아웃)
        self.driver = AuctionSniperDriver(timeout_millis=1000)

        # Joining 상태 확인
        self.driver.shows_sniper_status(STATUS_JOINING)

    def shows_sniper_has_lost_auction(self) -> None:
        """Sniper가 경매에서 졌음을 표시"""
        self.driver.shows_sniper_status(STATUS_LOST)

    def stop(self) -> None:
        """애플리케이션 정리"""
        if self.driver:
            self.driver.dispose()
```

**AuctionSniperDriver 구현**:
```java
// 원본: 120-132행
public class AuctionSniperDriver extends JFrameDriver {
    public AuctionSniperDriver(int timeoutMillis) {
        super(new GesturePerformer(),
              JFrameDriver.topLevelFrame(
                named(Main.MAIN_WINDOW_NAME),
                showingOnScreen()),
              new AWTEventQueueProber(timeoutMillis, 100));
    }

    // 주어진 상태 텍스트를 보여주는 레이블 확인
    public void showsSniperStatus(String statusText) {
        new JLabelDriver(
            this, named(Main.SNIPER_STATUS_NAME)
        ).hasText(equalTo(statusText));
    }
}
```

**주요 포인트**:
- WindowLicker가 동일 JVM 내 Swing 컴포넌트 제어
- ComponentDriver가 컴포넌트를 못 찾으면 타임아웃 에러 발생
- 이상적으로는 새 프로세스에서 시작하지만, 테스트를 위해 새 스레드 사용

---

### 3. 가짜 경매 서버

**참조**: content.md 142-265행

**이전 화제와의 관계**: 테스트 리그의 두 번째 구성 요소인 FakeAuctionServer 상세 구현

**설명**: XMPP 메시지를 통해 Auction Sniper가 경매와 어떻게 상호작용하는지 확인하는 대체 서버 (→ **핵심 개념 1: 테스트 인프라 우선 구축** 참조)

**세 가지 책임**:
1. XMPP 브로커에 연결하고 Sniper의 채팅 참여 요청 수락
2. Sniper로부터 채팅 메시지 수신 또는 타임아웃 시 실패
3. Southabee's On-Line 규격에 따라 Sniper에게 메시지 전송 허용

**Smack 객체와 콜백 구조**:
```
XMPPConnection
    ↓ (getChatManager)
ChatManager
    ↓ (addChatListener)
ChatManagerListener → chatCreated() 콜백
    ↓ (채팅 세션 생성 시)
Chat
    ↓ (addMessageListener)
MessageListener → processMessage() 콜백
```

**FakeAuctionServer 구현 (1단계)**:
```java
// 원본: 166-192행
public class FakeAuctionServer {
    public static final String ITEM_ID_AS_LOGIN = "auction-%s";
    public static final String AUCTION_RESOURCE = "Auction";
    public static final String XMPP_HOSTNAME = "localhost";
    private static final String AUCTION_PASSWORD = "auction";

    private final String itemId;
    private final XMPPConnection connection;
    private Chat currentChat;  // 테스트용이므로 단일 채팅만 관리

    public FakeAuctionServer(String itemId) {
        this.itemId = itemId;
        this.connection = new XMPPConnection(XMPP_HOSTNAME);
    }

    public void startSellingItem() throws XMPPException {
        connection.connect();
        connection.login(format(ITEM_ID_AS_LOGIN, itemId),
                         AUCTION_PASSWORD, AUCTION_RESOURCE);

        // ChatManagerListener 등록
        connection.getChatManager().addChatListener(
            new ChatManagerListener() {
                public void chatCreated(Chat chat, boolean createdLocally) {
                    currentChat = chat;  // 채팅 세션 보관
                }
            });
    }

    public String getItemId() {
        return itemId;
    }
}
```

**Python 버전**:
```python
# FakeAuctionServer의 Python 버전 (1단계)
from typing import Optional

class FakeAuctionServer:
    ITEM_ID_AS_LOGIN = "auction-{}"
    AUCTION_RESOURCE = "Auction"
    XMPP_HOSTNAME = "localhost"
    AUCTION_PASSWORD = "auction"

    def __init__(self, item_id: str):
        self.item_id = item_id
        self.connection = XMPPConnection(self.XMPP_HOSTNAME)
        self.current_chat: Optional[Chat] = None

    def start_selling_item(self) -> None:
        """경매 아이템 판매 시작"""
        # XMPP 브로커 연결
        self.connection.connect()
        self.connection.login(
            self.ITEM_ID_AS_LOGIN.format(self.item_id),
            self.AUCTION_PASSWORD,
            self.AUCTION_RESOURCE
        )

        # 채팅 리스너 등록
        def on_chat_created(chat: Chat, created_locally: bool) -> None:
            self.current_chat = chat

        self.connection.get_chat_manager().add_chat_listener(on_chat_created)

    def get_item_id(self) -> str:
        return self.item_id
```

**최소 가짜 구현의 특징**:
- 실제 경매 서버는 여러 입찰자를 위한 다중 채팅 관리 필요
- 가짜는 테스트 지원만이 목적이므로 단일 채팅만 필요
- 단순성이 핵심 (→ **핵심 개념 3: 필요한 최소한** 참조)

**FakeAuctionServer 구현 (2단계 - 메시지 처리)**:
```java
// 원본: 210-243행
public class FakeAuctionServer {
    private final SingleMessageListener messageListener =
        new SingleMessageListener();

    public void startSellingItem() throws XMPPException {
        connection.connect();
        connection.login(format(ITEM_ID_AS_LOGIN, itemId),
                         AUCTION_PASSWORD, AUCTION_RESOURCE);
        connection.getChatManager().addChatListener(
            new ChatManagerListener() {
                public void chatCreated(Chat chat, boolean createdLocally) {
                    currentChat = chat;
                    // MessageListener 추가
                    chat.addMessageListener(messageListener);
                }
            });
    }

    // 1. Join 메시지 도착 확인 (5초 내)
    public void hasReceivedJoinRequestFromSniper()
        throws InterruptedException {
        messageListener.receivesAMessage();
    }

    // 2. 경매 종료 알림
    public void announceClosed() throws XMPPException {
        currentChat.sendMessage(new Message());  // 빈 메시지
    }

    // 3. 연결 종료
    public void stop() {
        connection.disconnect();
    }
}

// SingleMessageListener: 단일 메시지 처리 헬퍼
public class SingleMessageListener implements MessageListener {
    private final ArrayBlockingQueue<Message> messages =
        new ArrayBlockingQueue<Message>(1);

    public void processMessage(Chat chat, Message message) {
        messages.add(message);
    }

    // 4. 5초 내 메시지 수신 확인, 없으면 실패
    public void receivesAMessage() throws InterruptedException {
        assertThat("Message",
                   messages.poll(5, SECONDS),  // 5초 대기
                   is(notNullValue()));
    }
}
```

**Python 버전**:
```python
# FakeAuctionServer의 Python 버전 (2단계)
import queue
from typing import Optional

class SingleMessageListener:
    """단일 메시지 처리 헬퍼"""
    def __init__(self):
        # 크기 1인 블로킹 큐
        self.messages = queue.Queue(maxsize=1)

    def process_message(self, chat: Chat, message: Message) -> None:
        """메시지 수신 시 호출"""
        self.messages.put(message)

    def receives_a_message(self) -> None:
        """5초 내 메시지 수신 확인"""
        try:
            # 5초 대기
            message = self.messages.get(timeout=5.0)
            assert message is not None, "Message should not be null"
        except queue.Empty:
            raise AssertionError("No message received within 5 seconds")


class FakeAuctionServer:
    def __init__(self, item_id: str):
        self.item_id = item_id
        self.connection = XMPPConnection(self.XMPP_HOSTNAME)
        self.current_chat: Optional[Chat] = None
        self.message_listener = SingleMessageListener()

    def start_selling_item(self) -> None:
        """경매 아이템 판매 시작"""
        self.connection.connect()
        self.connection.login(
            self.ITEM_ID_AS_LOGIN.format(self.item_id),
            self.AUCTION_PASSWORD,
            self.AUCTION_RESOURCE
        )

        # 채팅 리스너 등록
        def on_chat_created(chat: Chat, created_locally: bool) -> None:
            self.current_chat = chat
            # 메시지 리스너 추가
            chat.add_message_listener(self.message_listener)

        self.connection.get_chat_manager().add_chat_listener(on_chat_created)

    def has_received_join_request_from_sniper(self) -> None:
        """Sniper로부터 Join 요청 수신 확인"""
        self.message_listener.receives_a_message()

    def announce_closed(self) -> None:
        """경매 종료 알림"""
        self.current_chat.send_message(Message())  # 빈 메시지

    def stop(self) -> None:
        """연결 종료"""
        self.connection.disconnect()
```

**스레드 조정 전략**:
- 테스트 스레드와 Smack 스레드 간 조정 필요
- BlockingQueue로 메시지 도착 대기 및 타임아웃 처리
- 테스트에서는 한 번에 하나의 메시지만 처리

---

### 4. 테스트 실패와 통과

**참조**: content.md 281-586행

**이전 화제와의 관계**: 구축한 테스트 인프라를 사용해 실제 애플리케이션을 점진적으로 개발

**설명**: 테스트를 실행하고 실패를 확인한 후, 각 증상을 하나씩 수정하며 최소 기능 애플리케이션을 만드는 과정 (→ **핵심 개념 2: 점진적 실패 수정** 참조)

#### 4.1 첫 번째 사용자 인터페이스

**테스트 실패** (참조: 304-320행):
```
java.lang.AssertionError:
Tried to look for...
    exactly 1 JFrame (with name "Auction Sniper Main" and showing on screen)
    in all top level windows
but...
    all top level windows
contained 0 JFrame (with name "Auction Sniper Main" and showing on screen)
```

**구현** (참조: 325-353행):
```java
// Main 클래스
public class Main {
    private MainWindow ui;

    public Main() throws Exception {
        startUserInterface();
    }

    public static void main(String... args) throws Exception {
        Main main = new Main();
    }

    // Swing 이벤트 디스패치 스레드에서 UI 생성
    private void startUserInterface() throws Exception {
        SwingUtilities.invokeAndWait(new Runnable() {
            public void run() {
                ui = new MainWindow();
            }
        });
    }
}

// MainWindow 클래스
public class MainWindow extends JFrame {
    public MainWindow() {
        super("Auction Sniper");
        setName(MAIN_WINDOW_NAME);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
    }
}
```

**Python 버전**:
```python
# Main 클래스의 Python 버전
import tkinter as tk
from threading import Thread

class Main:
    def __init__(self):
        self.ui: Optional[MainWindow] = None
        self.start_user_interface()

    def start_user_interface(self) -> None:
        """UI 스레드에서 메인 윈도우 시작"""
        def create_ui():
            self.ui = MainWindow()

        # UI 스레드 실행
        ui_thread = Thread(target=create_ui)
        ui_thread.start()
        ui_thread.join()  # 완료 대기


class MainWindow(tk.Tk):
    MAIN_WINDOW_NAME = "Auction Sniper Main"

    def __init__(self):
        super().__init__()
        self.title("Auction Sniper")
        self.wm_title(self.MAIN_WINDOW_NAME)
        # 윈도우 표시
        self.mainloop()
```

**노트**: 최소한의 UI지만 애플리케이션 창을 시작하고 연결할 수 있음을 확인

#### 4.2 Sniper 상태 표시

**테스트 실패** (참조: 371-386행):
```
java.lang.AssertionError:
Tried to look for...
    exactly 1 JLabel (with name "sniper status")
    ...
but...
    ...
contained 0 JLabel (with name "sniper status")
```

**구현** (참조: 393-410행):
```java
public class MainWindow extends JFrame {
    public static final String SNIPER_STATUS_NAME = "sniper status";
    private final JLabel sniperStatus = createLabel(STATUS_JOINING);

    public MainWindow() {
        super("Auction Sniper");
        setName(MAIN_WINDOW_NAME);
        add(sniperStatus);  // 레이블 추가
        pack();
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
    }

    private static JLabel createLabel(String initialText) {
        JLabel result = new JLabel(initialText);
        result.setName(SNIPER_STATUS_NAME);
        result.setBorder(new LineBorder(Color.BLACK));
        return result;
    }
}
```

**Python 버전**:
```python
# MainWindow의 Python 버전 (상태 표시 추가)
import tkinter as tk
from tkinter import ttk

class MainWindow(tk.Tk):
    MAIN_WINDOW_NAME = "Auction Sniper Main"
    SNIPER_STATUS_NAME = "sniper status"
    STATUS_JOINING = "Joining"

    def __init__(self):
        super().__init__()
        self.title("Auction Sniper")
        self.wm_title(self.MAIN_WINDOW_NAME)

        # 상태 레이블 생성 및 추가
        self.sniper_status = self._create_label(self.STATUS_JOINING)
        self.sniper_status.pack()

        self.mainloop()

    def _create_label(self, initial_text: str) -> tk.Label:
        """상태 레이블 생성"""
        label = tk.Label(self, text=initial_text,
                        relief=tk.SOLID, borderwidth=1)
        label.configure(name=self.SNIPER_STATUS_NAME)
        return label
```

**노트**: 애플리케이션에 내용을 표시할 수 있음을 확인

#### 4.3 경매에 연결

**테스트 실패** (참조: 420-427행):
```
java.lang.AssertionError:
Expected: is not null
got: null
  at SingleMessageListener.receivesAMessage()
  at FakeAuctionServer.hasReceivedJoinRequestFromSniper()
```

**구현** (참조: 440-478행):
```java
public class Main {
    private static final int ARG_HOSTNAME = 0;
    private static final int ARG_USERNAME = 1;
    private static final int ARG_PASSWORD = 2;
    private static final int ARG_ITEM_ID  = 3;

    public static final String AUCTION_RESOURCE = "Auction";
    public static final String ITEM_ID_AS_LOGIN = "auction-%s";
    public static final String AUCTION_ID_FORMAT =
        ITEM_ID_AS_LOGIN + "@%s/" + AUCTION_RESOURCE;

    public static void main(String... args) throws Exception {
        Main main = new Main();

        // XMPP 연결 생성
        XMPPConnection connection = connectTo(
            args[ARG_HOSTNAME],
            args[ARG_USERNAME],
            args[ARG_PASSWORD]
        );

        // 채팅 생성 및 빈 메시지 전송
        Chat chat = connection.getChatManager().createChat(
            auctionId(args[ARG_ITEM_ID], connection),
            new MessageListener() {
                public void processMessage(Chat aChat, Message message) {
                    // 아직 아무것도 하지 않음
                }
            }
        );
        chat.sendMessage(new Message());  // 빈 메시지 전송
    }

    private static XMPPConnection connectTo(
        String hostname, String username, String password
    ) throws XMPPException {
        XMPPConnection connection = new XMPPConnection(hostname);
        connection.connect();
        connection.login(username, password, AUCTION_RESOURCE);
        return connection;
    }

    private static String auctionId(String itemId, XMPPConnection connection) {
        return String.format(AUCTION_ID_FORMAT, itemId,
                            connection.getServiceName());
    }
}
```

**Python 버전**:
```python
# Main 클래스의 Python 버전 (XMPP 연결 추가)
from typing import List

class Main:
    ARG_HOSTNAME = 0
    ARG_USERNAME = 1
    ARG_PASSWORD = 2
    ARG_ITEM_ID = 3

    AUCTION_RESOURCE = "Auction"
    ITEM_ID_AS_LOGIN = "auction-{}"
    AUCTION_ID_FORMAT = ITEM_ID_AS_LOGIN + "@{}/" + AUCTION_RESOURCE

    def __init__(self):
        self.ui: Optional[MainWindow] = None

    @staticmethod
    def main(*args: str) -> None:
        """애플리케이션 진입점"""
        main = Main()

        # XMPP 연결 생성
        connection = Main._connect_to(
            args[Main.ARG_HOSTNAME],
            args[Main.ARG_USERNAME],
            args[Main.ARG_PASSWORD]
        )

        # 채팅 생성
        def on_message(chat: Chat, message: Message) -> None:
            # 아직 아무것도 하지 않음
            pass

        chat = connection.get_chat_manager().create_chat(
            Main._auction_id(args[Main.ARG_ITEM_ID], connection),
            on_message
        )

        # 빈 메시지 전송
        chat.send_message(Message())

    @staticmethod
    def _connect_to(hostname: str, username: str, password: str) -> XMPPConnection:
        """XMPP 서버 연결"""
        connection = XMPPConnection(hostname)
        connection.connect()
        connection.login(username, password, Main.AUCTION_RESOURCE)
        return connection

    @staticmethod
    def _auction_id(item_id: str, connection: XMPPConnection) -> str:
        """경매 ID 생성"""
        return Main.AUCTION_ID_FORMAT.format(
            item_id,
            connection.get_service_name()
        )
```

**노트**:
- Sniper에서 경매로 연결을 설정할 수 있음을 확인
- 메시지 내용은 나중에 추가 (현재는 빈 메시지로 충분)
- 의도적으로 단순하게 작성하고, 나중에 개선 예정 (→ **핵심 개념 2: 점진적 실패 수정** 참조)

#### 4.4 경매로부터 응답 수신

**테스트 실패** (참조: 501-516행):
```
java.lang.AssertionError:
Tried to look for...
    exactly 1 JLabel (with name "sniper status")
    ...
and check that its label text is "Lost"
but...
    ...
label text was "Joining"
```

**구현** (참조: 530-580행):
```java
public class Main {
    @SuppressWarnings("unused")
    private Chat notToBeGCd;  // GC 방지용 참조

    public static void main(String... args) throws Exception {
        Main main = new Main();
        main.joinAuction(
            connection(args[ARG_HOSTNAME], args[ARG_USERNAME], args[ARG_PASSWORD]),
            args[ARG_ITEM_ID]
        );
    }

    private void joinAuction(XMPPConnection connection, String itemId)
        throws XMPPException {

        final Chat chat = connection.getChatManager().createChat(
            auctionId(itemId, connection),
            new MessageListener() {
                public void processMessage(Chat aChat, Message message) {
                    // Swing 스레드에서 UI 업데이트
                    SwingUtilities.invokeLater(new Runnable() {
                        public void run() {
                            ui.showStatus(MainWindow.STATUS_LOST);
                        }
                    });
                }
            }
        );

        this.notToBeGCd = chat;  // GC 방지
        chat.sendMessage(new Message());
    }
}

public class MainWindow extends JFrame {
    public void showStatus(String status) {
        sniperStatus.setText(status);
    }
}
```

**Python 버전**:
```python
# Main 클래스의 Python 버전 (응답 수신 추가)
from typing import Optional

class Main:
    def __init__(self):
        self.ui: Optional[MainWindow] = None
        self.not_to_be_gcd: Optional[Chat] = None  # GC 방지

    def join_auction(self, connection: XMPPConnection, item_id: str) -> None:
        """경매 참여"""
        def on_message(chat: Chat, message: Message) -> None:
            # UI 스레드에서 상태 업데이트
            self.ui.after(0, lambda: self.ui.show_status(
                MainWindow.STATUS_LOST
            ))

        # 채팅 생성
        chat = connection.get_chat_manager().create_chat(
            self._auction_id(item_id, connection),
            on_message
        )

        # GC 방지를 위해 참조 보관
        self.not_to_be_gcd = chat

        # 빈 메시지 전송
        chat.send_message(Message())


class MainWindow(tk.Tk):
    def show_status(self, status: str) -> None:
        """상태 표시"""
        self.sniper_status.config(text=status)
```

**Chat 필드가 필요한 이유** (참조: 556-568행):
- ChatManager 문서: "현재 모든 채팅에 대한 참조를 추적하지만 자체적으로 메모리에 참조를 보관하지 않으므로 채팅 객체 자체에 대한 참조를 유지해야 함"
- GC되면 Smack 런타임이 새 Chat을 생성하여 메시지 전달
- 의도적으로 어색하게 작성하여 이유를 명확히 표시

**노트**: Sniper가 경매와 연결을 설정하고, 응답을 받아 결과를 표시할 수 있음을 확인

---

### 5. 필요한 최소한

**참조**: content.md 587-621행

**이전 화제와의 관계**: 점진적 개발 과정을 통해 달성한 워킹 스켈레톤의 의미

**설명**: iteration zero에서 요구되는 집중도와 '필요한 최소한'의 판단력에 대한 성찰 (→ **핵심 개념 3: 필요한 최소한** 참조)

**필요한 최소한의 기준**:
1. **종단간 시스템 구조 설계 및 검증**
   - 패키지, 라이브러리, 도구 선택이 실제로 작동하는지 증명
   - 배포 환경까지 포함

2. **가정 테스트를 위한 절대적 최소 기능**
   - Sniper 메시지에 내용을 넣지 않음 (통신과 이벤트 처리 작동 확인이 목표)
   - 상세 코드 설계에 큰 노력을 들이지 않음 (조각들을 제자리에 놓는 단계)

3. **긴급성(sense of urgency)**
   - 팀이 기능을 절대적 최소로 줄이는 데 도움
   - 다양화와 논의는 생략 (편집된 하이라이트만 책에 수록)

**iteration zero의 특징**:
- 제품 문서와 토론 목록을 뒤지며 조각들을 찾아내는 과정
- 프로젝트 헌장 이슈 발생 (결정 기준을 찾기 위한 깊은 질문)
- 스폰서는 목적에 대한 심도 있는 질문에 답할 준비 필요

**성과**:
- 진행 상황의 가시적 증거 확보
- 첫 번째 항목 완료 표시
- 다음 단계: 실제 기능 구축

---

## 요약

이 장은 **테스트 인프라를 먼저 구축**하고, **점진적으로 실패를 수정**하며, **필요한 최소한**만 구현하여 첫 번째 종단간 테스트를 통과시키는 과정을 보여줍니다. ApplicationRunner와 FakeAuctionServer라는 테스트 도구를 만들고, 이를 사용해 GUI 표시부터 XMPP 통신까지 단계별로 기능을 추가했습니다. 이 과정에서 중요한 것은 완벽한 설계보다 **작동하는 워킹 스켈레톤**을 만들어 시스템 구조를 검증하는 것입니다.

# 옥션 스나이퍼 의뢰

## 압축 내용

경매 입찰 자동화 애플리케이션(Auction Sniper) 개발을 위해 요구사항을 분석하고, 프로토콜(XMPP)을 이해하며, 점진적 개발 계획(Walking Skeleton → 단일 아이템 입찰 → 다중 아이템 → UI 개선)을 수립하는 과정.

## 핵심 내용

### 1. **Auction Sniper 개념**
온라인 경매를 모니터링하며 가격이 변경될 때마다 자동으로 약간 더 높은 입찰을 하는 애플리케이션. 중지 가격(stop-price)에 도달하거나 경매가 종료될 때까지 입찰을 계속한다.
- 관련: [3. 기본 용어 정의](#3-기본-용어-정의), [5. XMPP 프로토콜](#5-xmpp-프로토콜)

### 2. **Walking Skeleton 접근법**
최소한의 기능으로 시작하여 점진적으로 복잡성을 추가하는 개발 방식. Swing, XMPP, 애플리케이션 로직을 연결하는 가장 작은 경로부터 구축한다.
- 관련: [8. 점진적 개발 계획](#8-점진적-개발-계획)

### 3. **기본 용어 정의**
Item, Bidder, Bid, Current price, Stop price, Auction, Auction house 등 경매 도메인의 핵심 개념을 명확히 정의.
- 관련: [1. Auction Sniper 개념](#1-auction-sniper-개념)

### 4. **Java Swing UI 설계**
데스크톱에서 실행되며 여러 아이템에 동시 입찰 가능. 각 아이템의 식별자, 중지 가격, 현재 경매 가격, 상태를 표시.
- 관련: [1. Auction Sniper 개념](#1-auction-sniper-개념)

### 5. **XMPP 프로토콜**
Southabee's 경매 시스템과의 통신을 위한 XML 기반 메시징 프로토콜. 실시간 구조화된 데이터 교환에 적합.
- 관련: [6. 경매 프로토콜](#6-경매-프로토콜), [7. 상태 머신](#7-상태-머신)

### 6. **경매 프로토콜**
Bidder가 보내는 명령(Join, Bid)과 Auction이 보내는 이벤트(Price, Close)로 구성된 단순한 메시징 프로토콜.
- 관련: [5. XMPP 프로토콜](#5-xmpp-프로토콜), [7. 상태 머신](#7-상태-머신)

### 7. **상태 머신**
Sniper의 행동을 나타내는 상태 전이: Join → Bidding → (Won | Lost). 중지 가격은 단순화를 위해 초기 단계에서 제외.
- 관련: [6. 경매 프로토콜](#6-경매-프로토콜)

### 8. **점진적 개발 계획**
7단계로 나눈 기능 개발 순서: Walking Skeleton → 입찰 추가 → 승리 구분 → 가격 상세 표시 → 다중 아이템 → UI 입력 → 중지 가격 적용.
- 관련: [2. Walking Skeleton 접근법](#2-walking-skeleton-접근법)

### 핵심 개념 간 관계

```
[Auction Sniper 개념]
    ↓ 구현 기반
[XMPP 프로토콜] ↔ [경매 프로토콜]
    ↓ 행동 모델링
[상태 머신]
    ↓ 구현 방법
[Walking Skeleton 접근법] → [점진적 개발 계획]
    ↓ 표시
[Java Swing UI]
```

- **기본 용어 정의**는 모든 개념의 공통 언어 기반
- **XMPP 프로토콜**과 **경매 프로토콜**은 Sniper와 경매 시스템 간 통신 메커니즘
- **상태 머신**은 프로토콜을 기반으로 Sniper의 행동 로직을 정의
- **Walking Skeleton**과 **점진적 개발 계획**은 전체 시스템 구현 전략

## 상세 내용

### 목차

1. [프로젝트 배경](#1-프로젝트-배경)
2. [Auction Sniper 요구사항](#2-auction-sniper-요구사항)
3. [기본 용어 정의](#3-기본-용어-정의)
4. [사용자 인터페이스 설계](#4-사용자-인터페이스-설계)
5. [XMPP 프로토콜](#5-xmpp-프로토콜)
6. [경매 프로토콜](#6-경매-프로토콜)
7. [상태 머신](#7-상태-머신)
8. [점진적 개발 계획](#8-점진적-개발-계획)
9. [현실적 제약사항](#9-현실적-제약사항)

---

### 1. 프로젝트 배경
**참조**: content.md 11-22줄

Markup and Gouge 회사는 온라인 경매(주로 Southabee's)에서 골동품을 구매한다. 문제는 구매자들이 경매 상태를 수동으로 확인하는 데 많은 시간을 소비하고, 빠르게 응답하지 못해 매력적인 아이템을 놓치는 경우가 발생한다는 것이다.

**핵심 개념 참조**: [1. Auction Sniper 개념](#1-auction-sniper-개념)

**이전 화제와의 관계**: 장의 시작점으로, 프로젝트의 필요성과 비즈니스 컨텍스트를 제공한다.

---

### 2. Auction Sniper 요구사항
**참조**: content.md 18-22, 42-57줄

경영진이 Auction Sniper 개발을 결정했다. 이 애플리케이션은:
- 온라인 경매를 감시
- 가격 변경 시 자동으로 약간 더 높은 입찰
- 중지 가격(stop-price) 도달 또는 경매 종료까지 입찰 지속

초기 논의에서 많은 요구사항(관련 아이템 그룹 입찰 등)이 나왔지만, 구매자들은 먼저 기본 애플리케이션을 작동시키는 데 동의했다.

**핵심 개념 참조**: [1. Auction Sniper 개념](#1-auction-sniper-개념), [8. 점진적 개발 계획](#8-점진적-개발-계획)

**이전 화제와의 관계**: [1. 프로젝트 배경](#1-프로젝트-배경)에서 제기된 문제에 대한 해결책을 구체화한다.

---

### 3. 기본 용어 정의
**참조**: content.md 23-39줄

혼란을 피하기 위해 합의한 기본 용어:

- **Item**: 식별되고 구매될 수 있는 것
- **Bidder**: 아이템 구매에 관심 있는 개인 또는 조직
- **Bid**: 입찰자가 아이템에 대해 지불할 가격 선언
- **Current price**: 아이템의 현재 최고 입찰가
- **Stop price**: 입찰자가 아이템에 대해 지불할 최대 금액
- **Auction**: 아이템에 대한 입찰을 관리하는 프로세스
- **Auction house**: 경매를 주최하는 기관

```python
# 용어를 Python 데이터 모델로 표현
from dataclasses import dataclass
from typing import Optional

@dataclass
class Item:
    """식별되고 구매될 수 있는 것"""
    identifier: str

@dataclass
class Bidder:
    """아이템 구매에 관심 있는 개인 또는 조직"""
    name: str

@dataclass
class Bid:
    """입찰자가 아이템에 대해 지불할 가격 선언"""
    bidder: Bidder
    price: int

@dataclass
class Auction:
    """아이템에 대한 입찰을 관리하는 프로세스"""
    item: Item
    current_price: int  # 현재 최고 입찰가

@dataclass
class AuctionSniper:
    """경매 스나이퍼 설정"""
    item: Item
    stop_price: int  # 입찰자가 지불할 최대 금액
```

**핵심 개념 참조**: [1. Auction Sniper 개념](#1-auction-sniper-개념)

**이전 화제와의 관계**: [2. Auction Sniper 요구사항](#2-auction-sniper-요구사항)에서 논의된 개념들의 명확한 정의를 제공한다.

---

### 4. 사용자 인터페이스 설계
**참조**: content.md 47-61줄

Java Swing 애플리케이션으로 구축:
- 데스크톱에서 실행
- 한 번에 여러 아이템 입찰 가능
- 각 스나이핑 아이템의 표시 정보:
  - 식별자
  - 중지 가격
  - 현재 경매 가격
  - 상태
- 사용자 인터페이스를 통해 새 아이템 추가 가능
- 경매 하우스에서 도착하는 이벤트에 응답하여 표시 값 변경

Figure 9.1은 초기 UI 스케치를 보여준다(완전하지 않고 예쁘지 않지만 시작하기에 충분).

```python
# UI 모델 예시
from dataclasses import dataclass
from enum import Enum

class SniperStatus(Enum):
    """스나이퍼 상태"""
    JOINING = "joining"
    BIDDING = "bidding"
    WINNING = "winning"
    LOST = "lost"
    WON = "won"

@dataclass
class SniperDisplayItem:
    """UI에 표시될 스나이퍼 아이템 정보"""
    item_id: str          # 아이템 식별자
    stop_price: int       # 중지 가격
    current_price: int    # 현재 경매 가격
    status: SniperStatus  # 현재 상태

class SniperUI:
    """스나이퍼 사용자 인터페이스 (Java Swing 개념을 Python으로 표현)"""

    def __init__(self):
        self.display_items: list[SniperDisplayItem] = []

    def add_item(self, item_id: str, stop_price: int):
        """새 아이템을 스나이핑 목록에 추가"""
        new_item = SniperDisplayItem(
            item_id=item_id,
            stop_price=stop_price,
            current_price=0,
            status=SniperStatus.JOINING
        )
        self.display_items.append(new_item)

    def update_price(self, item_id: str, new_price: int):
        """아이템의 현재 가격 업데이트"""
        for item in self.display_items:
            if item.item_id == item_id:
                item.current_price = new_price
                break

    def update_status(self, item_id: str, new_status: SniperStatus):
        """아이템의 상태 업데이트"""
        for item in self.display_items:
            if item.item_id == item_id:
                item.status = new_status
                break
```

**핵심 개념 참조**: [4. Java Swing UI 설계](#4-java-swing-ui-설계)

**이전 화제와의 관계**: [3. 기본 용어 정의](#3-기본-용어-정의)에서 정의한 개념들을 UI 요소로 구현한다.

---

### 5. XMPP 프로토콜
**참조**: content.md 62-98줄

Southabee's는 경매 입찰에 XMPP(Jabber)를 사용한다.

**XMPP 특징**:
- XML 요소를 네트워크를 통해 스트리밍하는 프로토콜
- 원래 Jabber 인스턴트 메시징용으로 설계
- IETF 인터넷 표준으로 승인될 때 XMPP로 이름 변경
- 실시간에 가까운 구조화된 데이터 교환에 사용 가능

**XMPP 아키텍처**:
- 분산형 클라이언트/서버 구조 (중앙 서버 없음)
- 누구나 XMPP 서버 운영 가능
- 사용자는 여러 장치/클라이언트에서 동시 로그인 가능
- 각 리소스에 우선순위 할당

**Jabber ID (JID)**:
- 형식: `username@example.com` (이메일 주소와 유사)
- 리소스 포함 시: `username@example.com/office`
- 네트워크의 모든 사용자는 고유한 JID 보유

```python
# XMPP 연결 개념을 Python으로 표현
from dataclasses import dataclass

@dataclass
class JabberID:
    """Jabber ID (JID) 표현"""
    username: str
    server: str
    resource: str = ""

    def __str__(self) -> str:
        """JID를 문자열로 변환"""
        base = f"{self.username}@{self.server}"
        if self.resource:
            return f"{base}/{self.resource}"
        return base

class XMPPConnection:
    """XMPP 연결 추상화"""

    def __init__(self, jid: JabberID, password: str):
        self.jid = jid
        self.password = password
        self.connected = False

    def connect(self):
        """XMPP 서버에 연결"""
        # 실제로는 네트워크 연결 로직이 필요
        self.connected = True
        print(f"Connected to {self.jid.server} as {self.jid}")

    def send_message(self, to_jid: JabberID, message: str):
        """메시지 전송"""
        if not self.connected:
            raise RuntimeError("Not connected to XMPP server")
        print(f"Sending to {to_jid}: {message}")

    def join_chat(self, chat_name: str):
        """채팅방 참여"""
        if not self.connected:
            raise RuntimeError("Not connected to XMPP server")
        print(f"Joining chat: {chat_name}")

# 사용 예시
sniper_jid = JabberID("sniper", "auction.example.com", "desktop")
connection = XMPPConnection(sniper_jid, "password")
connection.connect()
```

**핵심 개념 참조**: [5. XMPP 프로토콜](#5-xmpp-프로토콜)

**이전 화제와의 관계**: [4. 사용자 인터페이스 설계](#4-사용자-인터페이스-설계)에서 정의한 UI가 경매 시스템과 통신하는 메커니즘을 제공한다.

---

### 6. 경매 프로토콜
**참조**: content.md 102-145줄

**Bidder가 보내는 명령**:

1. **Join**: 입찰자가 경매에 참여. XMPP 메시지의 발신자가 입찰자를 식별하고, 채팅 세션 이름이 아이템을 식별.
2. **Bid**: 입찰자가 입찰 가격을 경매에 전송.

**Auction이 보내는 이벤트**:

1. **Price**: 경매가 현재 수락된 가격을 보고. 다음 입찰이 올려야 할 최소 증분과 이 가격을 입찰한 입찰자 이름 포함. 입찰자가 참여할 때와 새 입찰이 수락될 때마다 모든 입찰자에게 전송.
2. **Close**: 경매 종료 알림. 마지막 Price 이벤트의 승자가 경매 승자.

**XMPP 메시지 형식**:
- 단일 라인에 키/값 쌍으로 직렬화
- 프로토콜 버전 번호로 시작

```python
# 경매 프로토콜 메시지 구조
from dataclasses import dataclass
from typing import Optional

@dataclass
class AuctionCommand:
    """입찰자가 보내는 명령"""
    version: str = "1.1"

@dataclass
class JoinCommand(AuctionCommand):
    """경매 참여 명령"""
    command: str = "JOIN"

    def to_message(self) -> str:
        return f"SOLVersion: {self.version}; Command: {self.command};"

@dataclass
class BidCommand(AuctionCommand):
    """입찰 명령"""
    command: str = "BID"
    price: int = 0

    def to_message(self) -> str:
        return f"SOLVersion: {self.version}; Command: {self.command}; Price: {self.price};"

@dataclass
class AuctionEvent:
    """경매가 보내는 이벤트"""
    version: str = "1.1"

@dataclass
class PriceEvent(AuctionEvent):
    """가격 이벤트"""
    event: str = "PRICE"
    current_price: int = 0
    increment: int = 0
    bidder: str = ""

    def to_message(self) -> str:
        return (f"SOLVersion: {self.version}; Event: {self.event}; "
                f"CurrentPrice: {self.current_price}; Increment: {self.increment}; "
                f"Bidder: {self.bidder};")

    @staticmethod
    def from_message(message: str) -> 'PriceEvent':
        """메시지 문자열에서 PriceEvent 생성"""
        parts = {}
        for part in message.split(';'):
            if ':' in part:
                key, value = part.strip().split(':', 1)
                parts[key.strip()] = value.strip()

        return PriceEvent(
            current_price=int(parts.get('CurrentPrice', 0)),
            increment=int(parts.get('Increment', 0)),
            bidder=parts.get('Bidder', '')
        )

@dataclass
class CloseEvent(AuctionEvent):
    """경매 종료 이벤트"""
    event: str = "CLOSE"

    def to_message(self) -> str:
        return f"SOLVersion: {self.version}; Event: {self.event};"

# 사용 예시
# 입찰자 측
join = JoinCommand()
print(join.to_message())  # SOLVersion: 1.1; Command: JOIN;

bid = BidCommand(price=199)
print(bid.to_message())   # SOLVersion: 1.1; Command: BID; Price: 199;

# 경매 측
price_event = PriceEvent(current_price=192, increment=7, bidder="Someone else")
print(price_event.to_message())
# SOLVersion: 1.1; Event: PRICE; CurrentPrice: 192; Increment: 7; Bidder: Someone else;

close_event = CloseEvent()
print(close_event.to_message())  # SOLVersion: 1.1; Event: CLOSE;
```

**아이템 식별**:
- Southabee's는 로그인 이름으로 판매 아이템 식별
- 아이템 12793에 입찰하려면 `auction-12793` "사용자"와 Southabee's 서버에서 채팅 시작
- 서버는 계정이 미리 설정되어 있다고 가정하고 호출자의 신원에서 누가 입찰하는지 확인

**핵심 개념 참조**: [6. 경매 프로토콜](#6-경매-프로토콜)

**이전 화제와의 관계**: [5. XMPP 프로토콜](#5-xmpp-프로토콜)을 기반으로 구체적인 경매 통신 규칙을 정의한다.

---

### 7. 상태 머신
**참조**: content.md 127-132줄

Sniper의 행동을 나타내는 상태 전이 (Figure 9.3):

1. Sniper가 경매에 **Join** (참여)
2. 여러 **Bidding** (입찰) 라운드
3. 경매가 **Close** (종료)
4. 최종 상태: **Won** (승리) 또는 **Lost** (패배)

**단순화를 위한 결정**:
- 중지 가격(stop price)은 초기 단계에서 제외
- Chapter 18에서 추가될 예정

```python
# 스나이퍼 상태 머신
from enum import Enum, auto

class SniperState(Enum):
    """스나이퍼의 가능한 상태"""
    JOINING = auto()    # 경매에 참여 중
    BIDDING = auto()    # 입찰 중
    WINNING = auto()    # 현재 최고 입찰자
    LOST = auto()       # 경매 패배
    WON = auto()        # 경매 승리

class SniperStateMachine:
    """스나이퍼 상태 머신 관리"""

    def __init__(self):
        self.state = SniperState.JOINING

    def on_price_update(self, current_price: int, bidder: str, own_id: str):
        """가격 업데이트 이벤트 처리"""
        if self.state == SniperState.JOINING:
            # 첫 가격 이벤트: BIDDING 상태로 전환
            self.state = SniperState.BIDDING

        if bidder == own_id:
            # 자신이 최고 입찰자
            self.state = SniperState.WINNING
        else:
            # 다른 사람이 최고 입찰자
            if self.state != SniperState.JOINING:
                self.state = SniperState.BIDDING

    def on_auction_closed(self, last_bidder: str, own_id: str):
        """경매 종료 이벤트 처리"""
        if last_bidder == own_id:
            self.state = SniperState.WON
        else:
            self.state = SniperState.LOST

    def get_state(self) -> SniperState:
        """현재 상태 반환"""
        return self.state

# 사용 예시
sniper = SniperStateMachine()
print(f"Initial state: {sniper.get_state()}")  # JOINING

sniper.on_price_update(100, "other_bidder", "my_sniper")
print(f"After first price: {sniper.get_state()}")  # BIDDING

sniper.on_price_update(110, "my_sniper", "my_sniper")
print(f"After winning bid: {sniper.get_state()}")  # WINNING

sniper.on_auction_closed("my_sniper", "my_sniper")
print(f"After auction closed: {sniper.get_state()}")  # WON
```

**핵심 개념 참조**: [7. 상태 머신](#7-상태-머신)

**이전 화제와의 관계**: [6. 경매 프로토콜](#6-경매-프로토콜)의 이벤트와 명령을 기반으로 Sniper의 행동 로직을 모델링한다.

---

### 8. 점진적 개발 계획
**참조**: content.md 146-199줄

**점진적 개발의 중요성**:
- 애플리케이션이 한 번에 작성하기에는 너무 크다
- 기능을 작은 조각으로 나누는 것이 중요
- 각 조각은 의미 있고 구체적이어야 하며, 작고 집중적이어야 한다
- 작고 일관된 청크로 나누면 개발 위험 관리에 도움
- 정기적이고 구체적인 피드백으로 계획 조정 가능

**Walking Skeleton**:
- 절대적으로 가장 작은 기능
- Swing, XMPP, 애플리케이션을 연결하는 최소 경로
- 이러한 구성 요소를 연결할 수 있음을 보여주기에 충분

**개발 단계 계획**:

1. **Single item: join, lose without bidding** (Chapter 10)
   - 핵심 인프라 구축
   - 시작 케이스

2. **Single item: join, bid, and lose**
   - 기본 연결에 입찰 추가

3. **Single item: join, bid, and win**
   - 승리 입찰을 보낸 사람 구별

4. **Show price details**
   - 사용자 인터페이스 채우기 시작

5. **Multiple items**
   - 동일한 애플리케이션에서 여러 아이템 입찰 지원

6. **Add items through the user interface**
   - 사용자 인터페이스를 통한 입력 구현

7. **Stop bidding at the stop price**
   - Sniper 알고리즘에 더 많은 인텔리전스 추가

**우선순위 결정**:
- 구매자들은 중지 가격보다 사용자 인터페이스를 우선시
- 이유:
  - 애플리케이션에 편안함을 느끼고 싶어함
  - 사용자 인터페이스 없이 여러 아이템(각각 중지 가격 포함)을 추가하는 쉬운 방법이 없음

**향후 계획**:
- 기본 기능 안정화 후 더 복잡한 시나리오 작업
  - 입찰 실패 시 재시도
  - 입찰에 다른 전략 사용

```python
# 점진적 개발 계획을 작업 목록으로 표현
from dataclasses import dataclass
from enum import Enum

class FeatureStatus(Enum):
    """기능 개발 상태"""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

@dataclass
class DevelopmentFeature:
    """개발할 기능"""
    name: str
    description: str
    priority: int
    status: FeatureStatus = FeatureStatus.PLANNED
    chapter: str = ""

class IncrementalPlan:
    """점진적 개발 계획"""

    def __init__(self):
        self.features = [
            DevelopmentFeature(
                name="Walking Skeleton",
                description="Single item: join, lose without bidding",
                priority=1,
                chapter="Chapter 10"
            ),
            DevelopmentFeature(
                name="Basic Bidding",
                description="Single item: join, bid, and lose",
                priority=2
            ),
            DevelopmentFeature(
                name="Winning Logic",
                description="Single item: join, bid, and win",
                priority=3
            ),
            DevelopmentFeature(
                name="Price Details UI",
                description="Show price details",
                priority=4
            ),
            DevelopmentFeature(
                name="Multiple Items",
                description="Support bidding for multiple items",
                priority=5
            ),
            DevelopmentFeature(
                name="UI Input",
                description="Add items through the user interface",
                priority=6
            ),
            DevelopmentFeature(
                name="Stop Price",
                description="Stop bidding at the stop price",
                priority=7
            )
        ]

    def get_next_feature(self) -> DevelopmentFeature:
        """다음 개발할 기능 반환"""
        for feature in self.features:
            if feature.status == FeatureStatus.PLANNED:
                return feature
        raise ValueError("No planned features remaining")

    def start_feature(self, feature_name: str):
        """기능 개발 시작"""
        for feature in self.features:
            if feature.name == feature_name:
                feature.status = FeatureStatus.IN_PROGRESS
                break

    def complete_feature(self, feature_name: str):
        """기능 개발 완료"""
        for feature in self.features:
            if feature.name == feature_name:
                feature.status = FeatureStatus.COMPLETED
                break

    def print_plan(self):
        """계획 출력"""
        print("Incremental Development Plan:")
        print("=" * 60)
        for feature in self.features:
            status_symbol = {
                FeatureStatus.PLANNED: "📋",
                FeatureStatus.IN_PROGRESS: "🔄",
                FeatureStatus.COMPLETED: "✅"
            }[feature.status]

            print(f"{status_symbol} [{feature.priority}] {feature.name}")
            print(f"   {feature.description}")
            if feature.chapter:
                print(f"   ({feature.chapter})")
            print()

# 사용 예시
plan = IncrementalPlan()
plan.print_plan()

# 첫 번째 기능 시작
next_feature = plan.get_next_feature()
print(f"\nStarting: {next_feature.name}")
plan.start_feature(next_feature.name)
```

**핵심 개념 참조**: [2. Walking Skeleton 접근법](#2-walking-skeleton-접근법), [8. 점진적 개발 계획](#8-점진적-개발-계획)

**이전 화제와의 관계**: 앞서 정의한 모든 개념([3. 기본 용어](#3-기본-용어-정의), [6. 프로토콜](#6-경매-프로토콜), [7. 상태 머신](#7-상태-머신))을 실제로 구현하는 로드맵을 제시한다.

---

### 9. 현실적 제약사항
**참조**: content.md 200-226줄

책의 범위 내에서 실제 프로젝트의 느낌을 전달하기 위해 프로세스와 디자인에서 일부 지름길을 택했다:

**1. 비현실적인 아키텍처**
- XMPP는 신뢰할 수 없고 안전하지 않아 트랜잭션에 부적합
- 이러한 품질 보장은 범위 밖
- 하지만 기본 기술은 기본 아키텍처에 관계없이 적용됨
- (방어: HTTP처럼 부적절한 프로토콜로 주요 시스템이 구축됨)

**2. 애자일 계획이 아님**
- 프로젝트 계획을 서두르게 진행하여 단일 할 일 목록 생성
- 실제 프로젝트에서는 전체 결과물(릴리스 계획)을 먼저 파악
- 참조: [Shore07], [Cohn05]

**3. 현실적인 사용성 디자인이 아님**
- 좋은 사용자 경험 디자인은 최종 사용자가 실제로 달성하려는 것을 조사
- 이를 사용하여 일관된 경험 창출
- UX 커뮤니티는 반복적으로 수행하는 방법에 대해 애자일 개발 커뮤니티와 협력 중
- 이 프로젝트는 달성하고자 하는 비전의 초안을 작성하고 작업하기에 충분히 간단

```python
# 현실적 제약사항을 문서화하는 구조
from dataclasses import dataclass
from typing import List

@dataclass
class ProjectConstraint:
    """프로젝트 제약사항"""
    category: str
    limitation: str
    reason: str
    real_world_approach: str

class ProjectLimitations:
    """프로젝트의 현실적 제약사항 문서화"""

    def __init__(self):
        self.constraints: List[ProjectConstraint] = [
            ProjectConstraint(
                category="Architecture",
                limitation="XMPP는 신뢰할 수 없고 안전하지 않음",
                reason="트랜잭션에 부적합하지만 책의 범위를 단순화",
                real_world_approach="신뢰할 수 있고 안전한 프로토콜 사용 (예: TLS, 메시지 큐)"
            ),
            ProjectConstraint(
                category="Planning",
                limitation="간략한 계획, 단일 할 일 목록만 생성",
                reason="책의 범위 내에서 핵심 개념 전달",
                real_world_approach="전체 릴리스 계획, 반복 계획, 스토리 맵핑 (참조: Shore07, Cohn05)"
            ),
            ProjectConstraint(
                category="UX Design",
                limitation="실제 사용자 조사 없이 UI 초안 작성",
                reason="간단한 프로젝트로 비전 작성 가능",
                real_world_approach="사용자 조사, 페르소나, 사용자 여정 맵, 반복적 UX 디자인"
            )
        ]

    def print_limitations(self):
        """제약사항 출력"""
        print("Project Limitations (For Educational Purposes)")
        print("=" * 70)
        for constraint in self.constraints:
            print(f"\n⚠️ {constraint.category}")
            print(f"   Limitation: {constraint.limitation}")
            print(f"   Reason: {constraint.reason}")
            print(f"   ✅ Real-world: {constraint.real_world_approach}")

# 사용 예시
limitations = ProjectLimitations()
limitations.print_limitations()
```

**핵심 개념 참조**: 모든 핵심 개념의 현실적 한계 인정

**이전 화제와의 관계**: [8. 점진적 개발 계획](#8-점진적-개발-계획)에서 제시한 계획이 교육 목적으로 단순화되었음을 명시하고, 실무에서는 더 엄격한 접근이 필요함을 강조한다.

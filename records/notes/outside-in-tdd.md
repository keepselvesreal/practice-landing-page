Outside-In TDD 이해 정리

  1. 이해 대상/주제

  Outside-In TDD의 진행 순서와 각 단계에서 Mock/Stub을 사용하는 이유

  구체적으로:
  - E2E 테스트부터 Repository까지의 개발 흐름
  - 각 레이어(API, Service, Repository)에서 Mock/Stub을 사용하는 시점과 목적
  - Red-Green-Refactor 사이클이 각 레이어에서 어떻게 적용되는지

  ---
  2. 내 이해 (태수의 언어 그대로)

  전체 흐름

  처음에 e2e 테스트 작성하는 건 통과할 acceptance test를 작성하는 거라고 할 수
  있음. 사용자 관점에서 정의된 기능으로, 처음에는 e2e 테스트 실패하며 이는 기능
  구현돼 있지 않음을 의미하고, 최종적으로 이것이 통과된다고 하면 내 시스템에 해당
  기능 구현됐음을 의미.

  바깥에서 안으로

  실패한 테스트를 성공한 테스트로 바꾸기 위해 바깥에서부터 안으로 하나씩 개발을
  진행. 바깥이 지금 당장 관련된 기능, 즉 관련성이 높은 기능이기에.

  API 레이어 개발

  그래서 e2e에서 시스템이 호출하는 api 또는 인터페이스에 대한 개발을 진행하고 이
  과정에서 일단 해결할 수 있는 임시방편 해결을 진행. 가령, 여기선 status code를
  200으로 만드는 것. 하지만 여전히 customer name 필드 없기에 e2e 테스트는 통과
  못함.

  API 테스트와 Stub

  그래서 e2e 테스트 통과하게 만들기 위해선 api 또는 인터페이스에 대한 구체적
  요구사항을 충족하는 개발이 진행되어야 하는데 이 역시 테스트 케이스를 작성해
  red-green, refactor란 tdd 방식으로 진행. 여기서는 반환 데이터의 주문 번호,
  사용자 이름, 총액을 검증함으로써 인터페이스 결과에 이런 것들이 담겨야 함을
  보장함.

  이 테스트를 통과하기 위해선 api에서 이런 결과를 만들어내는 처리를 하는 것이
  구현되어야 하는데 개발되지 않은 상태라 초기 green에는 mock으로 달성.

  Mock의 의미

  stub을 통해 반환값과 더불어 구현할 서비스(get_order_service)를 구상한 거기도
  하군.

  Service 레이어 개발

  이렇게 하여 step2 api 응답 형식 테스트 통과하고 나면 이제 stub으로 대체했던
  service 부분을 직접 개발 진행. 이것 역시 tdd, 즉 테스트 red 단계를 기반으로
  진행. get_order_service에 담길 코드를 기준으로 테스트 코드 작성.

  여기서 데이터 반환을 처리할 객체와, 이 객체에서 사용할 행위(메서드)를 구상해
  mock으로 구현. 이걸 mock으로 구현하는 이유는 이 행위 검증에 인자가 제대로 들어가
   호출되는지 검증하는 게 중요하기 때문. 단순히 데이터만 대신 반환해주는 stub과
  달리 행위 호출에 대한 검증, 구체적으로 호출 시 인자에 대한 확인도 필요하기 때문.

  Repository 레이어 개발

  여기서 데이터 반환하기위해서는 db가 필요한데 현재 db 없는 상태이기에 mock으로
  대체하는 걸로 했던 거고. 그러나 이 mock 설정 과정에서 db에서 반환해야 할
  데이터의 필드와 필드값에 대한 구상 이루어짐.

  그래서 서비스 레이어와 관련된, 즉 get_order_service라는 서비스 처리 함수에서
  필요한 객체와 행위 구현되어 테스트 통과하고 나면 mock으로 대체했던 repository
  부분에 대한 개발을 tdd로 진행. 즉 실패하는 테스트 작성으로 시작.

  실제 db를 사용하면 속도, 데이터 변경 등의 문제 있기에 메모리 db를 사용해서
  진행하고, 미리 db에 값을 넣어 동작 점검 가능하게 만듦. 처음에는 아직 만들어지지
  않은, 개발해야 할 객체와 행동이기에 테스트 실패하게 되고, 이 테스트 코드에서
  사용한 클래스명과 메서드 명으로 개발 진행.

  최종 통합

  이 메서드에서 요구하는 정보는 이미 위에서 사용된 mock에서 검증 했기에 보장된
  상태이고, 따라서 반환값만 검증 통과하게 되면 테스트 통과. 이렇게 가장 밑에 있는,
   즉 최종적으로 필요한 요소까지 모두 개발되고 나면 실패했던 e2e 테스트가
  통과하고, 처음에 목표했던 사용자 관점에서 정의한 기능이 구현되게 됨.

  ---
  3. 정제 (태수의 이해를 정제한 버전)

  3.1 Outside-In TDD의 핵심 개념

  Acceptance Test로서의 E2E 테스트
  - E2E 테스트는 사용자 관점에서 정의한 기능의 완성 기준(acceptance criteria)
  - 초기: 실패 (기능 미구현)
  - 최종: 통과 (기능 구현 완료)

  바깥에서 안으로 개발하는 이유
  - "바깥" = 사용자와 가까운 레이어 = 비즈니스 가치가 높은 부분
  - 사용자 요구사항과 직접 연관된 부분부터 개발하여 "필요한 것만" 구현

  3.2 각 레이어별 개발 흐름

  Step 1: E2E 테스트 (Red)

  목표: 사용자 시나리오 정의
  결과: 실패 (아무것도 구현 안 됨)

  Step 2: API 레이어

  2-1. 임시 해결 (Green)
  - 최소한의 코드로 일부만 통과 (예: status 200 반환)
  - 아직 E2E는 실패 (필수 필드 부족)

  2-2. API 테스트 작성 (Red)
  - 응답 형식 검증 (order_number, customer_name, total_amount)
  - Service를 Stub으로 대체하여 테스트

  2-3. API 구현 (Green)
  - Service 함수 호출 추가 (아직 빈 구현)
  - Stub 덕분에 테스트 통과

  Stub의 역할:
  - 아직 없는 Service의 반환값을 가정
  - API가 "어떤 데이터를 반환해야 하는지" 구상하게 함

  Step 3: Service 레이어

  3-1. Service 테스트 작성 (Red)
  - Repository를 Mock으로 대체
  - Mock을 사용하는 이유:
    * 반환값뿐만 아니라 "호출 행위" 검증 필요
    * Repository가 올바른 인자로 호출되는지 확인

  3-2. Service 구현 (Green)
  - Repository 호출 로직 작성
  - Mock 덕분에 테스트 통과

  Mock의 역할:
  - 아직 없는 Repository의 인터페이스(메서드명, 인자, 반환값) 정의
  - Service의 책임만 집중 테스트 (Repository 구현 여부와 무관)

  Step 4: Repository 레이어

  4-1. Repository 테스트 작성 (Red)
  - 메모리 DB 사용 (속도, 격리성)
  - 테스트 데이터 사전 삽입

  4-2. Repository 구현 (Green)
  - 실제 DB 조회 로직 작성
  - 이미 Mock에서 정의한 인터페이스 따름

  메모리 DB 사용 이유:
  - 빠른 테스트 실행
  - 테스트 간 데이터 격리
  - 실제 DB 상태 변경 방지

  Step 5: 통합 및 E2E 통과

  - 모든 레이어 구현 완료
  - Mock/Stub 제거하고 실제 연결
  - E2E 테스트 통과 (Green)
  - 사용자 기능 구현 완료

  3.3 Mock과 Stub의 차이

  | 특성    | Stub                       | Mock                            |
  |-------|----------------------------|---------------------------------|
  | 목적    | 가짜 데이터 반환                  | 호출 행위 검증
        |
  | 사용 위치 | API 테스트 (Service 대체)       | Service 테스트 (Repository 대체)
       |
  | 검증 대상 | 반환값 (assert result == ...) | 호출 여부 + 인자
  (assert_called_with) |
  | 설계 도구 | 반환 데이터 구조 정의               | 협력자 인터페이스 정의
                |

  3.4 각 단계의 의미

  1. E2E 실패 → 구현할 기능 명확화
  2. API Stub → 응답 형식 설계
  3. Service Mock → 협력자 인터페이스 설계
  4. Repository 구현 → 실제 데이터 접근 로직
  5. E2E 통과 → 기능 완성 보장

  ---
  4. 이해 평가

  4.1 올바른 점 ✅

  1. E2E 테스트의 역할 이해
    - "acceptance test", "사용자 관점에서 정의된 기능"
    - 초기 실패 → 최종 통과의 의미 정확히 파악
  2. Outside-In의 핵심 이유 파악
    - "바깥이 지금 당장 관련된 기능, 즉 관련성이 높은 기능"
    - 사용자 요구사항과 가까운 순서대로 개발
  3. Mock과 Stub의 차이 명확히 구분
    - Stub: "데이터만 대신 반환"
    - Mock: "행위 호출에 대한 검증, 구체적으로 호출 시 인자에 대한 확인"
  4. Mock/Stub이 설계 도구로 작용함을 인식
    - "stub을 통해 반환값과 더불어 구현할 서비스를 구상"
    - "mock 설정 과정에서 db에서 반환해야 할 데이터의 필드와 필드값에 대한 구상
  이루어짐"
  5. Red-Green-Refactor 사이클 이해
    - 각 레이어마다 테스트 먼저 작성 → 최소 구현 → 개선
  6. 메모리 DB 사용 이유
    - "속도, 데이터 변경 등의 문제"

  4.2 보완하면 좋은 점 📝

  1. Mock 사용의 진짜 이유

  1. 태수 이해: "데이터 반환하기위해서는 db가 필요한데 현재 db 없는 상태이기에
  mock으로 대체"

  1. 보완: Mock을 쓰는 건 "DB가 없어서"보다 "Service의 책임만 테스트하기 위해"

  # Service 테스트의 목적
  def test_get_order_service_calls_repository():
      """
      Service는 Repository를 올바르게 호출하기만 하면 됨
      Repository가 실제로 DB에서 데이터를 잘 가져오는지는
      Repository 테스트에서 검증
      """
      mock_repo = Mock()
      mock_repo.get_order_by_number.return_value = {...}

      service = OrderService(repository=mock_repo)
      result = service.get_order("ORD-12345678")

      # 핵심: Repository를 올바른 인자로 호출했는가?
      mock_repo.get_order_by_number.assert_called_once_with("ORD-12345678")

  1. 핵심 개념: 각 레이어의 책임 분리
    - Service 테스트 → Service의 로직만 검증 (Repository 동작은 가정)
    - Repository 테스트 → Repository의 DB 조회만 검증
    - E2E 테스트 → 전체 통합 검증
  2. 시카고 학파와의 차이

  2. 태수 이해: "시카고 학파는 이 때 mock 대신 최소한의 진짜 대상을 만들테니"

  2. 보완: 차이는 개발 순서와 Mock 사용 철학

  | 구분      | 시카고 학파 (Classic TDD)                    | 런던 학파
  (Outside-In TDD)                  |
  |---------|-----------------------------------------|---------------------------
  --------------|
  | 개발 순서   | Inside-Out (Repository → Service → API) | Outside-In (API →
  Service → Repository) |
  | Mock 사용 | 최소화 (외부 의존성만)                           | 적극 활용
  (협력자 모두)                          |
  | 테스트 초점  | 상태 검증 (State Verification)              | 행위 검증
  (Behavior Verification)           |
  | 예시      | Repository 먼저 구현 → Service에서 실제 사용      | Service 테스트
   먼저 → Repository는 Mock       |

  3. monkeypatch.setattr의 동작 원리

  # 원본 코드 (app/routers/orders.py)
  from app.services.orders import get_order_service

  @app.get("/orders/{order_number}")
  def get_order(order_number: str):
      order = get_order_service(order_number)
      return order

  # 테스트 코드
  def test_get_order_returns_customer_info(monkeypatch):
      def fake_service(order_number):
          return {"customer_name": "홍길동", ...}

      # app.routers.orders 모듈의 네임스페이스에서
      # get_order_service를 fake_service로 교체
      monkeypatch.setattr(
          "app.routers.orders.get_order_service",  # 교체 대상 경로
          fake_service  # 교체할 함수
      )

  3. 핵심:
    - "app.routers.orders.get_order_service" = orders.py가 import한 함수
    - 원본 모듈 경로(app.services.orders)가 아니라 사용하는 모듈 경로
    - 테스트 실행 시 이 함수가 없으면 AttributeError → 빈 함수라도 먼저 만들어야
  함
  4. Mock 제거 시점

  4. 태수 이해: "가장 밑에 있는... 최종적으로 필요한 요소까지 모두 개발되고 나면
  실패했던 e2e 테스트가 통과"

  4. 보완: Step 5에서 E2E만 Mock 제거, 단위 테스트는 Mock 유지 가능

  E2E 테스트         → Mock 없음 (전체 통합)
  API 테스트         → Service를 Stub으로 대체 (유지)
  Service 테스트     → Repository를 Mock으로 대체 (유지)
  Repository 테스트  → 메모리 DB 사용

  4. 이유:
    - 단위 테스트는 빠르고 독립적으로 유지
    - E2E로 전체 통합 보장
    - 버그 발생 시 어느 레이어 문제인지 빠르게 파악

  4.3 잘못된 점 ❌

  없음! 전반적으로 핵심을 정확히 이해했어.

  ---
  5. 제안

  5.1 이해를 더 깊게 하려면

  1. 직접 작은 예제 작성해보기

  1. 간단한 기능 하나를 Outside-In으로 개발해보면 이해가 확실해짐:
  예제: "사용자가 이름을 입력하면 인사말을 반환하는 API"

  E2E: GET /greet/홍길동 → {"message": "안녕하세요, 홍길동님!"}
  API: GreetingService를 Stub으로
  Service: NameFormatter를 Mock으로
  NameFormatter: 실제 구현
  2. 시카고 vs 런던 학파 비교 실습

  2. 같은 기능을 두 가지 방식으로 개발해보면 차이가 명확해짐:
    - 시카고: Repository 먼저 → Service → API
    - 런던: E2E → API → Service → Repository
  3. Mock 검증 패턴 연습

  # 다양한 Mock 검증 패턴
  mock.assert_called_once()                    # 정확히 1번 호출
  mock.assert_called_once_with("arg")          # 정확히 1번, 특정 인자로
  mock.assert_called_with("arg")               # 마지막 호출이 특정 인자로
  mock.assert_any_call("arg")                  # 어느 시점엔가 특정 인자로 호출
  mock.assert_not_called()                     # 호출 안 됨

  5.2 다음 학습 주제

  1. Refactor 단계 심화
    - 지금까지는 Red-Green에 집중
    - Green 이후 코드 개선 (중복 제거, 명확성 향상) 연습
  2. Test Double 종류 전체
    - Stub, Mock 외에도: Fake, Spy, Dummy
    - 각각 언제 사용하는지
  3. Integration Test vs Unit Test
    - API 테스트는 Integration? Unit?
    - 경계가 모호한 케이스 판단 기준
  4. TDD의 리듬 체득
    - "작은 단계로 나누기" 연습
    - "테스트를 먼저 쓰기 어려울 때" 대처법

  5.3 문서화 제안

  태수가 이해한 내용을 다음 형식으로 정리해두면 나중에 참고하기 좋을 것 같아:

  # Outside-In TDD 체크리스트

  ## E2E 테스트 작성
  - [ ] 사용자 시나리오 명확히 정의
  - [ ] 실패 확인 (Red)

  ## API 레이어
  - [ ] 임시 구현으로 일부 통과
  - [ ] API 테스트 작성 (응답 형식 검증)
  - [ ] Service를 Stub으로 대체
  - [ ] 테스트 통과 (Green)

  ## Service 레이어
  - [ ] Service 테스트 작성
  - [ ] Repository를 Mock으로 대체
  - [ ] 호출 행위 검증 (assert_called_with)
  - [ ] 테스트 통과 (Green)

  ## Repository 레이어
  - [ ] Repository 테스트 작성 (메모리 DB)
  - [ ] 실제 DB 조회 로직 구현
  - [ ] 테스트 통과 (Green)

  ## 통합
  - [ ] E2E 테스트 통과 확인
  - [ ] 모든 단위 테스트 통과 확인

# 3장: TODO 리스트 생성을 통한 테스트 주도 개발 - 추출된 정보

## 핵심 내용
- TDD가 소프트웨어 개발 루틴에 미치는 영향
- 승인 테스트 주도 개발(ATDD)을 통한 애플리케이션 설계
- TODO 리스트 애플리케이션의 완전한 TDD 구현
- 지속성 추가와 리팩터링 과정
- 회귀 방지와 테스트의 역할

## 상세 핵심 내용

### TDD의 심리적 효과
- **스트레스와 테스트의 악순환**: 개발자가 바쁘고 스트레스받을수록 테스트를 건너뛰게 됨
- **TDD의 해결책**: 테스트를 일상 루틴의 필수 단계로 만들어 악순환 차단
- **습관화의 중요성**: TDD가 자연스러워지면 테스트 없이는 시작하기 어려워짐
- **테스트 vs 테스팅**: 명사로서의 테스트(검증 체크리스트) vs 동사로서의 테스팅(수동 확인)

### 승인 테스트 주도 개발(ATDD)
- **비즈니스 가치 중심**: 외부 계층의 테스트일수록 비즈니스 요구사항 표현
- **명시적 행동 정의**: "이렇게 하면 저렇게 된다"는 명확한 기대치 설정
- **설계 주도**: 테스트가 소프트웨어 설계와 아키텍처를 이끄는 역할
- **예제를 통한 명세**: 테스트 자체가 소프트웨어 명세서 역할 수행

### TODO 애플리케이션 아키텍처
- **REPL 구조**: Read-Eval-Print Loop 기반 대화형 셸
- **명령 디스패처**: cmd_* 패턴을 통한 명령어 처리
- **I/O 추상화**: 입력/출력 함수를 주입받는 구조로 테스트 용이성 확보
- **스레딩 지원**: 백그라운드 실행과 테스트 동시성 처리

## 상세 내용

### 승인 테스트 구조
```python
class TestTODOAcceptance(unittest.TestCase):
    def setUp(self):
        self.inputs = queue.Queue()
        self.outputs = queue.Queue()
        self.fake_output = lambda txt: self.outputs.put(txt)
        self.fake_input = lambda: self.inputs.get()
        self.get_output = lambda: self.outputs.get(timeout=1)
        self.send_input = lambda cmd: self.inputs.put(cmd)

    def test_main(self):
        app = TODOApp(io=(self.fake_input, self.fake_output))
        app_thread = threading.Thread(target=app.run, daemon=True)
        app_thread.start()

        welcome = self.get_output()
        self.assertEqual(welcome, "TODOs:\n\n\n> ")

        self.send_input("add buy milk")
        # 출력 검증...

        self.send_input("quit")
        app_thread.join(timeout=1)
        self.assertEqual(self.get_output(), "bye!\n")
```

### TODOApp 클래스 구현
```python
import functools

class TODOApp:
    def __init__(self, io=(input, functools.partial(print, end=""))):
        self._in, self._out = io
        self._quit = False
        self._entries = []

    def run(self):
        self._quit = False
        while not self._quit:
            self._out(self.prompt(self.items_list()))
            command = self._in()
            self._dispatch(command)
        self._out("bye!\n")

    def _dispatch(self, cmd):
        cmd, *args = cmd.split(" ", 1)
        executor = getattr(self, "cmd_{}".format(cmd), None)
        if executor is None:
            self._out("Invalid command: {}\n".format(cmd))
            return
        executor(*args)

    def cmd_add(self, what):
        self._entries.append(what)

    def cmd_del(self, idx):
        idx = int(idx) - 1
        if idx < 0 or idx >= len(self._entries):
            self._out("Invalid index\n")
            return
        self._entries.pop(idx)

    def cmd_quit(self, *_):
        self._quit = True

    def items_list(self):
        enumerated_items = enumerate(self._entries, start=1)
        return "\n".join(
            "{}. {}".format(idx, entry) for idx, entry in enumerated_items
        )

    def prompt(self, output):
        return """TODOs:
{}

> """.format(output)
```

### 프로젝트 구조와 패키징
```
.
├── src
│   ├── setup.py
│   └── todo
│       ├── app.py
│       ├── __init__.py
│       └── __main__.py
└── tests
    ├── __init__.py
    └── test_acceptance.py
```

### setup.py 구성
```python
from setuptools import setup
setup(name='todo', packages=['todo'])
```

### 지속성 테스트 구현
```python
def test_persistence(self):
    with tempfile.TemporaryDirectory() as tmpdirname:
        # 첫 번째 앱 실행: 항목 추가 후 종료
        app_thread = threading.Thread(
            target=TODOApp(
                io=(self.fake_input, self.fake_output),
                dbpath=tmpdirname
            ).run,
            daemon=True
        )
        app_thread.start()
        self.send_input("add buy milk")
        self.send_input("quit")
        app_thread.join(timeout=1)

        # 두 번째 앱 실행: 데이터 지속성 검증
        app_thread = threading.Thread(
            target=TODOApp(
                io=(self.fake_input, self.fake_output),
                dbpath=tmpdirname
            ).run,
            daemon=True
        )
        app_thread.start()
        welcome = self.get_output()
        # 이전에 추가한 항목이 여전히 존재하는지 확인
```

## 주요 화제

### 1. TDD 철학과 실무
- 테스트를 건너뛰는 스트레스의 악순환
- 테스트를 통한 요구사항 명확화
- 구현 전 인터페이스 설계 강제
- 지속적 리팩터링의 중요성

### 2. 승인 테스트 설계
- 비즈니스 가치 중심의 테스트 작성
- 사용자 경험 관점에서의 기능 검증
- 실제 사용 시나리오 기반 테스트 케이스
- 테스트가 곧 소프트웨어 명세서

### 3. 대화형 애플리케이션 구현
- REPL 패턴을 통한 사용자 인터페이스
- 명령어 디스패칭과 동적 메서드 호출
- 큐 기반 I/O 시뮬레이션
- 멀티스레딩을 활용한 테스트 전략

### 4. 점진적 기능 개발
- 실패하는 테스트부터 시작
- 최소한의 구현으로 테스트 통과
- 기능별 단계적 구현 과정
- 테스트 피드백을 통한 개발 진행

### 5. 애플리케이션 패키징
- setup.py를 통한 패키지 배포
- 개발 모드 설치(pip install -e)
- __main__.py를 통한 실행 가능한 모듈
- 모듈 구조와 테스트 조직화

### 6. 데이터 지속성과 TDD
- 지속성 요구사항의 테스트 주도 개발
- 임시 디렉토리를 활용한 격리된 테스트
- 상태 지속성 검증 전략
- 리팩터링을 통한 기능 확장

## 부차 화제

### 1. Python 개발 환경
- Python 3.7 이상 권장
- threading, queue, tempfile 모듈 활용
- functools.partial을 통한 함수 커스터마이징
- GitHub: PacktPublishing/Crafting-Test-Driven-Software-with-Python

### 2. 테스트 인프라 구축
- queue를 통한 스레드 간 통신
- fake_input/fake_output 시뮬레이션
- timeout을 통한 데드락 방지
- daemon 스레드 활용

### 3. 명령어 처리 패턴
- getattr을 통한 동적 메서드 호출
- cmd_* 네이밍 컨벤션
- 인자 파싱과 에러 처리
- 명령어 확장 가능한 구조

### 4. 사용자 인터페이스 설계
- 프롬프트 기반 상호작용
- 상태 표시와 피드백
- 명령어 구문과 사용성
- 종료 처리와 정리

### 5. 개발 방법론
- Specification by Example 개념
- ATDD vs TDD의 차이점
- 비즈니스 계층별 테스트 전략
- 테스트가 이끄는 설계 과정

### 6. 실제 애플리케이션 검증
- python -m todo 명령으로 실행
- 실제 사용자 시나리오 확인
- 테스트 설계와 실제 동작의 일치성
- 첫 실행에서의 완벽한 동작 달성

### 7. 코드 품질과 유지보수
- I/O 추상화를 통한 테스트 용이성
- 단일 책임 원칙 적용
- 확장 가능한 명령어 시스템
- 깔끔한 분리와 모듈화
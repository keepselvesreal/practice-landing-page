# 11장: 웹 테스팅: WSGI vs HTTP - 추출된 정보

## 핵심 내용
- HTTP 클라이언트와 서버 테스팅 방법론
- requests-mock을 활용한 HTTP 클라이언트 테스팅
- WSGI와 WebTest를 사용한 웹 애플리케이션 테스팅
- 다양한 웹 프레임워크별 테스트 접근법

## 상세 핵심 내용

### HTTP 클라이언트 테스팅
- **네트워킹 문제**: 실제 서버 연결 시 느린 속도와 플래키 테스트 발생
- **requests-mock**: requests 라이브러리 기반 HTTP 요청을 가짜 응답으로 대체
- **Mocker 컨텍스트**: `requests_mock.Mocker()`로 HTTP 요청을 가로채어 미리 정의된 응답 제공
- **성능 개선**: 실제 네트워킹 없이 밀리초 단위의 빠른 테스트 실행

### WSGI 프로토콜과 WebTest
- **WSGI**: Web Server Gateway Interface, Python 웹 애플리케이션과 서버 간 표준 인터페이스
- **순수 Python**: 메모리 내에서 함수 호출을 통한 빠른 통신
- **기본 구조**: environ과 start_response 매개변수를 받는 callable 객체
- **WebTest**: WSGI 애플리케이션을 네트워킹 없이 테스트할 수 있는 라이브러리

### HTTPClient 구현
- **HTTP 메서드**: GET, POST, DELETE 지원
- **URL 탐색**: follow() 메서드로 상대 경로 탐색
- **requests 의존성**: requests 라이브러리를 활용한 HTTP 요청 처리
- **명령행 인터페이스**: sys.argv 파싱을 통한 CLI 도구 구현

### WSGI 애플리케이션 구조
- **Application 클래스**: `__call__` 메서드로 WSGI 인터페이스 구현
- **environ**: 요청 정보를 담은 환경 변수 딕셔너리
- **start_response**: HTTP 상태 코드와 헤더를 설정하는 콜백 함수
- **응답 반환**: UTF-8로 인코딩된 바이트 문자열의 이터러블

## 상세 내용

### HTTPClient 기본 구현
```python
import urllib.parse
import requests

class HTTPClient:
    def __init__(self, url):
        self._url = url

    def GET(self):
        return requests.get(self._url).text

    def POST(self, **kwargs):
        return requests.post(self._url, data=kwargs).text

    def DELETE(self):
        return requests.delete(self._url).text

    def follow(self, path):
        baseurl = self._url
        if not baseurl.endswith("/"):
            baseurl += "/"
        return HTTPClient(urllib.parse.urljoin(baseurl, path))
```

### requests-mock 사용법
```python
import requests_mock

def test_GET(self):
    client = HTTPClient(url="http://httpbin.org/get")
    with requests_mock.Mocker() as m:
        m.get(client._url,
              text='{"Host": "httpbin.org", "args": {}}')
        response = client.GET()
    assert '"Host": "httpbin.org"' in response
```

### WSGI 애플리케이션 예제
```python
class Application:
    def __call__(self, environ, start_response):
        start_response(
            '200 OK',
            [('Content-type', 'text/plain; charset=utf-8')]
        )
        return ["Hello World".encode("utf-8")]
```

### WebTest 사용법
```python
import webtest
from wsgiwebtest import Application

def test_GET(self):
    client = webtest.TestApp(Application())
    response = client.get("http://httpbin.org/get").text
    assert '"Host": "httpbin.org"' in response
```

## 주요 화제

### 1. HTTP 클라이언트 테스트 전략
- 실제 서버 연결의 한계와 문제점
- requests-mock을 통한 가짜 응답 생성
- 테스트 속도 향상 (1.37초 → 0.03초)
- 네트워크 의존성 제거로 안정적인 테스트

### 2. WSGI 프로토콜의 이해
- Python 웹 애플리케이션의 표준 인터페이스
- environ 딕셔너리를 통한 요청 정보 전달
- start_response 콜백을 통한 응답 헤더 설정
- 메모리 내 통신을 통한 빠른 처리

### 3. WebTest를 활용한 통합 테스트
- 클라이언트-서버 통신을 네트워킹 없이 테스트
- TestApp을 통한 WSGI 애플리케이션 테스트
- 실제 HTTP 요청과 동일한 인터페이스 제공
- 도메인에 관계없이 애플리케이션 테스트 가능

### 4. 웹 프레임워크별 테스트 접근법
- Django 테스트 클라이언트 활용
- Flask, Pyramid, TurboGears2 등 다양한 프레임워크 지원
- 각 프레임워크별 특화된 테스트 도구와 방법론
- 프레임워크별 테스트와 일반적인 WSGI 테스트의 차이점

## 부차 화제

### 1. 명령행 도구 구현
- **sys.argv 파싱**: 명령행 인수를 HTTP 메서드, URL, 매개변수로 분리
- **에러 처리**: ValueError를 통한 잘못된 인수 처리
- **매개변수 형식**: "name=value" 형식의 매개변수를 딕셔너리로 변환

### 2. 패키지 구조와 설치
- **src 디렉토리**: 소스 코드와 설정 파일 구조화
- **__main__.py**: python -m 명령어로 실행 가능한 모듈
- **setup.py**: pip install -e로 개발 모드 설치
- **setuptools**: 패키지 설정과 의존성 관리

### 3. httpbin.org 활용
- **테스트 서비스**: HTTP 요청을 에코하는 온라인 서비스
- **응답 검증**: 요청한 데이터가 올바르게 서버에 전달되었는지 확인
- **JSON 응답**: 구조화된 응답을 통한 세밀한 검증

### 4. wsgiref 모듈 활용
- **표준 라이브러리**: Python 내장 WSGI 참조 구현
- **make_server**: 간단한 WSGI 서버 생성
- **개발 환경**: 프로덕션이 아닌 개발과 테스트용

### 5. 테스트 성능 최적화
- **실행 시간 비교**: 실제 네트워킹 vs 가짜 응답
- **플래키 테스트 제거**: 네트워크 문제로 인한 불안정성 해결
- **확장성**: 대규모 테스트 스위트에서의 성능 고려

### 6. 통합 테스트의 한계와 해결책
- **클라이언트-서버 동기화**: 가짜 응답과 실제 서버 응답의 차이
- **API 변경 감지**: 서버 응답 변경 시 클라이언트 호환성 문제
- **WSGI를 통한 해결**: 실제 서버 로직을 네트워킹 없이 테스트
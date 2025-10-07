# 12장: Robot Framework를 활용한 End-to-End 테스팅 - 추출된 정보

## 핵심 내용
- Robot Framework를 사용한 웹 브라우저 기반 End-to-End 테스팅
- SeleniumLibrary를 통한 실제 브라우저 제어
- 자연어 기반 테스트 스크립트 작성
- 웹 애플리케이션의 JavaScript와 CSS 동작 검증

## 상세 핵심 내용

### Robot Framework 소개
- **자동화 프레임워크**: ATDD(Acceptance Test Driven Development)와 BDD(Behavior Driven Development) 스타일 지원
- **자연어 기반**: 영어와 유사한 자연어로 테스트 작성
- **PyTest 대체**: PyTest 기반이 아닌 독립적인 테스트 프레임워크
- **Nokia 개발**: 오픈소스로 발전한 안정적이고 검증된 솔루션

### .robot 파일 구조
- ***** Settings *****: Robot Framework 설정과 라이브러리 임포트
- ***** Variables *****: 여러 테스트에서 재사용할 변수 정의
- ***** Test Cases *****: 실제 테스트 케이스들
- ***** Keywords *****: 사용자 정의 명령어 정의

### 기본 라이브러리와 확장
- **Builtin 라이브러리**: 기본 제공되는 라이브러리 (Should Contain, Expression 등)
- **OperatingSystem 라이브러리**: 파일, 디렉토리, 시스템 셸과 상호작용
- **SeleniumLibrary**: 웹 브라우저 제어를 위한 라이브러리
- **webdrivermanager**: 브라우저 드라이버 자동 설치 및 관리

### 웹 브라우저 테스팅
- **실제 브라우저**: Chrome, Firefox 등 실제 브라우저에서 테스트 실행
- **JavaScript 지원**: WebTest로 불가능한 JavaScript 동작 테스트
- **CSS 검증**: CSS로 숨겨진 요소나 비활성화된 버튼 등 UI 상태 검증
- **크로스 브라우저**: 주요 브라우저에서의 호환성 테스트

## 상세 내용

### 기본 Robot Framework 테스트 예제
```robot
*** Settings ***
Library     OperatingSystem

*** Test Cases ***
Hello World
    Run    echo "Hello World" > hello.txt
    ${filecontent} =    Get File    hello.txt
    Should Contain    ${filecontent}    Hello
```

### 웹 브라우저 테스트 예제
```robot
*** Settings ***
Library SeleniumLibrary

*** Test Cases ***
Search On Google
     Open Browser    http://www.google.com    Chrome
     Wait Until Page Contains Element    cnsw
     Select Frame    //iframe
     Submit Form    //form
     Input Text    name=q    Stephen\ Hawking
     Press Keys    name=q    ENTER
     Page Should Contain    Wikipedia
     Close Window
```

### 브라우저 드라이버 설치
```bash
$ webdrivermanager firefox chrome
Downloading WebDriver for browser: "firefox"
Driver binary downloaded to: "./venv/WebDriverManager/gecko/..."
Symlink created: ./venv/bin/geckodriver
```

### 테스트 실행 및 결과
```bash
$ robot searchgoogle.robot
=======================================================
Searchgoogle
=======================================================
Search On Google                               | PASS |
-------------------------------------------------------
1 critical test, 1 passed, 0 failed
```

## 주요 화제

### 1. End-to-End 테스트의 필요성
- WebTest의 한계: JavaScript와 CSS 동작 검증 불가
- 실제 사용자 환경: 복잡한 레이아웃과 브라우저별 차이 검증
- 중요 경로 검증: 애플리케이션의 핵심 기능에 대한 실제 브라우저 테스트
- 품질 보장: 단위 테스트와 통합 테스트로 커버하지 못하는 영역

### 2. Robot Framework의 장점
- 자연어 기반 문법으로 비개발자도 이해 가능한 테스트
- 풍부한 라이브러리 생태계와 확장성
- Nokia에서 개발되어 오픈소스로 발전한 안정성
- 모바일(Appium)과 웹(Selenium) 모두 지원

### 3. SeleniumLibrary 활용
- Open Browser, Close Window 등 브라우저 생명주기 관리
- Input Text, Press Keys 등 사용자 입력 시뮬레이션
- Wait Until Page Contains Element 등 동적 콘텐츠 대기
- Page Should Contain 등 페이지 상태 검증

### 4. 테스트 실행과 디버깅
- robot 명령어를 통한 테스트 실행
- log.html 파일을 통한 상세한 실행 로그
- 실패 시 정확한 오류 메시지와 위치 정보
- 브라우저 창을 통한 시각적 테스트 진행 확인

## 부차 화제

### 1. 가상 환경과 의존성 관리
- **Python 가상 환경**: 브라우저 드라이버는 가상 환경별로 설치 필요
- **pip 설치**: robotframework, robotframework-seleniumlibrary 등
- **webdrivermanager**: 브라우저별 드라이버 자동 다운로드 및 심링크 생성

### 2. Robot Framework 문법 특징
- **공백 구분**: 여러 공백으로 명령어와 인수 구분
- **변수 문법**: ${variable} 형태로 변수 사용
- **이스케이프**: 공백이 포함된 문자열은 백슬래시로 이스케이프
- **섹션 헤더**: *** 로 구분되는 섹션 구조

### 3. 웹 요소 선택과 조작
- **name 속성**: name=q 형태로 HTML 요소 선택
- **XPath**: //iframe, //form 등 XPath 표현식 사용
- **프레임 선택**: Select Frame으로 iframe 내부 접근
- **폼 제출**: Submit Form으로 폼 자동 제출

### 4. 브라우저별 고려사항
- **Chrome, Firefox**: 주요 브라우저 지원
- **개인정보 정책**: Google 등 사이트의 개인정보 정책 팝업 처리
- **지역별 차이**: 국가별로 다른 웹사이트 동작 고려
- **헤드리스 모드**: UI 없는 브라우저 실행 옵션

### 5. 테스트 안정성과 성능
- **느린 실행 속도**: 실제 브라우저 사용으로 인한 속도 저하
- **플래키 테스트**: 네트워크 지연, 페이지 로딩 시간 등으로 인한 불안정성
- **Wait 전략**: 동적 콘텐츠 로딩 대기를 위한 적절한 대기 전략
- **테스트 비율**: 대부분은 단위/통합 테스트, 소수만 E2E 테스트

### 6. 로깅과 리포팅
- **log.html**: 각 명령어별 상세 실행 로그
- **report.html**: 테스트 결과 요약 보고서
- **스크린샷**: 실패 시 자동 스크린샷 캡처
- **비디오 녹화**: robotframework-screencaplibrary를 통한 테스트 실행 녹화

### 7. 모바일 테스팅 확장
- **Appium 라이브러리**: 모바일 애플리케이션 테스트 지원
- **실제 디바이스**: 실제 모바일 기기에서의 테스트 실행
- **크로스 플랫폼**: iOS, Android 모두 지원
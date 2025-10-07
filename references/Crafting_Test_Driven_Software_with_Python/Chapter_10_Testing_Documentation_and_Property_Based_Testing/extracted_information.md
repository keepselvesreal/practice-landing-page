# 10장: 문서 테스팅과 속성 기반 테스팅 - 추출된 정보

## 핵심 내용
- Sphinx와 doctest를 활용한 문서 테스팅
- Hypothesis를 사용한 속성 기반 테스팅
- 코너 케이스와 극한 값에서의 버그 탐지
- 문서와 코드의 동기화 보장

## 상세 핵심 내용

### 문서 테스팅
- **문서의 중요성**: 복잡한 시스템에서 팀원 온보딩과 시스템 탐색을 위한 필수 요소
- **문서의 문제점**: 작성 어려움과 코드 변화에 따른 빠른 노후화
- **해결책**: doctest를 통한 문서 예제의 자동 검증
- **Sphinx**: Python에서 가장 일반적인 문서화 도구, reStructuredText 형식 기반

### Sphinx 설정과 구성
- **sphinx-quickstart**: 새 문서 프로젝트 생성 명령어
- **확장 기능**: `--ext-doctest --ext-autodoc` 옵션으로 테스트 가능한 문서와 자동 문서 생성 활성화
- **autoclass 지시어**: 코드의 docstring을 기반으로 자동 참조 문서 생성
- **toctree**: 문서 섹션 구조화를 위한 지시어

### doctest 지시어들
- **testsetup**: 테스트 실행 전 필요한 설정 코드
- **testcode**: 실행되고 검증되는 코드 블록
- **testoutput**: 이전 testcode 블록의 예상 출력
- **code-block vs testcode**: 전자는 형식만, 후자는 실행 가능성까지 검증

### 속성 기반 테스팅
- **기본 원리**: 오류는 주로 코너 케이스와 극한 값에서 발생
- **Hypothesis**: Python에서 속성 기반 테스팅을 구현하는 라이브러리
- **불변성**: 함수나 메서드가 항상 유지해야 하는 속성들
- **자동 테스트 생성**: 함수 인수의 도메인을 기반으로 테스트 자동 생성

## 상세 내용

### Sphinx 문서 구조 예제
```rst
Welcome to Contacts's documentation!
===============================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   contacts
   reference
```

### autoclass 사용법
```rst
==============
Code Reference
==============

.. autoclass:: contacts.Application
    :members:
```

### doctest 예제
```rst
Manage Contacts
===============

.. testsetup::
    from contacts import Application
    app = Application()

Adding Contacts
================

.. testcode::
    app.run("contacts add Name 0123456789")

Listing Contacts
================

.. testcode::
    app.run("contacts ls")

.. testoutput::
    Name 0123456789
```

### Hypothesis 사용법
```python
import hypothesis
import hypothesis.strategies as st

@hypothesis.given(st.text())
def test_adding_contacts(name):
    app = Application()
    app.run(f"contacts add {name} 3456789")
    name = name.strip()
    if name:
        assert app._contacts == [(name, "3456789")]
    else:
        assert app._contacts == []
```

## 주요 화제

### 1. 문서와 코드의 동기화
- 코드 변경 시 문서 업데이트 누락 문제
- doctest를 통한 문서 예제의 자동 검증
- make doctest 명령으로 문서 테스트 실행
- CI 파이프라인에 문서 테스트 통합

### 2. 자동 문서 생성
- 코드 docstring을 기반으로 한 참조 문서 자동 생성
- autoclass, automodule 등의 지시어 활용
- 코드 구조 변경 시 문서 구조 자동 반영
- 사용자 가이드와 API 참조의 분리

### 3. 속성 기반 테스팅의 효과
- 개발자가 놓칠 수 있는 코너 케이스 자동 탐지
- parametrize 데코레이터 대비 더 포괄적인 테스트
- 실제 버그 발견과 불완전한 테스트 개선
- 테스트 실행 속도와 효과성의 균형

### 4. 공통 속성 테스트 생성
- hypothesis write 명령을 통한 자동 테스트 생성
- 멱등성(idempotent), 왕복(roundtrip), 동등성(equivalent) 테스트
- 리팩터링과 성능 최적화 시 동작 보장
- 타입 힌트를 활용한 적절한 테스트 생성

## 부차 화제

### 1. Sphinx 확장과 설정
- **doctest 확장**: 문서 내 코드 블록의 실행과 검증
- **autodoc 확장**: 소스 코드에서 자동 문서 생성
- **빌드 명령어**: make html (문서 빌드), make doctest (문서 테스트)

### 2. docstring 작성 방법
- **클래스 docstring**: 클래스의 목적과 사용법 설명
- **메서드 docstring**: 매개변수, 반환값, 예외 사항 명시
- **reStructuredText 형식**: Sphinx와 호환되는 문서 형식

### 3. Hypothesis 전략과 생성기
- **st.text()**: 임의의 텍스트 문자열 생성
- **st.integers()**: 정수 값 생성
- **st.booleans()**: 불린 값 생성
- **전략 조합**: one_of, iterables 등으로 복합 데이터 타입 생성

### 4. 오류 처리와 예외 관리
- **ValueError 처리**: 입력 파싱 실패 시 적절한 오류 메시지
- **빈 문자열 처리**: 공백 문자열 입력에 대한 검증
- **rsplit 사용**: 이름과 번호 분리 시 maxsplit 매개변수 활용

### 5. 테스트 최적화 기법
- **Hypothesis의 지능적 선택**: 문제를 자주 일으키는 값들 우선 테스트
- **과거 실패 기억**: 이전에 문제를 일으켰던 값들 재사용
- **테스트 속도와 효과성**: 무한한 도메인에서 효율적인 테스트 범위 선택

### 6. CI/CD 통합 전략
- **문서 빌드 자동화**: 코드 변경 시 문서 자동 빌드 및 검증
- **실패 감지**: 문서 예제 실패 시 빌드 중단
- **품질 게이트**: 문서 테스트를 릴리스 조건에 포함
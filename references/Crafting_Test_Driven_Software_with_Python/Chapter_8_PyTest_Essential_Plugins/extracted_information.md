# 8장: PyTest 필수 플러그인 - 추출된 정보

## 핵심 내용
- PyTest의 주요 플러그인들을 활용한 테스트 최적화
- 코드 커버리지 측정과 보고
- 성능 벤치마킹과 플래키 테스트 관리
- 테스트 자동화와 병렬 처리

## 상세 핵심 내용

### pytest-cov: 커버리지 리포팅
- **코드 커버리지**: 테스트가 실행하는 코드의 비율 측정
- **pytest-cov 설치**: `pip install pytest-cov`
- **사용법**: `pytest --cov=package_name`으로 특정 패키지의 커버리지 측정
- **미실행 라인 확인**: `--cov-report=term-missing` 옵션으로 실행되지 않은 라인 확인

### pytest-benchmark: 성능 벤치마킹
- **벤치마크 테스트**: 성능 측정을 위한 자동화된 테스트
- **benchmark fixture**: pytest-benchmark에서 제공하는 성능 측정 도구
- **다중 실행**: 안정적인 결과를 위해 함수를 여러 번 실행 후 통계 제공
- **비교 기능**: `--benchmark-autosave`와 `--benchmark-compare`로 이전 실행과 비교

### flaky: 불안정한 테스트 관리
- **플래키 테스트**: 때때로 무작위로 실패하는 테스트
- **원인**: 타이밍, 동시성, 외부 서비스 의존성 등
- **@flaky 데코레이터**: 테스트 실패 시 자동으로 재시도
- **설정**: `--max-runs` 옵션으로 최대 재시도 횟수 설정

### pytest-testmon: 코드 변경 기반 테스트 실행
- **선택적 테스트 실행**: 변경된 코드와 관련된 테스트만 실행
- **관계 그래프**: 코드와 테스트 간의 의존성 그래프 구축
- **효율성**: 전체 테스트 스위트 실행 시간 단축
- **사용법**: `--testmon` 옵션으로 활성화

### pytest-xdist: 병렬 테스트 실행
- **병렬 처리**: 여러 워커 프로세스를 사용한 테스트 실행
- **설정**: `-n numprocesses` 옵션으로 워커 수 지정
- **자동 설정**: `-n auto`로 CPU 수에 기반한 자동 워커 수 설정
- **주의사항**: 벤치마크는 병렬 실행 시 비활성화됨

## 상세 내용

### 커버리지 보고 세부사항
```bash
# 기본 커버리지 실행
pytest --cov=contacts

# 미실행 라인과 함께 보고
pytest --cov=contacts --cov-report=term-missing

# 커버리지 제외를 위한 pragma 주석
code_line  # pragma: no cover
```

### 벤치마크 예제
```python
from contacts import Application

def test_loading(benchmark):
    app = Application()
    app._contacts = [(f"Name {n}", "number") for n in range(1000)]
    app.save()
    benchmark(app.load)
```

### 플래키 테스트 처리
```python
from flaky import flaky

@flaky
def test_appender():
    l = []
    flaky_appender(l, range(7000))
    assert l == list(range(7000))
```

### pytest.ini 설정
```ini
[pytest]
addopts = --cov=contacts --cov-report=term-missing
```

## 주요 화제

### 1. 코드 커버리지 관리
- 테스트 신뢰도 측정의 중요한 지표
- 100% 커버리지의 의미와 한계
- pragma 주석을 통한 커버리지 제외 전략
- Coveralls와 Travis CI 연동을 통한 지속적 커버리지 모니터링

### 2. 성능 측정과 모니터링
- 벤치마크 테스트의 필요성과 구현
- 성능 회귀 방지를 위한 자동화된 비교
- cprofile을 활용한 성능 병목 지점 분석
- 반복 실행을 통한 안정적인 성능 측정

### 3. 테스트 안정성 확보
- 플래키 테스트의 정의와 원인 분석
- 동시성과 타이밍 이슈로 인한 테스트 불안정성
- 격리(quarantine) 전략을 통한 릴리스 프로세스 보호
- 플래키 테스트의 근본적 해결 방안

### 4. 테스트 효율성 최적화
- 대규모 프로젝트에서의 테스트 실행 시간 문제
- 코드 변경과 테스트의 의존성 그래프 활용
- 선택적 테스트 실행을 통한 개발 속도 향상
- 병렬 처리를 통한 전체 테스트 스위트 성능 개선

## 부차 화제

### 1. 외부 서비스 통합
- **Coveralls**: GitHub 연동 커버리지 서비스
- **Travis CI**: 지속적 통합 환경에서의 커버리지 보고
- **설정 파일**: .travis.yml을 통한 자동화 구성

### 2. 플러그인 설치와 관리
- **일괄 설치**: 모든 필수 플러그인을 한 번에 설치하는 방법
- **버전 호환성**: Python 버전과 플러그인 버전 간 호환성 고려
- **의존성 관리**: pip를 통한 플러그인 설치와 관리

### 3. 개발 워크플로 최적화
- **addopts 설정**: pytest.ini를 통한 기본 옵션 설정
- **디렉토리 구조**: 벤치마크 테스트의 별도 관리
- **필터링**: -k 옵션을 통한 테스트 선택적 실행

### 4. 성능 고려사항
- **병렬 처리의 오버헤드**: 작은 테스트 스위트에서의 성능 저하 가능성
- **벤치마크 정확성**: 시스템 부하가 벤치마크 결과에 미치는 영향
- **최소 실행 횟수**: pytest-benchmark의 최소 5회 실행 정책

### 5. 테스트 격리와 상태 관리
- **테스트 독립성**: 병렬 실행을 위한 테스트 간 격리 요구사항
- **상태 의존성**: 외부 설정 파일이나 데이터베이스 상태 변경 감지의 한계
- **픽스처 활용**: 각 테스트 실행 시 새로운 상태 설정의 중요성
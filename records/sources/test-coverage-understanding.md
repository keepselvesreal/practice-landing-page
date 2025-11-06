# 테스트 커버리지 측정 이해

**작성일:** 2025-11-06
**출처:** pytest 프로젝트 구조 설계 중 커버리지 관련 대화

---

## 1. 맥락 (Context)

### 1.1 구체적 상황

**배경:**
- pytest 기반 프로젝트 구조 설계 문서 작성 중
- 테스트 커버리지를 베스트 프랙티스에 추가하는 과정
- 커버리지 측정의 기본 개념에 대한 의문 발생

**질문 발생 시점:**
- "핵심 best practice 기반으로 답변한 부분에 테스트 커버리지 관련 내용 추가" 작업 완료 후
- 커버리지가 무엇을 측정하는지, 어떻게 작동하는지에 대한 근본적 질문

### 1.2 주요 의문점

- 테스트 커버리지는 무엇을 대상으로 측정되는가?
- Walking Skeleton E2E 테스트에서 커버리지는 어떻게 측정되는가?
- `pytest --cov` 명령어만 실행하면 되는가?
- 측정 빈도와 시점은?

---

## 2. 질문-응답 (Q&A)

### 질문 1: 커버리지 측정 대상

> "작성된 모든 테스트 케이스 중 실행된 테스트 케이스를 대상으로 작성돼?"

**답변:**

❌ **잘못된 이해:** "10개 테스트 중 8개 실행 = 80% 커버리지"

✅ **올바른 이해:** "애플리케이션 코드 100줄 중 80줄이 테스트에 의해 실행됨 = 80% 커버리지"

**핵심:**
- 테스트 케이스의 실행 비율을 측정하는 것이 아님
- **애플리케이션 코드가 얼마나 실행됐는지**를 측정
- 테스트는 코드를 실행시키는 도구일 뿐

---

### 질문 2: Walking Skeleton에서의 구체적 측정

> "워킹스켈레톤 e2e 구체적이고 단순 예시로 설명해줘"

**답변:**

**애플리케이션 코드 (backend/main.py):**
```python
# 총 21줄
@app.post("/api/register")      # 라인 5
def register(email: str):        # 라인 6
    if not email:                # 라인 7
        return {"error": "필요"} # 라인 8
    if "@" not in email:         # 라인 9
        return {"error": "형식"} # 라인 10
    return {"status": "success"} # 라인 16

@app.get("/api/health")          # 라인 19
def health_check():              # 라인 20
    return {"status": "ok"}      # 라인 21
```

**E2E 테스트:**
```python
def test_user_can_register_interest(page, base_url):
    page.goto(base_url)
    page.fill("#email-input", "test@example.com")  # 유효한 이메일만
    page.click("#submit-button")
    expect(page.locator("#success-message")).to_be_visible()
```

**커버리지 측정 결과:**
```bash
pytest tests/e2e/test_walking_skeleton.py --cov=backend

Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
backend/main.py      21     5    76%   7-10, 19-21
```

**분석:**
- 총 21줄 중 16줄 실행됨 = 76%
- 누락된 5줄:
  - 라인 7-8: 빈 이메일 검증 (테스트 안 함)
  - 라인 9-10: 잘못된 형식 검증 (테스트 안 함)
  - 라인 19-21: health check 엔드포인트 (호출 안 함)

**실행 흐름:**
```
E2E 테스트 → "test@example.com" 입력
→ POST /api/register 호출
→ backend 코드 실행:
   ✅ 라인 5-6: 함수 진입
   ✅ 라인 7: if not email (False, 건너뜀)
   ❌ 라인 8: 실행 안 됨
   ✅ 라인 9: if "@" not in email (False, 건너뜀)
   ❌ 라인 10: 실행 안 됨
   ✅ 라인 16: return success
   ❌ 라인 19-21: 호출 안 함
```

**커버리지 개선 방법:**
```python
# 추가 테스트 작성 → 누락된 라인 실행

def test_rejects_empty_email():        # → 라인 7-8 커버
    page.fill("#email-input", "")

def test_rejects_invalid_email():      # → 라인 9-10 커버
    page.fill("#email-input", "invalid")

def test_health_check_endpoint():      # → 라인 19-21 커버
    response = page.request.get("/api/health")
```

**개선 후 커버리지:**
```bash
Coverage: 100%  (21/21줄 모두 실행됨)
```

---

### 질문 3: 측정 방법

> "테스트 코드 작성은 평소처럼 하면 되고 pytest --cov 명령어만 수행하면 되는 거야?"

**답변:**

**기본 사용:**
```bash
# 1. 설치
pip install pytest-cov

# 2. 실행
pytest --cov=backend

# → 끝! 자동으로 측정됨
```

**실전 설정 (pytest.ini):**
```ini
[pytest]
addopts =
    --cov=backend
    --cov-report=term-missing
    --cov-report=html
```

**설정 후:**
```bash
pytest  # 자동으로 커버리지 측정
```

**핵심:**
- 테스트 코드는 평소처럼 작성
- `--cov` 옵션만 추가하면 자동 측정
- pytest.ini에 설정하면 매번 자동 적용

---

### 질문 4: 측정 빈도

> "테스트 커버리지는 어떻게 해야 측정되는 거야? 보통 언제 테스트 커버리지를 측정하고 이를 어떻게 측정해? 이 측정 빈도는 얼마나 돼?"

**답변:**

**측정 시점 및 빈도:**

| 환경 | 빈도 | 목적 | 방법 |
|------|------|------|------|
| **로컬 개발** | 필요 시 (선택적) | 현재 작업 확인 | `pytest --cov` |
| **CI/CD** | **매 커밋마다 (자동)** | 지속적 모니터링 | 파이프라인 설정 |
| **PR 리뷰** | PR마다 (자동) | 변경 영향 확인 | 자동 코멘트 |
| **릴리스** | 필수 | 최종 검증 | Quality Gate |

**로컬 개발:**
```bash
# 가끔 실행 (수동)
pytest --cov

# 변경 사항만 확인
pytest --lf --cov
```

**CI/CD (GitHub Actions):**
```yaml
# 매 푸시마다 자동 실행
- name: Run tests with coverage
  run: |
    pytest --cov=backend \
           --cov-report=xml \
           --cov-fail-under=80

# PR에 자동 코멘트
- name: Coverage comment
  uses: py-cov-action/python-coverage-comment-action@v3
```

**현업 기준:**
- **신규 프로젝트:** 80%+ 목표
- **레거시:** 60%+ (점진적 증가)
- **Critical path:** 100% (결제, 인증 등)

**단계별 목표:**
```
Walking Skeleton:  60%+  (기본 흐름만)
MVP 단계:         75%+  (주요 기능)
Production Ready: 80%+  (엣지 케이스)
Critical Path:    95%+  (핵심 기능)
```

---

## 요약

### 핵심 개념

1. **커버리지 = 애플리케이션 코드 실행 비율**
   - 테스트 실행 비율 ❌
   - 코드 라인 실행 비율 ✅

2. **측정 원리:**
   ```
   테스트 실행 → 애플리케이션 코드 실행
   → 실행된 라인 추적
   → 실행 라인 / 전체 라인 = 커버리지
   ```

3. **Walking Skeleton 예시:**
   - 첫 E2E 테스트: 50-70% (성공 경로만)
   - 점진적 증가: 기능 추가하면서 자연스럽게
   - 목표: 80%+ (완벽한 100%는 불필요)

4. **사용 방법:**
   ```bash
   # 설치
   pip install pytest-cov

   # 실행
   pytest --cov=backend

   # 자동화 (pytest.ini 설정 후)
   pytest  # 자동 측정
   ```

5. **측정 빈도:**
   - 로컬: 필요 시 (수동)
   - CI/CD: 매 커밋 (자동)
   - 핵심: **CI/CD에서 자동으로 매번 측정**

6. **목표 설정:**
   - Walking Skeleton: 60%
   - MVP: 75%
   - Production: 80%
   - Critical: 95%

7. **품질 주의:**
   - 100% 커버리지 ≠ 완벽한 테스트
   - 80% + 의미있는 assertion > 100% 무의미한 실행

---

**참고:**
- 이 내용은 `/home/nadle/para/projects/practice-landing-page/docs/pytest-project-structure-best-practices.md` 문서의 섹션 2.4에 상세히 포함됨

# Walking Skeleton과 CI/CD First 접근법 이해

## 1. 맥락 (Context)

### 1.1 구체적인 상황

**프로젝트:**
- 랜딩페이지 MVP 개발 시작
- Outside-In TDD 방식 적용 시도

**기술 스택:**
- Frontend: HTML, Vanilla JavaScript
- Backend: FastAPI, SQLite
- 인프라: Firebase Hosting, Cloud Run
- 외부 서비스: PayPal, Google Places API

**초기 질문:**
- GOOS(Growing Object-Oriented Software) 책 Part 3에서 Walking Skeleton으로 CI/CD를 가장 먼저 구축하라는 내용 발견
- 일반적인 TDD 접근법(로컬 개발 → CI/CD 추가)과 다른 것 같은데, 구체적으로 어떻게 진행해야 하는지 불명확

### 1.2 AI 탐색 과정

**문서 확인:**
- `/home/nadle/para/projects/practice-landing-page/references/growing-object-oriented-software/toc.md` 목차 확인
- Part III "A Worked Example" 내 관련 챕터 식별
- Chapter 4 "Kick-Starting the Test-Driven Cycle" (pp.31-39) 내용 확인
- Chapter 10 "The Walking Skeleton" (pp.83-86) 상세 내용 확인

**주요 발견:**
- Chapter 4.2: "First, Test a Walking Skeleton" - 개념 정의
- Chapter 4.4: "Build Sources of Feedback" - CI/CD의 중요성
- Chapter 10.1: "Get the Skeleton out of the Closet" - 실제 구현 시작점
- Chapter 10.2: "Our Very First Test" - 구체적인 예시

### 1.3 이해의 진화

**단계 1: 초기 혼란**
- "맨 처음에 CI/CD 파이프라인을 구축한다"는 것의 의미가 모호
- 로컬에서 테스트 작성 → 통과 → CI/CD 추가하는 것과의 차이점 불분명

**단계 2: 대화를 통한 명확화**
- 질문: "E2E 테스트를 로컬에서 통과 여부를 확인하는 게 아니라, CI/CD 구성하는 인프라에서 테스트가 실행되고 최소 구현으로 통과하게 하여 이후 TDD 개발이 CI/CD로 운영되는 환경에서 실제 진행되게 하는 거야?"
- 답변: "정확해! 완벽하게 이해했어!"

## 2. 내 이해 (My Understanding)

### 2.1 초기 질문

> "outside in tdd 방식으로 개발하려 하는데, 맨 처음에 cicd 파이프라인 구축하는 단계는 어떻게 진행해?"

### 2.2 핵심 의문점

**질문 1: 순서 문제**
- E2E 테스트를 로컬에서 통과시킨 후 CI/CD를 추가하는 것인가?
- 아니면 CI/CD 환경 자체를 먼저 만들고 그 안에서 개발하는 것인가?

**질문 2: 환경 문제**
- "로컬에서 개발"과 "CI/CD 환경에서 개발"의 차이는 무엇인가?
- 왜 로컬에서 테스트 통과시키는 것으로는 부족한가?

### 2.3 도달한 핵심 이해

> **핵심은 E2E 테스트를 작성 후 로컬에서 통과 여부를 확인하는 게 아니라, CI/CD 구성하는 인프라에서 테스트가 실행되고 최소 구현으로 통과하게 하여 이후 TDD 개발이 CI/CD로 운영되는 환경에서 실제 진행되게 하는 것이다.**

**핵심 인사이트:**
- CI/CD는 "나중에 추가하는 도구"가 아니라 "개발 환경 그 자체"
- 로컬은 단지 코드를 편집하는 공간, 실제 개발/테스트는 CI/CD 환경에서
- Walking Skeleton은 "배포 가능한 최소 기능"이 아니라 "배포 프로세스 자체를 구축하는 것"

## 3. 정제 (Refined Understanding)

### 3.1 Walking Skeleton의 정의

**GOOS의 정의 (p.32):**
> "A 'walking skeleton' is an implementation of the thinnest possible slice of real functionality that we can automatically build, deploy, and test end-to-end."

**핵심 요소:**
1. **가장 얇은 조각** (thinnest possible slice)
   - 기능이 간단하다는 뜻이 아님
   - 전체 스택을 관통하는 최소한의 흐름

2. **자동으로** (automatically)
   - 수동 배포/테스트가 아님
   - 모든 과정이 자동화되어야 함

3. **빌드, 배포, 테스트** (build, deploy, and test)
   - 이 세 가지가 모두 자동화되어야 함
   - 하나라도 빠지면 진짜 Walking Skeleton이 아님

4. **End-to-End**
   - 시스템의 End-to-End (UI → Backend → DB)
   - **프로세스의 End-to-End** (코드 작성 → 빌드 → 배포 → 테스트)

**예시 (GOOS p.32):**
- 데이터베이스 기반 웹앱: DB 필드 하나를 평면 웹페이지에 표시
- Auction Sniper: UI에 값 하나 표시 + 서버에 핸드셰이크 메시지 전송

### 3.2 왜 CI/CD가 먼저인가

**1. "Unknown Unknown" 리스크 조기 발견 (GOOS p.31)**

책에서 언급한 실패 사례들:
- 몇 달 개발 후 배포를 안정적으로 못 해서 프로젝트 취소
- 새 기능 추가마다 몇 달간 수동 회귀 테스트 필요 → 높은 에러율
- DB 설정에 6주와 4개의 서명 필요하다는 걸 배포 직전에 발견

**2. 프로세스 자동화를 통한 이해 (GOOS p.32)**
> "One lesson that we've learned repeatedly is that nothing forces us to understand a process better than trying to automate it."

- 배포 과정을 자동화하려고 시도하면서 몰랐던 문제들 발견
- 시스템 관리자, 외부 벤더와의 협업 필요성 조기 파악

**3. Iteration Zero 개념 (GOOS p.33)**
- 첫 기능 개발 전 인프라 구축 단계
- 시간을 제한하되(time-box), 인프라에 집중
- Walking Skeleton으로 초기 아키텍처 테스트

**4. 불확실성의 Front-loading (GOOS p.36)**

```
일반적 프로젝트:  [평온] ──────────────────→ [혼돈]
                  시작                      배포

Incremental TDD:  [혼돈] ──────────────────→ [안정]
                  시작                      배포
```

- 초기에 불확실성을 직면하고 해결
- 배포 시점에는 이미 안정화됨

### 3.3 잘못된 접근 vs 올바른 접근

#### ❌ 일반적 방식 (로컬 중심)

```
1. 로컬에서 E2E 테스트 작성
2. 로컬에서 기능 구현
3. 로컬에서 테스트 통과 확인
4. 여러 기능 완성
5. 나중에 CI/CD 추가
6. 배포 시도 → 문제 발견 → 위기
```

**문제점:**
- 배포 환경의 제약사항을 늦게 발견
- 로컬과 프로덕션의 차이로 인한 예상치 못한 문제
- CI/CD 구축 자체가 어려워서 미루게 됨

#### ✅ GOOS 방식 (CI/CD 중심)

```
1. E2E 테스트 작성 (실패하는)
2. CI/CD 파이프라인 구축
   - 자동 빌드
   - 자동 배포
   - 자동 테스트 실행
3. 배포 환경 구축 (Firebase, Cloud Run 등)
4. 파이프라인에서 테스트 실패 확인
5. 최소 구현으로 테스트 통과
6. 파이프라인에서 테스트 통과 확인
7. ✅ Walking Skeleton 완성!
8. 이제 CI/CD 위에서 TDD 진행
```

**장점:**
- 배포 관련 문제를 첫날에 발견
- 모든 개발이 "배포 가능한 상태"에서 진행
- 피드백 루프가 실제 환경 기반

### 3.4 "End-to-End"의 진짜 의미

**GOOS p.32:**
> "It's also important to realize that the 'end' in 'end-to-end' refers to the process, as well as the system."

#### 시스템의 End-to-End (일반적 이해)
```
User Interface → API → Database
```

#### 프로세스의 End-to-End (GOOS의 핵심)
```
1. 처음부터 시작 (from scratch)
2. 배포 가능한 시스템 빌드 (build a deployable system)
3. 프로덕션 같은 환경에 배포 (deploy into production-like environment)
4. 배포된 시스템을 통해 테스트 실행 (run tests through deployed system)
```

**로컬 테스트의 한계:**
- `localhost`에서 통과 ≠ 프로덕션에서 통과
- 파일시스템, 네트워크, 권한, CORS 등의 차이
- 진짜 배포 프로세스의 문제를 발견할 수 없음

### 3.5 구체적인 실행 순서

#### Day 1: E2E 테스트 + CI/CD 파이프라인

**1) E2E 테스트 작성**
```python
# tests/e2e/test_walking_skeleton.py
def test_user_can_register_interest(page, base_url):
    # Given: 랜딩페이지가 배포되어 있고
    page.goto(base_url)

    # When: 사용자가 이메일을 입력하고 등록하면
    page.fill("#email", "test@example.com")
    page.click("#submit")

    # Then: 성공 메시지가 표시된다
    expect(page.locator(".success")).to_be_visible()
```

**2) GitHub Actions 파이프라인 작성**
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # Backend 빌드
      - name: Build FastAPI
        run: docker build -t backend ./backend

      # 로컬 서비스 시작 (테스트용)
      - name: Start services
        run: docker-compose up -d

      # E2E 테스트 실행
      - name: Run E2E tests
        run: pytest tests/e2e/

  deploy:
    needs: build-and-test
    if: github.ref == 'refs/heads/main'
    steps:
      # Firebase Hosting 배포
      - name: Deploy frontend
        run: firebase deploy --only hosting

      # Cloud Run 배포
      - name: Deploy backend
        run: gcloud run deploy ...

      # 배포된 환경에서 Smoke Test
      - name: Production smoke test
        run: pytest tests/e2e/ --base-url=${{ secrets.PRODUCTION_URL }}
```

**3) 첫 커밋 & 푸시**
```bash
git add .
git commit -m "Add walking skeleton: E2E test + CI/CD pipeline"
git push
```

→ GitHub Actions 실행 → 테스트 실패 → **예상된 결과!**

#### Day 2: 최소 구현으로 파이프라인 통과

**더미 구현:**

```python
# backend/main.py
from fastapi import FastAPI
app = FastAPI()

@app.post("/api/register")
def register(email: str):
    return {"status": "success"}
```

```html
<!-- frontend/index.html -->
<!DOCTYPE html>
<html>
<body>
  <input id="email" type="email">
  <button id="submit">Register</button>
  <div class="success" style="display:none">Success!</div>
  <script src="app.js"></script>
</body>
</html>
```

```javascript
// frontend/app.js
document.getElementById('submit').addEventListener('click', async () => {
  const email = document.getElementById('email').value;
  await fetch('/api/register', {
    method: 'POST',
    body: JSON.stringify({email})
  });
  document.querySelector('.success').style.display = 'block';
});
```

**커밋 & 푸시:**
```bash
git commit -m "Add minimal implementation to pass walking skeleton test"
git push
```

→ GitHub Actions 실행 → **테스트 통과!** → 자동 배포 → **프로덕션 URL 생성!**

#### Day 3~: CI/CD 환경 위에서 TDD

이제부터 모든 개발:

```
1. 새 기능의 E2E/Unit 테스트 작성
2. git push
3. CI/CD가 자동으로:
   - 빌드
   - 테스트 실행
   - 통과하면 배포
   - 실패하면 배포 중단
4. 피드백 확인
5. 반복
```

**중요한 점:**
- 로컬은 코드 편집만
- 실제 검증은 항상 CI/CD 환경에서
- 매 푸시마다 전체 파이프라인 실행

### 3.6 랜딩페이지 MVP에 적용

#### 가장 얇은 조각 선택

**선택한 기능: 이메일 관심 등록**
```
User 입력 → Frontend → API → SQLite 저장 → 성공 응답 → UI 업데이트
```

**Walking Skeleton 범위:**
```
┌─────────────────────────────────────────────┐
│         Walking Skeleton                    │
├─────────────────────────────────────────────┤
│                                             │
│  Frontend (Firebase Hosting)                │
│  ├─ index.html (이메일 입력 폼)             │
│  └─ app.js (API 호출)                       │
│                                             │
│  Backend (Cloud Run)                        │
│  ├─ FastAPI 앱                              │
│  ├─ POST /api/register                      │
│  └─ SQLite 저장                             │
│                                             │
│  CI/CD (GitHub Actions)                     │
│  ├─ 자동 빌드                               │
│  ├─ E2E 테스트                              │
│  ├─ Firebase 배포                           │
│  └─ Cloud Run 배포                          │
│                                             │
└─────────────────────────────────────────────┘
```

#### 조기에 발견할 수 있는 문제들

**1. Cloud Run + SQLite 문제**
- **문제**: Cloud Run은 stateless, 파일시스템이 휘발성
- **로컬**: 문제 없음 (로컬 파일로 저장)
- **CI/CD 환경에서 발견**: 재배포 시 데이터 손실
- **해결**: Cloud Storage나 Cloud SQL로 전환 필요성 조기 인식

**2. Firebase Hosting CORS**
- **문제**: Firebase에서 Cloud Run API 호출 시 CORS 에러
- **로컬**: `localhost`라서 문제 없음
- **CI/CD 환경에서 발견**: 실제 도메인 간 통신에서 에러
- **해결**: Cloud Run에 CORS 설정 추가

**3. 환경변수 관리**
- **문제**: API 키, DB 연결 정보 관리
- **로컬**: `.env` 파일
- **CI/CD 환경에서 발견**: Secret Manager 설정 필요
- **해결**: GitHub Secrets + Cloud Run Secret Manager 구성

**4. PayPal, Google Places API**
- **문제**: API 도메인 검증, 권한 설정
- **로컬**: 테스트 키로 가능
- **CI/CD 환경에서 발견**: 프로덕션 도메인 등록 필요
- **해결**: 사전에 도메인 검증 및 API 설정 완료

**5. SQLite 백업 to GCloud**
- **문제**: 백업 스크립트가 실제로 동작하는가
- **로컬**: 테스트 어려움
- **CI/CD 환경에서 발견**: 권한, 경로, 타이밍 문제
- **해결**: 배포 파이프라인에 백업 프로세스 포함

### 3.7 핵심 인사이트 정리

#### 1. CI/CD는 도구가 아니라 환경

**잘못된 인식:**
> "CI/CD는 나중에 추가하는 편의 도구다"

**올바른 인식:**
> "CI/CD는 개발이 이루어지는 환경 그 자체다"

#### 2. 로컬의 역할 재정의

**Before:**
- 로컬 = 개발 + 테스트 + 검증
- CI/CD = 자동화된 재검증

**After (GOOS 방식):**
- 로컬 = 코드 편집
- CI/CD = 개발 + 테스트 + 검증 + 배포

#### 3. Walking Skeleton ≠ MVP

**Walking Skeleton:**
- 목적: 인프라와 프로세스 검증
- 기능: 의미 없을 정도로 단순 (DB 값 하나 표시)
- 완성 시점: 며칠 ~ 1주

**MVP:**
- 목적: 시장 검증, 사용자 피드백
- 기능: 최소한이지만 가치 있는 기능
- 완성 시점: 몇 주 ~ 몇 달

#### 4. "Test First"의 확장

**Unit Test First:**
```
Test 작성 → 구현 → 테스트 통과 → 리팩토링
```

**Infrastructure First:**
```
E2E Test 작성 → CI/CD 구축 → 구현 → 파이프라인 통과 → 기능 추가
```

#### 5. 피드백 루프의 현실화

**로컬 기반:**
```
코드 변경 → 로컬 테스트 → ✓ 통과 → 배포 → ✗ 프로덕션 에러
```

**CI/CD 기반:**
```
코드 변경 → git push → CI/CD 테스트 → ✓/✗ 즉각 피드백
```

## 결론

**Walking Skeleton + CI/CD First 접근법의 본질:**

1. **개발 환경 = 배포 환경**
   - 로컬은 단지 편집 도구
   - 실제 개발은 CI/CD 파이프라인에서

2. **인프라가 코드보다 먼저**
   - 기능을 만들기 전에 빌드/배포/테스트 자동화
   - "Unknown unknown" 문제들을 조기에 발견

3. **프로세스의 End-to-End**
   - 시스템만이 아니라 프로세스도 end-to-end
   - 코드 작성 → 빌드 → 배포 → 테스트 전체가 자동화

4. **불확실성의 Front-loading**
   - 초기에 혼돈을 겪고, 나중에 안정
   - 배포 시점에는 이미 모든 프로세스가 검증됨

**다음 단계:**
- E2E 테스트 작성
- GitHub Actions 파이프라인 구축
- Firebase + Cloud Run 배포 자동화
- 더미 구현으로 Walking Skeleton 완성
- 실제 기능 TDD 시작

---

*작성일: 2025-11-06*
*출처: Growing Object-Oriented Software, Guided by Tests (GOOS) - Part II, Chapter 4 & Part III, Chapter 10*

# GitHub Actions CI/CD 설정 가이드

## 📋 목차
1. [GitHub Secrets 설정](#1-github-secrets-설정)
2. [GitHub Environments 설정](#2-github-environments-설정)
3. [Firebase 설정](#3-firebase-설정-선택사항)
4. [워크플로우 사용법](#4-워크플로우-사용법)
5. [트러블슈팅](#5-트러블슈팅)

---

## 1. GitHub Secrets 설정

### Settings → Secrets and variables → Actions → New repository secret

#### 필수 Secrets:

| Secret 이름 | 설명 | 예시 |
|-------------|------|------|
| `GOOGLE_PLACES_API_KEY` | Google Places API 키 (E2E 테스트 필수) | `AIzaSyB...` |
| `PAYPAL_API_BASE` | PayPal API 베이스 URL | `https://api-m.sandbox.paypal.com` |
| `PAYPAL_CLIENT_ID` | PayPal 클라이언트 ID | `Ad4mhU...` |
| `PAYPAL_CLIENT_SECRET` | PayPal 클라이언트 시크릿 | `EBWKj...` |
| `GMAIL_ADDRESS` | Gmail 주소 (이메일 발송용) | `your-email@gmail.com` |
| `GMAIL_APP_PASSWORD` | Gmail 앱 비밀번호 | `abcd efgh ijkl mnop` |
| `SMTP_HOST` | SMTP 호스트 | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP 포트 | `587` |

#### Firebase 배포용 (선택):

| Secret 이름 | 설명 | 획득 방법 |
|-------------|------|----------|
| `FIREBASE_SERVICE_ACCOUNT_STAGING` | Staging 서비스 계정 | Firebase Console → Project Settings → Service Accounts |
| `FIREBASE_SERVICE_ACCOUNT_PROD` | Production 서비스 계정 | 동일 |
| `FIREBASE_PROJECT_ID` | Firebase 프로젝트 ID | Firebase Console 확인 |

---

## 2. GitHub Environments 설정

### Settings → Environments → New environment

#### 2.1 Staging Environment 생성

1. **이름**: `staging`
2. **Deployment protection rules**:
   - ✅ Required reviewers: (선택사항)
   - ✅ Wait timer: 0 minutes
3. **Environment secrets**: (Staging 전용 secrets 추가 가능)

#### 2.2 Production Environment 생성

1. **이름**: `production`
2. **Deployment protection rules**:
   - ✅ **Required reviewers**: ⭐ 중요!
     - 본인 또는 팀원 추가
     - 최소 1명 이상의 승인 필요
   - ✅ Wait timer: 5 minutes (선택사항)
   - ✅ Allowed branches: `main` only
3. **Environment secrets**: (Production 전용 secrets)

### 승인 프로세스:

```
1. 운영 배포 워크플로우 시작
2. GitHub이 자동으로 대기 상태로 전환
3. 지정된 승인자에게 알림
4. 승인자가 "Review deployments" 클릭
5. 승인 또는 거부
6. 승인 시 배포 계속 진행
```

---

## 3. Firebase 설정 (선택사항)

### 3.1 Firebase CLI 설치 (로컬)

```bash
npm install -g firebase-tools
firebase login
```

### 3.2 Firebase 초기화

```bash
# 프로젝트 루트에서
firebase init hosting

# 선택:
# - Hosting: Configure files for Firebase Hosting
# - Use an existing project
# - Public directory: frontend
# - Configure as single-page app: Yes
# - Set up automatic builds with GitHub: No (워크플로우로 관리)
```

### 3.3 firebase.json 생성

```json
{
  "hosting": [
    {
      "target": "staging",
      "public": "frontend",
      "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
      "rewrites": [
        {
          "source": "/api/**",
          "function": "api"
        },
        {
          "source": "**",
          "destination": "/index.html"
        }
      ]
    },
    {
      "target": "production",
      "public": "frontend",
      "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
      "rewrites": [
        {
          "source": "/api/**",
          "function": "api"
        },
        {
          "source": "**",
          "destination": "/index.html"
        }
      ]
    }
  ]
}
```

### 3.4 Service Account 키 생성

```bash
# Firebase Console
# → Project Settings
# → Service Accounts
# → Generate New Private Key
# → JSON 파일 다운로드

# GitHub Secrets에 등록:
# - FIREBASE_SERVICE_ACCOUNT_STAGING: JSON 파일 내용 전체
# - FIREBASE_SERVICE_ACCOUNT_PROD: JSON 파일 내용 전체
```

---

## 4. 워크플로우 사용법

### 4.1 자동 CI (빌드 & 테스트)

**트리거**: PR 생성 또는 푸시

```bash
# PR 생성 시 자동 실행
git checkout -b feature/new-feature
git push origin feature/new-feature
# → GitHub에서 PR 생성
# → ci.yml 자동 실행
```

### 4.2 스테이징 배포

**트리거**: `main` 브랜치에 푸시

```bash
# main에 머지
git checkout main
git merge feature/new-feature
git push origin main
# → deploy-staging.yml 자동 실행
# → 스테이징 환경 배포
# → 스테이징 테스트 자동 실행
```

### 4.3 운영 배포 (수동 승인)

**트리거**: 수동 실행 (workflow_dispatch)

```bash
# GitHub UI에서:
# 1. Actions 탭 이동
# 2. "Deploy to Production" 워크플로우 선택
# 3. "Run workflow" 클릭
# 4. Version 입력 (e.g., v1.0.0)
# 5. "Run workflow" 확인

# ⏸️ Waiting for approval...
# 📧 승인자에게 알림 발송
# ✅ 승인자가 "Approve" 클릭
# 🚀 운영 배포 시작
# ✅ 스모크 테스트 실행
# 🎉 배포 완료!
```

---

## 5. 트러블슈팅

### 문제 1: Docker 서비스가 healthy 상태가 안 됨

**증상:**
```
Error: Timeout waiting for services to be healthy
```

**해결:**
```bash
# 로컬에서 테스트
docker compose -f docker-compose.test.yml up

# 로그 확인
docker compose -f docker-compose.test.yml logs backend

# healthcheck 확인
docker compose -f docker-compose.test.yml ps
```

### 문제 2: Playwright 브라우저 설치 실패

**증상:**
```
Error: Executable doesn't exist at /root/.cache/ms-playwright/...
```

**해결:**
```yaml
# ci.yml에 추가
- name: Install system dependencies
  run: |
    sudo apt-get update
    sudo apt-get install -y \
      libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
      libcups2 libdrm2 libxkbcommon0 libxcomposite1 \
      libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2
```

### 문제 3: 환경변수 누락

**증상:**
```
ValueError: TEST_ENV environment variable must be set
```

**해결:**
```yaml
# 워크플로우 파일에서 env 섹션 확인
env:
  TEST_ENV: docker
  GOOGLE_PLACES_API_KEY: ${{ secrets.GOOGLE_PLACES_API_KEY }}
```

### 문제 4: Firebase 배포 실패

**증상:**
```
Error: Service account key is invalid
```

**해결:**
```bash
# Service Account JSON이 올바른지 확인
# GitHub Secrets에 JSON 전체 내용이 들어갔는지 확인
# (공백, 줄바꿈 포함 전체)

# 또는 Firebase CLI로 직접 테스트
firebase deploy --only hosting:staging
```

---

## 6. 워크플로우 흐름도

```
┌─────────────────┐
│   Code Push     │
└────────┬────────┘
         │
    ┌────▼────┐
    │ CI Test │ ← PR/Push to any branch
    └────┬────┘
         │ ✅ Pass
         │
    ┌────▼─────────┐
    │ Push to main │
    └────┬─────────┘
         │
    ┌────▼──────────────┐
    │ Deploy to Staging │ ← 자동
    └────┬──────────────┘
         │
    ┌────▼────────────────┐
    │ Test Staging        │
    └────┬────────────────┘
         │ ✅ Pass
         │
    ┌────▼─────────────────┐
    │ Manual Trigger       │ ← 수동
    └────┬─────────────────┘
         │
    ┌────▼─────────────────┐
    │ ⏸️ Awaiting Approval │ ← 승인 대기
    └────┬─────────────────┘
         │ ✅ Approved
         │
    ┌────▼───────────────────┐
    │ Deploy to Production   │
    └────┬───────────────────┘
         │
    ┌────▼────────────┐
    │ Smoke Test      │
    └────┬────────────┘
         │ ✅ Pass
         │
    ┌────▼─────┐
    │ Success! │
    └──────────┘
```

---

## 7. 비용 고려사항

### GitHub Actions 무료 티어:
- Public 저장소: 무제한
- Private 저장소: 월 2,000분

### 예상 사용량 (Private 저장소 기준):
- CI 워크플로우: ~10분/실행
- 스테이징 배포: ~5분/실행
- 운영 배포: ~7분/실행

**월 예상:**
- 하루 10번 커밋 × 10분 × 30일 = 3,000분
- → Free tier 초과 가능 → Pro 플랜 필요 ($4/월)

---

## 8. 다음 단계

- [ ] GitHub Secrets 모두 등록
- [ ] Environments 설정 (승인자 지정)
- [ ] Firebase 프로젝트 생성 (또는 다른 호스팅)
- [ ] 첫 번째 배포 테스트 (Staging)
- [ ] 운영 배포 리허설
- [ ] 롤백 프로세스 문서화
- [ ] 모니터링 설정 (Sentry, LogRocket 등)

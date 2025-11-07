---
version: 1
created_date: 25-11-07 15:38
note:
---

## 메모

### 개발 도구 설치

#### 필수 도구
```bash
# Python 3.11+ 설치 확인
python --version  # 3.11 이상이어야 함

# uv 설치 (의존성 관리)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version

# Docker Desktop 설치 (로컬 PostgreSQL용)
# https://www.docker.com/products/docker-desktop/
docker --version
docker-compose --version

# Firebase CLI 설치
npm install -g firebase-tools
firebase --version

# gcloud CLI 설치
# https://cloud.google.com/sdk/docs/install
gcloud --version
```

---

### 외부 서비스 계정 생성 및 설정

#### 1. PayPal Developer Account

**계정 생성:**
1. https://developer.paypal.com 접속
2. "Log in to Dashboard" → 계정 생성 또는 로그인

**A. 개발/테스트용: Sandbox 앱 생성**
1. "Apps & Credentials" → "Sandbox" 탭 선택
2. "Create App" 버튼 클릭
3. App Name 입력 (예: "Scout Landing Page Sandbox")
4. App Type: "Merchant" 선택
5. "Create App" 클릭

**발급받을 정보:**
- `PAYPAL_CLIENT_ID_SANDBOX`: Client ID (Sandbox)
- `PAYPAL_CLIENT_SECRET_SANDBOX`: Secret (Show 클릭 후 복사)
- API Base URL: `https://api-m.sandbox.paypal.com`

**B. 운영용: Production 앱 생성**
1. "Apps & Credentials" → "Live" 탭 선택
2. "Create App" 버튼 클릭
3. PayPal 검토 대기 (수일 소요 가능)

---

#### 2. Google Cloud Platform

**프로젝트 생성:**
1. https://console.cloud.google.com 접속
2. "프로젝트 선택" → "새 프로젝트"
3. 프로젝트 이름 입력 (예: "scout-landing-page")
4. 프로젝트 ID 기록 (예: `scout-landing-page-123456`)

**필수 API 활성화:**
```bash
gcloud config set project PROJECT_ID

gcloud services enable \
  sqladmin.googleapis.com \
  run.googleapis.com \
  secretmanager.googleapis.com \
  cloudscheduler.googleapis.com
```

**서비스 계정 생성:**
1. IAM & Admin → Service Accounts
2. "Create Service Account"
3. 이름: `scout-api-service-account`
4. 역할 부여: Cloud Run Admin, Cloud SQL Client, Secret Manager Secret Accessor, Cloud Scheduler Admin

**JSON 키 다운로드:**
1. 생성된 서비스 계정 클릭 → "Keys" 탭 → "Add Key" → "Create new key"
2. JSON 선택 → "Create"
3. 이 파일 내용을 GitHub Secrets의 `GCP_SA_KEY`에 등록

---

#### 3. Firebase

**프로젝트 생성 및 GCP 연동:**
1. https://console.firebase.google.com 접속
2. "프로젝트 추가" → 기존 GCP 프로젝트 선택

**Hosting 활성화:**
1. Firebase Console → "Hosting" 메뉴 → "시작하기"

**Firebase CLI 로그인:**
```bash
firebase login
firebase projects:list

cd practice-landing-page
firebase init hosting
# Public directory: frontend
# Configure as single-page app: No
```

**Service Account 생성 (GitHub Actions용):**
1. Firebase Console → 프로젝트 설정 → "서비스 계정" 탭
2. "새 비공개 키 생성" → JSON 다운로드
3. GitHub Secrets의 `FIREBASE_SERVICE_ACCOUNT`에 등록

---

#### 4. Gmail SMTP 설정 (신규)

**Gmail 계정 준비:**
1. Gmail 계정 로그인 (또는 신규 생성)
2. Google 계정 관리 → 보안

**2단계 인증 활성화:**
1. "2단계 인증" → 설정 따라 진행
2. 인증 완료 확인

**앱 비밀번호 생성:**
1. Google 계정 관리 → 보안 → "2단계 인증"
2. 맨 아래 "앱 비밀번호" 클릭
3. 앱 선택: "메일", 기기 선택: "기타" (Scout Landing Page 입력)
4. "생성" 클릭
5. 16자리 비밀번호 복사 (공백 제거)

**발급받을 정보:**
- `GMAIL_ADDRESS`: 사용할 Gmail 주소
- `GMAIL_APP_PASSWORD`: 생성한 16자리 앱 비밀번호
- `SMTP_SERVER`: smtp.gmail.com
- `SMTP_PORT`: 587

---

#### 5. GitHub Repository Secrets

**설정 위치:**
Repository → Settings → Secrets and variables → Actions → "New repository secret"

**등록할 Secrets:**
1. `GCP_SA_KEY` - GCP 서비스 계정 JSON 키 전체 내용
2. `FIREBASE_SERVICE_ACCOUNT` - Firebase 서비스 계정 JSON 키 전체 내용

---

### 준비사항 체크리스트

#### 개발 도구
- [ ] Python 3.11+ 설치 완료
- [ ] uv 설치 및 버전 확인
- [ ] Docker Desktop 설치 및 실행 확인
- [ ] Firebase CLI 설치 및 로그인
- [ ] gcloud CLI 설치 및 로그인

#### PayPal
- [ ] PayPal Developer 계정 생성
- [ ] Sandbox 앱 생성
- [ ] Client ID 및 Secret 발급 완료
- [ ] Sandbox 테스트 계정 확인

#### GCP
- [ ] GCP 프로젝트 생성
- [ ] 프로젝트 ID 기록
- [ ] 필수 API 활성화 (Cloud SQL, Cloud Run, Secret Manager, Scheduler)
- [ ] 서비스 계정 생성 및 역할 부여
- [ ] JSON 키 다운로드

#### Firebase
- [ ] Firebase 프로젝트 생성 (GCP 연동)
- [ ] Hosting 활성화
- [ ] Firebase CLI 로그인
- [ ] `firebase init hosting` 완료
- [ ] Service Account JSON 다운로드

#### Gmail SMTP (신규)
- [ ] Gmail 계정 준비
- [ ] 2단계 인증 활성화
- [ ] 앱 비밀번호 생성
- [ ] 환경변수 기록 (GMAIL_ADDRESS, GMAIL_APP_PASSWORD)

#### GitHub
- [ ] `GCP_SA_KEY` Secrets 등록
- [ ] `FIREBASE_SERVICE_ACCOUNT` Secrets 등록


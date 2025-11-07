---
version: 1
created_date: 25-11-07 15:38
note:
---

## 메모

### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloud Run and Firebase

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: uv sync

      - name: Run tests
        run: uv run pytest --cov=backend

      - name: Run linter
        run: uv run ruff check .

      - name: Run type checker
        run: uv run mypy backend

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Authenticate to GCP
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v1

      - name: Deploy Backend to Cloud Run
        run: |
          gcloud run deploy scout-api \
            --source=./backend \
            --region=asia-northeast3 \
            --platform=managed \
            --allow-unauthenticated \
            --set-secrets="DATABASE_URL=prod-db-url:latest,
                           PAYPAL_CLIENT_ID=paypal-client-id:latest,
                           PAYPAL_CLIENT_SECRET=paypal-secret:latest,
                           ADMIN_API_KEY=admin-api-key:latest,
                           GMAIL_ADDRESS=gmail-address:latest,
                           GMAIL_APP_PASSWORD=gmail-app-password:latest,
                           ENCRYPTION_KEY=encryption-key:latest" \
            --set-env-vars="ALLOWED_ORIGINS=https://your-project.web.app,
                            PAYPAL_API_BASE=https://api-m.paypal.com,
                            SMTP_SERVER=smtp.gmail.com,
                            SMTP_PORT=587,
                            DEFAULT_COMMISSION_RATE=20"

      - name: Deploy Frontend to Firebase Hosting
        uses: FirebaseExtended/action-hosting-deploy@v0
        with:
          repoToken: ${{ secrets.GITHUB_TOKEN }}
          firebaseServiceAccount: ${{ secrets.FIREBASE_SERVICE_ACCOUNT }}
          channelId: live
          projectId: your-project-id
```

---

### Cloud SQL 연결 설정
```bash
# Cloud SQL 인스턴스 생성
gcloud sql instances create scout-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=asia-northeast3

# 데이터베이스 생성
gcloud sql databases create scout --instance=scout-db

# 사용자 생성
gcloud sql users create scout-user \
  --instance=scout-db \
  --password=SECURE_PASSWORD

# Cloud Run에서 Cloud SQL 접근 권한 부여
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SERVICE_ACCOUNT@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudsql.client"
```

---

### 배포 순서

**중요**: Firebase Hosting의 rewrites 설정이 Cloud Run URL을 참조하므로, **Backend를 먼저 배포**해야 합니다.

#### 1. 인프라 준비
```bash
# Cloud SQL 생성 (위 명령어 참조)
gcloud sql instances create scout-db ...

# 데이터베이스 초기화
uv run python scripts/init_db.py
```

#### 2. Secret Manager 시크릿 등록
```bash
# 환경에 맞는 시크릿 등록 (로컬/스테이징/운영)
gcloud secrets create prod-db-url ...
gcloud secrets create prod-paypal-client-id ...
gcloud secrets create prod-gmail-address ...
gcloud secrets create prod-encryption-key ...
# (섹션 13 참조)
```

#### 3. Backend Cloud Run 배포 (먼저!)
```bash
gcloud run deploy scout-api \
  --source=./backend \
  --region=asia-northeast3 \
  --set-secrets=... \
  --set-env-vars=...

# ✅ 배포 완료 후 Cloud Run URL 확인
# 예: https://scout-api-xxxxx-an.a.run.app
```

#### 4. Cloud Scheduler 설정
```bash
gcloud scheduler jobs create http paypal-retry-schedule ...
# (섹션 12 참조)
```

#### 5. Firebase Hosting 배포
```bash
# firebase.json에서 Backend URL 확인 후
firebase deploy --only hosting
```

#### 배포 순서 요약
1. Cloud SQL → 2. Secret Manager → 3. **Backend (먼저)** → 4. Scheduler → 5. Frontend

---

### 배포 전 체크리스트

#### 인프라 및 서비스 준비
- [ ] GCP 프로젝트 생성 완료
- [ ] Firebase 프로젝트 생성 및 GCP 연동
- [ ] Firebase Hosting 활성화
- [ ] Cloud SQL 인스턴스 생성 및 DATABASE_URL 확인
- [ ] GCP Secret Manager에 환경별 시크릿 등록 (개발/스테이징/운영)
- [ ] 서비스 계정 생성 및 권한 부여
- [ ] GitHub Secrets에 GCP_SA_KEY 및 FIREBASE_SERVICE_ACCOUNT 등록

#### PayPal 설정
- [ ] PayPal Sandbox 계정 및 앱 생성 (개발/테스트용)
- [ ] **PayPal Production 앱 생성 및 PayPal 승인 완료** (운영 배포 시)
- [ ] 운영 환경 시크릿이 Production API 사용하는지 확인
  - `PAYPAL_API_BASE=https://api-m.paypal.com`
  - Production Client ID/Secret 사용

#### Gmail SMTP (신규)
- [ ] Gmail 계정 준비
- [ ] 2단계 인증 활성화
- [ ] 앱 비밀번호 생성
- [ ] Secret Manager에 Gmail 시크릿 등록

#### 암호화 (신규)
- [ ] Fernet 암호화 키 생성 (환경별로 다른 키)
- [ ] Secret Manager에 암호화 키 등록
- [ ] 운영 환경 키는 절대 공유하지 않도록 주의

#### 배포 설정
- [ ] firebase.json에서 Cloud Run 서비스 ID 확인
- [ ] ALLOWED_ORIGINS에 Firebase Hosting 도메인 설정
- [ ] **Backend 먼저 배포 후 Cloud Run URL 확인**
- [ ] Cloud Scheduler 설정 (PayPal 재시도)

#### 테스트
- [ ] 로컬에서 전체 테스트 통과 확인
- [ ] E2E 테스트 시나리오 작성 및 통과
- [ ] 스테이징 환경에서 충분한 테스트 완료 (운영 배포 전)

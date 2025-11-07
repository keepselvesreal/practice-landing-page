---
version: 1
created_date: 25-11-07 15:38
note:
---

## 메모

### 로컬 개발 환경 (.env - gitignore)
```bash
# Database
DATABASE_URL=postgresql://dev:dev@localhost:5432/scout

# PayPal (Sandbox)
PAYPAL_CLIENT_ID=your_sandbox_client_id
PAYPAL_CLIENT_SECRET=your_sandbox_client_secret
PAYPAL_API_BASE=https://api-m.sandbox.paypal.com

# Admin
ADMIN_API_KEY=local-dev-key

# CORS (Firebase Hosting emulator)
ALLOWED_ORIGINS=http://localhost:5000

# Gmail SMTP (신규)
GMAIL_ADDRESS=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-digit-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# 암호화 (신규)
ENCRYPTION_KEY=your-fernet-encryption-key

# 어필리에이트 (신규)
DEFAULT_COMMISSION_RATE=20
```

---

### 스테이징/테스트 환경 (GCP Secret Manager)
```bash
# Secret Manager에 시크릿 생성
gcloud secrets create staging-db-url --data-file=-
gcloud secrets create staging-paypal-client-id --data-file=-
gcloud secrets create staging-paypal-secret --data-file=-
gcloud secrets create staging-admin-api-key --data-file=-
gcloud secrets create staging-gmail-address --data-file=-
gcloud secrets create staging-gmail-app-password --data-file=-
gcloud secrets create staging-encryption-key --data-file=-

# Cloud Run 배포 시 시크릿 참조 (Sandbox API 사용)
gcloud run deploy scout-api-staging \
  --set-secrets="DATABASE_URL=staging-db-url:latest,
                 PAYPAL_CLIENT_ID=staging-paypal-client-id:latest,
                 PAYPAL_CLIENT_SECRET=staging-paypal-secret:latest,
                 ADMIN_API_KEY=staging-admin-api-key:latest,
                 GMAIL_ADDRESS=staging-gmail-address:latest,
                 GMAIL_APP_PASSWORD=staging-gmail-app-password:latest,
                 ENCRYPTION_KEY=staging-encryption-key:latest" \
  --set-env-vars="ALLOWED_ORIGINS=https://staging-project.web.app,
                  PAYPAL_API_BASE=https://api-m.sandbox.paypal.com,
                  SMTP_SERVER=smtp.gmail.com,
                  SMTP_PORT=587,
                  DEFAULT_COMMISSION_RATE=20"
```

**⚠️ 주의**: 스테이징 환경도 PayPal Sandbox API 사용

---

### 운영 환경 (GCP Secret Manager)
```bash
# Secret Manager에 시크릿 생성
gcloud secrets create prod-db-url --data-file=-
gcloud secrets create prod-paypal-client-id --data-file=-
gcloud secrets create prod-paypal-secret --data-file=-
gcloud secrets create prod-admin-api-key --data-file=-
gcloud secrets create prod-gmail-address --data-file=-
gcloud secrets create prod-gmail-app-password --data-file=-
gcloud secrets create prod-encryption-key --data-file=-

# Cloud Run 배포 시 시크릿 참조 (Production API 사용)
gcloud run deploy scout-api \
  --set-secrets="DATABASE_URL=prod-db-url:latest,
                 PAYPAL_CLIENT_ID=prod-paypal-client-id:latest,
                 PAYPAL_CLIENT_SECRET=prod-paypal-secret:latest,
                 ADMIN_API_KEY=prod-admin-api-key:latest,
                 GMAIL_ADDRESS=prod-gmail-address:latest,
                 GMAIL_APP_PASSWORD=prod-gmail-app-password:latest,
                 ENCRYPTION_KEY=prod-encryption-key:latest" \
  --set-env-vars="ALLOWED_ORIGINS=https://your-project.web.app,
                  PAYPAL_API_BASE=https://api-m.paypal.com,
                  SMTP_SERVER=smtp.gmail.com,
                  SMTP_PORT=587,
                  DEFAULT_COMMISSION_RATE=20"
```

**⚠️ 중요**:
- 운영 환경은 **PayPal Production API** 사용 (`https://api-m.paypal.com`)
- 실제 결제 처리되므로 배포 전 충분한 테스트 필요
- Production Client ID/Secret은 PayPal 승인 완료 후 사용 가능
- **암호화 키는 환경별로 다르게 생성** (절대 공유하지 말 것)

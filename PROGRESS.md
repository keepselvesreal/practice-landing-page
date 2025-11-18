# 워킹 스켈레톤 구축 진행 상황

## 1. 현재 완료 상태 요약

### ✅ 완료된 작업

#### 인프라
- [x] Cloud SQL 인스턴스 생성 (`kbeauty-db`, IP: 34.50.3.36)
- [x] Cloud SQL 데이터베이스 생성 (`kbeauty`)
- [x] Cloud SQL 사용자 생성 (`kbeauty_user`)
- [x] Service Account 권한 설정 (Cloud Run Admin, Cloud SQL Client, Service Account User)
- [x] GitHub Secrets 설정 완료 (GCP_SA_KEY)

#### Backend (FastAPI)
- [x] 프로젝트 구조 생성 (`backend/app/`)
- [x] 모델 정의 (`Order`, `EmailLog`)
- [x] API 엔드포인트 구현 (`POST /api/orders/create`)
- [x] Gmail SMTP 이메일 발송 기능
- [x] Alembic 마이그레이션 설정 및 파일 생성
- [x] Dockerfile 작성
- [x] 환경변수 설정 (config.py)

#### Frontend
- [x] HTML/CSS 구현 (랜딩 페이지, 주문 확인 페이지)
- [x] JavaScript 구현 (main.js)
- [x] Google Places API 통합 (플레이스홀더)
- [x] PayPal SDK 통합 (플레이스홀더)
- [x] 환경변수 주입 스크립트 (`scripts/inject-env-local.sh`)

#### E2E 테스트
- [x] 테스트 구조 설계 (환경변수 기반: local/docker/production)
- [x] conftest.py 작성 (PostgreSQL container, Backend/Frontend server fixtures)
- [x] 워킹 스켈레톤 테스트 작성 (`test_when_order_submitted_then_saved_to_database_email_sent_paypal_displayed_and_redirected_to_confirmation`)
- [x] Playwright 의존성 추가

#### 설정
- [x] firebase.json API 프록시 설정 (Cloud Run 연동)
- [x] .env 파일 구성 (환경변수 관리)

### 📁 생성된 주요 파일

```
backend/
├── app/
│   ├── main.py              # FastAPI 앱
│   ├── config.py            # 환경변수 설정
│   ├── database.py          # DB 연결
│   ├── models.py            # Order, EmailLog 모델
│   ├── schemas.py           # Pydantic 스키마
│   ├── routers/
│   │   └── orders.py        # 주문 API
│   └── services/
│       ├── email_service.py # 이메일 발송
│       └── order_service.py # 주문 생성
├── alembic/
│   ├── env.py
│   └── versions/
│       └── 3c65a54758fa_initial_schema.py
├── tests/
│   └── e2e/
│       ├── conftest.py      # 테스트 설정
│       └── test_walking_skeleton.py
├── Dockerfile
├── .dockerignore
└── pyproject.toml

frontend/
├── index.html               # 랜딩 페이지 (환경변수 플레이스홀더)
├── order-confirmation.html  # 주문 확인 페이지
├── css/
│   └── style.css
└── js/
    └── main.js              # Frontend 로직

scripts/
└── inject-env-local.sh      # 환경변수 주입 스크립트

firebase.json                # Firebase + Cloud Run 프록시
.env                         # 환경변수 (TODO: DATABASE_URL 수정 필요)
```

---

## 2. 다음 작업 순서 (Phase별)

### Phase 1: PostgreSQL Docker 설정 및 로컬 E2E 테스트

**목표:** 로컬 환경에서 E2E 테스트 통과

#### Step 1: PostgreSQL Docker Container 생성
```bash
# 1. PostgreSQL container 시작
docker run -d --name kbeauty-postgres \
  -e POSTGRES_DB=kbeauty_test \
  -e POSTGRES_USER=test_user \
  -e POSTGRES_PASSWORD=test_pass \
  -p 5433:5432 \
  postgres:15

# 2. Container 상태 확인
docker ps | grep kbeauty-postgres

# 3. DB 접속 테스트
docker exec -it kbeauty-postgres psql -U test_user -d kbeauty_test
# \dt  (테이블 목록 - 아직 비어있음)
# \q   (종료)
```

#### Step 2: .env 파일 수정
```bash
# .env 파일에서 DATABASE_URL 주석 해제 및 수정
# Before:
DATABASE_URL=postgresql://nadle:1089@localhost:5432/k_beauty_landing_page

# After:
DATABASE_URL=postgresql://test_user:test_pass@localhost:5433/kbeauty_test
```

#### Step 3: DB 마이그레이션 실행
```bash
cd backend
uv run alembic upgrade head

# 확인
docker exec -it kbeauty-postgres psql -U test_user -d kbeauty_test -c "\dt"
# orders, email_logs 테이블 생성 확인
```

#### Step 4: Playwright 브라우저 설치
```bash
uv run playwright install chromium
```

#### Step 5: 로컬 E2E 테스트 실행
```bash
cd backend
TEST_ENV=local uv run pytest tests/e2e/ -v

# 예상 출력:
# - PostgreSQL container 시작 (또는 이미 실행 중)
# - Backend server 시작 (uvicorn)
# - Frontend server 시작 (http.server)
# - 테스트 실행
# - 서버 종료
```

#### 검증 항목
- [ ] PostgreSQL container 정상 실행
- [ ] DB 마이그레이션 성공
- [ ] Backend API 시작 (http://localhost:8000/health)
- [ ] Frontend 시작 (http://localhost:8080)
- [ ] E2E 테스트 통과
- [ ] 주문 데이터 DB 저장 확인
- [ ] 이메일 발송 성공 (Gmail SMTP)

---

### Phase 2: Docker 환경 E2E 테스트

**목표:** docker-compose로 전체 환경 구성 및 테스트 통과

#### Step 1: docker-compose.test.yml 작성
```yaml
# backend/tests/e2e/docker/docker-compose.test.yml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: kbeauty_test
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_pass
    ports:
      - "5433:5432"

  backend:
    build:
      context: ../../..
      dockerfile: Dockerfile
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql://test_user:test_pass@postgres:5432/kbeauty_test
      # ... 기타 환경변수
    ports:
      - "8000:8000"

  frontend:
    image: nginx:alpine
    volumes:
      - ../../../../frontend:/usr/share/nginx/html
    ports:
      - "8080:80"
```

#### Step 2: Docker 환경 테스트 실행
```bash
# 1. docker-compose 시작
cd backend/tests/e2e/docker
docker-compose -f docker-compose.test.yml up -d

# 2. 마이그레이션
docker-compose -f docker-compose.test.yml exec backend alembic upgrade head

# 3. 테스트 실행
cd ../..
TEST_ENV=docker uv run pytest tests/e2e/ -v

# 4. 정리
cd tests/e2e/docker
docker-compose -f docker-compose.test.yml down
```

#### 검증 항목
- [ ] 모든 container 정상 실행
- [ ] container 간 네트워크 통신 성공
- [ ] E2E 테스트 통과

---

### Phase 3: GitHub Actions CI/CD

**목표:** GitHub Actions에서 자동 빌드, 테스트, 배포

#### Step 1: GitHub Actions 워크플로우 작성
```yaml
# .github/workflows/walking-skeleton.yml
name: Walking Skeleton CI/CD

on:
  push:
    branches: [main, mvp/v2]

jobs:
  test-docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Docker E2E tests
        run: |
          cd backend/tests/e2e/docker
          docker-compose -f docker-compose.test.yml up -d
          # ... 테스트 실행
          docker-compose -f docker-compose.test.yml down

  deploy:
    needs: test-docker
    runs-on: ubuntu-latest
    steps:
      - name: Deploy Backend to Cloud Run
      - name: Deploy Frontend to Firebase
      - name: Run Production E2E tests
```

#### Step 2: GitHub에 Push 및 CI/CD 확인
```bash
git add .
git commit -m "feat: 워킹 스켈레톤 구현 완료"
git push origin mvp/v2
```

#### 검증 항목
- [ ] Docker E2E 테스트 통과 (GitHub Actions)
- [ ] Backend Cloud Run 배포 성공
- [ ] Frontend Firebase 배포 성공
- [ ] Production E2E 테스트 통과

---

### Phase 4: Production 환경 테스트

**목표:** 실제 배포 환경에서 E2E 테스트 통과

#### Step 1: Production E2E 테스트 실행
```bash
TEST_ENV=production uv run pytest tests/e2e/ -v
```

#### 검증 항목
- [ ] https://kbeauty-landing-page.web.app 접속 성공
- [ ] Firebase → Cloud Run API 프록시 동작
- [ ] Cloud SQL 연결 성공
- [ ] 실제 주문 생성 및 이메일 발송
- [ ] E2E 테스트 통과

---

## 다음 세션 시작 시

1. **PostgreSQL Docker container 생성**부터 시작
2. DATABASE_URL 변경
3. 로컬 E2E 테스트 실행

**참조 문서:**
- `walking-skeleton.md`: 워킹 스켈레톤 결정사항
- `PROGRESS.md`: 이 문서
- `backend/tests/e2e/conftest.py`: 테스트 설정

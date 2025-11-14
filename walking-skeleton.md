워킹 스켈레톤 구축 - 결정 사항

  1. Step 1: Acceptance Test 작성

  1.1 테스트 전략

  - 테스트 범위: 단일 E2E 테스트
  - 외부 API/인프라: 실제 사용 (Mock 없음)
    - Gmail SMTP: 실제 발송 (building.ensemble@gmail.com)
    - Google Places API: 실제 호출
    - PayPal Sandbox: SDK 통합 확인 (결제창 표시까지)
    - PostgreSQL: 실제 DB 저장

  1.2 테스트 구조

  - 파일 위치: tests/e2e/test_walking_skeleton.py
  - Helper fixtures: tests/e2e/conftest.py

  1.3 테스트 시나리오

  1. 배포된 랜딩 페이지 접속 (https://kbeauty-landing-page.web.app)
  2. 폼 필드 표시 확인
  3. 고객 정보 입력
  4. 주소 자동완성 (Google Places API)
  5. 결제 버튼 클릭 → PayPal 팝업 확인
  6. Backend API 호출 → DB 저장 → 이메일 발송 확인
  7. 주문 확인 페이지 이동

  1.4 이메일 발송 확인

  - 방식: Backend API 응답에서 발송 성공 여부 확인
  - 실제 발송: Gmail SMTP 사용
  - 검증: window.lastOrderResponse.email_sent === true

  1.5 End-to-End 실행 원칙

  - [4.2, p.32]: "deploy it into a production-like environment, and then run the tests through the
  deployed system"
  - 배포 환경 테스트: 로컬이 아닌 실제 배포된 URL 사용
  - 환경변수: E2E_BASE_URL (로컬/배포 전환)

  ---
  2. Step 2: 인프라 결정

  2.1 프로젝트 구조

  practice-landing-page/
  ├── frontend/
  │   ├── index.html
  │   └── js/
  │       └── main.js          # Frontend 진입점
  ├── backend/
  │   ├── app/
  │   │   ├── main.py          # Backend 진입점 [10, p.85]
  │   │   ├── database.py
  │   │   └── routers/
  │   ├── alembic/             # DB 마이그레이션
  │   │   └── versions/
  │   ├── tests/
  │   └── pyproject.toml
  ├── tests/
  │   └── e2e/
  │       ├── test_walking_skeleton.py
  │       └── conftest.py
  ├── .github/
  │   └── workflows/
  │       └── walking-skeleton.yml
  └── scripts/                 # (선택) 로컬 실행 스크립트

  2.2 로컬 개발 환경

  - PostgreSQL: 이미 설치된 로컬 postgres
  - Backend: uv run uvicorn app.main:app --reload
  - Frontend: python -m http.server 8080
  - 환경변수: .env 파일
  - 목적: 개발 중 빠른 피드백

  2.3 워킹 스켈레톤 환경 (Production-like)

  2.3.1 Cloud SQL

  인스턴스명: kbeauty-db
  리전: asia-northeast3
  티어: db-f1-micro (최소 사양)
  PostgreSQL 버전: 15
  Public IP: 사용
  DB명: kbeauty
  User: kbeauty_user

  2.3.2 Cloud Run

  서비스명: kbeauty-api
  리전: asia-northeast3
  최소/최대 인스턴스: 0/1
  메모리: 512Mi
  CPU: 1
  인증: allow unauthenticated
  포트: 8000

  2.3.3 Firebase Hosting

  프로젝트: kbeauty-landing-page (기존)
  배포 디렉토리: frontend/
  사이트: kbeauty-landing-page.web.app

  2.3.4 Service Account

  이름: github-actions-deployer
  역할:
    - Cloud Run Admin
    - Cloud SQL Client
    - Service Account User
  JSON 키 → GitHub Secrets (GCP_SA_KEY)

  2.4 API 호출 방식

  - 선택: Firebase Hosting 프록시 (옵션 A)
  - 설정: firebase.json에서 /api/** → Cloud Run
  - 장점:
    - CORS 불필요
    - URL 간단 (/api/orders/create)
    - Cloud Run URL 변경 시에도 Frontend 수정 불필요

  2.5 환경변수 관리

  - 로컬: .env 파일
  - CI/CD: GitHub Repository Secrets
  - Cloud Run: 환경변수 설정

  GitHub Secrets 목록:
  GCP_PROJECT_ID=kbeauty-landing-page
  GCP_SA_KEY=<service-account-json>
  DATABASE_URL=postgresql://...
  GMAIL_ADDRESS=building.ensemble@gmail.com
  GMAIL_APP_PASSWORD=czqi vxgm osqk vfxz
  GOOGLE_PLACES_API_KEY=<key>
  PAYPAL_CLIENT_ID=<sandbox-id>
  PAYPAL_CLIENT_SECRET=<sandbox-secret>

  2.6 DB 전환 (로컬 ↔ Cloud SQL)

  - 방식: 환경변수 DATABASE_URL만 변경
  - 로컬: postgresql://localhost:5432/kbeauty_local
  - Cloud Run: postgresql://kbeauty_user:PASSWORD@/kbeauty?host=/cloudsql/...
  - Backend 코드: 동일 (환경변수만 읽음)

  2.7 Main 파일 역할

  - Backend: backend/app/main.py - FastAPI app 초기화 [10, p.85]
  - Frontend: frontend/js/main.js - Google Places, PayPal SDK 초기화
  - E2E 검증: 배포된 환경에서 main을 통한 초기화 확인
    - Cloud Run: Dockerfile CMD로 backend main 실행
    - Firebase: index.html이 main.js 로드

  ---
  3. Step 3: DB 마이그레이션 및 CI/CD

  3.1 DB 마이그레이션 전략

  3.1.1 마이그레이션 개념

  - 정의: DB 스키마 변경 작업 (컬럼 추가, 테이블 생성 등)
  - 필요성:
    - 변경 추적 (Git으로 관리)
    - 버전 관리 (현재 스키마 버전 확인)
    - 롤백 가능 (문제 시 이전 버전으로)
    - 팀 협업 (모두 동일한 스키마 유지)

  3.1.2 도구 선택: Alembic

  - 이유:
    - Python 생태계 표준
    - SQLAlchemy 기반 (FastAPI와 궁합)
    - 자동 마이그레이션 생성 가능
    - MVP에 적합 (간단하면서 확장 가능)

  3.1.3 마이그레이션 자동화

  - 정의: 코드 배포 시 마이그레이션도 자동 실행
  - 필요 이유:
    a. 워킹 스켈레톤 원칙 [4.2, p.32]: "automate the build, deploy, and test cycle"
    b. 실수 방지: 코드와 DB 변경이 동기화됨
    c. 버전 관리: DB 스키마도 Git으로 추적
    d. 팀 협업: 자동으로 동기화

  워크플로우:
  1. 코드 수정 + 마이그레이션 파일 생성
  2. Git commit
  3. GitHub Push
  4. GitHub Actions:
     a. 마이그레이션 실행 (alembic upgrade head)
     b. Backend 배포
     c. E2E 테스트

  3.2 워킹 스켈레톤용 DB 스키마

  -- alembic/versions/001_initial_schema.py 내용
  CREATE TABLE orders (
      id SERIAL PRIMARY KEY,
      order_number VARCHAR(50) UNIQUE NOT NULL,
      customer_name VARCHAR(100) NOT NULL,
      email VARCHAR(100) NOT NULL,
      phone VARCHAR(50) NOT NULL,
      address TEXT NOT NULL,
      place_id VARCHAR(255),
      created_at TIMESTAMP DEFAULT NOW()
  );

  CREATE TABLE email_logs (
      id SERIAL PRIMARY KEY,
      order_id INTEGER REFERENCES orders(id),
      recipient VARCHAR(100) NOT NULL,
      subject VARCHAR(255) NOT NULL,
      status VARCHAR(20) NOT NULL,  -- 'sent', 'failed'
      created_at TIMESTAMP DEFAULT NOW()
  );

  3.3 스키마 적용 방법

  Phase 1: 최초 설정 (수동)

  # 1. Cloud SQL 인스턴스 생성
  gcloud sql instances create kbeauty-db ...

  # 2. DB/User 생성
  gcloud sql databases create kbeauty ...
  gcloud sql users create kbeauty_user ...

  # 3. Alembic 초기화
  cd backend
  uv add alembic sqlalchemy psycopg2-binary
  alembic init alembic

  # 4. 최초 마이그레이션 생성 및 적용
  alembic revision --autogenerate -m "initial schema"
  alembic upgrade head

  Phase 2: 이후 변경 (자동)

  - Alembic + GitHub Actions
  - 코드 배포 시 자동으로 마이그레이션 실행

  3.4 CI/CD 파이프라인

  3.4.1 GitHub Actions 워크플로우 구조

  # .github/workflows/walking-skeleton.yml
  name: Walking Skeleton - Build, Deploy, Test

  on:
    push:
      branches: [main, mvp/v2]

  jobs:
    deploy-and-test:
      runs-on: ubuntu-latest

      steps:
        1. 코드 체크아웃
        2. GCP 인증 (Service Account)
        3. Backend Docker 빌드
        4. GCR에 이미지 푸시
        5. 마이그레이션 실행 (Cloud Run Job)
        6. Cloud Run 배포
        7. Frontend Firebase 배포
        8. 배포 완료 대기
        9. E2E 테스트 실행 (배포된 URL)

  3.4.2 배포 플로우

  GitHub Push
    ↓
  GitHub Actions
    ↓
  1. Backend 빌드 (Docker)
  2. Cloud Run 배포
  3. 마이그레이션 실행 (배포된 환경)
  4. Frontend 배포 (Firebase)
  5. E2E 테스트 (https://kbeauty-landing-page.web.app)

  3.4.3 검증 항목 [4.2, p.32]

  ✅ 빌드 가능한가? (Docker 이미지)✅ 배포 가능한가? (Cloud Run, Firebase)✅ Cloud SQL 연결되는가?✅
   마이그레이션 동작하는가?✅ Firebase → Cloud Run 프록시 동작하는가?✅ Gmail SMTP 동작하는가?✅
  Google Places API 동작하는가?✅ PayPal SDK 동작하는가?✅ 전체 플로우 동작하는가?

  3.5 작업 목록

  1. ⏳ Cloud SQL 인스턴스 생성 및 DB 초기화
  2. ⏸️ Service Account 생성 및 권한 부여
  3. ⏸️ GitHub Secrets 설정
  4. ⏸️ Backend Dockerfile 작성
  5. ⏸️ firebase.json 설정 (API 프록시)
  6. ⏸️ GitHub Actions 워크플로우 작성 (배포 자동화)
  7. ⏸️ DB 마이그레이션 스크립트 작성 (Alembic)
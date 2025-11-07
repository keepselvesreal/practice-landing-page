---
version: 1
created_date: 25-11-07 15:38
note:
---

## 메모

### 목적
- 실제 운영용 전자상거래 랜딩페이지 개발
- 단계적 구현으로 전자상거래 풀 플로우 구현
- Outside-In TDD 방법론 적용

---

### 배포 전략

**개발/테스트 환경:**
- PayPal Sandbox API 사용
- 로컬 개발: Docker PostgreSQL
- 스테이징: Cloud Run + Cloud SQL (개발용 인스턴스)

**운영 환경:**
- PayPal Production API 사용 (실제 결제 처리)
- Firebase Hosting (프론트엔드)
- Cloud Run (백엔드 API)
- Cloud SQL (프로덕션 데이터베이스)

---

### 기술 스택

#### Frontend
- HTML5, Vanilla JavaScript
- CSS
- **i18n 라이브러리** (다국어: 영어 ⇄ Tagalog)
- Firebase Hosting (배포)

#### Backend
- **FastAPI** (웹 프레임워크)
- **PostgreSQL** (데이터베이스)
- **Cloud SQL** (관리형 PostgreSQL)
- **Cloud Run** (배포 환경)
- **Python 3.11+**

#### 테스트
- **pytest** (테스트 프레임워크)
- **pytest-cov** (커버리지)
- **pytest-playwright** (E2E 테스트)

#### 개발 도구
- **uv** (의존성 관리 - pip 대체)
- **ruff** (linter + formatter)
- **mypy** (타입 체커)
- **email-validator** (이메일 검증)
- **pyproject.toml** (통합 설정)
- **Docker** (로컬 PostgreSQL)

#### CI/CD
- **GitHub Actions** (테스트 + 배포)
- Firebase CLI
- gcloud CLI

#### 외부 서비스
- PayPal Sandbox/Production (결제 - Phase 3)
- **Gmail SMTP** (이메일 발송)
- **Python `cryptography`** (개인정보 암호화 - Fernet)
- Google Places API (주소 - Phase 4)

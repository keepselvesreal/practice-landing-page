---
version: 1
created_date: 25-11-07 15:38
note:
---

## 메모

```
practice-landing-page/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI 앱
│   ├── models.py            # Pydantic 모델/스키마
│   ├── db.py                # PostgreSQL 연결 + 연결 풀
│   ├── validators.py        # 입력 검증
│   ├── crypto.py            # 암호화/복호화 (Fernet) - 신규
│   ├── email.py             # Gmail SMTP 이메일 발송 - 신규
│   ├── api/
│   │   ├── __init__.py
│   │   ├── orders.py        # 주문 API
│   │   ├── payment.py       # PayPal 결제 API
│   │   ├── admin.py         # 관리자 API
│   │   ├── refunds.py       # 환불 API
│   │   └── affiliates.py    # 어필리에이트 API - 신규
│   └── db/
│       ├── __init__.py
│       └── connection.py    # DB 연결 관리
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   ├── main.js
│   │   │   └── i18n.js      # 다국어 처리 - 신규
│   │   └── images/          # 제품 이미지 - 신규
│   │       ├── product_main.jpg
│   │       └── product_*.jpg
│   └── templates/
│       ├── index.html           # 메인 랜딩페이지
│       ├── order_check.html     # 주문 조회 페이지
│       ├── admin_shipments.html # 배송 관리
│       ├── admin_refunds.html   # 환불 관리
│       ├── affiliate_stats.html # 인플루언서 대시보드 - 신규
│       └── contact.html         # 문의 페이지 - 신규
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # pytest 설정
│   ├── data/
│   │   └── sample_purchases.json
│   ├── fixtures/
│   │   ├── __init__.py
│   │   ├── factories.py     # 테스트 데이터 팩토리
│   │   └── helpers.py       # 테스트 헬퍼 함수
│   ├── e2e/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   └── test_order_flow.py    # E2E 테스트
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_orders.py        # 주문 API 통합 테스트
│   │   ├── test_payment.py       # 결제 통합 테스트
│   │   └── test_refunds.py       # 환불 통합 테스트
│   └── unit/
│       ├── __init__.py
│       ├── test_validators.py    # 단위 테스트
│       └── test_models.py
├── docs/
│   ├── project-plan.md          # 메인 목차
│   ├── 00-preparation.md
│   ├── 01-overview.md
│   ├── ... (17개 모듈)
│   ├── inbox/
│   └── reviews/                 # AI 리뷰 기록
├── records/
│   ├── notes/                   # 개발 노트
│   └── sources/                 # 참고 자료
├── references/                  # 테스팅 관련 책
│   ├── growing-object-oriented-software/
│   ├── effective-software-testing/
│   └── ...
├── scripts/
│   ├── init_db.py               # DB 초기화
│   └── retry_payments.py        # PayPal 검증 재시도 (Cloud Run Job)
├── .github/
│   └── workflows/
│       └── deploy.yml           # GitHub Actions 배포
├── .env                         # 로컬 환경변수 (gitignore)
├── .firebaserc                  # Firebase 프로젝트 설정
├── firebase.json                # Firebase Hosting 설정
├── docker-compose.yml           # 로컬 PostgreSQL
├── pyproject.toml               # uv 설정
├── uv.lock
├── CLAUDE.md                    # Claude Code 프로젝트 설정
└── README.md
```

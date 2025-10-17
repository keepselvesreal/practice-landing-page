---
created_at: 2025-10-10 00:00:00
links:
   - ./index.md
---

# 2. 프로젝트 폴더 구조

## 2.1 전체 폴더 구조 개요

```
cosmetics_landing/
├── src/
│   └── cosmetics_landing/
│       ├── domain/                    # 도메인 계층 (가장 안쪽)
│       │   ├── __init__.py
│       │   ├── order.py               # Order 엔티티
│       │   ├── affiliate.py           # Affiliate 엔티티
│       │   └── commission.py          # Commission 값 객체
│       │
│       ├── application/               # 애플리케이션 계층
│       │   ├── __init__.py
│       │   ├── port/
│       │   │   ├── __init__.py
│       │   │   ├── in_/               # Incoming ports (Use Cases)
│       │   │   │   ├── __init__.py
│       │   │   │   ├── place_order_use_case.py
│       │   │   │   ├── track_affiliate_use_case.py
│       │   │   │   ├── calculate_commission_use_case.py
│       │   │   │   └── send_inquiry_use_case.py
│       │   │   │
│       │   │   └── out/               # Outgoing ports
│       │   │       ├── __init__.py
│       │   │       ├── order_repository.py
│       │   │       ├── affiliate_repository.py
│       │   │       ├── payment_gateway.py
│       │   │       ├── email_sender.py
│       │   │       └── address_validator.py
│       │   │
│       │   └── service/               # Use Case 구현
│       │       ├── __init__.py
│       │       ├── place_order_service.py
│       │       ├── track_affiliate_service.py
│       │       ├── calculate_commission_service.py
│       │       └── send_inquiry_service.py
│       │
│       ├── adapter/                   # 어댑터 계층
│       │   ├── __init__.py
│       │   ├── in_/                   # Incoming adapters
│       │   │   ├── __init__.py
│       │   │   └── web/               # FastAPI 웹 어댑터
│       │   │       ├── __init__.py
│       │   │       ├── order_controller.py
│       │   │       ├── affiliate_controller.py
│       │   │       ├── inquiry_controller.py
│       │   │       └── dto/           # 웹 전용 DTO
│       │   │           ├── __init__.py
│       │   │           ├── order_request.py
│       │   │           ├── affiliate_response.py
│       │   │           └── inquiry_request.py
│       │   │
│       │   └── out/                   # Outgoing adapters
│       │       ├── __init__.py
│       │       ├── persistence/       # 영속성 어댑터
│       │       │   ├── __init__.py
│       │       │   ├── order_persistence_adapter.py
│       │       │   ├── affiliate_persistence_adapter.py
│       │       │   └── model/         # DB 모델
│       │       │       ├── __init__.py
│       │       │       ├── order_model.py
│       │       │       └── affiliate_model.py
│       │       │
│       │       ├── payment/           # 결제 어댑터
│       │       │   ├── __init__.py
│       │       │   └── paypal_adapter.py
│       │       │
│       │       ├── email/             # 이메일 어댑터
│       │       │   ├── __init__.py
│       │       │   └── gmail_smtp_adapter.py
│       │       │
│       │       └── geocoding/         # 주소 검증 어댑터
│       │           ├── __init__.py
│       │           └── google_places_adapter.py
│       │
│       └── config/                    # 설정 계층 (가장 바깥)
│           ├── __init__.py
│           ├── settings.py            # 환경 설정
│           ├── dependencies.py        # 의존성 주입 설정
│           └── main.py                # FastAPI 앱 초기화
│
├── tests/                             # 테스트
│   ├── unit/                          # 단위 테스트
│   │   ├── domain/
│   │   │
│   │   └── application/
│   │
│   ├── integration/                   # 통합 테스트
│   │   ├── adapter/
│   │   │
│   │   └── end_to_end/                # 시스템 테스트
│   │
│   └── conftest.py                    # pytest 설정
│
├── migrations/                        # 데이터베이스 마이그레이션 (Alembic)
│   └── versions/
│
├── static/                            # 정적 파일
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/                         # HTML 템플릿 (Jinja2)
│   ├── landing.html                   # Walking Skeleton 최소 페이지
│   ├── order_form.html                # Epic 1: 주문 폼 (Phase 2에서 추가)
│   └── affiliate_stats.html           # Epic 2: 어필리에이트 통계
│
├── pyproject.toml                     # 프로젝트 메타데이터 (uv)
├── README.md
└── .env.example                       # 환경변수 예시
```

## 2.2 폴더 구조 설계 근거

**출처**: Chapter 3 "Organizing Code", Lines 114-171

**계층별 패키지 설명**:

1. **domain 패키지** (public entities)
   - **근거**: Chapter 3, Lines 179-180
   - **역할**: 도메인 모델 포함, 비즈니스 규칙 캡슐화
   - **가시성**: public (다른 계층에서 접근 필요)
   - **의존성**: 다른 계층에 의존하지 않음

2. **application 패키지**
   - **근거**: Chapter 3, Lines 180-186
   - **역할**: 유스케이스 구현, 포트 정의
   - **하위 구조**:
     - `port/in_`: Incoming ports (Use Case 인터페이스) - public
     - `port/out`: Outgoing ports (Repository, Gateway 인터페이스) - public
     - `service`: Use Case 구현 - package-private 가능

3. **adapter 패키지**
   - **근거**: Chapter 3, Lines 183-186
   - **역할**: 외부 세계와의 통신 담당
   - **하위 구조**:
     - `in_/web`: HTTP 요청 처리 (Incoming adapter)
     - `out/persistence`: 데이터베이스 통신 (Outgoing adapter)
     - `out/payment`: 결제 서비스 통신 (Outgoing adapter)
     - `out/email`: 이메일 발송 (Outgoing adapter)
     - `out/geocoding`: 주소 검증 서비스 통신 (Outgoing adapter)
   - **가시성**: package-private (포트를 통해서만 접근)

4. **config 패키지** (Configuration Layer)
   - **근거**: Chapter 9, Lines 23-49
   - **역할**: 의존성 주입, 애플리케이션 조립
   - **책임**: 모든 객체 인스턴스화 및 연결

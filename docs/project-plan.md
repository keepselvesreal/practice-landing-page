# Scout Landing Page MVP - Project Plan

**Version**: 4
**Created**: 2025-11-07
**Note**: 모듈화 구조 + 새 요구사항 반영 (배송비, 어필리에이트, 암호화, Gmail SMTP, 다국어)

---

## 목차

### 준비 및 개요
- [00-preparation](00-preparation.md) - 개발 시작 전 준비사항
- [01-overview](01-overview.md) - 프로젝트 개요

### 데이터 및 상태 설계
- [02-database-schema](02-database-schema.md) - 데이터베이스 스키마
- [03-product-info](03-product-info.md) - 상품 정보
- [04-state-management](04-state-management.md) - 상태 관리

### 비즈니스 로직 및 검증
- [05-business-logic](05-business-logic.md) - 비즈니스 로직
- [06-error-handling](06-error-handling.md) - 에러 처리 정책
- [07-data-validation](07-data-validation.md) - 데이터 검증 규칙

### UI/UX 및 구조
- [08-pages](08-pages.md) - 페이지 구성
- [09-ui-ux](09-ui-ux.md) - UI/UX 정책
- [10-project-structure](10-project-structure.md) - 프로젝트 구조

### 개발 방법론 및 구현
- [11-methodology](11-methodology.md) - 개발 방법론
- [12-implementation](12-implementation.md) - 기술적 구현 세부사항

### 환경 및 배포
- [13-environment](13-environment.md) - 환경 변수
- [14-local-dev](14-local-dev.md) - 로컬 개발 환경
- [15-deployment](15-deployment.md) - 배포 설정

### 성능 및 이메일
- [16-performance](16-performance.md) - 성능 요구사항
- [17-email-templates](17-email-templates.md) - 이메일 템플릿

---

## 주요 변경사항 (v4)

### 새 요구사항 반영
- ✅ **배송비**: orders 테이블에 `shipping_fee` 추가 (기본 100페소)
- ✅ **어필리에이트**: affiliates, affiliate_stats 테이블 추가 (20% 커미션)
- ✅ **개인정보 암호화**: Fernet 암호화로 고객 정보 보호
- ✅ **Gmail SMTP**: 이메일 자동 발송 (주문 확인, 배송 완료 등)
- ✅ **다국어 지원**: 영어 ⇄ Tagalog 토글

### 문서 구조화
- 기존 1191줄 통합 문서를 17개 모듈로 분리
- Obsidian 백링크를 활용한 탐색 최적화

---

## 백업 파일
- 이전 버전: [[project-plan-11-07-1519]]

---
created_at: 2025-10-10 00:00:00
links:
   - ./index.md
---

# 6. 추가 고려사항

## 6.1 프로덕션 준비

1. **환경 분리**
   - 개발/스테이징/프로덕션 설정 분리
   - `.env` 파일 관리

2. **로깅 및 모니터링**
   - 구조화된 로깅 (JSON)
   - Cloud Logging 통합

3. **보안**
   - API 키 보안
   - HTTPS 강제
   - CORS 설정

## 6.2 확장 가능성

1. **어댑터 교체**
   - PayPal → Stripe 전환 시 `PayPalAdapter`만 교체
   - SQLite → PostgreSQL 전환 시 설정만 변경

2. **새 기능 추가**
   - SMS 알림: `adapter/out/sms/` 추가
   - 소셜 로그인: `adapter/in_/web/auth_controller.py` 추가

3. **UI 개선**
   - Vanilla JS → React/Vue 전환 시 adapter/in_/web만 수정
   - SSR → SPA 전환 시 템플릿 계층만 교체

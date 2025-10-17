---
created_at: 2025-10-17 16:58:47
version: 2
status: Active
address: "landing_page/epic-overview"
links:
  in: [
    ./inbox/epic-overview--25-10-17.md,
    ./templates/epic-overview.md,
  ]
  out: [
    ./prd/cosmetics_landing_mvp.md,
    ./architecture/system_architecture.md,
    ./ai_sessions/cc_session_bf132ef3-d7d2-4eee-813c-aeadf30c88e0.txt,
    ./ai_sessions/cc_session_113544ee-e153-400b-86c7-dddfa0709a88.txt,
  ]
tags: [epic-overview, mvp, k-beauty, philippines, planning, outside-in-tdd]
notes: "Outside-In TDD 방식으로 Epic 구성 재조정 (v1에서 수정)"
---

## 1. 압축 내용

**Epic Overview 한 줄 요약:**
- 주문-결제-알림-어필리에이트 기능을 통해 2주 내 10개 판매 달성 및 운영 프로세스 검증을 제공하며, 총 4개 Epic으로 1주에 걸쳐 구현한다.

---

## 2. 핵심 내용

**핵심 목표**
- 2주 내 10개 판매 달성
- 운영 프로세스(구매-배송-피드백) 검증 및 개선점 수집
- 어필리에이트 마케팅으로 지속 협업 가능한 인플루언서 2명 이상 확보

✨(수정) **주요 Epic**
- Epic 001: 주문 관리 - 주문 생성/조회/재고 관리/주문 취소 기능
- Epic 002: 결제 통합 - PayPal 결제/환불/Webhook 처리
- Epic 004: 알림 서비스 - 이메일 발송/재판매 알림
- Epic 003: 어필리에이트 추적 - 클릭 추적/판매 기록/성과 조회

✨(수정) **구현 전략**
- Iteration Zero (Day 1): CI/CD 파이프라인 구축 + 개발 인프라 설정
- Walking Skeleton (Day 2-3): End-to-End 흐름 구축 (주문 → 결제 → 이메일)
- Feature Completion (Day 4-5): P0 Epic 완성 + P1 Epic 추가
- Polish & Deploy (Day 6-7): Edge case + 리팩토링 + 프로덕션 배포
- 예상 완료 기간: 1주

---

## 3. 상세 내용

### 📋 목차
- [Epic 목록](#epic-목록)
- [의존성](#의존성)
- [실행 순서](#실행-순서)
- [요구사항 매핑](#요구사항-매핑)
- [성공 지표](#성공-지표)
- [리스크](#리스크)

---

### Epic 목록

✨(수정) #### EPIC-001: 주문 관리
- 상태: planning
- 우선순위: P0
- 한 줄 설명: 주문 생성/조회, 재고 관리, 주문 취소 기능 구현
- 관련 요구사항: [REQ-F03], [REQ-F04], [REQ-F14], [REQ-F15], [REQ-F25], [REQ-F26], [REQ-F27], [REQ-F28], [REQ-F29]

✨(수정) #### EPIC-002: 결제 통합
- 상태: planning
- 우선순위: P0
- 한 줄 설명: PayPal 결제 요청, Webhook 처리, 환불 처리 구현
- 관련 요구사항: [REQ-F02], [REQ-F09], [REQ-NF03]

✨(수정) #### EPIC-004: 알림 서비스
- 상태: planning
- 우선순위: P0
- 한 줄 설명: 주문 확인/배송 시작/재구매 관심 확인 이메일 발송 구현
- 관련 요구사항: [REQ-F10], [REQ-F11]

✨(수정) #### EPIC-003: 어필리에이트 추적
- 상태: planning
- 우선순위: P1
- 한 줄 설명: 어필리에이트 클릭 추적, 판매 기록, 성과 조회 대시보드 구현
- 관련 요구사항: [REQ-F05], [REQ-F06], [REQ-F07], [REQ-F08]

---

### 의존성

**기술적 의존성:**
- Epic 간 선후 관계 (A → B: A 완료 후 B 시작 가능)
  - EPIC-001 → EPIC-002: 주문 생성 후 결제 요청 가능
  - EPIC-002 → EPIC-004: 결제 완료 후 알림 발송 가능
  - EPIC-002 → EPIC-003: 결제 완료 시 어필리에이트 판매 기록

**외부 의존성:**
- 외부 API/서비스: PayPal API (결제/환불), Gmail SMTP (이메일 발송), 주소 자동완성 API (무료 플랜)
- 인프라: Railway (백엔드 호스팅), Cloudflare Pages (프론트엔드 호스팅)
- 디자인/리소스: 필리핀 현지 파트너 (배송 처리, 가장 나중 단계)

✨(수정) **외부 의존성 우선순위:**
1. Railway (백엔드 호스팅) - Phase 0 (Iteration Zero) CI/CD 구축 시 즉시 필요
2. PayPal API (결제 처리) - Phase 1 (Walking Skeleton) E2E 테스트에 필수
3. Gmail SMTP (이메일 발송) - Phase 1 (Walking Skeleton) E2E 완성에 필수
4. PayPal Refund API (환불 처리) - Phase 2 (Feature Completion) 주문 취소 기능 구현 시
5. 주소 자동완성 API - Phase 2 (Feature Completion) 사용자 편의 기능
6. 필리핀 현지 파트너 (배송) - Phase 3 이후 운영 단계

✨(수정) **블로킹 위험:**
- PayPal API 또는 Gmail SMTP 연동 지연 시 Walking Skeleton (Phase 1) 블로킹
- 완화 방안: PayPal Sandbox + 테스트 이메일 계정 먼저 연동, Mock 사용하여 개발 진행

---

### 실행 순서

✨(수정) | Phase | Epic | 목적/작업 내용 |
|-------|------|---------------|
| Phase 0 (Day 1) | 인프라 | **Iteration Zero**: CI/CD 파이프라인 구축 (GitHub Actions + Railway), 기본 프로젝트 구조, 헬스체크 엔드포인트, E2E 테스트 인프라 |
| Phase 1 (Day 2-3) | EPIC-001 (최소), EPIC-002 (최소), EPIC-004 (최소) | **Walking Skeleton**: E2E 테스트 작성 (주문 → 결제 → 이메일), 최소 기능 구현, CI/CD 통과 확인 |
| Phase 2 (Day 4-5) | EPIC-001 (완성), EPIC-002 (완성), EPIC-003 | **Feature Completion**: 재고 관리/주문 취소/환불 처리, 어필리에이트 추적, 추가 알림 기능 |
| Phase 3 (Day 6-7) | 전체 Epic | **Polish & Deploy**: Edge case 처리, 통합 테스트 보강, 리팩토링, 프로덕션 배포 |

✨(추가) **Walking Skeleton 구축 순서 (Phase 1):**
1. CI/CD 파이프라인 활용 (Phase 0에서 구축 완료)
2. E2E 테스트 작성 (Red): "주문 생성 → 결제 완료 → 이메일 발송" 시나리오
3. EPIC-001 최소 구현 (Green): 주문 생성/조회 API
4. EPIC-002 최소 구현 (Green): PayPal 결제 요청/Webhook 처리
5. EPIC-004 최소 구현 (Green): Gmail SMTP 연동, 주문 확인 이메일 발송
6. E2E 테스트 통과 확인: CI/CD 파이프라인에서 자동 검증

---

### 요구사항 매핑

| 요구사항 ID | 내용 요약 | 관련 Epic | 상태 |
|------------|---------|----------|------|
| REQ-F02 | PayPal 결제 | EPIC-002 | 계획중 |
| REQ-F03 | 배송지 정보 입력 | EPIC-001 | 계획중 |
| REQ-F04 | 주소 자동완성 | EPIC-001 | 계획중 |
| REQ-F05 | 어필리에이트 코드 추적 | EPIC-003 | 계획중 |
| REQ-F06 | 판매 데이터 기록 | EPIC-003 | 계획중 |
| REQ-F07 | 성과 조회 URL | EPIC-003 | 계획중 |
| REQ-F08 | 대시보드 표시 | EPIC-003 | 계획중 |
| REQ-F09 | 주문 확인 이메일 (주문 조회 링크) | EPIC-002 | 계획중 |
| REQ-F10 | 배송 완료 시 운송장 이메일 | EPIC-004 | 계획중 |
| REQ-F11 | 재구매 관심 확인 이메일 | EPIC-004 | 계획중 |
| REQ-F14 | 재고 자동 관리 | EPIC-001 | 계획중 |
| REQ-F15 | 주문 데이터 집계 | EPIC-001 | 계획중 |
| REQ-F25 | 주문 취소 기능 | EPIC-001 | 계획중 |
| REQ-F26 | 배송 전 취소 시 전액 환불 | EPIC-001 | 계획중 |
| REQ-F27 | 배송 후 취소 시 배송비 차감 환불 | EPIC-001 | 계획중 |
| REQ-F28 | 취소 확인 이메일 | EPIC-001 | 계획중 |
| REQ-F29 | 취소 시 재고 복구 | EPIC-001 | 계획중 |
| REQ-NF03 | HTTPS 보안 처리 | EPIC-002 | 계획중 |

**커버리지**: 전체 요구사항 18개 중 18개 매핑 완료

---

### 성공 지표

**프로젝트 레벨 목표:**
- 전체 Epic 완료율: 100% (4개 Epic 모두 done 상태)
- E2E 테스트: Git push 시 자동 테스트 + 배포 성공
- 배포 성공: Railway Production 환경 정상 동작

**측정 방법:**
- Epic 완료: 각 Epic의 Acceptance Test 모두 통과
- E2E 테스트: GitHub Actions 자동 실행 통과
- 배포 확인: `/health` 엔드포인트 200 OK + 수동 주문 테스트 성공

---

### 리스크

| 리스크 | 영향도 | 완화 방안 | 관련 Epic |
|--------|--------|----------|----------|
| PayPal API 연동 지연 | High | PayPal Sandbox 먼저 연동 + Mock 사용하여 개발 진행 | EPIC-002 |
| TDD 미숙으로 개발 속도 저하 | Medium | AI 도구 적극 활용 + 페어 프로그래밍 | 전체 |
| ✨(수정) 1주 일정 초과 | High | 중간 마일스톤 + 구현 범위 재조정<br>- Day 1: CI/CD 파이프라인 미완 시 수동 배포로 임시 대체<br>- Day 3: Walking Skeleton 미완 시 이메일 기능 Phase 2로 연기<br>- Day 5: P0 Epic 미완 시 P1 Epic 포기<br>- Day 6: 통합 테스트 미완 시 수동 테스트로 대체 | 전체 |

---

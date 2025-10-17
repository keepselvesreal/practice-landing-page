---
created_at: 2025-10-17 15:07:21
version: 1
status: Superseded
address: "landing_page/epic-overview"
links:
  in: [
    ./templates/epic-overview.md,
  ]
  out: [
    ../epic-overview.md,
    ./prd/cosmetics_landing_mvp.md,
    ./architecture/system_architecture.md,
    ./ai_sessions/cc_session_bf132ef3-d7d2-4eee-813c-aeadf30c88e0.txt,
  ]
tags: [epic-overview, mvp, k-beauty, philippines, planning]
notes: "필리핀 K-뷰티 랜딩페이지 MVP Epic 전체 조율 문서"
---

## 1. 압축 내용

**Epic Overview 한 줄 요약:**
- 주문-결제-어필리에이트-알림 기능을 통해 2주 내 10개 판매 달성 및 운영 프로세스 검증을 제공하며, 총 4개 Epic으로 1주에 걸쳐 구현한다.

---

## 2. 핵심 내용

**핵심 목표**
- 2주 내 10개 판매 달성
- 운영 프로세스(구매-배송-피드백) 검증 및 개선점 수집
- 어필리에이트 마케팅으로 지속 협업 가능한 인플루언서 2명 이상 확보

**주요 Epic**
- Epic 001: 주문 관리 - 주문 생성/조회/재고 관리/주문 취소 기능
- Epic 002: 결제 통합 - PayPal 결제/환불/Webhook 처리
- Epic 003: 어필리에이트 추적 - 클릭 추적/판매 기록/성과 조회
- Epic 004: 알림 서비스 - 이메일 발송/재판매 알림

**구현 전략**
- Walking Skeleton 우선 (Day 1-2: 전체 시나리오 최소 동작 + CI/CD)
- 핵심 기능 완성 (Day 3-5: P0 Epic 완료 + P1 Epic 추가)
- 통합 및 배포 (Day 6-7: Edge case + 리팩토링 + 배포)
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

#### EPIC-001: 주문 관리
- 상태: planning
- 우선순위: P0
- 한 줄 설명: 주문 생성/조회, 재고 관리, 주문 취소 기능 구현
- 관련 요구사항: [REQ-F03], [REQ-F04], [REQ-F14], [REQ-F15], [REQ-F25], [REQ-F26], [REQ-F27], [REQ-F28], [REQ-F29]

#### EPIC-002: 결제 통합
- 상태: planning
- 우선순위: P0
- 한 줄 설명: PayPal 결제 요청, Webhook 처리, 환불 처리 구현
- 관련 요구사항: [REQ-F02], [REQ-F09], [REQ-NF03]

#### EPIC-003: 어필리에이트 추적
- 상태: planning
- 우선순위: P1
- 한 줄 설명: 어필리에이트 클릭 추적, 판매 기록, 성과 조회 대시보드 구현
- 관련 요구사항: [REQ-F05], [REQ-F06], [REQ-F07], [REQ-F08]

#### EPIC-004: 알림 서비스
- 상태: planning
- 우선순위: P1
- 한 줄 설명: 주문 확인/배송 시작/재구매 관심 확인 이메일 발송 구현
- 관련 요구사항: [REQ-F10], [REQ-F11]

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

**외부 의존성 우선순위:**
1. PayPal API (결제 처리) - Walking Skeleton 구축 시 즉시 필요
2. PayPal Refund API (환불 처리) - Walking Skeleton 이후
3. Gmail SMTP (이메일 발송) - Walking Skeleton 이후
4. 주소 자동완성 API - Walking Skeleton 이후
5. 필리핀 현지 파트너 (배송) - 구현 완료 후 운영 단계

**블로킹 위험:**
- PayPal API 통합 지연 시 EPIC-002, 003, 004 모두 블로킹
- 완화 방안: PayPal Sandbox 먼저 연동, Mock 사용하여 개발 진행

---

### 실행 순서

| Phase | Epic | 의존성/이유 |
|-------|------|------------|
| Phase 1 (Day 1-2) | EPIC-001 (최소), EPIC-002 (최소) | Walking Skeleton 구축: 주문-결제 E2E 흐름 + CI/CD 파이프라인 |
| Phase 2 (Day 3-5) | EPIC-001 (완성), EPIC-002 (완성), EPIC-003, EPIC-004 | 핵심 기능 완성: 재고/취소/환불 + 어필리에이트/알림 추가 |
| Phase 3 (Day 6-7) | 전체 Epic | 통합 테스트, Edge case 처리, 리팩토링, 프로덕션 배포 |

**Walking Skeleton 구축 순서:**
1. EPIC-001 (최소): 주문 생성/조회
2. EPIC-002 (최소): PayPal 결제 요청/Webhook
3. CI/CD 파이프라인 구축 (Railway + GitHub Actions)
4. 첫 E2E 테스트 통과 (주문 생성 → 결제 → 주문 확정)

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
| 1주 일정 초과 | High | 중간 마일스톤 + 구현 범위 재조정<br>- Day 2: Walking Skeleton 미완 시 즉시 구현 범위 축소<br>- Day 4: P0 Epic 미완 시 P1 Epic 포기<br>- Day 6: 통합 테스트 미완 시 수동 테스트로 대체 | 전체 |

---

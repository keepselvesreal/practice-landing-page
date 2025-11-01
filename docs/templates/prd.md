---
version: 정수만 허용
notes: ""
created_date: [현재 한국 시간 YYYY-MM-DD HH:mm:ss 형식]
---

## 1. 압축 내용

이 PRD의 전체 핵심을 **한 문장**으로 요약
- 제품/서비스 전체 또는 특정 기능의 핵심 가치 제안

---

## 2. 핵심 내용

**해결할 문제**
- 2-3줄로 현재 페인 포인트 설명
- 시장/사용자가 겪는 문제 또는 기회

**제안 솔루션**
- 2-3줄로 어떻게 해결할지
- 제품/서비스 또는 기능의 접근 방식

**예상 임팩트**
- 2-3줄로 정량적 기대 효과
- 비즈니스 지표 또는 사용자 경험 개선 목표

---

## 3. 상세 내용

### 📋 목차
- [Opportunity](#opportunity)
- [Goals & Non-Goals](#goals--non-goals)
- [Constraints](#constraints)
- [Users & Scenarios](#users--scenarios)
- [Requirements (MoSCoW)](#requirements-moscow)
- [Traceability](#traceability)
- [Dependencies & Risks](#dependencies--risks)
- [Rollout & Feature Flags](#rollout--feature-flags)

---

### Opportunity

**제품/서비스 전체 PRD인 경우:**
- 시장 규모 (TAM/SAM/SOM)
- 경쟁 환경 분석
- 시장 기회 및 타이밍

**특정 기능 PRD인 경우:**
- 내부 데이터 (사용자 피드백, 지표)
- 경쟁사 유사 기능 현황
- 비즈니스 임팩트 예측

불릿 포인트로 간결하게

---

### Goals & Non-Goals

**Goals**
- 달성하려는 것들 (3-5개)
- 제품 전체 목표 또는 특정 기능 목표

**Non-Goals**
- 명시적으로 하지 않을 것들 (스코프 크리프 방지)
- Phase 구분이 필요한 경우 명시

#### Metrics

| 지표 | 목표 | 측정 시점 |
|------|------|-----------|
| [지표명] | [목표값] | [기간] |
| ... | ... | ... |

핵심 지표 3-5개, 정량적으로
- 제품 전체: 비즈니스 지표 (매출, 가입자, NPS 등)
- 특정 기능: 기능 사용 지표 (전환율, 사용 빈도 등)

#### Measurement Method

- 사용할 도구
- 추적할 이벤트 목록
- 측정 수식이나 집계 방법

---

### Constraints

**기술적 제약**
- 사용해야 하는 기술/플랫폼
- 용량/성능 제한

**비즈니스 제약**
- 정책적 제한
- 예산/비용 제약

**규제 제약**
- 법적 요구사항
- 컴플라이언스

#### Violation Actions

- [위반 사항] 시 [조치 방법]
- [위반 횟수/조건] 시 [추가 조치]

---

### Users & Scenarios

**Primary Users**

**1. [페르소나명] - [직업/역할]**
- 목표: [무엇을 달성하려 하는가]
- 페인 포인트: [현재 겪는 문제]
- 시나리오: [제품/기능을 어떻게 사용하는지 2-3문장으로 서술]

**2. [페르소나명] - [직업/역할]**
- 목표: ...
- 페인 포인트: ...
- 시나리오: ...

주요 사용자 2-3개 (제품 전체는 더 많을 수 있음)

---

### Requirements (MoSCoW)

**작성 범위:**
- 제품 전체 PRD: MVP 핵심 기능 중심, 높은 수준
- 특정 기능 PRD: 상세하고 구체적인 요구사항

#### Must Have (M)

**Functional**
- REQ-F01: [주체]는 [행동]을 할 수 있어야 함 ([조건/세부사항])
- REQ-F02: ...

**Non-Functional**
- REQ-NF01: [성능/보안/규정 요구사항] ([측정 가능한 기준])
- REQ-NF02: ...

#### Should Have (S)

- REQ-F##: ...
- REQ-NF##: ...

#### Could Have (C)

- REQ-F##: ...

#### Won't Have (W)

- REQ-F##: [하지 않을 것과 이유]

---

### Traceability

**Requirements → Epic 매핑**

*Epic Overview 문서 작성 후 이 섹션을 업데이트하세요.*

- REQ-F01 → [EP-##](../epics/ep-##-name.md)
- REQ-F02 → [EP-##](../epics/ep-##-name.md)
- ...

*Epic → Requirements 역추적은 Epic Overview 문서에서 다룹니다.*

---

### Dependencies & Risks

**Dependencies**
- [의존 항목], [예상 소요 기간] → **Critical Path 여부**
- 외부 API, 라이브러리, 인프라 등
- ...

**Risks**

| 리스크 | 영향도 | 대응 방안 |
|--------|--------|----------|
| [리스크 설명] | High/Medium/Low | [구체적 대응 방법] |
| ... | ... | ... |

---

### Rollout & Feature Flags

**(이 섹션은 다음 조건에만 포함)**
- 복잡한 시스템/높은 비즈니스 리스크
- 대규모 트래픽 예상
- 단계적 검증이 필요한 경우
- 제품 전체 PRD에서는 필수 권장

**Phase 1: [단계명] (Week X-Y)**
- Flag: `[flag_name]`
- 대상: [사용자 그룹]
- 포함 기능: [Epic 목록]
- 목표: [이 단계의 목표]

**Phase 2: [단계명] (Week X)**
- Flag: `[flag_name]`
- 대상: [사용자 그룹]
- 포함 기능: [Epic 목록]
- 모니터링: [추적할 지표]

**Kill Switch**
- `[emergency_flag_name]`: [어떤 상황에서 비활성화할지]

---

## 작성 원칙

1. **정량화**: 모든 목표와 요구사항은 측정 가능한 수치로 표현
2. **원자성**: 한 요구사항 = 한 기능/행위/조건
3. **간결성**: 불릿/표 활용, 장황한 설명 지양
4. **추적성**: 모든 REQ는 Epic와 연결 (Epic Overview 작성 후 Traceability 섹션 업데이트)
5. **What/Why만**: How(구현 방법)는 Tech Spec으로 분리
6. **MECE 원칙**: 요구사항은 상호 배타적이고 완전히 포괄적으로
7. **Non-Goals 명시**: 스코프 크리프 방지를 위해 명확히 제외 항목 정의
8. **범위 명확화**: 제품 전체 vs 특정 기능을 문서 시작 시 명시
9. **상세도 조절**: 제품 전체는 높은 수준, 특정 기능은 구체적으로
---
created_at: 2025-10-17 15:53:21
version: 2
status: Active
address: ""
links:
  in: [

  ]
  out: [
    ../epic-overview.md
  ]
tags: []
notes: ""
---

## 1. 압축 내용

**Epic Overview 한 줄 요약:**
- [핵심 기능]을 통해 [목적/가치]를 제공하며, 총 [N]개 Epic으로 [M]단계에 걸쳐 구현한다.

---

## 2. 핵심 내용

**핵심 목표**
- 이 프로젝트가 달성하고자 하는 비즈니스/기술적 목표
- 사용자/시스템에 제공하는 핵심 가치

**주요 Epic**
- Epic 1: 핵심 기능과 역할
- Epic 2: 핵심 기능과 역할
- Epic 3: 핵심 기능과 역할

**구현 전략**
- Epic 간 연관성과 구현 순서
- 예상 완료 기간

---

## 3. 상세 내용

### 📋 목차
- [Epic 목록](#epic-목록)
- [의존성](#의존성)
- [실행 순서](#실행-순서)
- [요구사항 매핑](#요구사항-매핑)
- [성공 지표](#성공-지표)
- [리스크](#리스크)
- [결정 사항](#결정-사항)
- [문서 버전 관리](#문서-버전-관리)

---

### Epic 목록

> 각 Epic은 아래 형식으로 작성합니다. 모든 참조는 마크다운 링크 형식 `[제목](경로)` 사용.

#### [EPIC-001: Epic 제목](./epics/epic-001-제목.md)
- 상태: planning (신규 Epic은 planning으로 시작) | in-progress | done
- 우선순위: P0(필수) | P1(중요) | P2(부가)
- 한 줄 설명: 이 Epic이 구체적으로 무엇을 만드는가 ("~을 구현", "~기능" 같은 명확한 표현 사용)
- 관련 요구사항: [REQ-XXX], [REQ-YYY]

**Epic ID 규칙**: EPIC-{순번 3자리}  
예: 첫 번째 Epic은 EPIC-001 (001부터 시작)  
파일 위치: `./epics/` 하위에 `epic-001-제목.md` 형식

---

### 의존성

**표기법**: A → B (A 완료 후 B 시작 가능, 화살표 방향 일관되게 사용)

**기술적 의존성:**
- Epic 간 선후 관계
  - EPIC-001 → EPIC-002: 이유

**외부 의존성:**
- 외부 API/서비스: 설명
- 인프라: 설명
- 디자인/리소스: 설명

**블로킹 위험:**
- 핵심 Epic 지연 시 영향 범위
- 완화 방안

---

### 실행 순서

| Phase | Epic | 의존성/이유 |
|-------|------|------------|
| Phase 1 | EPIC-001, EPIC-002 | 이유 |
| Phase 2 | EPIC-003 | 이유 |

**참고:**
- Phase는 1부터 시작
- 같은 Phase에 여러 Epic = 병렬 진행 가능

---

### 요구사항 매핑

| 요구사항 ID | 내용 요약 | 관련 Epic | 상태 |
|------------|---------|----------|------|
| REQ-001 | 요약 | [EPIC-001](링크) | 진행중/계획중/대기 |

**커버리지**: 전체 요구사항 N개 중 M개 매핑 완료

---

### 성공 지표

**프로젝트 레벨 목표:**
- 측정 가능한 목표 (완료율, 품질 지표)

**측정 방법:**
- 구체적인 측정 방식

---

### 리스크

| 리스크 | 영향도 | 완화 방안 | 관련 Epic |
|--------|--------|----------|----------|
| 설명 | High/Medium/Low | 대응책 | EPIC-001 |

---

### 결정 사항

| 날짜 | 내용 | 이유 | 관련 Epic |
|------|------|------|----------|
| YYYY-MM-DD | 결정 내용 | 상세한 이유와 근거 | EPIC-001 |

**날짜 형식**: YYYY-MM-DD

---

### 문서 버전 관리

**신규 파일 메타데이터 작성 가이드:**

신규 파일 생성 시 아래 형식에 맞춰 작성:
```yaml
---
created_at: 2025-10-17 15:30:00  # 현재 한국 시간 (YYYY-MM-DD HH:mm:ss)
version: 1  # 신규 파일은 1로 시작, 수정 시마다 +1
status: Active  # Active | Superseded | Deprecated
address: "k-cosmetics_landing_page/epic"  # 프로젝트/문서타입 형식
links:
  in: [
    ../epic-overview.md,  # 이 파일을 참조하는 파일들의 상대 경로
  ]
  out: [
    ./stories/story-001-001.md,  # 이 파일이 참조하는 파일들의 상대 경로
    ./stories/story-001-002.md,
  ]
tags: [epic, authentication, mvp]  # 검색/분류용 태그
notes: "사용자 인증 Epic"  # 파일에 대한 간단한 설명
---
```

**필드 작성 규칙:**
- `created_at`: 파일 생성 시점의 현재 한국 시간 입력 (수정 시에도 최신 시간으로 갱신)
- `version`: 신규 파일은 1, 수정할 때마다 1씩 증가 (정수만 허용)
- `status`: 신규 파일은 Active로 시작
- `address`: 프로젝트명/문서타입 형식으로 문서 주소 표현
- `links.in`: 현재 파일을 링크하는 상위 문서들의 상대 경로 입력
- `links.out`: 현재 파일이 링크하는 하위 문서들의 상대 경로 입력 (신규 파일은 빈 배열로 시작)
- `tags`: 문서 분류 및 검색에 도움되는 태그들을 배열로 작성
- `notes`: 파일 목적이나 주요 내용을 한 줄로 요약

---

**파일 구조:**
- Epic Overview 파일 위치: `docs/landing_page/` 하위에 `epic-overview.md` 형식으로 생성
- 아카이브 위치: `docs/landing_page/inbox/`

**파일 아카이브 규칙:**
1. 기존 파일을 `docs/landing_page/inbox/` 서브폴더로 이동
2. 파일명에 수정 날짜 추가 (YY-MM-DD 형식)

**파일명 규칙:**
```
원본 경로: docs/landing_page/epic-overview.md
아카이브: docs/landing_page/inbox/epic-overview--25-10-17.md
```

**새 버전 파일 생성:**
1. 원본과 동일한 파일명으로 새 파일 생성
2. 합의된 수정사항 반영
3. 수정된 부분에 표시 추가

**수정 부분 표시:**

Markdown 문서:
```markdown
✨(추가) **EPIC-004**: 새로운 Epic
🔧(수정) **EPIC-002**: 기존 Epic 내용 변경
```

**메타데이터 업데이트:**

**version 처리:**
```yaml
# 기존 파일
version: 1

# 새 파일
version: 2
```

**created_at 처리:**
```yaml
# 새 파일
created_at: 2025-10-17 15:30:00  # 현재 날짜/시간
```

**status 처리:**
```yaml
# 아카이브된 이전 파일 (inbox/)
status: Superseded

# 새 파일
status: Active
```

**links 처리:**
```yaml
# 새 파일
links:
  in: [
    inbox/epic-overview--25-10-17.md,  # 이전 버전 추가
    ../index.md,
  ]
  out: [
    ./epics/epic-001-제목.md,  # Epic 파일 생성 후 경로 추가
  ]
```

**notes 처리:**
```yaml
# 새 파일
notes: "EPIC-004 추가, EPIC-002 수정 (v1에서 수정)"
```
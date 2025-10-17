---
created_at: 2025-10-17 15:55:03
version: 1
status: Active
address: ""
links:
  in: []  # 현재 파일을 참조하는 파일의 상대 경로
  out: []  # 현재 파일이 참조하는 파일의 상대 경로
tags: []
notes: ""
---

## 1. 압축 내용

**Epic 한 줄 요약:**
- [기능]을 구현하여 [사용자 가치]를 제공하며, [N]개의 User Story로 구성된다.

---

## 2. 핵심 내용

**Epic 목표**
- 이 Epic으로 달성하려는 구체적 목표

**사용자 가치**
- 사용자가 얻는 실질적 혜택, 해결되는 문제

**기술적 범위**
- 구현할 기능과 기술 요소, 시스템 경계

**미포함 사항**
- 이 Epic에서 다루지 않는 것, 명시적 제외 항목

**완료 조건**
- Epic이 완료되었다고 판단하는 명확한 기준 (모든 AC 통과, Story 완료 등)

---

## 3. 상세 내용

### 📋 목차
- [User Story 목록](#user-story-목록)
- [의존성](#의존성)
- [실행 순서](#실행-순서)
- [Acceptance Criteria](#acceptance-criteria)
- [성공 지표](#성공-지표)
- [리스크](#리스크)
- [문서 버전 관리](#문서-버전-관리)

---

### User Story 목록

> 각 Story는 아래 형식으로 작성합니다. 모든 참조는 마크다운 링크 형식 `[제목](경로)` 사용.

#### [STORY-001-001: Story 제목](./stories/story-001-001.md)
- 상태: planning (신규 Story는 planning으로 시작) | in-progress | done
- 우선순위: P0 | P1 | P2
- 한 줄 설명: "사용자는 ~할 수 있다" 형식으로 사용자 관점 기능
- 예상 복잡도: S(작음) | M(중간) | L(큼) | XL(매우 큼)

**Story ID 규칙**: STORY-{EPIC번호}-{순번 3자리}  
예: EPIC-001의 첫 번째 Story는 STORY-001-001 (Story의 Epic 번호는 이 Epic 번호와 반드시 일치)  
파일 위치: `./stories/` 하위에 `story-001-001.md` 형식

---

### 의존성

**표기법**: A → B (A 완료 후 B 시작 가능, 화살표 방향 일관되게 사용)

**Story 간 의존성:**
- STORY-001-002 → STORY-001-001
  - 이유: [왜 선행 Story가 필요한가]
- STORY-001-004 → STORY-001-002, STORY-001-003
  - 이유: [복수 의존성 이유]

**외부 Epic 의존성:**
- [EPIC-002](../epic-002-제목.md)
  - 관계: [어떤 기능/데이터가 필요한가]
- [EPIC-003](../epic-003-제목.md)
  - 관계: [의존 관계 설명]

**기술적 의존성:**
- 외부 라이브러리, API, 인프라 등
- 각 의존성이 왜 필요한지 간단히 설명

---

### 실행 순서

| 순서 | Story | 의존성 | 이유 |
|------|-------|--------|------|
| 1 | STORY-001-001, STORY-001-002 | 없음 | 병렬 진행 가능, 독립적 기능 |
| 2 | STORY-001-003 | STORY-001-001 | 001의 인증 기능 필요 |
| 3 | STORY-001-004 | STORY-001-002, 003 | 002의 데이터와 003의 권한 체크 필요 |

**참고:**
- 순서는 1부터 시작
- 같은 순서에 여러 Story = 병렬 진행 가능
- 의존성 컬럼: 선행 완료 필요한 Story ID (없으면 "없음")
- 이유 컬럼: 왜 이 순서인가, 왜 의존성이 있는가

---

### Acceptance Criteria

**Epic 레벨의 AC를 체크리스트 형식으로:**

- [ ] AC-001: [기능 설명] (예: 사용자는 Google 계정으로 로그인할 수 있다)
- [ ] AC-002: [시스템 동작] (예: 로그인 실패 시 명확한 에러 메시지가 표시된다)
- [ ] AC-003: [성능/품질 기준] (예: 세션은 7일간 유지된다)

**AC ID 규칙**: AC-{순번 3자리}

**총 AC**: [개수] 정의

**(각 AC가 어느 User Story에서 구현되는지는 개별 Story 문서 참조)**

**각 AC는:**
- 측정 가능해야 함
- 검증 가능해야 함
- 사용자 관점 또는 시스템 동작 관점

---

### 성공 지표

**Epic 레벨 목표:**
- 모든 AC 통과율 100%
- User Story 완료율 100%
- 성능 기준: [구체적 메트릭]
- 품질 기준: [테스트 커버리지 등]

**측정 방법:**
- Story별 완료 체크리스트
- AC 검증 테스트 통과 여부
- 성능/품질 메트릭 모니터링 방법

---

### 리스크

| 리스크 | 영향도 | 완화 방안 | 관련 Story |
|--------|--------|----------|-----------|
| [위험 요소] | High/Medium/Low | [구체적 대응 방법] | STORY-001-001 |

**각 리스크는:**
- 구체적으로 어떤 문제가 발생할 수 있는가
- 어느 Story에 영향을 주는가
- 실행 가능한 완화 방안

**Story별 상세 리스크는 개별 문서 참조**

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
- Epic 파일 위치: `docs/landing_page/epics/` 하위에 `epic-001-제목.md` 형식으로 생성
- 아카이브 위치: `docs/landing_page/inbox/`

**파일 아카이브 규칙:**
1. 기존 파일을 `docs/landing_page/inbox/` 서브폴더로 이동
2. 파일명에 수정 날짜 추가 (YY-MM-DD 형식)

**파일명 규칙:**
```
원본 경로: docs/landing_page/epics/epic-001-제목.md
아카이브: docs/landing_page/inbox/epic-001-제목--25-10-17.md
```

**새 버전 파일 생성:**
1. 원본과 동일한 파일명으로 새 파일 생성
2. 합의된 수정사항 반영
3. 수정된 부분에 표시 추가

**수정 부분 표시:**

Markdown 문서:
```markdown
✨(추가) **STORY-001-005**: 새로운 User Story
🔧(수정) **STORY-001-002**: 기존 Story 내용 변경
```

**메타데이터 업데이트:**

version 처리:
```yaml
# 기존 파일
version: 1

# 새 파일
version: 2
```

created_at 처리:
```yaml
# 새 파일
created_at: 2025-10-17 15:30:00  # 현재 날짜/시간
```

status 처리:
```yaml
# 아카이브된 이전 파일 (inbox/)
status: Superseded

# 새 파일
status: Active
```

links 처리:
```yaml
# 새 파일
links:
  in: [
    ../../inbox/epic-001-제목--25-10-17.md,  # 이전 버전 추가
    ../epic-overview.md,
  ]
  out: [
    ./stories/story-001-001.md,  # User Story 파일 생성 후 경로 추가
  ]
```

notes 처리:
```yaml
# 새 파일
notes: "STORY-001-005 추가 (v1에서 수정)"
```
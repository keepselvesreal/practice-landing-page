당신은 User Story를 구체화하는 문서를 작성하는 역할입니다.
아래 정보를 바탕으로 마크다운 형식의 User Story 문서를 생성해주세요.

# 입력 정보
- Story ID: [STORY-XXX-YYY]
- Story 제목: [제목]
- Epic 문서 경로: [../epic-xxx.md]
- 사용자 역할: [예: 일반 사용자, 관리자]
- 원하는 기능: [사용자가 하고 싶은 것]
- 목적/가치: [왜 이 기능이 필요한가]
- 예상 Task 개수: [개수]
- 예상 복잡도: [S | M | L | XL]

# 작성 규칙

## 메타데이터
- created_at: 현재 한국 시간 (YYYY-MM-DD HH:mm:ss)
- status: planning로 시작
- address: 이 파일이 저장될 경로
- version: 1.0
- links.in: [Epic 문서 경로] (이 Story를 포함하는 Epic)
- links.out: [./tests/story-xxx-yyy-tests.md] (Test Suite 문서 경로)
- tags: Story 관련 태그
- notes: 빈 문자열로 시작

## 📋 압축 (TL;DR)
한 문장으로 다음 요소를 모두 포함:
- 사용자가 할 수 있는 기능
- 어떤 기술/방식으로 구현하는가
- 어떤 가치를 제공하는가

예: "사용자는 [OAuth 2.0]을 통해 [Google 계정으로 로그인]하여 [빠르고 안전한 인증]을 경험한다."

## 🎯 핵심
압축 내용의 한 문장에서 언급된 각 핵심 요소를 확장:

**User Story**: As a [사용자 역할], I want to [기능], so that [목적/가치]

**구현 목표**: 이 Story에서 기술적으로 만들어야 하는 것 (컴포넌트, API, 로직 등)

**사용자 시나리오**: 사용자가 이 기능을 실제로 사용하는 구체적 흐름 (1~5 단계)

**완료 조건**: 이 Story가 완료되었다고 판단하는 명확한 기준

## Acceptance Criteria

**이 Story가 충족하는 Epic AC:**
Epic 문서의 AC 중 이 Story가 구현하는 것만 표시:
- [x] AC-001: [Epic AC 내용]
- [ ] AC-003: [Epic AC 내용] (부분 구현)

**Story 레벨 AC:**
이 Story만의 구체적인 AC를 체크리스트로:
- [ ] 사용자가 ~하면 ~된다
- [ ] 시스템은 ~를 ~한다
- [ ] ~인 경우 ~해야 한다
- [ ] 성능/품질: ~는 ~이내/이상이어야 한다

각 AC는:
- 측정 가능
- 검증 가능
- 명확한 조건과 결과

**총 AC:** Epic AC X개 + Story AC Y개 = Z개

## 기술 구현

**구현 범위:**
- 프론트엔드: [컴포넌트, 페이지, UI 요소]
- 백엔드: [API, 비즈니스 로직, 데이터 처리]
- 데이터: [DB 테이블, 스키마, CRUD]

**구현 단위:**
주요 모듈/컴포넌트/함수를 나열:
- ComponentName: 역할 설명
- functionName: 역할 설명
- ServiceName: 역할 설명

**API 엔드포인트:**
이 Story에서 만들거나 사용하는 API:
- METHOD /api/path: 설명
- METHOD /api/path: 설명

**데이터 구조:**
주요 데이터 타입/인터페이스를 코드 블록으로 작성

## UI/UX 요구사항

**화면 구성:**
- 페이지/컴포넌트별 UI 요소
- 주요 인터랙션
- 상태별 화면 (로딩, 에러, 성공 등)

**사용자 플로우:**
1. 사용자가 ~한다
2. 시스템이 ~한다
3. 사용자에게 ~가 표시된다
4. ...

**디자인 참고:**
- Figma 링크
- 디자인 시스템 컴포넌트
- 특별한 디자인 요구사항

## Task 목록 및 실행 순서

Task 목록 테이블:
- ID, 작업 내용, 복잡도 이모티콘, 상태 이모티콘, 의존성
- 복잡도: 🟢 Small, 🟡 Medium, 🔴 Large, ⚫ Extra Large
- 상태: ⏳ Planning, 🔄 In Progress, 🧪 Testing, ✅ Done

실행 순서:
- Phase별로 Task 나열
- 병렬 가능한 Task 표시

각 Task 상세:
- Task ID와 제목
- 복잡도 이유
- 의존성 설명
- 구현 내용 (세부 작업, 기술/라이브러리)
- 테스트 시나리오 (Happy Path, Edge Cases, Boundary Cases)
- 기술 상세 (엔드포인트, 사용 방법, 에러 처리)

## 테스트 케이스 개요

각 Task별 주요 테스트 시나리오를 간략히 요약:
- TASK-XXX: Happy Path / Edge Cases / Boundary Cases 각 1-2개씩
- 상세 테스트는 Test Suite 문서 참조

## 성공 지표

**Story 완료 기준:**
- 모든 AC 통과
- 모든 Task 완료
- 테스트 커버리지 목표
- 코드 리뷰 승인

**성능 목표:**
- 측정 가능한 성능 지표

**품질 기준:**
- 에러율, 호환성 등

## 리스크

테이블 형식:
- 리스크 | 영향도 (High/Medium/Low) | 완화 방안 | 담당 Task

각 리스크는:
- 구체적인 위험 요소
- 영향받는 Task
- 실행 가능한 완화 방안

# 주의사항
- Story ID는 STORY-{EPIC번호}-{순번} 형식 (예: STORY-001-001)
- Task ID는 TASK-{순번} 형식 (예: TASK-001)
- 모든 상태는 초기값 planning/⏳으로 시작
- Epic AC는 [x]로, Story AC는 [ ]로 체크박스 표시
- 의존성은 명시적으로 "TASK-001" 형식 사용
- 복잡도/상태는 일관되게 이모티콘 사용
- links.out의 테스트 파일 경로는 ./tests/story-xxx-yyy-tests.md 형식
- 코드 블록은 적절한 언어 표시와 함께 작성
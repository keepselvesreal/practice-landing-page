---
created_at: 2025-10-10 00:00:00
links:
  - ./guide_project_overview_v1.md
  - ./guide_folder_structure_v1.md
  - ./guide_detailed_design_v1.md
  - ./guide_tdd_application_v1.md
  - ./guide_references_v1.md
  - ./guide_additional_considerations_v1.md
---

# 화장품 랜딩페이지 구현 가이드
## Hexagonal Architecture 기반 프로젝트 설계

---

## 📋 목차

1. [프로젝트 개요](./guide_project_overview_v1.md)
2. [프로젝트 폴더 구조](./guide_folder_structure_v1.md)
3. [모듈별 상세 설계](./guide_detailed_design_v1.md)
4. [TDD 적용 가이드](./guide_tdd_application_v1.md)
5. [참조 및 근거](./guide_references_v1.md)
6. [추가 고려사항](./guide_additional_considerations_v1.md)

---

## 결론

이 문서는 **Hexagonal Architecture**와 **TDD** 원칙에 따라 화장품 랜딩페이지 프로젝트의 폴더 구조, 모듈 설계, 테스트 전략을 제공합니다.

**핵심 원칙**:
1. **도메인 중심**: 비즈니스 로직을 중앙에 배치
2. **의존성 역전**: 모든 의존성이 내부를 향함
3. **포트-어댑터**: 외부 세계와의 통신을 격리
4. **교체 가능성**: 어댑터를 쉽게 교체 가능
5. **TDD 사이클**: Red → Green → Refactor
6. **Walking Skeleton**: E2E 테스트부터 시작

이 문서를 참고하여 실제 프로젝트 폴더와 파일을 생성하고, 각 모듈의 역할과 책임을 이해하며, TDD를 통해 안정적인 코드를 작성할 수 있습니다.

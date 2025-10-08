---
created_at: "Tue Oct 07 21:58:35 KST 2025 KST"
links:
  - docs/landing_page/imple_guide_25-10-06.md
  - references/Growing_object_oriented_software_guided_by_tests/Chapter_4_Kick_Starting_the_Test_Driven_Cycle/extracted_information.md
  - references/Growing_object_oriented_software_guided_by_tests/Chapter_5_Maintaining_the_Test_Driven_Cycle/extracted_information.md
  - references/Growing_object_oriented_software_guided_by_tests/Chapter_6_Object_Oriented_Style/extracted_information.md
  - references/Growing_object_oriented_software_guided_by_tests/Chapter_7_Achieving_Object_Oriented_Design/extracted_information.md
  - references/Growing_object_oriented_software_guided_by_tests/Chapter_8_Building_on_Third_Party_Code/extracted_information.md
  - references/Growing_object_oriented_software_guided_by_tests/Chapter_20_Listening_to_the_Tests/extracted_information.md
  - references/Growing_object_oriented_software_guided_by_tests/Chapter_21_Test_Readability/extracted_information.md
  - references/Growing_object_oriented_software_guided_by_tests/Chapter_22_Constructing_Complex_Test_Data/extracted_information.md
  - references/Growing_object_oriented_software_guided_by_tests/Chapter_23_Test_Diagnostics/extracted_information.md
  - references/Growing_object_oriented_software_guided_by_tests/Chapter_24_Test_Flexibility/extracted_information.md
---

## 압축 내용
Walking Skeleton 기반 인수 테스트로 외곽을 고정하고, 포트·어댑터 경계와 지원 도구(빌더, 진단, 유연성)를 통해 테스트 가능성과 설계 적응력을 유지한다.

## 핵심 내용

### 핵심 개념들
- **Walking Skeleton 인수 파이프라인** — references/Growing_object_oriented_software_guided_by_tests/Chapter_4_Kick_Starting_the_Test_Driven_Cycle/extracted_information.md:41-115; references/Growing_object_oriented_software_guided_by_tests/Chapter_5_Maintaining_the_Test_Driven_Cycle/extracted_information.md:20-176
- **Outside-In 포트 설계** — references/Growing_object_oriented_software_guided_by_tests/Chapter_6_Object_Oriented_Style/extracted_information.md:32-154; references/Growing_object_oriented_software_guided_by_tests/Chapter_7_Achieving_Object_Oriented_Design/extracted_information.md:21-128
- **테스트 데이터 및 지원 라이브러리** — references/Growing_object_oriented_software_guided_by_tests/Chapter_22_Constructing_Complex_Test_Data/extracted_information.md:17-66; references/Growing_object_oriented_software_guided_by_tests/Chapter_23_Test_Diagnostics/extracted_information.md:1-50
- **테스트가 제공하는 설계 피드백** — references/Growing_object_oriented_software_guided_by_tests/Chapter_20_Listening_to_the_Tests/extracted_information.md:9-51; references/Growing_object_oriented_software_guided_by_tests/Chapter_21_Test_Readability/extracted_information.md:36-49
- **어댑터 계약과 제3자 통합** — references/Growing_object_oriented_software_guided_by_tests/Chapter_8_Building_on_Third_Party_Code/extracted_information.md:59-177
- **테스트 유연성과 상호작용 제어** — references/Growing_object_oriented_software_guided_by_tests/Chapter_24_Test_Flexibility/extracted_information.md:19-74

### 핵심 개념 설명
- **Walking Skeleton 인수 파이프라인**: 첫 기능 전에 배포·테스트 가능한 얇은 시스템을 세우고, 인수 테스트로 red→green 흐름을 추적해 리스크를 조기에 드러낸다. 이를 통해 초기부터 전체 피드백 루프를 확보한다. (references/Growing_object_oriented_software_guided_by_tests/Chapter_4_Kick_Starting_the_Test_Driven_Cycle/extracted_information.md:41-115; references/Growing_object_oriented_software_guided_by_tests/Chapter_5_Maintaining_the_Test_Driven_Cycle/extracted_information.md:20-176)
- **Outside-In 포트 설계**: 포트·어댑터 아키텍처와 테스트 우선 접근으로 인터페이스를 애플리케이션 용어로 정의하고, 협력 객체 간 통신을 좁은 책임으로 유지한다. (references/Growing_object_oriented_software_guided_by_tests/Chapter_6_Object_Oriented_Style/extracted_information.md:32-154; references/Growing_object_oriented_software_guided_by_tests/Chapter_7_Achieving_Object_Oriented_Design/extracted_information.md:21-128)
- **테스트 데이터 및 지원 라이브러리**: 테스트 데이터 빌더와 공통 매처/스파이를 도입해 복잡한 입력을 선언적으로 표현하고 실패 시 즉시 진단한다. (references/Growing_object_oriented_software_guided_by_tests/Chapter_22_Constructing_Complex_Test_Data/extracted_information.md:17-66; references/Growing_object_oriented_software_guided_by_tests/Chapter_23_Test_Diagnostics/extracted_information.md:1-50)
- **테스트가 제공하는 설계 피드백**: 테스트 작성이 어렵거나 읽기 어렵다면 설계를 개선해야 하며, 명확한 이름과 구조로 의도 표현을 유지해야 한다. (references/Growing_object_oriented_software_guided_by_tests/Chapter_20_Listening_to_the_Tests/extracted_information.md:9-51; references/Growing_object_oriented_software_guided_by_tests/Chapter_21_Test_Readability/extracted_information.md:36-49)
- **어댑터 계약과 제3자 통합**: 제3자 타입을 직접 Mock하지 않고, 우리 포트를 구현하는 얇은 어댑터와 집중된 통합 테스트로 계약을 검증한다. (references/Growing_object_oriented_software_guided_by_tests/Chapter_8_Building_on_Third_Party_Code/extracted_information.md:59-177)
- **테스트 유연성과 상호작용 제어**: Allow/Expect 규칙과 정보-표현 분리를 적용해 테스트가 구현 세부사항에 결합되지 않도록 한다. (references/Growing_object_oriented_software_guided_by_tests/Chapter_24_Test_Flexibility/extracted_information.md:19-74)

### 핵심 개념 간 관계
Walking Skeleton 인수 파이프라인이 전체 피드백 루프를 열면, Outside-In 포트 설계가 서비스·도메인 경계를 구체화하고, 테스트 데이터/지원 라이브러리가 해당 경계를 선언적으로 재사용할 수 있게 한다. 이 과정에서 테스트가 제공하는 설계 피드백이 인터페이스와 데이터 모델을 다듬고, 어댑터 계약 테스트가 외부 의존성을 격리하며, 유연성 규칙이 테스트 스위트가 리팩터링을 방해하지 않도록 보정한다. (references/Growing_object_oriented_software_guided_by_tests/Chapter_4_Kick_Starting_the_Test_Driven_Cycle/extracted_information.md:41-115; references/Growing_object_oriented_software_guided_by_tests/Chapter_5_Maintaining_the_Test_Driven_Cycle/extracted_information.md:20-176; references/Growing_object_oriented_software_guided_by_tests/Chapter_6_Object_Oriented_Style/extracted_information.md:32-154; references/Growing_object_oriented_software_guided_by_tests/Chapter_8_Building_on_Third_Party_Code/extracted_information.md:59-177; references/Growing_object_oriented_software_guided_by_tests/Chapter_24_Test_Flexibility/extracted_information.md:19-74)

## 상세 내용
1. **Walking Skeleton과 CI 파이프라인 구성**: 최소 경로와 자동 배포·테스트 루프를 준비해 인수 테스트가 즉시 실행되도록 한다. (references/Growing_object_oriented_software_guided_by_tests/Chapter_4_Kick_Starting_the_Test_Driven_Cycle/extracted_information.md:41-115)
2. **첫 인수 시나리오 정의**: 도메인 용어로 실패하는 시나리오를 작성하고 진행 중 테스트와 회귀 테스트를 분리한다. (references/Growing_object_oriented_software_guided_by_tests/Chapter_5_Maintaining_the_Test_Driven_Cycle/extracted_information.md:20-176)
3. **Outside-In 서비스 개발**: Acceptance에서 노출된 경계를 기준으로 포트 상호작용을 테스트하고, 협력 객체 책임을 좁게 유지한다. (references/Growing_object_oriented_software_guided_by_tests/Chapter_6_Object_Oriented_Style/extracted_information.md:32-154; references/Growing_object_oriented_software_guided_by_tests/Chapter_7_Achieving_Object_Oriented_Design/extracted_information.md:21-128)
4. **도메인 타입 정제와 테스트 데이터 빌더 도입**: 값 타입과 엔티티 테스트를 강화하고 반복적인 설정은 빌더/헬퍼로 추상화한다. (references/Growing_object_oriented_software_guided_by_tests/Chapter_22_Constructing_Complex_Test_Data/extracted_information.md:17-66)
5. **어댑터 계약 확립**: 포트 인터페이스를 구현한 어댑터를 집중 통합 테스트로 검증하고 실패/롤백 분기를 캡처한다. (references/Growing_object_oriented_software_guided_by_tests/Chapter_8_Building_on_Third_Party_Code/extracted_information.md:59-177)
6. **가독성과 진단 강화**: TestDox 이름, 명확한 구조, 자기 설명 매처로 테스트가 의도를 전달하도록 리팩터링한다. (references/Growing_object_oriented_software_guided_by_tests/Chapter_21_Test_Readability/extracted_information.md:36-49; references/Growing_object_oriented_software_guided_by_tests/Chapter_23_Test_Diagnostics/extracted_information.md:1-50)
7. **테스트 유연성 보정**: Allow/Expect 규칙과 무관한 객체 무시 전략을 적용해 테스트가 리팩터링에 견디도록 유지한다. (references/Growing_object_oriented_software_guided_by_tests/Chapter_24_Test_Flexibility/extracted_information.md:19-74; references/Growing_object_oriented_software_guided_by_tests/Chapter_20_Listening_to_the_Tests/extracted_information.md:9-51)

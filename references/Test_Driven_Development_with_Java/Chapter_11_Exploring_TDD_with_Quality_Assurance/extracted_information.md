# Test_Driven_Development_with_Java_Chapter_11_Exploring_TDD_with_Quality_Assurance

## 압축 내용

TDD는 자동화된 테스트를 통해 개발 시점의 기능 검증과 회귀 테스트를 효과적으로 제공하지만, 수동 탐색적 테스트, 코드 리뷰, UI/UX 평가, 보안 테스트 등의 인간 중심 활동과 결합되어야만 최고 품질의 소프트웨어를 완성할 수 있다는 종합적 품질 보증 전략을 제시한다. (Lines 2-464)

---

## 핵심 내용

### TDD의 한계와 수동 테스트의 필요성 → [1. TDD의 한계 인식]
- TDD는 개발 시점 기능 테스트와 회귀 테스트 자동화로 많은 수동 프로세스를 제거하지만, 인간의 창의성과 판단이 필요한 영역은 여전히 수동 개입이 필수적임
- 자동화된 테스트는 소프트웨어 머신으로서 시각적 검사, UI 평가, 사용자 경험 판단 등을 수행할 수 없음 (Lines 21-87)

### 수동 탐색적 테스트 (Manual Exploratory Testing) → [2. 탐색적 테스트 전략]
- 자동화된 테스트가 놓친 결함을 찾는 중요한 방어선으로, 인간의 창의성과 통찰력을 활용해 경계 조건과 누락된 테스트를 발견
- 자동화 테스트와 수동 탐색적 테스트의 특성 비교: 반복 가능 vs 창의적, 알려진 결과 검증 vs 미지의 결과 발견 (Lines 88-164)

### 코드 리뷰와 앙상블 프로그래밍 → [3. 코드 품질 검증 방법]
- 정적 분석 도구(Sonarqube 등)는 고정된 규칙을 적용하지만, 인간 리뷰는 컨텍스트 기반 판단과 경험적 학습을 제공
- Pull Request 리뷰, 페어 프로그래밍, 앙상블(Mob) 프로그래밍 등 다양한 방식으로 코드 작성 중 또는 후에 품질 향상 가능 (Lines 165-235)

### UI/UX 테스트 → [4. 사용자 인터페이스 검증], [5. 사용자 경험 평가]
- TDD로 UI 기능 요소의 존재를 검증할 수 있지만, 디자인 품질, 브랜드 정렬, 사용 편의성, 논리적 흐름 등은 인간만이 평가 가능
- 사용자 경험 디자인은 공감, 심리학, 실험을 결합한 인간 활동으로, 실제 사용자 피드백 수집과 분석이 필수 (Lines 236-323)

### 보안 테스트와 운영 모니터링 → [6. 보안 및 운영 관리]
- 침투 테스트(Pentesting)는 새로운 취약점과 미지의 보안 위협을 발견하기 위해 인간의 독창성이 필요한 특수한 수동 탐색적 테스트
- OWASP Top 10, STRIDE 위협 모델, Fuzzing 등의 도구와 방법론을 활용한 보안 검증 (Lines 324-363)

### CI/CD 워크플로우와 수동 프로세스 통합 → [7. 자동화와 수동화 조화]
- Blocking Workflow: 각 수동 단계 완료까지 자동화를 중단하는 방식으로 단순하지만 배포 주기가 길어짐
- Dual-Track Workflow: Feature Flag를 활용해 자동화 배포와 수동 테스트를 병렬로 진행하여 더 빈번한 배포 가능 (Lines 364-412)

### 핵심 개념 간 관계
- **TDD의 한계** → **수동 탐색적 테스트**: TDD가 자동화할 수 없는 창의적 테스트 영역 보완
- **자동화 테스트** ↔ **수동 테스트**: 서로 대체가 아닌 상호 보완 관계로 품질 향상
- **코드 리뷰** → **페어/앙상블 프로그래밍**: 사후 검토에서 실시간 협업으로 발전
- **UI 기능 테스트** → **UX 평가**: 기능 존재 확인에서 사용자 만족도 평가로 확장
- **보안 테스트** → **운영 모니터링**: 취약점 발견에서 지속적 건강 상태 관리로 연결
- **수동 프로세스** → **CI/CD 통합**: 자동화 파이프라인 내 인간 의사결정 지점 삽입

---

## 상세 내용

### 목차
1. [TDD의 한계 인식](#1-tdd의-한계-인식)
2. [탐색적 테스트 전략](#2-탐색적-테스트-전략)
3. [코드 품질 검증 방법](#3-코드-품질-검증-방법)
4. [사용자 인터페이스 검증](#4-사용자-인터페이스-검증)
5. [사용자 경험 평가](#5-사용자-경험-평가)
6. [보안 및 운영 관리](#6-보안-및-운영-관리)
7. [자동화와 수동화 조화](#7-자동화와-수동화-조화)

---

### 1. TDD의 한계 인식

**핵심 내용(압축 내용, 핵심 내용)과의 관계**: TDD의 한계와 수동 테스트의 필요성

TDD는 Kent Beck이 1996년 Chrysler Comprehensive Compensation 프로젝트에서 도입한 test-first 단위 테스트에서 현대적 기원을 찾을 수 있다. 이 프로젝트는 작은 반복, 빈번한 릴리스, 광범위한 단위 테스트 사용이 특징이었다. (Lines 30-38)

전통적인 수동 테스트 방식은 테스트 전략 문서와 상세 테스트 계획서 작성에 많은 시간을 소비했으며, 각 릴리스마다 테스트 데이터 준비, 애플리케이션 실행, UI 클릭, 결과 문서화, 결함 보고 등의 수작업이 필요했다. (Lines 39-53)

```java
// TDD를 통한 자동화된 테스트 예시
@Test
public void convertsToLowerCase() {
    // TDD는 이런 테스트를 실행 가능한 코드로 작성하여
    // 언제든 반복 실행 가능하고, 코드 변경 시 자동으로 업데이트됨
    var username = new Username("SirJakington35179");
    String actual = username.asLowerCase();
    assertThat(actual).isEqualTo("sirjakington35179");
}
```

**TDD가 제거하는 수동 프로세스** (Lines 59-72):
- **개발 중 기능 테스트**: 새 기능 개발 시 자동화된 테스트를 먼저 작성하므로, 테스트 설정과 UI 클릭 과정이 자동화됨
- **릴리스 전 회귀 테스트**: 모든 테스트를 소스 제어에 보관하고 모든 빌드마다 자동 실행하여 기존 기능 손상 방지

```python
# Python 버전 - 회귀 테스트 스위트 개념
class RegressionTestSuite:
    def __init__(self):
        # 모든 과거 테스트를 축적하여 보관
        self.all_tests = []

    def add_test(self, test):
        # 새 기능 추가 시 테스트도 추가
        self.all_tests.append(test)

    def run_all_tests(self):
        # 모든 빌드마다 전체 테스트 실행
        # "빠르게 움직이되 아무것도 깨뜨리지 않는다"
        for test in self.all_tests:
            test.execute()
```

**자동화 테스트의 한계** (Lines 83-87):
- 스스로 생각할 수 없음
- 코드를 시각적으로 검사할 수 없음
- 사용자 인터페이스의 외관 평가 불가
- 사용자 경험의 좋고 나쁨 판단 불가
- 전체 시스템의 목적 적합성 판단 불가

---

### 2. 탐색적 테스트 전략

**이전 주제와의 관계**: TDD의 한계 인식 → TDD가 놓친 테스트를 발견하는 탐색적 테스트 필요

**핵심 내용(압축 내용, 핵심 내용)과의 관계**: 수동 탐색적 테스트 (Manual Exploratory Testing)

TDD의 가장 큰 위협은 소프트웨어가 처리해야 하는 모든 조건을 생각하는 능력의 한계이다. 복잡한 소프트웨어는 엄청난 입력 조합, 경계 사례, 설정 옵션을 가진다. (Lines 91-93)

```java
// 경계 조건 테스트 누락 예시
public class RestrictedSalesTest {
    @Test
    void saleRestrictedTo17yearOld() {
        // 17세는 판매 제한 확인
        // ... test code omitted
    }

    @Test
    void salePermittedTo19yearOld() {
        // 19세는 판매 허용 확인
        // ... test code omitted
    }

    // 문제: 18세 경계 조건 테스트가 누락됨!
    // 18세가 구매 가능한지 불가능한지 알 수 없음
}
```

```python
# Python 버전 - 경계 조건 테스트 누락
class RestrictedSalesTest:
    def test_sale_restricted_to_17_year_old(self):
        # 17세는 판매 제한
        age = 17
        result = can_purchase_restricted_item(age)
        assert result == False

    def test_sale_permitted_to_19_year_old(self):
        # 19세는 판매 허용
        age = 19
        result = can_purchase_restricted_item(age)
        assert result == True

    # 누락: 18세 경계 테스트
    # 이것이 수동 탐색적 테스트가 발견해야 할 부분
```

**자동화 테스트가 할 수 없는 두 가지** (Lines 115-117):
1. 이해관계자에게 소프트웨어가 무엇을 해야 하는지 질문
2. 누락된 테스트 발견

**수동 탐색적 테스트의 특징** (Lines 118-128):
- 인간의 창의성을 최대한 활용
- 본능과 지능으로 누락된 테스트 파악
- 과학적 실험으로 예측 검증
- 발견 사항을 피드백하고 결함 수정
- 새로운 자동화 테스트 작성으로 미래 회귀 테스트 제공

**자동화 vs 수동 탐색적 테스트 비교** (Lines 134-148):

| 특성 | 자동화 테스트 | 수동 탐색적 테스트 |
|------|---------------|-------------------|
| 반복성 | 반복 가능 (Repeatable) | 창의적 (Creative) |
| 목적 | 알려진 결과 테스트 | 미지의 결과 발견 |
| 수행 주체 | 기계 가능 | 인간 창의성 필요 |
| 테스트 방식 | 행동 검증 | 행동 조사 |
| 계획성 | 계획됨 | 기회주의적 |
| 통제 주체 | 코드가 테스트 통제 | 인간 마음이 테스트 통제 |

```python
# 탐색적 테스트 발견 후 TDD 프로세스
class ExploratoryTestingWorkflow:
    def discover_unexpected_behavior(self):
        # 1. 수동 탐색으로 예상치 못한 동작 발견
        # 예: 18세 경계 조건에서 예상 밖 결과
        pass

    def write_tdd_test(self):
        # 2. TDD로 올바른 동작 테스트 작성
        def test_sale_permitted_to_18_year_old(self):
            age = 18
            result = can_purchase_restricted_item(age)
            assert result == True  # 정책 확인 후 작성

    def confirm_defect(self):
        # 3. 결함 존재 확인
        pass

    def develop_fix(self):
        # 4. 수정 개발
        pass

    def ensure_regression_protection(self):
        # 5. 회귀 테스트 확보
        # 이제 18세 테스트가 영구적으로 보호됨
        pass
```

수동 탐색적 테스트는 놓친 결함에 대한 가장 빠른 피드백 루프이며, 자동화 테스트와 TDD는 수동 노력을 덜 중요하게 만드는 것이 아니라 그 가치를 증폭시킨다. (Lines 158-161)

---

### 3. 코드 품질 검증 방법

**이전 주제와의 관계**: 탐색적 테스트 전략 → 테스트뿐 아니라 코드 품질 검증도 인간 개입 필요

**핵심 내용(압축 내용, 핵심 내용)과의 관계**: 코드 리뷰와 앙상블 프로그래밍

TDD는 주로 코드 설계에 관여하며, 단위 테스트를 작성할 때 코드가 소비자에 의해 어떻게 사용될지를 정의한다. 하지만 구현 자체는 테스트의 관심사가 아니지만 소프트웨어 엔지니어로서는 관심사이다. 구현이 잘 수행되고 다음 독자가 이해하기 쉬워야 한다. (Lines 167-171)

**정적 코드 분석 도구** (Lines 172-187):
- 대표적 도구: Sonarqube (https://www.sonarqube.org/)
- 코드를 실행하지 않고 소스 코드의 자동화된 리뷰 수행
- 검출 항목:
  - 변수 명명 규칙 미준수
  - 초기화되지 않은 변수로 인한 NullPointerException 가능성
  - 보안 취약점
  - 프로그래밍 구조의 부적절하거나 위험한 사용
  - 커뮤니티 표준 및 관행 위반

**자동화 분석 vs 인간 리뷰 비교** (Lines 194-202):

| 특성 | 자동화 분석 | 인간 리뷰 |
|------|-------------|-----------|
| 규칙 적용 | 고정된 규칙 (예: 변수명 길이) | 컨텍스트 기반 규칙 완화 |
| 평가 기준 | 고정된 평가 기준 세트 적용 | 경험적 학습 적용 |
| 결과 제공 | 통과/실패 보고 | 대안적 개선 제안 |

```java
// 자동화 분석의 한계 예시
int x;  // 자동화 도구: 너무 짧은 변수명 경고
WordRepository repo;  // 자동화 도구: 적절한 길이 통과

// 하지만 인간 리뷰는 컨텍스트 이해:
// - int는 원시 타입이므로 더 서술적 이름 필요
// - WordRepository는 타입 자체가 의미를 담고 있어 짧은 이름도 OK
```

**코드 리뷰 방법** (Lines 206-226):

1. **Pull Request 코드 리뷰**:
   - 개발자가 메인 코드베이스에 통합 요청 시 수행
   - 다른 개발자가 작업을 검토하고 개선 제안
   - 시각적으로 결함 발견 가능
   - 합의된 변경 후 승인 및 병합

2. **페어 프로그래밍**:
   - 두 개발자가 동일 작업을 동시에 수행
   - 코드 작성 최선 방법에 대한 지속적 토론
   - 연속적 리뷰 프로세스
   - 문제 발견이나 개선 제안 즉시 논의 및 결정
   - 코드가 개발되면서 지속적으로 수정 및 개선

3. **앙상블(Mob) 프로그래밍**:
   - 전체 팀이 하나의 작업에 참여
   - 협업의 궁극적 형태
   - 작성되는 모든 코드에 전체 팀의 전문성과 의견 집중

```python
# 코드 리뷰 프로세스 비교
class CodeReviewProcess:
    def pull_request_review(self):
        # 1. Pull Request 리뷰: 코드 작성 후 리뷰
        write_code()
        submit_pull_request()
        wait_for_review()  # 시간차 존재
        receive_feedback()
        make_changes()  # 대대적 변경은 어려울 수 있음
        merge_code()

    def pair_programming(self):
        # 2. 페어 프로그래밍: 코드 작성 중 리뷰
        while coding:
            write_code_together()
            discuss_immediately()  # 즉시 논의
            refine_continuously()  # 지속적 개선
            # 문제 발견 즉시 수정

    def ensemble_programming(self):
        # 3. 앙상블 프로그래밍: 전체 팀 참여
        while coding:
            whole_team_writes_together()
            apply_collective_expertise()
            make_instant_decisions()
            # 모든 코드에 팀 전체의 지식 적용
```

**페어/앙상블 프로그래밍의 장점** (Lines 227-233):
- 코드 리뷰는 코드 작성 후 수행되어 의미 있는 변경이 너무 늦을 수 있음
- 페어링과 모빙은 코드 작성 중 리뷰하고 개선하여 이를 방지
- 변경 사항이 식별되는 순간 즉시 수행
- 코드 후 리뷰 워크플로우 대비 더 빠른 시간에 더 높은 품질 출력 가능

---

### 4. 사용자 인터페이스 검증

**이전 주제와의 관계**: 코드 품질 검증 방법 → 코드뿐 아니라 사용자 인터페이스 품질도 인간 평가 필요

**핵심 내용(압축 내용, 핵심 내용)과의 관계**: UI/UX 테스트 (사용자 인터페이스 검증 파트)

사용자 인터페이스는 가장 중요한 사람들인 사용자에게 유일하게 중요한 소프트웨어 시스템 부분이다. CLI, 모바일 웹 애플리케이션, 데스크톱 GUI 모두 사용자 인터페이스가 작업을 도와주거나 방해할 수 있다. (Lines 240-243)

**성공적인 사용자 인터페이스의 두 가지 조건** (Lines 244-246):
1. 사용자가 필요하고 원하는 모든 기능 제공
2. 사용자가 효과적이고 효율적인 방식으로 목표 달성 가능

첫 번째 조건(기능 제공)은 프로그래밍적이며, TDD로 서버 측 코드 설계를 주도하는 것처럼 프론트엔드 코드에도 사용 가능하다. (Lines 247-250)
- Java 애플리케이션이 HTML 생성(서버 사이드 렌더링): TDD 사용이 간단
- 브라우저에서 실행되는 JavaScript/TypeScript 프레임워크: Jest 같은 테스트 프레임워크로 TDD 가능

TDD로 모든 적절한 그래픽 요소가 UI에 존재하는지 검증할 수 있지만, 사용자 요구를 충족하는지는 알 수 없다. (Lines 256-258)

```java
// 가상의 UI 테스트 - 기능적 요소만 검증
@Test
public void productPurchaseUIHasRequiredElements() {
    // UI에 필요한 요소들이 존재하는지 테스트
    assertThat(ui.hasProductNameField()).isTrue();
    assertThat(ui.hasQuantityField()).isTrue();
    assertThat(ui.hasAddToCartButton()).isTrue();

    // 하지만 이것들이 사용자에게 좋은 경험을 주는지는 모름!
}
```

**UI 평가에 필요한 질문** (Lines 262-267):
- 보기 좋고 느낌이 좋은가?
- 기업 브랜딩 및 하우스 스타일 가이드에 부합하는가?
- T-셔츠 구매 작업에 사용하기 쉬운가?
- 사용자에게 논리적 흐름을 제시하여 작업을 안내하는가?

```python
# Python - UI 품질 평가 체크리스트
class UIQualityAssessment:
    def __init__(self, ui_interface):
        self.ui = ui_interface

    def functional_test(self):
        # TDD로 검증 가능
        assert self.ui.has_product_name_field()
        assert self.ui.has_quantity_field()
        assert self.ui.has_add_to_cart_button()
        return True

    def quality_assessment(self):
        # 인간만이 평가 가능한 항목들
        questions = {
            "look_and_feel": "보기 좋고 느낌이 좋은가?",
            "brand_alignment": "브랜딩에 부합하는가?",
            "ease_of_use": "사용하기 쉬운가?",
            "logical_flow": "논리적 흐름을 제시하는가?"
        }
        # 이러한 질문들은 자동화된 테스트로 답할 수 없음
        # 인간 평가자의 판단 필요
        return "REQUIRES_HUMAN_EVALUATION"
```

**나쁜 UI 예시의 문제점** (Lines 267-271, Figure 11.2):
- 스타일, 느낌, 브랜드 정체성 없음
- 제품명을 텍스트 필드에 입력해야 함
- 제품 이미지, 설명, 가격 없음
- 전자상거래 제품 판매 페이지로서 최악의 UI
- 하지만 모든 자동화된 기능 테스트는 통과함

효과적인 사용자 인터페이스 설계는 매우 인간적인 기술로, 작업이 주어졌을 때 인간이 어떻게 행동하는지에 대한 약간의 심리학, 예술적 안목, 창의성이 혼합된 것이다. (Lines 272-274)

---

### 5. 사용자 경험 평가

**이전 주제와의 관계**: 사용자 인터페이스 검증 → UI 개별 요소를 넘어 전체 사용자 경험 평가로 확장

**핵심 내용(압축 내용, 핵심 내용)과의 관계**: UI/UX 테스트 (사용자 경험 평가 파트)

사용자 경험은 개별 요소나 UI의 뷰를 넘어선다. 사용자가 가지는 전체 경험을 end-to-end로 의미한다. (Lines 281-286)
- Wordz T-셔츠를 전자상거래 스토어에서 주문할 때 전체 프로세스가 쉽기를 원함
- 모든 화면의 워크플로우가 명확하고, 정돈되고, 틀리기보다 맞히기 쉽기를 원함
- 서비스 디자인은 T-셔츠를 원하는 것부터 입는 것까지의 경험 최적화

훌륭한 사용자 경험 보장은 사용자 경험 디자이너의 역할로, 공감, 심리학, 실험을 결합하는 인간 활동이다. (Lines 287-288)

**자동화 가능 영역** (Lines 288-292):
- **Invision** (https://www.invisionapp.com/): 상호작용 가능한 화면 모형 제작
- **Google Forms**: 웹을 통해 피드백 수집, 코드 설정 불필요

```python
# 사용자 경험 피드백 수집 구조
class UserExperienceFeedback:
    def __init__(self):
        self.feedback_form = {
            "experiences": [],
            "ratings": {},
            "comments": {}
        }

    def create_mockup(self):
        # Invision 같은 도구로 모형 제작
        mockup = create_interactive_mockup()
        return mockup

    def conduct_experiment(self, users, task):
        # 잠재적 사용자에게 작업 제공
        for user in users:
            user.attempt_task(task)
            feedback = user.provide_feedback()
            self.collect_feedback(feedback)

    def collect_feedback(self, feedback):
        # 피드백 수집 (수동 양식)
        self.feedback_form["experiences"].append(feedback.experience)
        self.feedback_form["ratings"][feedback.category] = feedback.rating
        self.feedback_form["comments"][feedback.category] = feedback.comment

    def analyze_results(self):
        # 결과 평가는 인간 활동
        # 도구는 모형 생성과 결과 수집까지만
        return "HUMAN_ANALYSIS_REQUIRED"
```

**사용자 경험 피드백 양식 예시** (Lines 296-317, Table 11.3):

| 경험 항목 | 평가 (1-5) | 코멘트 |
|----------|------------|--------|
| 작업 완료 용이성 | 4 | 연구자의 프롬프트 후 작업을 완료했습니다 |
| 지시 없이 작업 완료 자신감 | 2 | T-셔츠 사이즈 텍스트 입력 필드가 혼란스러웠습니다. 사용 가능한 옵션의 드롭다운으로 할 수 있나요? |
| 인터페이스의 작업 안내 | 3 | 결국엔 괜찮았지만 - 텍스트 필드가 불편해서 점수를 낮췄습니다 |

**UX 디자인 프로세스** (Lines 318-321):
1. 비전의 모형 생성
2. 실험 결과 수집 (도구 활용)
3. 실제 사용자와 세션 실행
4. 경험에 대한 의견 수집
5. 개선된 디자인으로 결과 피드백 (인간 평가)

---

### 6. 보안 및 운영 관리

**이전 주제와의 관계**: 사용자 경험 평가 → 사용자 경험 외에 보안과 운영도 중요한 인간 중심 활동

**핵심 내용(압축 내용, 핵심 내용)과의 관계**: 보안 테스트와 운영 모니터링

잘 설계되고 결함이 매우 적은 애플리케이션을 만들고, 사용자 경험 피드백도 긍정적이지만, 애플리케이션을 계속 실행할 수 없다면 모든 잠재력은 순식간에 사라진다. 해커가 사이트를 공격하고 사용자에게 해를 끼치면 상황은 더욱 악화된다. (Lines 330-333)

실행되지 않는 애플리케이션은 존재하지 않는다. 운영(DevOps) 분야는 애플리케이션을 건강하게 유지하고 건강 상태가 나빠지면 경고하는 것을 목표로 한다. (Lines 334-335)

**보안 테스트(침투 테스트)** (Lines 336-343):
- 수동 탐색적 테스트의 특수한 경우
- 새로운 익스플로잇과 알려지지 않은 취약점 찾기가 목적
- 자동화는 이미 알려진 것을 반복하므로 부적합
- 미지의 것을 발견하려면 인간의 독창성 필요
- 소프트웨어를 가져와 보안을 우회하려는 시도
- 보안 침해는 회사에 비용이 많이 들고, 창피하거나, 사업을 끝낼 수 있음

```java
// 보안 리스크 카테고리 (의사 코드)
public class SecurityRisks {
    // 보안 리스크의 간단한 분류

    void thingsWeShouldNotSee() {
        // 우리가 봐서는 안 되는 것들
        // 예: 다른 사용자의 개인정보, 관리자 페이지
    }

    void thingsWeShouldNotChange() {
        // 우리가 변경해서는 안 되는 것들
        // 예: 다른 사용자의 데이터, 시스템 설정
    }

    void thingsWeShouldNotUseAsOften() {
        // 우리가 자주 사용해서는 안 되는 것들
        // 예: API 속도 제한, DDoS 방지
    }

    void thingsWeShouldNotLieAbout() {
        // 우리가 거짓말할 수 없어야 하는 것들
        // 예: 사용자 인증, 거래 무결성
    }
}
```

```python
# Python - 보안 테스트 접근 방식
class SecurityTesting:
    def __init__(self):
        self.risks = {
            "unauthorized_access": "봐서는 안 되는 것",
            "unauthorized_modification": "변경해서는 안 되는 것",
            "rate_limit_abuse": "자주 사용해서는 안 되는 것",
            "authentication_bypass": "거짓말할 수 없어야 하는 것"
        }

    def manual_penetration_testing(self):
        # 이 테스트는 적응적, 창의적, 교활하고, 지속적으로 업데이트되어야 함
        # 자동화 접근은 이런 것들을 제공하지 못함
        # 따라서 보안 테스트는 개발 프로세스의 수동 단계로 자리 잡아야 함

        for risk_type, description in self.risks.items():
            test_result = self.attempt_exploit(risk_type)
            if test_result.vulnerable:
                self.report_vulnerability(risk_type, test_result)

    def attempt_exploit(self, risk_type):
        # 인간의 창의성으로 보안 우회 시도
        # 자동화된 도구로는 발견할 수 없는 취약점 찾기
        pass
```

**보안 테스트 리소스** (Lines 353-362):
- **OWASP Top 10**: 최신 웹 애플리케이션 보안 위험 (https://owasp.org/www-project-top-ten/)
- **STRIDE 위협 모델**:
  - Spoofing (스푸핑)
  - Tampering (변조)
  - Repudiation (부인)
  - Information Disclosure (정보 노출)
  - Denial of Service (서비스 거부)
  - Elevation of Privilege (권한 상승)
  - 참조: https://www.eccouncil.org/threat-modeling/
- **Fuzzing**: 자동화된 결함 발견 방법이지만 실패한 테스트 결과는 인간이 해석 필요
  - OWASP 도구: https://owasp.org/www-community/Fuzzing

수동 탐색적 테스트처럼, 이런 임시 실험은 미래의 테스트 자동화로 이어질 수 있다. 하지만 진정한 가치는 미지의 것을 조사하는 데 적용된 창의성에 있다. (Lines 361-362)

---

### 7. 자동화와 수동화 조화

**이전 주제와의 관계**: 보안 및 운영 관리 → 수동 개입의 중요성 확인 후 자동화 워크플로우와 통합 방법 모색

**핵심 내용(압축 내용, 핵심 내용)과의 관계**: CI/CD 워크플로우와 수동 프로세스 통합

수동 프로세스가 전체 워크플로우에서 중요할 뿐만 아니라 일부는 대체 불가능함을 확인했다. 하지만 수동 단계가 고도로 자동화된 워크플로우에 어떻게 맞을까? (Lines 367-373)

CI/CD 파이프라인에 수동 프로세스를 통합하는 것은 어려울 수 있다. 두 접근 방식은 선형적이고 반복 가능한 활동 시퀀스 측면에서 자연스러운 파트너가 아니다. 궁극적 목표에 따라 접근 방식이 달라진다: 완전 자동화된 지속적 배포 시스템을 원하는가, 아니면 일부 수동 중단을 받아들일 수 있는가? (Lines 374-377)

**1. Blocking Workflow (차단 워크플로우)** (Lines 378-389):

```python
# Blocking Workflow 구조
class BlockingWorkflow:
    def __init__(self):
        self.stages = []

    def add_automated_stage(self, stage):
        self.stages.append({"type": "automated", "stage": stage})

    def add_manual_stage(self, stage):
        self.stages.append({"type": "manual", "stage": stage})

    def execute(self):
        for stage in self.stages:
            if stage["type"] == "automated":
                # 자동화 단계는 빠르게 실행
                stage["stage"].run()
            elif stage["type"] == "manual":
                # 수동 단계는 완료될 때까지 모든 것을 차단
                print(f"수동 프로세스 대기: {stage['stage'].name}")
                stage["stage"].wait_for_completion()
                print(f"수동 프로세스 완료: {stage['stage'].name}")

            # 각 단계는 다음 단계를 차단
            # 가치 흐름이 각 단계에 의해 차단됨

# 예시 실행
workflow = BlockingWorkflow()
workflow.add_automated_stage(BuildStage())
workflow.add_automated_stage(UnitTestStage())
workflow.add_manual_stage(CodeReviewStage())      # 차단점
workflow.add_manual_stage(SecurityTestStage())    # 차단점
workflow.add_automated_stage(DeploymentStage())
workflow.execute()
```

**Blocking Workflow 특징**:
- **장점**:
  - 이해하고 운영하기 간단
  - 각 반복마다 모든 자동화 및 수동 프로세스 실행
  - 그 시점에서 만들 수 있는 최고 품질의 릴리스 (Lines 386-388)
- **단점**:
  - 각 반복이 모든 수동 프로세스 완료를 기다려야 함
  - 배포 주기가 길어짐 (Line 389)

**2. Dual-Track Workflow (이중 트랙 워크플로우)** (Lines 390-404):

```python
# Dual-Track Workflow 구조
class DualTrackWorkflow:
    def __init__(self):
        self.automated_track = []
        self.manual_track = []
        self.feature_flags = {}

    def add_to_automated_track(self, stage):
        self.automated_track.append(stage)

    def add_to_manual_track(self, stage):
        self.manual_track.append(stage)

    def set_feature_flag(self, feature, enabled):
        # Feature Flag로 개발 중 기능 제어
        self.feature_flags[feature] = enabled

    def execute_automated_track(self):
        # 자동화 트랙은 독립적으로 빠르게 실행
        for stage in self.automated_track:
            stage.run()

        # 배포는 feature flag로 제어됨
        # 진행 중인 기능은 비활성화 상태로 배포
        for feature, enabled in self.feature_flags.items():
            if not enabled:
                print(f"{feature}는 배포되었지만 비활성화 상태")

    def execute_manual_track(self):
        # 수동 트랙은 병렬로 독립적으로 실행
        for stage in self.manual_track:
            # 수동 테스트 중에는 feature flag 활성화
            self.enable_features_for_testing()
            stage.execute_manually()

    def enable_features_for_testing(self):
        # 수동 테스트 시 진행 중 기능 활성화
        for feature in self.feature_flags:
            self.feature_flags[feature] = True

    def run_parallel(self):
        # 두 트랙 병렬 실행
        import threading

        auto_thread = threading.Thread(target=self.execute_automated_track)
        manual_thread = threading.Thread(target=self.execute_manual_track)

        auto_thread.start()
        manual_thread.start()

        # 배포는 중단 없이 계속
        # 수동 테스트는 독립적으로 진행

# 예시 실행
dual_workflow = DualTrackWorkflow()

# 자동화 트랙 설정
dual_workflow.add_to_automated_track(BuildStage())
dual_workflow.add_to_automated_track(UnitTestStage())
dual_workflow.add_to_automated_track(DeploymentStage())

# 수동 트랙 설정
dual_workflow.add_to_manual_track(ExploratoryTestStage())
dual_workflow.add_to_manual_track(SecurityTestStage())

# Feature Flag 설정
dual_workflow.set_feature_flag("new_feature_v2", False)  # 배포되지만 비활성화

# 병렬 실행
dual_workflow.run_parallel()
```

**Dual-Track Workflow 특징** (Lines 395-404):
- **단일 메인 트렁크 사용**: 모든 개발자가 메인 트렁크에 커밋, 다른 브랜치 없음
- **Feature Flag로 격리**: 개발 중인 기능을 Boolean 값으로 런타임에 제어
  - true/false로 설정 가능
  - 코드가 플래그를 검사하여 기능 실행 여부 결정
- **수동 테스트 시**: 진행 중 기능을 관련 feature flag를 통해 활성화
- **일반 사용자 대상**: 진행 중 기능은 비활성화
- **배포 중단 없음**: 수동 테스트가 배포를 일시 중지하지 않음

**워크플로우 선택 트레이드오프** (Lines 401-407):
- **Blocking Workflow**: 재작업이 적은 대신 배포 주기가 길어짐
- **Dual-Track Workflow**: 더 빈번한 기능 배포 가능, 수동 프로세스가 결함을 발견하기 전에 프로덕션에 결함이 있을 위험 존재

적절한 프로세스 선택은 기능 릴리스 속도와 결함 허용 간의 트레이드오프를 포함한다. 어떤 것을 선택하든 목표는 전체 팀의 전문성을 낮은 결함률의 소프트웨어 생성에 집중하는 것이다. (Lines 405-407)

---

## 요약 (Lines 413-423)

이 장에서는 개발 중 다양한 수동 프로세스의 중요성을 논의했다.

**주요 내용**:
1. **TDD의 한계**: TDD가 모든 종류의 소프트웨어 결함을 방지할 수 없음
2. **수동 탐색적 테스트**: TDD 중 놓친 결함을 발견하는 인간 창의성 적용의 이점
3. **코드 리뷰와 분석**: 품질 향상 효과
4. **UI/UX 설계**: 훌륭한 사용자 인터페이스와 만족스러운 사용자 경험 생성 및 검증의 수동적 특성
5. **보안 테스트와 운영 모니터링**: 라이브 시스템을 잘 작동하게 유지하는 중요성
6. **CI/CD 통합**: 수동 단계를 자동화 워크플로우에 통합하는 접근 방식과 필요한 트레이드오프

다음 장에서는 테스트를 개발하는 시기와 위치에 관련된 작업 방법을 검토한 후, 이 책의 Part 3에서 Wordz 애플리케이션 구축을 완료할 것이다. (Lines 422-423)

---

## Q&A (Lines 428-445)

**Q1. TDD와 CI/CD 파이프라인이 수동 테스트의 필요성을 제거했나요?**

아니요. 가치가 있는 위치를 변경했습니다. 일부 수동 프로세스는 무관해졌지만, 다른 것들은 중요성이 증가했습니다. 전통적으로 기능 테스트와 회귀 테스트를 위한 테스트 문서 따르기 같은 수동 단계는 더 이상 필요하지 않습니다. 기능 및 회귀 테스트 실행은 워드 프로세서에서 테스트 계획 작성에서 IDE에서 테스트 코드 작성으로 변경되었습니다. 하지만 많은 인간 중심 작업의 경우, 루프에 인간의 마음을 갖는 것이 성공에 여전히 중요합니다. (Lines 431-437)

**Q2. 인공지능(AI)이 남은 작업들을 자동화할까요?**

알 수 없습니다. 현재(2020년대 초반) AI의 발전은 시각적 식별과 정적 코드 분석을 개선할 수 있습니다. AI 이미지 분석이 언젠가 사용성의 좋고/나쁨 분석을 제공할 수 있다는 것은 상상할 수 있지만, 이는 오늘날 AI의 미술 작품 생성 능력에 기반한 순수한 추측입니다. 그런 것은 불가능할 수도 있습니다. 현재의 실용적 조언 측면에서, 이 장에서 권장하는 수동 프로세스는 당분간 수동으로 남을 것이라고 가정하십시오. (Lines 439-445)

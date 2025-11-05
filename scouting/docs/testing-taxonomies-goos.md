# Software Testing Taxonomies - GOOS Mapping

**작성일**: 2025-11-04
**작성자**: Claude & 태수

이 문서는 소프트웨어 테스팅 범주 체계와 "Growing Object-Oriented Software, Guided by Test" 책의 관련 챕터를 매핑합니다.

---

## 범주 체계 및 GOOS 챕터 매핑

- [소프트웨어 테스팅](#소프트웨어-테스팅)
  - [테스트 구조화 패턴](#테스트-구조화-패턴)
    - [AAA 패턴과 Given-When-Then 패턴](./testing-taxonomies-qa.md#aaa-pattern-given-when-then) **[Ch 21.3, p.226]**
  - [테스트 명명 규칙](./testing-taxonomies-qa.md#test-naming-conventions) **[Ch 21.2, p.223]**
  - [테스트 프로젝트 구조](#테스트-프로젝트-구조)
    - [디렉터리 조직화](./testing-taxonomies-qa.md#directory-organization)
    - [테스트 설정 파일](./testing-taxonomies-qa.md#test-config-files)
    - [테스트 데이터 관리](#테스트-데이터-관리) **[Ch 22, p.232]**
      - [Factory 패턴](./testing-taxonomies-qa.md#factory-pattern) **[Ch 22.5, p.236]**
      - [Builder 패턴](./testing-taxonomies-qa.md#builder-pattern) **[Ch 22.2, p.233]**
      - [Object Mother 패턴](./testing-taxonomies-qa.md#object-mother-pattern) **[Ch 22.3, p.234]**
      - [Fixture 패턴](./testing-taxonomies-qa.md#fixture-pattern)
    - [모킹 전략](./testing-taxonomies-qa.md#mocking-strategy) **[Ch 2.7, p.xviii | Ch 8, p.44]**
  - [테스트 커버리지](#테스트-커버리지)
    - [커버리지 측정 지표](./testing-taxonomies-qa.md#coverage-metrics)
    - [커버리지 도구](./testing-taxonomies-qa.md#coverage-tools)
    - [커버리지 관리 전략](./testing-taxonomies-qa.md#coverage-management)

---

## References

**Growing Object-Oriented Software, Guided by Test**
- 저자: Steve Freeman, Nat Pryce
- 출판: Addison-Wesley, 2009
- [목차](../../references/growing-object-oriented-software/toc.md)

### 주요 매핑 챕터

**Part IV: Sustainable Test-Driven Development**
- **Chapter 21: Test Readability** - 테스트 구조화, 명명 규칙
  - 21.2: Test Names Describe Features (p.223)
  - 21.3: Canonical Test Structure (p.226)

- **Chapter 22: Constructing Complex Test Data** - 테스트 데이터 패턴
  - 22.2: Test Data Builders (p.233)
  - 22.3: Creating Similar Objects (p.234)
  - 22.5: Emphasizing the Domain Model with Factory Methods (p.236)

**Part I: Introduction & Part II: The Process**
- **Chapter 2: Test-Driven Development with Objects**
  - 2.7: Support for TDD with Mock Objects (p.xviii)

- **Chapter 8: Building on Third-Party Code** (p.44)
  - 모킹 전략 및 테스트 더블 사용

### 범주별 상세 매핑

#### 직접 다루는 주제
- ✅ **테스트 구조화 패턴** (AAA/Given-When-Then): Ch 21.3
- ✅ **테스트 명명 규칙**: Ch 21.2
- ✅ **Factory 패턴**: Ch 22.5
- ✅ **Builder 패턴**: Ch 22.2
- ✅ **Object Mother 패턴**: Ch 22.3 (Creating Similar Objects)
- ✅ **모킹 전략**: Ch 2.7, Ch 8

#### 책에서 직접 다루지 않는 주제
- ❌ **디렉터리 조직화** - 프로젝트별 실무 관례
- ❌ **테스트 설정 파일** - 프레임워크 특화 내용
- ❌ **Fixture 패턴** - pytest/unittest 프레임워크 특화
- ❌ **테스트 커버리지** - 측정 도구 및 관리 전략

---
created_at: 2025-10-10 00:00:00
links:
   - ./index.md
---

# 5. 참조 및 근거

## 5.1 주요 참조 문서

| 챕터 | 주요 내용 | 적용 위치 |
|------|----------|-----------|
| Chapter 3 | 패키지 구조 설계 | 전체 폴더 구조 |
| Chapter 4 | Use Case 구현 | 애플리케이션 계층 |
| Chapter 5 | Web Adapter 구현 | 웹 어댑터 |
| Chapter 6 | Persistence Adapter 구현 | 영속성 어댑터 |
| Chapter 7 | 테스트 전략 | 전체 테스트 |
| Chapter 8 | 외부 라이브러리 통합 | 어댑터 계층 |
| Chapter 9 | 의존성 주입 | 설정 계층 |
| Chapter 10 | 아키텍처 경계 강제 | 패키지 가시성 |
| Chapter 20 | 테스트가 주는 신호 | TDD 프로세스 |
| Chapter 21 | 테스트 가독성 | 테스트 작성 |
| Chapter 22 | 복잡한 테스트 데이터 | Test Data Builder |
| Chapter 23 | 테스트 진단성 | 실패 메시지 개선 |
| Chapter 24 | 테스트 유연성 | Brittle Test 방지 |

## 5.2 핵심 설계 결정 및 근거

1. **포트-어댑터 패턴**
   - **근거**: Chapter 3, Lines 180-186
   - **적용**: application/port, adapter 분리

2. **도메인 중심 설계**
   - **근거**: Chapter 4, Lines 12-129
   - **적용**: domain 패키지

3. **Use Case별 Input/Output 분리**
   - **근거**: Chapter 4, Lines 403-427, 548-575
   - **적용**: 각 Use Case마다 전용 Command/Result

4. **컨트롤러 슬라이싱**
   - **근거**: Chapter 5, Lines 268-343
   - **적용**: 유스케이스별 컨트롤러

5. **도메인-영속성 모델 분리**
   - **근거**: Chapter 6, Lines 584-591
   - **적용**: domain/order.py ≠ model/order_model.py

6. **Java Config 방식 의존성 주입**
   - **근거**: Chapter 9, Lines 231-317
   - **적용**: config/dependencies.py

7. **Walking Skeleton 우선**
   - **근거**: Chapter 4, 5
   - **적용**: E2E 테스트부터 시작

8. **Test Data Builder 패턴**
   - **근거**: Chapter 22
   - **적용**: tests/builders.py

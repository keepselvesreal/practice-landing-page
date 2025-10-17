차원 1: 패턴의 본질 (Pattern Essence)
  ├─ 헥사고날 아키텍처의 목적
  │  ├─ 비즈니스 로직 보호
  │  ├─ 기술 독립성
  │  └─ 테스트 용이성
  ├─ 핵심 구성 요소
  │  ├─ Domain (비즈니스 로직의 핵심)
  │  ├─ Ports (계약/인터페이스)
  │  └─ Adapters (외부 세계와의 연결)
  └─ 근본 원칙
     ├─ 의존성 역전 (Dependency Inversion)
     ├─ 관심사의 분리 (Separation of Concerns)
     └─ 단일 책임 (Single Responsibility)

차원 2: 패턴의 작동 방식 (Pattern Mechanics)
├─ Port의 종류와 역할
│  ├─ Primary Port (애플리케이션이 제공하는 기능)
│  └─ Secondary Port (애플리케이션이 필요로 하는 기능)
├─ Adapter의 종류와 역할
│  ├─ Primary Adapter (Driving/Inbound - 애플리케이션 호출)
│  └─ Secondary Adapter (Driven/Outbound - 애플리케이션에 의해 호출됨)
├─ 의존성 흐름
│  ├─ 외부 → 내부로만 흐름
│  ├─ Domain은 외부 의존성 없음
│  └─ Port를 통한 의존성 역전
└─ 계층 간 통신
    ├─ Adapter → Port → Domain
    ├─ Domain → Port ← Adapter
    └─ 런타임 vs 컴파일타임 의존성

차원 3: 패턴 적용 실습 (Pattern Practice)
├─ 도메인 식별 및 모델링
│  ├─ Use Case 정의
│  ├─ Entity 설계
│  └─ 비즈니스 규칙 캡슐화
├─ Port 설계
│  ├─ Primary Port 인터페이스 정의
│  ├─ Secondary Port 인터페이스 정의
│  └─ Port 네이밍 규칙
└─ Adapter 구현
    ├─ REST API Adapter (Primary)
    ├─ Database Adapter (Secondary)
    └─ External API Adapter (Secondary)
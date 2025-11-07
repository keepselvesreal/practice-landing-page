---
version: 1
created_date: 25-11-07 15:38
note:
---

## 메모

### 성능 요구사항
- **페이지 로딩 속도**: 3초 이내 (모바일 3G 환경)
- **Lighthouse 점수**: 90+ (Performance)
- **목표**: 필리핀 모바일 사용자 최적화

---

### 최적화 전략

#### 이미지 최적화
- **WebP 포맷 사용**: 기존 JPG 대비 30% 이상 용량 감소
- **이미지 압축**: TinyPNG, ImageOptim 등 사용
- **지연 로딩**: `loading="lazy"` 속성 활용
- **적절한 해상도**: 모바일/데스크톱 별도 제공

#### CSS/JS 최적화
- **번들 최소화**: Minify 적용
- **인라인 Critical CSS**: 초기 렌더링 속도 개선
- **불필요한 스크립트 제거**: Vanilla JS 활용으로 의존성 최소화

#### CDN 활용
- **Firebase Hosting CDN**: 전 세계 엣지 로케이션에서 제공
- **정적 파일 캐싱**: 이미지, CSS, JS 장기 캐시 설정

#### 백엔드 성능
- **PostgreSQL 인덱스**: 주문번호, PayPal ID, 어필리에이트 코드
- **연결 풀링**: psycopg2 연결 풀 활용 (최대 10 연결)
- **Cloud Run 오토스케일링**: 트래픽에 따라 자동 확장

---

### 성능 측정
```bash
# Lighthouse 측정
npx lighthouse https://your-project.web.app --view

# 핵심 지표
# - First Contentful Paint (FCP): < 1.8s
# - Largest Contentful Paint (LCP): < 2.5s
# - Time to Interactive (TTI): < 3.8s
```

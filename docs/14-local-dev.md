---
version: 1
created_date: 25-11-07 15:38
note:
---

## 메모

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
      POSTGRES_DB: scout
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

### 로컬 개발 시작
```bash
# 1. PostgreSQL 시작
docker-compose up -d

# 2. 의존성 설치
uv sync

# 3. 데이터베이스 초기화
uv run python scripts/init_db.py

# 4. Backend 개발 서버 실행
uv run uvicorn backend.main:app --reload --port 8000

# 5. Frontend 개발 서버 실행 (별도 터미널)
firebase emulators:start --only hosting

# 6. 테스트 실행
uv run pytest

# 7. 커버리지 확인
uv run pytest --cov=backend --cov-report=html
```

---

### Firebase 설정
```json
// firebase.json
{
  "hosting": {
    "public": "frontend",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "/api/**",
        "run": {
          "serviceId": "scout-api",
          "region": "asia-northeast3"
        }
      }
    ]
  }
}
```

```json
// .firebaserc
{
  "projects": {
    "default": "your-project-id"
  }
}
```

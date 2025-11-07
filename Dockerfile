# 멀티스테이지 빌드: 의존성 설치 단계
FROM python:3.11-slim AS builder

# uv 설치
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사
COPY pyproject.toml uv.lock ./

# 의존성 설치 (--system으로 시스템 파이썬에 설치)
RUN uv pip install --system --no-cache -r pyproject.toml

# 최종 이미지
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# builder 단계에서 설치한 패키지 복사
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 애플리케이션 코드 복사
COPY backend ./backend

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# 포트 노출
EXPOSE 8000

# uvicorn으로 FastAPI 앱 실행
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

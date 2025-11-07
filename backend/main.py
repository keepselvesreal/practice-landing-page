"""FastAPI 메인 애플리케이션"""
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.orders import router as orders_router

app = FastAPI(
    title="Scout Landing Page API",
    description="주문 관리 API",
    version="0.1.0",
)

# CORS 설정 (개발 환경용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 환경에서는 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """헬스체크 엔드포인트"""
    return {"status": "ok"}


# 라우터 등록
app.include_router(orders_router)

# 정적 파일 서빙 (frontend) - 가장 마지막에 마운트 (catch-all)
frontend_path = Path(__file__).parent.parent / "frontend"
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

"""FastAPI 메인 애플리케이션"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# 라우터 등록
app.include_router(orders_router)


@app.get("/health")
async def health_check():
    """헬스체크 엔드포인트"""
    return {"status": "ok"}

"""
FastAPI Application Entry Point
Chapter 9: Application Assembly
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .settings import get_settings
from .dependencies import (
    override_place_order_use_case,
    override_track_affiliate_use_case,
    override_affiliate_stats_query
)
from ..adapter.in_.web import order_controller


def create_app() -> FastAPI:
    """
    FastAPI 애플리케이션 생성 및 조립

    Chapter 9: Configuration Component가 모든 것을 조립
    """
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="0.1.0"
    )

    # CORS 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 의존성 주입 Override (비판적 검토: 명시적 연결)
    app.dependency_overrides[order_controller.get_place_order_use_case] = (
        override_place_order_use_case
    )

    # 라우터 등록
    app.include_router(order_controller.router)

    @app.get("/")
    def root():
        """헬스 체크"""
        return {
            "app": settings.app_name,
            "status": "running",
            "version": "0.1.0"
        }

    @app.get("/health")
    def health():
        """헬스 체크 엔드포인트"""
        return {"status": "healthy"}

    return app


# FastAPI 인스턴스 생성
app = create_app()

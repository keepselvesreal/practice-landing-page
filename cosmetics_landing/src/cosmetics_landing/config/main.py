"""
FastAPI Application Entry Point
Chapter 9: Application Assembly
"""
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from .settings import get_settings
from .dependencies import (
    override_place_order_use_case,
    override_track_affiliate_use_case,
    override_affiliate_stats_query,
    override_send_inquiry_use_case
)
from ..adapter.in_.web import order_controller, affiliate_controller, inquiry_controller


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
    app.dependency_overrides[affiliate_controller.get_affiliate_stats_query] = (
        override_affiliate_stats_query
    )
    app.dependency_overrides[affiliate_controller.get_track_affiliate_use_case] = (
        override_track_affiliate_use_case
    )
    app.dependency_overrides[inquiry_controller.get_send_inquiry_use_case_dependency] = (
        override_send_inquiry_use_case
    )

    # 라우터 등록
    app.include_router(order_controller.router)
    app.include_router(affiliate_controller.router)
    app.include_router(inquiry_controller.router)

    @app.get("/", response_class=HTMLResponse)
    def landing_page(ref: str = None):
        """
        랜딩 페이지 서빙

        Walking Skeleton: 사용자가 실제로 보는 화면
        Epic 2: 어필리에이트 링크 클릭 추적
        """
        # 어필리에이트 클릭 추적
        if ref:
            from ..adapter.in_.web.affiliate_controller import get_track_affiliate_use_case
            from ..application.port.in_.track_affiliate_command import TrackClickCommand
            try:
                use_case = override_track_affiliate_use_case()
                use_case.track_click(TrackClickCommand(affiliate_code=ref))
            except Exception:
                # 클릭 추적 실패해도 랜딩 페이지는 보여줌
                pass

        template_path = Path(__file__).parent.parent.parent.parent / "templates" / "landing.html"
        return HTMLResponse(content=template_path.read_text())

    @app.get("/health")
    def health():
        """헬스 체크 엔드포인트"""
        return {"status": "healthy"}

    return app


# FastAPI 인스턴스 생성
app = create_app()

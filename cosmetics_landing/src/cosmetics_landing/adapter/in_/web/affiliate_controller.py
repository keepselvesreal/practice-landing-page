"""
Affiliate Web Controller
어필리에이트 API 엔드포인트
"""
from fastapi import APIRouter, Depends, HTTPException, status
from decimal import Decimal
from pydantic import BaseModel

from ....application.port.in_.get_affiliate_stats_query import GetAffiliateStatsQuery
from ....application.port.in_.track_affiliate_command import TrackAffiliateClickUseCase, TrackClickCommand


router = APIRouter(prefix="/api/affiliates", tags=["affiliates"])


class AffiliateStatsResponse(BaseModel):
    """어필리에이트 통계 응답 DTO"""
    code: str
    total_clicks: int
    total_sales: int
    total_commission: float
    pending_commission: float


def get_affiliate_stats_query() -> GetAffiliateStatsQuery:
    """의존성 주입 - config/dependencies.py에서 override"""
    raise NotImplementedError("Query must be injected via dependencies")


def get_track_affiliate_use_case() -> TrackAffiliateClickUseCase:
    """의존성 주입 - config/dependencies.py에서 override"""
    raise NotImplementedError("Use case must be injected via dependencies")


@router.get("/{affiliate_code}/stats", response_model=AffiliateStatsResponse)
def get_affiliate_stats(
    affiliate_code: str,
    query: GetAffiliateStatsQuery = Depends(get_affiliate_stats_query)
) -> AffiliateStatsResponse:
    """
    어필리에이트 통계 조회

    Args:
        affiliate_code: 어필리에이트 코드

    Returns:
        통계 데이터
    """
    try:
        stats = query.get_stats(affiliate_code)
        return AffiliateStatsResponse(
            code=stats.code,
            total_clicks=stats.total_clicks,
            total_sales=stats.total_sales,
            total_commission=float(stats.total_commission),
            pending_commission=float(stats.pending_commission)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

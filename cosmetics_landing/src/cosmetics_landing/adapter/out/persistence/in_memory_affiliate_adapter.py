"""
In-Memory Affiliate Persistence Adapter
Walking Skeleton용 간단한 메모리 저장소
"""
from typing import Optional, Dict

from ....application.port.out.affiliate_repository import SaveAffiliatePort, LoadAffiliatePort
from ....domain.affiliate import Affiliate, AffiliateId


class InMemoryAffiliateAdapter(SaveAffiliatePort, LoadAffiliatePort):
    """In-Memory 어필리에이트 저장소 어댑터"""

    def __init__(self):
        self._affiliates: Dict[int, Affiliate] = {}
        self._affiliates_by_code: Dict[str, Affiliate] = {}
        self._next_id = 1

    def save(self, affiliate: Affiliate) -> AffiliateId:
        """어필리에이트 저장"""
        if affiliate.id is None:
            # 새 어필리에이트 생성
            affiliate_id = AffiliateId(value=self._next_id)
            self._next_id += 1

            affiliate_with_id = Affiliate(
                id=affiliate_id,
                code=affiliate.code,
                total_clicks=affiliate.total_clicks,
                total_sales=affiliate.total_sales,
                total_commission=affiliate.total_commission,
                pending_commission=affiliate.pending_commission,
                created_at=affiliate.created_at
            )
            self._affiliates[affiliate_id.value] = affiliate_with_id
            self._affiliates_by_code[affiliate.code] = affiliate_with_id
            return affiliate_id
        else:
            # 기존 어필리에이트 업데이트
            self._affiliates[affiliate.id.value] = affiliate
            self._affiliates_by_code[affiliate.code] = affiliate
            return affiliate.id

    def load_by_id(self, affiliate_id: AffiliateId) -> Optional[Affiliate]:
        """ID로 어필리에이트 조회"""
        return self._affiliates.get(affiliate_id.value)

    def load_by_code(self, code: str) -> Optional[Affiliate]:
        """코드로 어필리에이트 조회"""
        return self._affiliates_by_code.get(code)

"""
Track Affiliate Service - Command Use Case 구현
"""
from ..port.in_.track_affiliate_command import TrackAffiliateClickUseCase, TrackClickCommand
from ..port.out.affiliate_repository import LoadAffiliatePort, SaveAffiliatePort


class TrackAffiliateService(TrackAffiliateClickUseCase):
    """
    어필리에이트 클릭 추적 서비스 (Command)

    상태 변경만 담당, 조회는 별도 Query Service에서 처리
    """

    def __init__(
        self,
        load_affiliate_port: LoadAffiliatePort,
        save_affiliate_port: SaveAffiliatePort
    ):
        self.load_affiliate = load_affiliate_port
        self.save_affiliate = save_affiliate_port

    def track_click(self, command: TrackClickCommand) -> None:
        """클릭 추적"""
        affiliate = self.load_affiliate.load_by_code(command.affiliate_code)

        if not affiliate:
            raise ValueError(f"Affiliate not found: {command.affiliate_code}")

        updated_affiliate = affiliate.record_click()
        self.save_affiliate.save(updated_affiliate)

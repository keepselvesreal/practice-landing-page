"""
Track Affiliate Command Use Case - Incoming Port (Command)
CQS 원칙: 상태 변경 명령만 담당
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class TrackClickCommand:
    """어필리에이트 클릭 추적 명령"""
    affiliate_code: str

    def __post_init__(self):
        if not self.affiliate_code or not self.affiliate_code.strip():
            raise ValueError("affiliate_code is required")


class TrackAffiliateClickUseCase(ABC):
    """
    어필리에이트 클릭 추적 Use Case (Command)

    Chapter 4: CQS 원칙에 따라 상태 변경만 담당
    """

    @abstractmethod
    def track_click(self, command: TrackClickCommand) -> None:
        """
        어필리에이트 링크 클릭 기록

        Args:
            command: 클릭 추적 명령
        """
        pass

"""
Fake Address Validator
Walking Skeleton용 주소 검증 시뮬레이터
"""
from ....application.port.out.address_validator import ValidateAddressPort


class FakeAddressValidator(ValidateAddressPort):
    """
    Fake 주소 검증 어댑터

    Walking Skeleton: 실제 Google Places API 대신 간단한 규칙 사용
    추후 실제 Google Places 어댑터로 교체
    """

    def __init__(self, invalid_patterns: list[str] = None):
        """
        Args:
            invalid_patterns: 이 패턴이 포함되면 무효로 판단
        """
        self.invalid_patterns = invalid_patterns or ["invalid", "fake"]

    def is_valid(self, address: str) -> bool:
        """
        주소 유효성 검증 시뮬레이션

        간단한 규칙:
        - 5자 이상
        - invalid_patterns에 해당하는 단어가 없으면 유효
        """
        if not address or len(address.strip()) < 5:
            return False

        address_lower = address.lower()
        for pattern in self.invalid_patterns:
            if pattern in address_lower:
                return False

        return True

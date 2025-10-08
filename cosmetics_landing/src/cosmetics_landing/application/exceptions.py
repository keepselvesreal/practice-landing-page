"""
Application Layer Exceptions
"""


class ApplicationError(Exception):
    """애플리케이션 계층 기본 예외"""
    pass


class PaymentFailedError(ApplicationError):
    """결제 실패 예외"""

    def __init__(self, message: str):
        super().__init__(f"Payment failed: {message}")
        self.message = message


class InvalidAddressError(ApplicationError):
    """유효하지 않은 주소 예외"""

    def __init__(self, address: str):
        super().__init__(f"Invalid address: {address}")
        self.address = address

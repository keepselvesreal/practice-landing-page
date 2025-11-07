"""테스트 데이터 Factory 함수들"""
from typing import Dict, Any


def create_purchase_data(
    name: str = "Juan Dela Cruz",
    phone: str = "+63-917-123-4567",
    email: str = "juan@example.com",
    address: str = "123 Rizal Avenue, Makati City, Metro Manila",
    **kwargs: Any,
) -> Dict[str, str]:
    """구매 정보 테스트 데이터 생성 (필리핀 고객 기준)"""
    data = {
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
    }
    data.update(kwargs)
    return data

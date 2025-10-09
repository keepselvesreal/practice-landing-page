"""
Google Places (Geocoding) Adapter
실제 Google Geocoding API 연동

Learning Test 기반 구현:
- tests/learning/test_google_geocoding_contract.py에서 학습한 API 계약 준수
"""
import requests
from typing import Optional

from ....application.port.out.address_validator import ValidateAddressPort


class GooglePlacesAdapter(ValidateAddressPort):
    """
    Google Geocoding API 주소 검증 어댑터

    Learning Test 기반 계약:
    - Status "OK": 유효한 주소 (최소 1개 결과)
    - Status "ZERO_RESULTS": 주소 없음
    - Status "REQUEST_DENIED": API 키 문제
    - Status "INVALID_REQUEST": 파라미터 누락
    """

    def __init__(
        self,
        api_key: str,
        timeout: int = 10,
        require_rooftop: bool = False
    ):
        """
        Google Geocoding API 설정

        Args:
            api_key: Google API 키
            timeout: 요청 타임아웃 (초)
            require_rooftop: True면 ROOFTOP 정확도만 허용
        """
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        self.timeout = timeout
        self.require_rooftop = require_rooftop

    def is_valid(self, address: str) -> bool:
        """
        주소 유효성 검증

        Learning Test 기반 계약:
        1. GET 요청: base_url?address={address}&key={api_key}
        2. response.json()["status"] 확인
        3. "OK" → 유효, "ZERO_RESULTS" → 무효

        Args:
            address: 검증할 주소

        Returns:
            bool: 주소 유효 여부
        """
        if not address or len(address.strip()) < 3:
            return False

        try:
            # Learning Test에서 학습한 요청 구조
            response = requests.get(
                self.base_url,
                params={
                    "address": address,
                    "key": self.api_key
                },
                timeout=self.timeout
            )

            # HTTP 에러 확인
            response.raise_for_status()

            data = response.json()

            # Learning Test에서 학습한 Status 코드 처리
            status = data.get("status")

            if status == "OK":
                # 추가 검증: location_type 확인
                if self.require_rooftop:
                    return self._is_rooftop_location(data)
                return True

            elif status == "ZERO_RESULTS":
                # 주소 없음 (정상 응답이지만 무효 주소)
                return False

            elif status == "REQUEST_DENIED":
                # API 키 문제 - 예외 발생
                error_message = data.get("error_message", "API key denied")
                raise ValueError(f"Google API error: {error_message}")

            elif status == "INVALID_REQUEST":
                # 잘못된 요청 - 예외 발생
                raise ValueError("Invalid request to Google API")

            elif status == "OVER_QUERY_LIMIT":
                # 할당량 초과 - 예외 발생
                raise ValueError("Google API quota exceeded")

            else:
                # 알 수 없는 상태 - 안전하게 False 반환
                return False

        except requests.RequestException as e:
            # 네트워크 에러 - 예외 발생
            raise ValueError(f"Failed to connect to Google API: {str(e)}")

    def _is_rooftop_location(self, data: dict) -> bool:
        """
        ROOFTOP 정확도 확인 (가장 정확한 주소)

        Learning Test에서 학습:
        - location_type: ROOFTOP > RANGE_INTERPOLATED > GEOMETRIC_CENTER > APPROXIMATE
        """
        if not data.get("results"):
            return False

        result = data["results"][0]
        geometry = result.get("geometry", {})
        location_type = geometry.get("location_type")

        return location_type == "ROOFTOP"

    def get_coordinates(self, address: str) -> Optional[tuple[float, float]]:
        """
        주소의 좌표 조회 (선택적 기능)

        Learning Test에서 학습:
        - geometry.location.lat/lng 추출

        Args:
            address: 조회할 주소

        Returns:
            (latitude, longitude) 또는 None
        """
        try:
            response = requests.get(
                self.base_url,
                params={
                    "address": address,
                    "key": self.api_key
                },
                timeout=self.timeout
            )

            data = response.json()

            if data.get("status") == "OK" and data.get("results"):
                result = data["results"][0]
                location = result["geometry"]["location"]
                return (location["lat"], location["lng"])

            return None

        except Exception:
            return None

"""
Google Places Adapter Integration Test
Chapter 8: "Mapping Between Boundaries" - Third-Party Integration

목적:
- 실제 Google Geocoding API로 어댑터 동작 검증
- Learning Test에서 학습한 계약 준수 확인
- 에러 처리 검증

실행:
    pytest tests/integration/adapter/test_google_places_adapter.py -v -m integration
"""
import pytest
import os

from cosmetics_landing.adapter.out.geocoding.google_places_adapter import GooglePlacesAdapter


@pytest.fixture(scope="module")
def google_adapter():
    """Google Places 어댑터 픽스처"""
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")

    if not api_key:
        pytest.skip("Google API key not configured")

    return GooglePlacesAdapter(api_key=api_key)


@pytest.mark.integration
class TestGooglePlacesAdapterIntegration:
    """Google Places 어댑터 통합 테스트"""

    def test_validates_real_address_successfully(self, google_adapter):
        """
        실제 Google API로 유효한 주소 검증 성공

        검증:
        - 유효한 주소 → True 반환
        """
        # Given: 명확한 실제 주소
        valid_addresses = [
            "1600 Amphitheatre Parkway, Mountain View, CA",
            "서울시 강남구 테헤란로 152",
            "London, UK"
        ]

        for address in valid_addresses:
            # When
            is_valid = google_adapter.is_valid(address)

            # Then
            assert is_valid is True
            print(f"✅ Valid: '{address}'")

    def test_rejects_invalid_address(self, google_adapter):
        """무효한 주소 거부"""
        # Given: 존재하지 않는 주소
        invalid_addresses = [
            "asdfasdfasdfasdf",
            "xyzxyzxyzxyzxyz"
        ]

        for address in invalid_addresses:
            # When
            is_valid = google_adapter.is_valid(address)

            # Then
            assert is_valid is False
            print(f"❌ Invalid: '{address}'")

    def test_rejects_too_short_address(self, google_adapter):
        """너무 짧은 주소 거부"""
        # Given
        short_address = "ab"

        # When
        is_valid = google_adapter.is_valid(short_address)

        # Then
        assert is_valid is False
        print(f"❌ Too short: '{short_address}'")

    def test_handles_empty_address(self, google_adapter):
        """빈 주소 처리"""
        # When
        is_valid = google_adapter.is_valid("")

        # Then
        assert is_valid is False

    def test_returns_coordinates_for_valid_address(self, google_adapter):
        """유효한 주소의 좌표 반환"""
        # Given
        address = "1600 Amphitheatre Parkway, Mountain View, CA"

        # When
        coords = google_adapter.get_coordinates(address)

        # Then
        assert coords is not None
        lat, lng = coords
        assert isinstance(lat, float)
        assert isinstance(lng, float)
        assert -90 <= lat <= 90
        assert -180 <= lng <= 180

        print(f"\n✅ Coordinates: ({lat}, {lng})")

    def test_returns_none_for_invalid_address_coordinates(self, google_adapter):
        """무효한 주소는 좌표 None 반환"""
        # Given
        address = "asdfasdfasdfasdf"

        # When
        coords = google_adapter.get_coordinates(address)

        # Then
        assert coords is None


@pytest.mark.integration
class TestGooglePlacesAdapterErrorHandling:
    """Google Places 어댑터 에러 처리 검증"""

    def test_raises_error_with_invalid_api_key(self):
        """잘못된 API 키로 예외 발생"""
        # Given: 잘못된 API 키
        bad_adapter = GooglePlacesAdapter(api_key="INVALID_KEY")

        # When/Then: ValueError 발생 (메시지 패턴 수정)
        with pytest.raises(ValueError, match="Google API error"):
            bad_adapter.is_valid("Test Address")

    def test_raises_error_on_network_failure(self):
        """네트워크 실패 시 예외 발생"""
        # Given: 잘못된 base_url (수동 설정)
        adapter = GooglePlacesAdapter(api_key="test_key", timeout=1)
        adapter.base_url = "http://invalid-url-that-does-not-exist-123456789.com"

        # When/Then: ValueError 발생
        with pytest.raises(ValueError, match="Failed to connect"):
            adapter.is_valid("Test Address")


@pytest.mark.integration
class TestGooglePlacesAdapterRooftopMode:
    """ROOFTOP 정확도 모드 테스트"""

    def test_validates_with_rooftop_requirement(self):
        """ROOFTOP 정확도 요구 모드"""
        # Given
        api_key = os.getenv("GOOGLE_PLACES_API_KEY")
        if not api_key:
            pytest.skip("Google API key not configured")

        adapter = GooglePlacesAdapter(api_key=api_key, require_rooftop=True)

        # When: 정확한 주소 (ROOFTOP 가능성 높음)
        precise_address = "1600 Amphitheatre Parkway, Mountain View, CA 94043"
        is_valid = adapter.is_valid(precise_address)

        # Then: 검증 (실제 결과는 Google 데이터에 따라 다를 수 있음)
        # ROOFTOP이면 True, 아니면 False
        print(f"\n📍 Address with ROOFTOP requirement: {is_valid}")
        assert isinstance(is_valid, bool)


@pytest.mark.integration
class TestGooglePlacesAdapterPortCompliance:
    """Google Places 어댑터의 포트 인터페이스 준수 검증"""

    def test_implements_validate_address_port(self, google_adapter):
        """ValidateAddressPort 인터페이스 구현 확인"""
        from cosmetics_landing.application.port.out.address_validator import ValidateAddressPort

        assert isinstance(google_adapter, ValidateAddressPort)

    def test_is_valid_returns_bool(self, google_adapter):
        """is_valid 메서드가 bool 반환"""
        result = google_adapter.is_valid("Test Address")

        assert isinstance(result, bool)

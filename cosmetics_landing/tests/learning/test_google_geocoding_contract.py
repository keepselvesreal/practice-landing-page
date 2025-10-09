"""
Google Geocoding API Contract Learning Test
Chapter 22: "Maintaining the TDD Cycle"

목적:
1. 실제 Google Geocoding API 동작 확인
2. API 계약(request/response) 구조 학습
3. Status 코드별 처리 방식 이해
4. Mock 및 실제 어댑터 구현 근거 마련

실행:
    pytest tests/learning/test_google_geocoding_contract.py -v -m learning
"""
import pytest
import os
import requests
from typing import Dict, Any


@pytest.fixture(scope="module")
def google_api_config():
    """Google Geocoding API 설정"""
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")

    if not api_key:
        pytest.skip("Google API key not configured in .env")

    return {
        "api_key": api_key,
        "base_url": "https://maps.googleapis.com/maps/api/geocode/json"
    }


def geocode_address(address: str, api_key: str, base_url: str) -> Dict[str, Any]:
    """주소 Geocoding 요청 헬퍼"""
    response = requests.get(
        base_url,
        params={"address": address, "key": api_key},
        timeout=10
    )
    return response.json()


@pytest.mark.learning
class TestGoogleGeocodingBasicContract:
    """Google Geocoding API 기본 계약 학습"""

    def test_valid_address_returns_ok_status(self, google_api_config):
        """
        학습 목표: 유효한 주소는 OK 상태를 반환한다

        API 계약 검증:
        - status == "OK"
        - results 배열 존재 및 비어있지 않음
        - formatted_address 포함
        - geometry.location (lat/lng) 포함
        """
        # Given: 명확한 실제 주소
        address = "1600 Amphitheatre Parkway, Mountain View, CA"

        # When
        data = geocode_address(
            address,
            google_api_config["api_key"],
            google_api_config["base_url"]
        )

        # Then: 응답 구조 검증
        assert data["status"] == "OK", f"Expected OK, got {data['status']}"
        assert "results" in data
        assert len(data["results"]) > 0, "No results returned"

        # 첫 번째 결과 검증
        result = data["results"][0]

        # formatted_address 존재
        assert "formatted_address" in result
        assert len(result["formatted_address"]) > 0
        print(f"\n✅ Formatted Address: {result['formatted_address']}")

        # geometry 정보 존재
        assert "geometry" in result
        assert "location" in result["geometry"]

        location = result["geometry"]["location"]
        assert "lat" in location
        assert "lng" in location
        assert isinstance(location["lat"], (int, float))
        assert isinstance(location["lng"], (int, float))
        print(f"   Location: ({location['lat']}, {location['lng']})")

        # place_id 존재
        assert "place_id" in result
        print(f"   Place ID: {result['place_id']}")

    def test_invalid_address_returns_zero_results(self, google_api_config):
        """
        학습 목표: 존재하지 않는 주소는 ZERO_RESULTS를 반환한다

        API 계약 검증:
        - status == "ZERO_RESULTS"
        - results 배열이 비어있음
        """
        # Given: 존재하지 않는 주소
        address = "asdfasdfasdfasdf"

        # When
        data = geocode_address(
            address,
            google_api_config["api_key"],
            google_api_config["base_url"]
        )

        # Then
        assert data["status"] == "ZERO_RESULTS", f"Expected ZERO_RESULTS, got {data['status']}"
        assert "results" in data
        assert len(data["results"]) == 0, "Expected empty results"

        print(f"\n✅ Invalid address correctly rejected: {data['status']}")

    def test_response_includes_location_type(self, google_api_config):
        """
        학습 목표: 응답에 location_type이 포함되어 정확도 판단 가능

        API 계약 검증:
        - geometry.location_type 존재
        - ROOFTOP, RANGE_INTERPOLATED, GEOMETRIC_CENTER, APPROXIMATE 중 하나
        """
        # Given
        address = "1600 Amphitheatre Parkway, Mountain View, CA"

        # When
        data = geocode_address(
            address,
            google_api_config["api_key"],
            google_api_config["base_url"]
        )

        # Then
        assert data["status"] == "OK"
        result = data["results"][0]

        assert "geometry" in result
        assert "location_type" in result["geometry"]

        location_type = result["geometry"]["location_type"]
        valid_types = ["ROOFTOP", "RANGE_INTERPOLATED", "GEOMETRIC_CENTER", "APPROXIMATE"]
        assert location_type in valid_types, f"Unexpected location_type: {location_type}"

        print(f"\n✅ Location Type: {location_type}")
        print(f"   (정확도: ROOFTOP > RANGE_INTERPOLATED > GEOMETRIC_CENTER > APPROXIMATE)")


@pytest.mark.learning
class TestGoogleGeocodingAddressComponents:
    """Google Geocoding 주소 컴포넌트 학습"""

    def test_response_includes_address_components(self, google_api_config):
        """
        학습 목표: 응답에 주소 구성 요소가 포함된다

        API 계약 검증:
        - address_components 배열 존재
        - 각 컴포넌트에 long_name, short_name, types 포함
        """
        # Given
        address = "1600 Amphitheatre Parkway, Mountain View, CA 94043"

        # When
        data = geocode_address(
            address,
            google_api_config["api_key"],
            google_api_config["base_url"]
        )

        # Then
        result = data["results"][0]
        assert "address_components" in result
        assert len(result["address_components"]) > 0

        print("\n📋 Address Components:")
        for component in result["address_components"]:
            assert "long_name" in component
            assert "short_name" in component
            assert "types" in component
            assert isinstance(component["types"], list)

            print(f"   - {component['long_name']} ({', '.join(component['types'])})")

    def test_types_field_classification(self, google_api_config):
        """
        학습 목표: types 필드로 주소 종류 분류 가능

        API 계약 검증:
        - types 배열 존재
        - street_address, route, locality 등 포함
        """
        # Given
        address = "1600 Amphitheatre Parkway, Mountain View, CA"

        # When
        data = geocode_address(
            address,
            google_api_config["api_key"],
            google_api_config["base_url"]
        )

        # Then
        result = data["results"][0]
        assert "types" in result
        assert isinstance(result["types"], list)
        assert len(result["types"]) > 0

        print(f"\n✅ Address Types: {', '.join(result['types'])}")


@pytest.mark.learning
class TestGoogleGeocodingVariousAddresses:
    """다양한 주소 패턴 테스트"""

    def test_short_address_validation(self, google_api_config):
        """
        학습 목표: 짧은 주소도 검증 가능

        API 계약 학습:
        - 도시명, 우편번호도 유효한 주소로 인식
        - API는 관대하게 동작 (OK 또는 ZERO_RESULTS 반환)
        """
        test_cases = [
            "Seoul",   # 도시명
            "12345",   # 우편번호 형식
            "abc",     # 짧은 문자열
        ]

        for address in test_cases:
            data = geocode_address(
                address,
                google_api_config["api_key"],
                google_api_config["base_url"]
            )

            # Google API는 매우 관대하게 동작
            # 짧은 문자열도 OK 또는 ZERO_RESULTS 반환
            assert data["status"] in ["OK", "ZERO_RESULTS", "INVALID_REQUEST"]
            print(f"   '{address}': {data['status']}")

    def test_international_addresses(self, google_api_config):
        """
        학습 목표: 국제 주소 지원 확인

        API 계약 검증:
        - 한국, 일본 등 다양한 국가 주소 처리
        """
        test_addresses = [
            "서울시 강남구 테헤란로 152",  # 한국
            "東京都渋谷区道玄坂1丁目2-3",    # 일본
            "London, UK",                # 영국
        ]

        for address in test_addresses:
            data = geocode_address(
                address,
                google_api_config["api_key"],
                google_api_config["base_url"]
            )

            # 모든 주소가 OK 또는 ZERO_RESULTS 반환
            assert data["status"] in ["OK", "ZERO_RESULTS"]

            if data["status"] == "OK":
                result = data["results"][0]
                print(f"✅ '{address}'")
                print(f"   → {result['formatted_address']}")


@pytest.mark.learning
class TestGoogleGeocodingErrorHandling:
    """Google Geocoding API 에러 처리 학습"""

    def test_invalid_api_key_returns_request_denied(self):
        """
        학습 목표: 잘못된 API 키는 REQUEST_DENIED를 반환한다

        API 계약 검증:
        - status == "REQUEST_DENIED"
        - error_message 포함
        """
        # Given: 잘못된 API 키
        invalid_key = "INVALID_KEY_FOR_TESTING"
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"

        # When
        data = geocode_address("Test Address", invalid_key, base_url)

        # Then
        assert data["status"] == "REQUEST_DENIED"
        assert "error_message" in data
        print(f"\n✅ Invalid key rejected: {data['status']}")
        print(f"   Error: {data['error_message']}")

    def test_missing_address_parameter(self, google_api_config):
        """
        학습 목표: 주소 파라미터 누락 시 INVALID_REQUEST

        API 계약 검증:
        - address 파라미터 필수
        """
        # Given: 주소 파라미터 없이 요청
        response = requests.get(
            google_api_config["base_url"],
            params={"key": google_api_config["api_key"]},  # address 누락
            timeout=10
        )
        data = response.json()

        # Then
        assert data["status"] == "INVALID_REQUEST"
        print(f"\n✅ Missing parameter rejected: {data['status']}")


@pytest.mark.learning
class TestGoogleGeocodingResponseStructure:
    """Google Geocoding 응답 구조 상세 학습"""

    def test_complete_response_structure(self, google_api_config):
        """
        학습 목표: 전체 응답 구조 파악

        API 계약 검증:
        - 모든 필드와 데이터 타입 확인
        """
        # Given
        address = "1600 Amphitheatre Parkway, Mountain View, CA"

        # When
        data = geocode_address(
            address,
            google_api_config["api_key"],
            google_api_config["base_url"]
        )

        # Then: 응답 구조 분석
        print("\n📋 Complete Response Structure:")
        print(f"   Status: {data['status']}")

        if data["status"] == "OK":
            result = data["results"][0]

            # 1. Address Components
            print(f"\n   Address Components: {len(result['address_components'])} items")

            # 2. Formatted Address
            print(f"   Formatted Address: {result['formatted_address']}")

            # 3. Geometry
            geometry = result["geometry"]
            print(f"\n   Geometry:")
            print(f"      Location: {geometry['location']}")
            print(f"      Location Type: {geometry['location_type']}")
            print(f"      Viewport: {geometry.get('viewport', 'N/A')}")

            # 4. Place ID
            print(f"\n   Place ID: {result['place_id']}")

            # 5. Types
            print(f"   Types: {', '.join(result['types'])}")

            # 필수 필드 존재 확인
            assert "formatted_address" in result
            assert "geometry" in result
            assert "place_id" in result
            assert "types" in result
            assert "address_components" in result

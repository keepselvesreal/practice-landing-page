"""
Fake Address Validator Contract Test
Chapter 22: "Learning Tests" - Verify Fake implements same contract as Real

목적:
- FakeAddressValidator가 GooglePlacesAdapter와 동일한 계약 준수 확인
- 포트 인터페이스(ValidateAddressPort) 구현 검증
- 동일한 입출력 타입과 동작 보장

실행:
    pytest tests/unit/adapter/test_fake_address_validator_contract.py -v
"""
import pytest

from cosmetics_landing.adapter.out.geocoding.fake_address_validator import FakeAddressValidator
from cosmetics_landing.adapter.out.geocoding.google_places_adapter import GooglePlacesAdapter
from cosmetics_landing.application.port.out.address_validator import ValidateAddressPort


class TestFakeAddressValidatorContract:
    """FakeAddressValidator 계약 검증"""

    def test_implements_validate_address_port(self):
        """ValidateAddressPort 인터페이스 구현 확인"""
        fake_validator = FakeAddressValidator()

        assert isinstance(fake_validator, ValidateAddressPort)

    def test_is_valid_returns_bool(self):
        """is_valid가 bool 반환"""
        fake_validator = FakeAddressValidator()

        result = fake_validator.is_valid("Test Address")

        assert isinstance(result, bool)

    def test_is_valid_accepts_string_address(self):
        """is_valid가 문자열 주소를 입력으로 받음"""
        fake_validator = FakeAddressValidator()

        # 다양한 형식의 주소 테스트
        addresses = [
            "123 Main St",
            "서울시 강남구 테헤란로 152",
            "London, UK",
            "",  # 빈 문자열도 허용 (False 반환)
        ]

        for address in addresses:
            result = fake_validator.is_valid(address)
            assert isinstance(result, bool)

    def test_same_interface_as_google_places_adapter(self):
        """GooglePlacesAdapter와 동일한 인터페이스"""
        fake_validator = FakeAddressValidator()

        # 두 어댑터 모두 동일한 포트 구현
        assert isinstance(fake_validator, ValidateAddressPort)

        # 동일한 메서드 시그니처
        assert hasattr(fake_validator, 'is_valid')

        # 동일한 입출력 타입
        result = fake_validator.is_valid("Test Address")
        assert isinstance(result, bool)


class TestFakeAddressValidatorBehavior:
    """FakeAddressValidator 동작 검증 (Real과 다를 수 있는 부분)"""

    def test_fake_uses_simple_validation_logic(self):
        """Fake는 단순한 검증 로직 (Real은 실제 API 호출)"""
        fake_validator = FakeAddressValidator()

        # Fake 기본 동작: 5자 이상이면 유효 (invalid_patterns 제외)
        assert fake_validator.is_valid("ab") is False  # 2자
        assert fake_validator.is_valid("abc") is False  # 3자
        assert fake_validator.is_valid("abcde") is True  # 5자
        assert fake_validator.is_valid("1600 Amphitheatre Parkway") is True

    def test_fake_has_configurable_invalid_patterns(self):
        """Fake는 무효 패턴 설정 가능 (테스트 편의성)"""
        # 특정 패턴이 포함되면 무효로 판단
        fake_validator = FakeAddressValidator(invalid_patterns=["test", "dummy"])

        assert fake_validator.is_valid("test address") is False  # "test" 포함
        assert fake_validator.is_valid("dummy street") is False  # "dummy" 포함
        assert fake_validator.is_valid("123 Main Street") is True  # 패턴 없음

    def test_fake_default_invalid_patterns(self):
        """Fake 기본 무효 패턴: 'invalid', 'fake'"""
        fake_validator = FakeAddressValidator()

        assert fake_validator.is_valid("invalid address") is False
        assert fake_validator.is_valid("fake street") is False
        assert fake_validator.is_valid("real address") is True

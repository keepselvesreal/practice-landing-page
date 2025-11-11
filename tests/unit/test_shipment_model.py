"""Shipment 도메인 로직 Unit 테스트"""
import pytest
from backend.models.db import ShipmentDB
from backend.models.db.shipment import InvalidTransitionError


@pytest.mark.unit
def test_when_transitioning_from_preparing_to_delivered_then_raises_error():
    """
    상태 전환 규칙 검증: PREPARING → DELIVERED 직접 전환 불가

    Given: PREPARING 상태 Shipment
    When: update_status("DELIVERED") 호출
    Then: InvalidTransitionError 발생, 상태 변경 안 됨
    """
    # Given: PREPARING 상태 Shipment
    shipment = ShipmentDB(
        order_id=1,
        shipping_status="PREPARING",
        tracking_number=None,
        courier=None
    )

    # When & Then: DELIVERED로 직접 전환 시도 → 예외 발생
    with pytest.raises(InvalidTransitionError) as exc_info:
        shipment.update_status(
            new_status="DELIVERED",
            tracking_number="123",
            courier="LBC"
        )

    # 에러 메시지 검증
    assert "PREPARING" in str(exc_info.value)
    assert "DELIVERED" in str(exc_info.value)
    assert "SHIPPED" in str(exc_info.value)

    # 상태가 변경되지 않았는지 확인
    assert shipment.shipping_status == "PREPARING"


@pytest.mark.unit
def test_when_delivered_then_cannot_transition_to_any_status():
    """
    종료 상태 불변성 검증: DELIVERED → 어떤 상태든 전환 불가

    Given: DELIVERED 상태 Shipment
    When: update_status("SHIPPED") 호출 (또는 다른 어떤 상태)
    Then: InvalidTransitionError 발생, 상태 변경 안 됨
    """
    # Given: DELIVERED 상태 Shipment
    shipment = ShipmentDB(
        order_id=1,
        shipping_status="DELIVERED",
        tracking_number="123",
        courier="LBC"
    )

    # When & Then: SHIPPED로 전환 시도 → 예외 발생
    with pytest.raises(InvalidTransitionError) as exc_info:
        shipment.update_status(new_status="SHIPPED")

    # 에러 메시지 검증
    assert "DELIVERED" in str(exc_info.value)
    assert "[]" in str(exc_info.value) or "허용: []" in str(exc_info.value)

    # 상태가 변경되지 않았는지 확인
    assert shipment.shipping_status == "DELIVERED"


@pytest.mark.unit
def test_when_shipped_without_tracking_number_then_raises_error():
    """
    필수 필드 검증: SHIPPED 전환 시 운송장 번호 필수

    Given: PREPARING 상태 Shipment
    When: update_status("SHIPPED", tracking_number=None)
    Then: ValueError 발생, 상태 변경 안 됨
    """
    # Given: PREPARING 상태 Shipment
    shipment = ShipmentDB(
        order_id=1,
        shipping_status="PREPARING"
    )

    # When & Then: 운송장 번호 없이 SHIPPED 전환 시도 → 예외 발생
    with pytest.raises(ValueError) as exc_info:
        shipment.update_status(
            new_status="SHIPPED",
            tracking_number=None,
            courier="LBC Express"
        )

    # 에러 메시지 검증
    assert "운송장" in str(exc_info.value) or "tracking" in str(exc_info.value).lower()

    # 상태가 변경되지 않았는지 확인
    assert shipment.shipping_status == "PREPARING"


@pytest.mark.unit
def test_when_shipped_without_courier_then_raises_error():
    """
    필수 필드 검증: SHIPPED 전환 시 택배사 필수

    Given: PREPARING 상태 Shipment
    When: update_status("SHIPPED", courier=None)
    Then: ValueError 발생, 상태 변경 안 됨
    """
    # Given: PREPARING 상태 Shipment
    shipment = ShipmentDB(
        order_id=1,
        shipping_status="PREPARING"
    )

    # When & Then: 택배사 없이 SHIPPED 전환 시도 → 예외 발생
    with pytest.raises(ValueError) as exc_info:
        shipment.update_status(
            new_status="SHIPPED",
            tracking_number="1234567890",
            courier=None
        )

    # 에러 메시지 검증
    assert "택배사" in str(exc_info.value) or "courier" in str(exc_info.value).lower()

    # 상태가 변경되지 않았는지 확인
    assert shipment.shipping_status == "PREPARING"


@pytest.mark.unit
def test_when_shipped_without_tracking_number_argument_then_raises_error():
    """
    필수 필드 검증: SHIPPED 전환 시 tracking_number 인자 생략

    Given: PREPARING 상태 Shipment
    When: update_status("SHIPPED") - tracking_number 인자 자체를 생략
    Then: ValueError 발생, 상태 변경 안 됨
    """
    # Given: PREPARING 상태 Shipment
    shipment = ShipmentDB(
        order_id=1,
        shipping_status="PREPARING"
    )

    # When & Then: tracking_number 인자 자체를 생략 → 예외 발생
    with pytest.raises(ValueError) as exc_info:
        shipment.update_status(
            new_status="SHIPPED",
            courier="LBC Express"
        )

    # 에러 메시지 검증
    assert "운송장" in str(exc_info.value) or "tracking" in str(exc_info.value).lower()

    # 상태가 변경되지 않았는지 확인
    assert shipment.shipping_status == "PREPARING"


@pytest.mark.unit
def test_when_shipped_without_courier_argument_then_raises_error():
    """
    필수 필드 검증: SHIPPED 전환 시 courier 인자 생략

    Given: PREPARING 상태 Shipment
    When: update_status("SHIPPED") - courier 인자 자체를 생략
    Then: ValueError 발생, 상태 변경 안 됨
    """
    # Given: PREPARING 상태 Shipment
    shipment = ShipmentDB(
        order_id=1,
        shipping_status="PREPARING"
    )

    # When & Then: courier 인자 자체를 생략 → 예외 발생
    with pytest.raises(ValueError) as exc_info:
        shipment.update_status(
            new_status="SHIPPED",
            tracking_number="1234567890"
        )

    # 에러 메시지 검증
    assert "택배사" in str(exc_info.value) or "courier" in str(exc_info.value).lower()

    # 상태가 변경되지 않았는지 확인
    assert shipment.shipping_status == "PREPARING"

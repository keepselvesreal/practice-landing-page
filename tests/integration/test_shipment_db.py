"""배송 상태 DB 영속성 Integration 테스트"""
import pytest
from backend.models.db import ShipmentDB
from backend.services.shipment_service import update_shipment_status, get_shipment_by_order_id


@pytest.mark.integration
def test_when_updating_to_shipped_then_persists_tracking_and_timestamp(db_session, test_data):
    """
    DB 영속성 검증: PREPARING → SHIPPED

    Given: PREPARING 상태 Shipment
    When: update_shipment_status() 함수로 상태 업데이트
    Then: DB에서 조회 시 status=SHIPPED, tracking, courier, shipped_at 확인
    """
    # Given: test_data fixture에서 PREPARING Shipment 가져오기
    order_id = test_data["order"].id
    shipment_before = test_data["shipment"]
    assert shipment_before.shipping_status == "PREPARING"
    assert shipment_before.shipped_at is None

    # When: Service 함수로 상태 업데이트
    update_shipment_status(
        db_session,
        order_id=order_id,
        new_status="SHIPPED",
        tracking_number="1234567890",
        courier="LBC Express"
    )

    # Then: DB에서 다시 조회하여 검증
    saved_shipment = db_session.query(ShipmentDB).filter_by(
        order_id=order_id
    ).first()

    assert saved_shipment is not None
    assert saved_shipment.shipping_status == "SHIPPED"
    assert saved_shipment.tracking_number == "1234567890"
    assert saved_shipment.courier == "LBC Express"
    assert saved_shipment.shipped_at is not None


@pytest.mark.integration
def test_when_updating_to_delivered_then_records_delivered_timestamp(db_session, test_data):
    """
    DB 영속성 검증: SHIPPED → DELIVERED

    Given: SHIPPED 상태 Shipment
    When: update_shipment_status()로 DELIVERED로 업데이트
    Then: DB에서 조회 시 status=DELIVERED, delivered_at IS NOT NULL
    """
    # Given: Shipment를 먼저 SHIPPED 상태로 만듦
    order_id = test_data["order"].id
    update_shipment_status(
        db_session,
        order_id=order_id,
        new_status="SHIPPED",
        tracking_number="1234567890",
        courier="LBC Express"
    )

    # When: DELIVERED로 상태 업데이트
    update_shipment_status(
        db_session,
        order_id=order_id,
        new_status="DELIVERED"
    )

    # Then: DB에서 조회하여 검증
    saved_shipment = db_session.query(ShipmentDB).filter_by(
        order_id=order_id
    ).first()

    assert saved_shipment is not None
    assert saved_shipment.shipping_status == "DELIVERED"
    assert saved_shipment.delivered_at is not None
    assert saved_shipment.shipped_at is not None
    # delivered_at이 shipped_at보다 나중이어야 함
    assert saved_shipment.delivered_at >= saved_shipment.shipped_at


@pytest.mark.integration
def test_when_querying_nonexistent_order_then_returns_none(db_session):
    """
    조회 함수 검증: 존재하지 않는 order_id

    Given: DB에 존재하지 않는 order_id (999999)
    When: get_shipment_by_order_id() 호출
    Then: None 반환
    """
    # Given: 존재하지 않는 order_id
    non_existent_order_id = 999999

    # When: Shipment 조회
    result = get_shipment_by_order_id(db_session, non_existent_order_id)

    # Then: None 반환
    assert result is None


@pytest.mark.integration
def test_when_querying_existing_order_then_returns_shipment(db_session, test_data):
    """
    조회 함수 검증: 존재하는 order_id

    Given: DB에 존재하는 Shipment
    When: get_shipment_by_order_id() 호출
    Then: Shipment 객체 반환
    """
    # Given: test_data에 있는 order_id
    order_id = test_data["order"].id
    expected_shipment = test_data["shipment"]

    # When: Shipment 조회
    result = get_shipment_by_order_id(db_session, order_id)

    # Then: Shipment 객체 반환
    assert result is not None
    assert result.id == expected_shipment.id
    assert result.order_id == order_id
    assert result.shipping_status == "PREPARING"

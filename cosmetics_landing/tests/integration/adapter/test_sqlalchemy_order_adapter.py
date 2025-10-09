"""
SQLAlchemy Order Adapter Integration Test
Chapter 6: "Implementing a Persistence Adapter" - Database Integration

목적:
- 실제 SQLite 데이터베이스로 어댑터 동작 검증
- CRUD 작업 검증
- 도메인 ↔ ORM 매핑 검증

실행:
    pytest tests/integration/adapter/test_sqlalchemy_order_adapter.py -v -m integration
"""
import pytest
from decimal import Decimal
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from cosmetics_landing.adapter.out.persistence.sqlalchemy_models import Base, OrderModel
from cosmetics_landing.adapter.out.persistence.sqlalchemy_order_adapter import SQLAlchemyOrderAdapter
from cosmetics_landing.domain.order import Order, OrderId, Money


@pytest.fixture(scope="function")
def db_session():
    """
    테스트용 SQLite 인메모리 데이터베이스 세션

    각 테스트마다 새로운 DB 생성 (격리)
    """
    # In-Memory SQLite
    engine = create_engine("sqlite:///:memory:", echo=False)

    # 테이블 생성
    Base.metadata.create_all(engine)

    # Session 생성
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    yield session

    # 정리
    session.close()


@pytest.fixture
def order_adapter(db_session: Session):
    """SQLAlchemy 어댑터 픽스처"""
    return SQLAlchemyOrderAdapter(session=db_session)


@pytest.fixture
def sample_order():
    """테스트용 주문 (ID 없음 - 새 주문)"""
    return Order(
        id=None,  # 새 주문
        customer_email="test@example.com",
        customer_address="123 Main St, Manila, Philippines",
        product_price=Money.of(Decimal("29.99")),
        affiliate_code=None,
        created_at=datetime.now(),
        payment_status="pending"
    )


@pytest.mark.integration
class TestSQLAlchemyOrderAdapterBasicOperations:
    """SQLAlchemy 어댑터 기본 CRUD 작업 검증"""

    def test_saves_new_order_successfully(self, order_adapter, sample_order):
        """
        새 주문 저장 성공

        검증:
        - save() 호출 후 OrderId 반환
        - DB에 실제로 저장됨
        """
        # When: 주문 저장
        order_id = order_adapter.save(sample_order)

        # Then: ID 반환
        assert order_id is not None
        assert isinstance(order_id, OrderId)
        assert order_id.value > 0

        # Then: DB에서 조회 가능
        loaded_order = order_adapter.load_by_id(order_id)
        assert loaded_order is not None
        assert loaded_order.customer_email == "test@example.com"

    def test_loads_order_by_id_successfully(self, order_adapter, sample_order):
        """ID로 주문 조회 성공"""
        # Given: 주문 저장
        order_id = order_adapter.save(sample_order)

        # When: ID로 조회
        loaded_order = order_adapter.load_by_id(order_id)

        # Then: 올바르게 조회됨
        assert loaded_order is not None
        assert loaded_order.id == order_id
        assert loaded_order.customer_email == "test@example.com"
        assert loaded_order.customer_address == "123 Main St, Manila, Philippines"
        assert loaded_order.product_price.amount == Decimal("29.99")

    def test_returns_none_for_nonexistent_order(self, order_adapter):
        """존재하지 않는 주문은 None 반환"""
        # When: 존재하지 않는 ID로 조회
        loaded_order = order_adapter.load_by_id(OrderId(value=99999))

        # Then: None 반환
        assert loaded_order is None

    def test_updates_existing_order(self, order_adapter, sample_order):
        """기존 주문 업데이트"""
        # Given: 주문 저장
        order_id = order_adapter.save(sample_order)

        # Given: 주문 수정
        loaded_order = order_adapter.load_by_id(order_id)
        updated_order = Order(
            id=loaded_order.id,
            customer_email=loaded_order.customer_email,
            customer_address=loaded_order.customer_address,
            product_price=loaded_order.product_price,
            affiliate_code=loaded_order.affiliate_code,
            created_at=loaded_order.created_at,
            payment_status="completed"  # 상태 변경
        )

        # When: 업데이트
        order_adapter.save(updated_order)

        # Then: 변경사항 반영됨
        reloaded_order = order_adapter.load_by_id(order_id)
        assert reloaded_order.payment_status == "completed"


@pytest.mark.integration
class TestSQLAlchemyOrderAdapterAffiliateQueries:
    """어필리에이트 코드 조회 검증"""

    def test_loads_orders_by_affiliate_code(self, order_adapter):
        """어필리에이트 코드로 주문 목록 조회"""
        # Given: 동일한 어필리에이트 코드로 2개 주문 저장
        order1 = Order(
            id=None,
            customer_email="test1@example.com",
            customer_address="123 Main St",
            product_price=Money.of(Decimal("29.99")),
            affiliate_code="INFLUENCER123",
            created_at=datetime.now(),
            payment_status="pending"
        )
        order2 = Order(
            id=None,
            customer_email="test2@example.com",
            customer_address="456 Oak St",
            product_price=Money.of(Decimal("39.99")),
            affiliate_code="INFLUENCER123",
            created_at=datetime.now(),
            payment_status="pending"
        )

        order_adapter.save(order1)
        order_adapter.save(order2)

        # When: 어필리에이트 코드로 조회
        orders = order_adapter.load_by_affiliate_code("INFLUENCER123")

        # Then: 2개 주문 반환
        assert len(orders) == 2
        assert all(order.affiliate_code == "INFLUENCER123" for order in orders)

    def test_returns_empty_list_for_unknown_affiliate_code(self, order_adapter):
        """존재하지 않는 어필리에이트 코드는 빈 리스트 반환"""
        # When: 존재하지 않는 코드로 조회
        orders = order_adapter.load_by_affiliate_code("UNKNOWN")

        # Then: 빈 리스트
        assert orders == []


@pytest.mark.integration
class TestSQLAlchemyOrderAdapterDomainMapping:
    """도메인 ↔ ORM 매핑 검증"""

    def test_preserves_money_value_object(self, order_adapter, sample_order):
        """Money Value Object 올바르게 보존"""
        # Given: Money Value Object 포함된 주문
        order_id = order_adapter.save(sample_order)

        # When: 조회
        loaded_order = order_adapter.load_by_id(order_id)

        # Then: Money Value Object 정확히 복원
        assert loaded_order.product_price.amount == Decimal("29.99")

    def test_preserves_order_id_value_object(self, order_adapter, sample_order):
        """OrderId Value Object 올바르게 보존"""
        # Given: 주문 저장
        order_id = order_adapter.save(sample_order)

        # When: 조회
        loaded_order = order_adapter.load_by_id(order_id)

        # Then: OrderId Value Object 정확히 복원
        assert isinstance(loaded_order.id, OrderId)
        assert loaded_order.id.value == order_id.value

    def test_preserves_nullable_affiliate_code(self, order_adapter, sample_order):
        """Nullable 필드 (affiliate_code) 올바르게 처리"""
        # Given: affiliate_code가 None인 주문
        assert sample_order.affiliate_code is None
        order_id = order_adapter.save(sample_order)

        # When: 조회
        loaded_order = order_adapter.load_by_id(order_id)

        # Then: None으로 복원
        assert loaded_order.affiliate_code is None


@pytest.mark.integration
class TestSQLAlchemyOrderAdapterPortCompliance:
    """포트 인터페이스 준수 검증"""

    def test_implements_save_order_port(self, order_adapter):
        """SaveOrderPort 인터페이스 구현 확인"""
        from cosmetics_landing.application.port.out.order_repository import SaveOrderPort

        assert isinstance(order_adapter, SaveOrderPort)

    def test_implements_load_order_port(self, order_adapter):
        """LoadOrderPort 인터페이스 구현 확인"""
        from cosmetics_landing.application.port.out.order_repository import LoadOrderPort

        assert isinstance(order_adapter, LoadOrderPort)

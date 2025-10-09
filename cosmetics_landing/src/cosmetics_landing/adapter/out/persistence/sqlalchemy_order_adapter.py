"""
SQLAlchemy Order Persistence Adapter
Chapter 6: "Implementing a Persistence Adapter"

목적:
- Order 도메인 엔티티를 SQLAlchemy ORM으로 영속화
- 도메인 모델 ↔ ORM 모델 변환 (Mapper)
- 포트 인터페이스 구현 (SaveOrderPort, LoadOrderPort)
"""
from typing import Optional
from decimal import Decimal

from sqlalchemy.orm import Session

from .sqlalchemy_models import OrderModel
from ....application.port.out.order_repository import SaveOrderPort, LoadOrderPort
from ....domain.order import Order, OrderId, Money


class SQLAlchemyOrderAdapter(SaveOrderPort, LoadOrderPort):
    """
    SQLAlchemy 기반 주문 영속성 어댑터

    Chapter 6: 영속성 어댑터 패턴
    - 도메인 모델과 DB 모델 분리
    - 양방향 매핑 (to_domain / from_domain)
    - Session 관리
    """

    def __init__(self, session: Session):
        """
        Args:
            session: SQLAlchemy Session
        """
        self.session = session

    def save(self, order: Order) -> OrderId:
        """
        주문 저장

        Chapter 6: Domain → ORM 변환 후 저장
        """
        if order.id is None:
            # 새 주문 생성
            order_model = self._from_domain(order)
            self.session.add(order_model)
            self.session.commit()
            self.session.refresh(order_model)  # DB에서 생성된 ID 가져오기

            return OrderId(value=order_model.id)
        else:
            # 기존 주문 업데이트
            order_model = self.session.query(OrderModel).filter_by(id=order.id.value).first()

            if order_model is None:
                # 존재하지 않으면 새로 생성
                order_model = self._from_domain(order)
                self.session.add(order_model)
            else:
                # 기존 모델 업데이트
                self._update_model_from_domain(order_model, order)

            self.session.commit()
            self.session.refresh(order_model)

            return OrderId(value=order_model.id)

    def load_by_id(self, order_id: OrderId) -> Optional[Order]:
        """
        ID로 주문 조회

        Chapter 6: ORM → Domain 변환
        """
        order_model = self.session.query(OrderModel).filter_by(id=order_id.value).first()

        if order_model is None:
            return None

        return self._to_domain(order_model)

    def load_by_affiliate_code(self, affiliate_code: str) -> list[Order]:
        """
        어필리에이트 코드로 주문 목록 조회
        """
        order_models = self.session.query(OrderModel).filter_by(affiliate_code=affiliate_code).all()

        return [self._to_domain(model) for model in order_models]

    # ==================== Mapper Methods ====================

    @staticmethod
    def _to_domain(order_model: OrderModel) -> Order:
        """
        ORM Model → Domain Entity 변환

        Chapter 6: 매핑 책임 분리
        """
        return Order(
            id=OrderId(value=order_model.id),
            customer_email=order_model.customer_email,
            customer_address=order_model.customer_address,
            product_price=Money.of(Decimal(str(order_model.product_price_amount))),
            affiliate_code=order_model.affiliate_code,
            created_at=order_model.created_at,
            payment_status=order_model.payment_status
        )

    @staticmethod
    def _from_domain(order: Order) -> OrderModel:
        """
        Domain Entity → ORM Model 변환 (새 생성)
        """
        return OrderModel(
            id=order.id.value if order.id else None,
            customer_email=order.customer_email,
            customer_address=order.customer_address,
            product_price_amount=float(order.product_price.amount),
            product_price_currency="USD",  # Money 클래스에 currency 없음, 기본값 사용
            affiliate_code=order.affiliate_code,
            created_at=order.created_at,
            payment_status=order.payment_status
        )

    @staticmethod
    def _update_model_from_domain(order_model: OrderModel, order: Order) -> None:
        """
        Domain Entity → ORM Model 변환 (기존 업데이트)
        """
        order_model.customer_email = order.customer_email
        order_model.customer_address = order.customer_address
        order_model.product_price_amount = float(order.product_price.amount)
        order_model.product_price_currency = "USD"  # Money 클래스에 currency 없음, 기본값 사용
        order_model.affiliate_code = order.affiliate_code
        order_model.payment_status = order.payment_status

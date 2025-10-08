"""
In-Memory Order Persistence Adapter
Walking Skeleton용 간단한 메모리 저장소
"""
from typing import Optional, Dict

from ....application.port.out.order_repository import SaveOrderPort, LoadOrderPort
from ....domain.order import Order, OrderId


class InMemoryOrderAdapter(SaveOrderPort, LoadOrderPort):
    """
    In-Memory 주문 저장소 어댑터

    Chapter 6: 영속성 어댑터 패턴
    Walking Skeleton에서는 실제 DB 대신 메모리 사용
    """

    def __init__(self):
        self._orders: Dict[int, Order] = {}
        self._next_id = 1

    def save(self, order: Order) -> OrderId:
        """주문 저장"""
        if order.id is None:
            # 새 주문 생성
            order_id = OrderId(value=self._next_id)
            self._next_id += 1

            # ID를 가진 새 주문 객체 생성
            order_with_id = Order(
                id=order_id,
                customer_email=order.customer_email,
                customer_address=order.customer_address,
                product_price=order.product_price,
                affiliate_code=order.affiliate_code,
                created_at=order.created_at,
                payment_status=order.payment_status
            )
            self._orders[order_id.value] = order_with_id
            return order_id
        else:
            # 기존 주문 업데이트
            self._orders[order.id.value] = order
            return order.id

    def load_by_id(self, order_id: OrderId) -> Optional[Order]:
        """ID로 주문 조회"""
        return self._orders.get(order_id.value)

    def load_by_affiliate_code(self, affiliate_code: str) -> list[Order]:
        """어필리에이트 코드로 주문 목록 조회"""
        return [
            order for order in self._orders.values()
            if order.affiliate_code == affiliate_code
        ]

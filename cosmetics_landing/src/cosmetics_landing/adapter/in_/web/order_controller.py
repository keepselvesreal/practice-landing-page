"""
Order Web Controller
Chapter 5: Web Adapter 구현
"""
from fastapi import APIRouter, Depends, HTTPException, status
from decimal import Decimal

from .dto.order_request import OrderRequest, OrderResponse
from ....application.port.in_.place_order_use_case import (
    PlaceOrderUseCase,
    PlaceOrderCommand
)
from ....application.exceptions import PaymentFailedError, InvalidAddressError


router = APIRouter(prefix="/api/orders", tags=["orders"])


def get_place_order_use_case() -> PlaceOrderUseCase:
    """
    의존성 주입 (FastAPI Depends)

    실제 구현은 config/dependencies.py에서 제공
    """
    # 이 함수는 config/dependencies.py에서 override됨
    raise NotImplementedError("Use case must be injected via dependencies")


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    request: OrderRequest,
    place_order: PlaceOrderUseCase = Depends(get_place_order_use_case)
) -> OrderResponse:
    """
    주문 생성 엔드포인트

    Chapter 5, Lines 91-120: 웹 어댑터 책임 7단계
    1. HTTP 요청을 객체로 매핑 ✓ (FastAPI + Pydantic)
    2. 인증/인가 검사 (현재는 생략)
    3. 입력 검증 ✓ (Pydantic)
    4. 유스케이스 입력 모델로 변환
    5. 유스케이스 호출
    6. 유스케이스 출력을 HTTP로 매핑
    7. HTTP 응답 반환
    """
    try:
        # 4. Use Case 입력 모델로 변환
        command = PlaceOrderCommand(
            customer_email=request.customer_email,
            customer_address=request.customer_address,
            product_price=request.product_price,
            affiliate_code=request.affiliate_code
        )

        # 5. Use Case 호출
        order_id = place_order.place_order(command)

        # 6-7. HTTP 응답 반환
        return OrderResponse(
            order_id=order_id.value,
            status="success",
            message="Order placed successfully"
        )

    except ValueError as e:
        # 입력 검증 실패
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except InvalidAddressError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid address: {e.address}"
        )
    except PaymentFailedError as e:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=e.message
        )
    except Exception as e:
        # 예상치 못한 오류
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

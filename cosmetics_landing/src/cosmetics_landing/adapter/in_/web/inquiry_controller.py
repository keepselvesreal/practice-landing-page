"""
Inquiry Controller (입력 어댑터)
"""
from fastapi import APIRouter, status, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field

from cosmetics_landing.application.port.in_.send_inquiry_use_case import (
    SendInquiryUseCase,
    SendInquiryCommand
)


router = APIRouter(prefix="/api/inquiries", tags=["inquiries"])


class SendInquiryRequest(BaseModel):
    """문의 전송 요청 DTO"""
    customer_email: EmailStr = Field(..., description="고객 이메일")
    message: str = Field(..., min_length=1, description="문의 내용")


class SendInquiryResponse(BaseModel):
    """문의 전송 응답 DTO"""
    status: str
    inquiry_id: int


def get_send_inquiry_use_case_dependency():
    """의존성 주입 함수"""
    from cosmetics_landing.config.dependencies import override_send_inquiry_use_case
    return override_send_inquiry_use_case()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=SendInquiryResponse)
async def send_inquiry(
    request: SendInquiryRequest,
    send_inquiry_use_case: SendInquiryUseCase = Depends(get_send_inquiry_use_case_dependency)
):
    """
    고객 문의 전송 API

    Args:
        request: 문의 전송 요청
        send_inquiry_use_case: 문의 전송 유스케이스 (DI)

    Returns:
        SendInquiryResponse: 전송 성공 응답
    """
    try:
        command = SendInquiryCommand(
            customer_email=request.customer_email,
            message=request.message
        )

        result = send_inquiry_use_case.send_inquiry(command)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send inquiry email"
            )

        return SendInquiryResponse(
            status="success",
            inquiry_id=1  # 임시 ID (추후 데이터베이스 연동 시 실제 ID)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

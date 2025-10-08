"""
Dependency Injection Configuration
Chapter 9: Assembling the Application (Java Config 방식)

비판적 검토 반영: 모든 필요한 팩토리 함수 완성
"""
from functools import lru_cache

# Application Services
from ..application.service.place_order_service import PlaceOrderService
from ..application.service.track_affiliate_service import TrackAffiliateService
from ..application.service.get_affiliate_stats_service import GetAffiliateStatsService

# Adapters
from ..adapter.out.persistence.in_memory_order_adapter import InMemoryOrderAdapter
from ..adapter.out.persistence.in_memory_affiliate_adapter import InMemoryAffiliateAdapter
from ..adapter.out.payment.fake_payment_adapter import FakePaymentAdapter
from ..adapter.out.geocoding.fake_address_validator import FakeAddressValidator


# =============================================================================
# Adapter Beans (Singleton)
# =============================================================================

@lru_cache()
def get_order_persistence_adapter() -> InMemoryOrderAdapter:
    """
    Order Persistence Adapter Bean

    Walking Skeleton: In-Memory 구현
    추후 SQLAlchemy 어댑터로 교체 가능
    """
    return InMemoryOrderAdapter()


@lru_cache()
def get_affiliate_persistence_adapter() -> InMemoryAffiliateAdapter:
    """
    Affiliate Persistence Adapter Bean (비판적 검토: 누락 함수 추가)

    Walking Skeleton: In-Memory 구현
    추후 SQLAlchemy 어댑터로 교체 가능
    """
    return InMemoryAffiliateAdapter()


@lru_cache()
def get_payment_adapter() -> FakePaymentAdapter:
    """
    Payment Adapter Bean

    Walking Skeleton: Fake 구현
    추후 PayPalAdapter로 교체 가능
    """
    return FakePaymentAdapter(always_succeed=True)


@lru_cache()
def get_address_validator() -> FakeAddressValidator:
    """
    Address Validator Bean (비판적 검토: 누락 함수 추가)

    Walking Skeleton: Fake 구현
    추후 GooglePlacesAdapter로 교체 가능
    """
    return FakeAddressValidator()


# =============================================================================
# Use Case Beans
# =============================================================================

@lru_cache()
def get_place_order_service() -> PlaceOrderService:
    """
    Place Order Service Bean

    Chapter 9: 명시적 의존성 주입
    비판적 검토: 모든 의존성 명시적으로 주입
    """
    return PlaceOrderService(
        save_order_port=get_order_persistence_adapter(),
        process_payment_port=get_payment_adapter(),
        validate_address_port=get_address_validator()
    )


@lru_cache()
def get_track_affiliate_service() -> TrackAffiliateService:
    """Track Affiliate Service Bean (Command)"""
    return TrackAffiliateService(
        load_affiliate_port=get_affiliate_persistence_adapter(),
        save_affiliate_port=get_affiliate_persistence_adapter()
    )


@lru_cache()
def get_affiliate_stats_service() -> GetAffiliateStatsService:
    """Get Affiliate Stats Service Bean (Query)"""
    return GetAffiliateStatsService(
        load_affiliate_port=get_affiliate_persistence_adapter()
    )


# =============================================================================
# FastAPI Dependency Override
# =============================================================================

def override_place_order_use_case():
    """
    FastAPI Depends용 PlaceOrderUseCase 제공

    Chapter 5: Web Adapter와 Application Layer 연결
    """
    return get_place_order_service()


def override_track_affiliate_use_case():
    """FastAPI Depends용 TrackAffiliateClickUseCase 제공"""
    return get_track_affiliate_service()


def override_affiliate_stats_query():
    """FastAPI Depends용 GetAffiliateStatsQuery 제공"""
    return get_affiliate_stats_service()

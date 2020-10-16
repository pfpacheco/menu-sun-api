from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform


class AbstractOrderStatusPlatform(AbstractPlatform):
    seller_id: int = None
    seller_code: str = None
    order_id: str = None
    seller_order_id: str = None
    status_id: int = None
    status: str = None
    created_at: str = None
    integration_type: str = None
    comments: str = None

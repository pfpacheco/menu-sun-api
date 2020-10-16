from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform


class AbstractOrderStatusNotificationPlatform(AbstractPlatform):
    integration_type: str = None
    order_id: str = None
    seller_id: str = None
    seller_code: str = None

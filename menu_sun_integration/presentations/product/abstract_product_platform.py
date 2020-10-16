from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform
from menu_sun_integration.presentations.seller.abstract_seller_platform import AbstractSellerPlatform


class AbstractProductPlatform(AbstractSellerPlatform, AbstractPlatform):
    sku: str = None
    integration_type: str = None
    seller_code: int = None

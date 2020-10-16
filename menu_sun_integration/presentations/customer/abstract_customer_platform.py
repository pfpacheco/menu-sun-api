from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform
from menu_sun_integration.presentations.metafield.abstract_metafield_platform import AbstractMetafieldPlatform
from menu_sun_integration.presentations.seller.abstract_seller_platform import AbstractSellerPlatform


class AbstractCustomerPaymentTermPlatform(AbstractPlatform):
    deadline: str = None
    description: str = None
    payment_type: str = None


class AbstractCustomerPlatform(AbstractSellerPlatform, AbstractPlatform):
    document: str = None
    payment_terms: [AbstractCustomerPaymentTermPlatform] = None
    customer_metafields: [AbstractMetafieldPlatform] = []

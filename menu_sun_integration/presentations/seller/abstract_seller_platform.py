from menu_sun_integration.presentations.interfaces.abstract_message_platform import AbstractMessagePlatform
from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform
from menu_sun_integration.presentations.metafield.abstract_metafield_platform import AbstractMetafieldPlatform


class AbstractSellerPlatform(AbstractPlatform):
    seller_id: str = None
    seller_code: str = None
    integration_type: str = None
    seller_metafields: [AbstractMetafieldPlatform] = []


class AbstractSellerMessagePlatform(AbstractMessagePlatform):
    identifier: str
    body: AbstractSellerPlatform

    def __init__(self, identifier: str, body: AbstractSellerPlatform):
        self.identifier = identifier
        self.body = body

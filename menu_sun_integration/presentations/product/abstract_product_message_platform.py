from menu_sun_integration.presentations.product.abstract_product_platform import AbstractProductPlatform
from menu_sun_integration.presentations.interfaces.abstract_message_platform import AbstractMessagePlatform


class AbstractProductMessagePlatform(AbstractMessagePlatform):
    identifier: str
    body: AbstractProductPlatform

    def __init__(self, identifier: str, body: AbstractProductPlatform):
        self.identifier = identifier
        self.body = body

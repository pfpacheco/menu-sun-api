from menu_sun_integration.presentations.interfaces.abstract_message_platform import AbstractMessagePlatform
from menu_sun_integration.presentations.order.abstract_order_platform import AbstractOrderPlatform


class AbstractOrderMessagePlatform(AbstractMessagePlatform):
    identifier: str
    body: AbstractOrderPlatform

    def __init__(self, identifier: str, body: AbstractOrderPlatform):
        self.identifier = identifier
        self.body = body

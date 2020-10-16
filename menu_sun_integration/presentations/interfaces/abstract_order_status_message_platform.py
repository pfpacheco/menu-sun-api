from menu_sun_integration.presentations.interfaces.abstract_message_platform import AbstractMessagePlatform
from menu_sun_integration.presentations.order.abstract_order_platform import AbstractOrderPlatform
from menu_sun_integration.presentations.order.abstract_order_status_platform import \
    AbstractOrderStatusPlatform


class AbstractOrderStatusMessagePlatform(AbstractMessagePlatform):
    identifier: str
    body: AbstractOrderPlatform

    def __init__(self, identifier: str, body: AbstractOrderStatusPlatform):
        self.identifier = identifier
        self.body = body

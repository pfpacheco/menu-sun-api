from menu_sun_integration.presentations.interfaces.abstract_message_platform import AbstractMessagePlatform
from menu_sun_integration.presentations.order.abstract_order_platform import AbstractOrderPlatform
from menu_sun_integration.presentations.order.abstract_order_status_notification_platform import \
    AbstractOrderStatusNotificationPlatform


class AbstractOrderStatusNotificationMessagePlatform(AbstractMessagePlatform):
    identifier: str
    body: AbstractOrderPlatform

    def __init__(self, identifier: str, body: AbstractOrderStatusNotificationPlatform):
        self.identifier = identifier
        self.body = body

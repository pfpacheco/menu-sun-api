from menu_sun_integration.presentations.interfaces.abstract_order_status_message_platform import \
    AbstractOrderStatusMessagePlatform
from menu_sun_integration.presentations.order.abstract_order_status_platform import AbstractOrderStatusPlatform


class OrderStatusDetailSQSPlatform(AbstractOrderStatusPlatform):
    pass


class OrderStatusSQSPlatform(AbstractOrderStatusPlatform):
    pass


class OrderStatusSQSMessagePlatform(AbstractOrderStatusMessagePlatform):
    def __init__(self, receipt_handle: str, body: OrderStatusDetailSQSPlatform):
        super().__init__(receipt_handle, body)

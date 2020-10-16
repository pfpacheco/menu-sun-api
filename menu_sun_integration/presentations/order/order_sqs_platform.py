from menu_sun_integration.presentations.interfaces.abstract_order_message_platform import AbstractOrderMessagePlatform
from menu_sun_integration.presentations.order.abstract_order_platform import AbstractOrderItemPlatform, \
    AbstractOrderPlatform, AbstractOrderAddressPlatform, AbstractOrderCustomerPlatform, AbstractOrderStatusPlatform


class OrderItemDetailSQSPlatform(AbstractOrderItemPlatform):
    pass


class OrderDetailSQSPlatform(AbstractOrderPlatform):
    pass


class OrderCustomerSQSPlatform(AbstractOrderCustomerPlatform):
    pass


class OrderStatusSQSPlatform(AbstractOrderStatusPlatform):
    pass


class OrderAddressSQSPlatform(AbstractOrderAddressPlatform):
    pass


class OrderSQSMessagePlatform(AbstractOrderMessagePlatform):
    def __init__(self, receipt_handle: str, body: OrderDetailSQSPlatform):
        super().__init__(receipt_handle, body)

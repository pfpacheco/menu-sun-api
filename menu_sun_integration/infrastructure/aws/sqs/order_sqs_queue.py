import os
import json

from menu_sun_integration.infrastructure.aws.sqs.interfaces.abstract_order_platform_queue import \
    AbstractOrderPlatformQueue
from menu_sun_integration.presentations.order.order_sqs_platform import OrderDetailSQSPlatform, OrderAddressSQSPlatform, \
    OrderCustomerSQSPlatform, OrderStatusSQSPlatform, OrderItemDetailSQSPlatform, OrderSQSMessagePlatform


class OrderSQSQueue(AbstractOrderPlatformQueue):
    def __init__(self, url: str = os.getenv("ORDER_QUEUE_URL")):
        super().__init__(url)

    def map_payload(self, payload):
        receipt_handle = payload.get('ReceiptHandle', {})
        body = json.loads(payload.get('Body', {}))
        order_detail = OrderDetailSQSPlatform.from_dict(body)
        order_detail_items = [OrderItemDetailSQSPlatform.from_dict(item) for item in body.get('items', {})]
        order_detail.items = order_detail_items
        order_detail.shipping_address = OrderAddressSQSPlatform.from_dict(body.get("shipping_address", {}))
        order_detail.billing_address = OrderAddressSQSPlatform.from_dict(body.get("billing_address", {}))
        order_detail.customer = OrderCustomerSQSPlatform.from_dict(body.get("customer", {}))
        order_detail.statuses = [OrderStatusSQSPlatform.from_dict(item) for item in body.get('statuses', {})]

        return OrderSQSMessagePlatform(receipt_handle=receipt_handle, body=order_detail)


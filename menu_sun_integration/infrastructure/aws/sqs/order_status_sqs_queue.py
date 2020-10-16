import os
import json

from menu_sun_integration.infrastructure.aws.sqs.interfaces.abstract_order_status_platform_queue import \
    AbstractOrderStatusPlatformQueue
from menu_sun_integration.presentations.order.order_status_sqs_platform import OrderStatusDetailSQSPlatform, \
    OrderStatusSQSMessagePlatform


class OrderStatusSQSQueue(AbstractOrderStatusPlatformQueue):
    def __init__(self, url: str = os.getenv("ORDER_STATUS_QUEUE_URL")):
        super().__init__(url)

    def map_payload(self, payload):
        receipt_handle = payload.get('ReceiptHandle', {})
        body = json.loads(payload.get('Body', {}))
        order_detail = OrderStatusDetailSQSPlatform.from_dict(body)

        return OrderStatusSQSMessagePlatform(receipt_handle=receipt_handle, body=order_detail)


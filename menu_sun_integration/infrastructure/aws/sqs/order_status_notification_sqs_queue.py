import os
import json

from menu_sun_integration.infrastructure.aws.sqs.interfaces.abstract_order_status_notification_platform_queue import \
    AbstractOrderStatusNotificationPlatformQueue
from menu_sun_integration.presentations.order.order_sqs_platform import OrderDetailSQSPlatform, \
     OrderStatusSQSPlatform, OrderSQSMessagePlatform


class OrderStatusNotificationSQSQueue(AbstractOrderStatusNotificationPlatformQueue):
    def __init__(self, url: str = os.getenv("ORDER_STATUS_NOTIFICATION_QUEUE_URL")):
        super().__init__(url)

    def map_payload(self, payload):
        receipt_handle = payload.get('ReceiptHandle', {})
        body = json.loads(payload.get('Body', {}))
        order_detail = OrderDetailSQSPlatform.from_dict(body)
        order_detail.statuses = [OrderStatusSQSPlatform.from_dict(item) for item in body.get('statuses', {})]

        return OrderSQSMessagePlatform(receipt_handle=receipt_handle, body=order_detail)


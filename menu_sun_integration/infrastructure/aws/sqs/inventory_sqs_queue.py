import json
import os

from menu_sun_integration.infrastructure.aws.sqs.interfaces.abstract_inventory_platform_queue import \
    AbstractInventoryPlatformQueue
from menu_sun_integration.presentations.metafield.metafield_sql_platform import MetafieldSQSPlatform
from menu_sun_integration.presentations.product.abstract_product_message_platform import AbstractProductMessagePlatform
from menu_sun_integration.presentations.product.product_sqs_platform import ProductDetailSQSPlatform, \
    ProductSQSMessagePlatform


class InventorySQSQueue(AbstractInventoryPlatformQueue):
    def __init__(self, url: str = os.getenv("INVENTORY_BY_SKU_QUEUE_URL")):
        super().__init__(url=url)

    def map_payload(self, payload) -> AbstractProductMessagePlatform:
        receipt_handle = payload.get('ReceiptHandle', {})
        body = json.loads(payload.get('Body', {}))

        product_detail = ProductDetailSQSPlatform.from_dict(body)
        seller_metafield = [MetafieldSQSPlatform.from_dict(item) for item in body.get('seller_metafields', {})]
        product_detail.seller_metafields = seller_metafield

        return ProductSQSMessagePlatform(receipt_handle=receipt_handle, body=product_detail)

import json
import os

from menu_sun_integration.infrastructure.aws.sqs.interfaces.abstract_product_platform_queue import \
    AbstractProductPlatformQueue
from menu_sun_integration.presentations.metafield.metafield_sql_platform import MetafieldSQSPlatform
from menu_sun_integration.presentations.seller.abstract_seller_platform import AbstractSellerMessagePlatform
from menu_sun_integration.presentations.seller.seller_sqs_platform import SellerDetailSQSPlatform, \
    SellerSQSMessagePlatform


class ProductSQSQueue(AbstractProductPlatformQueue):
    def __init__(self, url: str = os.getenv("PRODUCT_QUEUE_URL")):
        super().__init__(url=url)

    def map_payload(self, payload) -> AbstractSellerMessagePlatform:
        receipt_handle = payload.get('ReceiptHandle', {})
        body = json.loads(payload.get('Body', {}))

        seller_detail = SellerDetailSQSPlatform.from_dict(body)
        seller_metafield = [MetafieldSQSPlatform.from_dict(item) for item in body.get('seller_metafields', {})]
        seller_detail.seller_metafields = seller_metafield

        return SellerSQSMessagePlatform(receipt_handle=receipt_handle, body=seller_detail)

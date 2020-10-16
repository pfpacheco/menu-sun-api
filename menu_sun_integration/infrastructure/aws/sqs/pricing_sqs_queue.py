import json
import os

from menu_sun_integration.infrastructure.aws.sqs.interfaces.abstract_pricing_platform_queue import \
    AbstractPricingPlatformQueue
from menu_sun_integration.presentations.customer.abstract_customer_message_platform import \
    AbstractCustomerMessagePlatform
from menu_sun_integration.presentations.customer.customer_sqs_platform import CustomerDetailSQSPlatform, \
    CustomerPaymentTermSQSPlatform, CustomerSQSMessagePlatform
from menu_sun_integration.presentations.product.product_sqs_platform import ProductDetailSQSPlatform

from menu_sun_integration.presentations.metafield.metafield_sql_platform import MetafieldSQSPlatform


class PricingSQSQueue(AbstractPricingPlatformQueue):
    def __init__(self, url: str = os.getenv("PRICING_QUEUE_URL")):
        super().__init__(url=url)

    def map_payload(self, payload) -> AbstractCustomerMessagePlatform:
        receipt_handle = payload.get('ReceiptHandle', {})
        body = json.loads(payload.get('Body', {}))
        customer_detail = CustomerDetailSQSPlatform.from_dict(body)
        product_detail = ProductDetailSQSPlatform.from_dict(body)
        customer_metafield = [MetafieldSQSPlatform.from_dict(item) for item in body.get('customer_metafields', {})]
        seller_metafield = [MetafieldSQSPlatform.from_dict(item) for item in body.get('seller_metafields', {})]
        payment_terms = [CustomerPaymentTermSQSPlatform.from_dict(item) for item in body.get('payment_terms', {})]
        customer_detail.customer_metafields = customer_metafield
        customer_detail.product = product_detail
        customer_detail.seller_metafields = seller_metafield
        customer_detail.payment_terms = payment_terms

        return CustomerSQSMessagePlatform(receipt_handle=receipt_handle, body=customer_detail)

from menu_sun_integration.presentations.product.abstract_product_message_platform import \
    AbstractProductMessagePlatform
from menu_sun_integration.presentations.product.abstract_product_platform import AbstractProductPlatform


class ProductDetailSQSPlatform(AbstractProductPlatform):
    pass


class ProductSQSMessagePlatform(AbstractProductMessagePlatform):
    def __init__(self, receipt_handle: str, body: ProductDetailSQSPlatform):
        super().__init__(receipt_handle, body)

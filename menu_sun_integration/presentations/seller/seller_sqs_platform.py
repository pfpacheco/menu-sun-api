
from menu_sun_integration.presentations.seller.abstract_seller_platform import AbstractSellerPlatform, \
    AbstractSellerMessagePlatform


class SellerDetailSQSPlatform(AbstractSellerPlatform):
    pass


class SellerSQSMessagePlatform(AbstractSellerMessagePlatform):
    def __init__(self, receipt_handle: str, body: SellerDetailSQSPlatform):
        super().__init__(receipt_handle, body)

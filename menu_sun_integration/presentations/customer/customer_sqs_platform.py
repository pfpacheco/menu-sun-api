from menu_sun_integration.presentations.customer.abstract_customer_message_platform import \
    AbstractCustomerMessagePlatform
from menu_sun_integration.presentations.customer.abstract_customer_platform import AbstractCustomerPlatform, \
    AbstractCustomerPaymentTermPlatform


class CustomerPaymentTermSQSPlatform(AbstractCustomerPaymentTermPlatform):
    pass


class CustomerDetailSQSPlatform(AbstractCustomerPlatform):
    pass


class CustomerSQSMessagePlatform(AbstractCustomerMessagePlatform):
    def __init__(self, receipt_handle: str, body: CustomerDetailSQSPlatform):
        super().__init__(receipt_handle, body)

from menu_sun_integration.presentations.customer.abstract_customer_platform import AbstractCustomerPlatform
from menu_sun_integration.presentations.interfaces.abstract_message_platform import AbstractMessagePlatform


class AbstractCustomerMessagePlatform(AbstractMessagePlatform):
    identifier: str
    body: AbstractCustomerPlatform

    def __init__(self, identifier: str, body: AbstractCustomerPlatform):
        self.identifier = identifier
        self.body = body

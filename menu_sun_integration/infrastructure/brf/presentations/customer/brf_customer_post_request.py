from menu_sun_integration.presentations.customer.abstract_customer_post_request import AbstractCustomerPostRequest


def get_attr(attr: object, default_value: object) -> object:
    if attr is None:
        return default_value
    else:
        return attr


class BRFCustomerPostRequest(AbstractCustomerPostRequest):
    def __init__(self, state_code: str, postal_code: str, email: str, document: str, phone_number: str):
        super().__init__(document, email)
        self.state_code = state_code
        self.postal_code = postal_code
        self.phone_number = phone_number

    @property
    def payload(self) -> str:
        return '{"document": "%s", "stateCode": "%s", "postalCode": "%s", "email": "%s", "phoneNumber": "%s"}' % (
            self.document,
            self.state_code,
            self.postal_code,
            self.email,
            self.phone_number)

    @property
    def resource(self) -> str:
        return "clients/v1/Client/"

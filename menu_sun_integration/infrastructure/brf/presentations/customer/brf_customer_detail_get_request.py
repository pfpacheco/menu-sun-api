from menu_sun_integration.presentations.customer.abstract_customer_detail_get_request import \
    AbstractCustomerDetailGetRequest


class BRFCustomerDetailGetRequest(AbstractCustomerDetailGetRequest):
    def __init__(self, cnpj: str, postal_code:str):
        super().__init__(cnpj)
        self.postal_code = postal_code

    @property
    def payload(self):
        return f"clients/v1/Client/?document={self._document}&CEP={self.postal_code}"

from menu_sun_integration.presentations.pricing.customer.abstract_customer_pricing_detail_get_request import \
    AbstractCustomerPricingDetailGetRequest


class BRFCustomerPricingDetailGetRequest(AbstractCustomerPricingDetailGetRequest):
    def __init__(self, document: str, postal_code: str):
        super().__init__(document=document)
        self.postal_code = postal_code

    @property
    def payload(self):
        return f"prices/v1/Pricing?Document={self.document}&PostalCode={self.postal_code}"


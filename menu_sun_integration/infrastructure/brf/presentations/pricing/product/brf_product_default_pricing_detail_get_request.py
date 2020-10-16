from menu_sun_integration.presentations.pricing.product.abstract_product_default_pricing_detail_get_request import \
    AbstractProductDefaultPricingDetailGetRequest


class BRFProductDefaultPricingDetailGetRequest(AbstractProductDefaultPricingDetailGetRequest):
    def __init__(self, document: str, postal_code: str):
        self.document = document
        self.postal_code = postal_code

    @property
    def payload(self):
        return f"prices/v1/Pricing?Document={self.document}&PostalCode={self.postal_code}"




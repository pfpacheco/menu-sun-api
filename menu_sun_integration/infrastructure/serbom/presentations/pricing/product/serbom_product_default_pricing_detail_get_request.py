from menu_sun_integration.presentations.pricing.product.abstract_product_default_pricing_detail_get_request import \
    AbstractProductDefaultPricingDetailGetRequest


class SerbomProductDefaultPricingDetailGetRequest(AbstractProductDefaultPricingDetailGetRequest):
    def __init__(self):
        super().__init__()

    @property
    def payload(self):
        return "prices.csv"

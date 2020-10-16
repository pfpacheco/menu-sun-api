from menu_sun_integration.presentations.product.abstract_product_get_request import AbstractProductGetRequest


class SerbomProductGetRequest(AbstractProductGetRequest):

    def __init__(self):
        super().__init__()

    def payload(self):
        return "products.csv"

from menu_sun_integration.presentations.product.abstract_product_get_request import AbstractProductGetRequest


class BRFProductGetRequest(AbstractProductGetRequest):
    @property
    def payload(self):
        payload = "products/v1/product"

        self._logger.info(
            key="products_get_request",
            description="payload",
            payload=payload)

        return payload

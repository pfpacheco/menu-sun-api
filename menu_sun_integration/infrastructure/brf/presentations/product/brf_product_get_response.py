from typing import Dict

from menu_sun_integration.infrastructure.brf.presentations.product.brf_product_response import BRFProductResponse
from menu_sun_integration.presentations.product.abstract_product_get_response import AbstractProductGetResponse


class BRFProductGetResponse(AbstractProductGetResponse):
    def __init__(self, payload: Dict):
        super().__init__(payload=payload)

    @property
    def succeeded(self) -> bool:
        result = False
        try:
            result = (len(self.payload) > 0)
        except Exception:
            result = False
        finally:
            if result:
                self._logger.info(
                    key="products_get_response",
                    description="products_found",
                    payload=self._logger.dumps(self.payload))
            else:
                self._logger.error(
                    key="products_get_response",
                    description="products_not_found",
                    payload=self._logger.dumps(self.payload))

        return result

    def get_products(self) -> [BRFProductResponse]:
        products_response = self.payload
        products = list(map(lambda product: BRFProductResponse(payload=product),
                            products_response))

        return products

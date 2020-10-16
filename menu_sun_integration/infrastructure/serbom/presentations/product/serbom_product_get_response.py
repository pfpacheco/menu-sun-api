from typing import Dict

from menu_sun_integration.infrastructure.serbom.presentations.product.serbom_product_response \
    import SerbomProductResponse
from menu_sun_integration.presentations.product.abstract_product_get_response import AbstractProductGetResponse


class SerbomProductGetResponse(AbstractProductGetResponse):
    """ This is the concrete class Serbom Product Get Response """

    def succeeded(self) -> bool:
        result = False
        try:
            result = len(self.payload) >= 1
        except Exception:
            result = False
        finally:
            if result:
                self._logger.info(
                    key="product_get_response",
                    description="product_found",
                    payload=self._logger.dumps(self.payload)
                )
            else:
                self._logger.error(
                    key="product_get_response",
                    description="product_not_found",
                    payload=self._logger.dumps(self.payload)
                )
        return result

    def get_products(self) -> [SerbomProductResponse]:
        products_response = self.payload
        products = list(map(lambda product: SerbomProductResponse(payload=product),
                            products_response))
        return products

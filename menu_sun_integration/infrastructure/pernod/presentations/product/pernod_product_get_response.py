from typing import Dict

from menu_sun_integration.infrastructure.pernod.presentations.product.pernod_product_response import \
    PernodProductResponse
from menu_sun_integration.presentations.product.abstract_product_get_response import AbstractProductGetResponse


class PernodProductGetResponse(AbstractProductGetResponse):
    def __init__(self, payload: Dict):
        super().__init__(payload=payload)

    @property
    def succeeded(self) -> bool:
        result = False
        try:
            result = "error" not in self.payload and len(self.payload["products"]) > 0
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

    def get_products(self) -> [PernodProductResponse]:
        products_response = self.payload["products"]
        products = list(map(lambda product: PernodProductResponse(payload=product),
                            products_response))

        return products

from typing import Dict

from menu_sun_integration.presentations.product.abstract_product_response import AbstractProductResponse


class BRFProductResponse(AbstractProductResponse):
    def __init__(self, payload: Dict):
        super().__init__(payload)

        self._logger.info(
            entity_id=self.sku,
            key="product_response",
            description="payload",
            payload=self._logger.dumps(payload))

    @property
    def sku(self) -> str:
        return self.payload.get("sku", "")

    @property
    def name(self) -> str:
        return self.payload.get("productName", "")

    @property
    def weight(self) -> float:
        return self.payload.get("sallesWeight", 0.0)

    @property
    def ean(self) -> str:
        return self.payload.get("ean", "")

    @property
    def description(self) -> str:
        return self.payload.get("description", "")

    @property
    def brand(self) -> str:
        return self.payload.get("category", "")

    @property
    def active(self) -> bool:
        return self.payload.get("skuActive", True)

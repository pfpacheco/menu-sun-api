from typing import Dict

from menu_sun_integration.presentations.product.abstract_product_response import AbstractProductResponse


class PernodProductResponse(AbstractProductResponse):
    def __init__(self, payload: Dict):
        super().__init__(payload)

    @property
    def sku(self) -> str:
        return self.payload.get("sku", "")

    @property
    def name(self) -> str:
        return self.payload.get("name", "")

    @property
    def ean(self) -> str:
        return self.payload.get("ean13", "")

    @property
    def description(self) -> str:
        return self.payload.get("description", "")

    @property
    def brand(self) -> str:
        return self.payload.get("brand", "")

    @property
    def height(self) -> float:
        return self.payload.get("height", 0.0)

    @property
    def width(self) -> float:
        return self.payload.get("width", 0.0)

    @property
    def weight(self) -> float:
        return self.payload.get("weightKg", 0.0)

    @property
    def length(self) -> float:
        return self.payload.get("length", 0.0)

    @property
    def active(self) -> bool:
        return self.payload.get("status", "") == "Synchronized"

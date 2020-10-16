from typing import Dict
from menu_sun_integration.presentations.product.abstract_product_response import AbstractProductResponse


class SerbomProductResponse(AbstractProductResponse):
    """ This is the Serbom Procuct Response class """

    def __init__(self, payload: Dict):
        super().__init__(payload=payload)

    @property
    def sku(self) -> str:
        return self.payload.get("sku", "")

    @property
    def name(self) -> str:
        return self.payload.get("name", "")

    @property
    def ncm(self) -> str:
        return self.payload.get("ncm", "")

    @property
    def status(self) -> str:
        return self.payload.get("status", "")

    @property
    def inventory(self) -> str:
        return self.payload.get("inventory", "")

    @property
    def cost(self) -> float:
        return float(self.payload.get("cost", "0,00").replace(",", "."))

    @property
    def height(self) -> float:
        return float(self.payload.get("height", "0,00").replace(",", "."))

    @property
    def length(self) -> float:
        return float(self.payload.get("height", "0,00").replace(",", "."))

    @property
    def width(self) -> float:
        return float(self.payload.get("width", "0,00").replace(",", "."))

    @property
    def status(self) -> str:
        return self.payload.get("status", "")

    @property
    def weight(self) -> float:
        return float(self.payload.get("weight", "0,00").replace(",", "."))

    @property
    def ean(self) -> str:
        return self.payload.get("ean", "")

    @property
    def description(self) -> str:
        return self.payload.get("description", "")

    @property
    def brand(self) -> str:
        return self.payload.get("brand", "")

    @property
    def active(self) -> bool:
        return bool(self.payload.get("active", ""))

    @property
    def list_price(self) -> float:
        return float(self.payload.get("list_price", "0,00").replace(",", "."))

    @property
    def sale_price(self) -> float:
        return float(self.payload.get("sale_price", "0,00").replace(",", "."))

    @property
    def promo_price(self) -> float:
        return float(self.payload.get("promo_price", "0,00").replace(",", "."))

from typing import Dict

from menu_sun_integration.presentations.pricing.abstract_pricing_response import AbstractPricingResponse


class SerbomPricingResponse(AbstractPricingResponse):
    def __init__(self, payload: Dict):
        super().__init__(payload=payload)

    @property
    def document(self) -> str:
        raise NotImplementedError

    @property
    def zip_code(self) -> str:
        raise NotImplementedError

    @property
    def sku(self) -> str:
        return self.payload.get("sku", "")

    @property
    def list_price(self) -> float:
        return float(self.payload.get("price", "0,00").replace(",", "."))

    @property
    def sale_price(self) -> float:
        return float(self.payload.get("price", "0,00").replace(",", "."))

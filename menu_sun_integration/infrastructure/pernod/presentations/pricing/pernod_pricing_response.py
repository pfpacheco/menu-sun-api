from typing import Dict

from menu_sun_integration.presentations.pricing.abstract_pricing_response import AbstractPricingResponse


class PernodPricingResponse(AbstractPricingResponse):
    def __init__(self, payload: Dict):
        super().__init__(payload=payload)

    @property
    def sku(self) -> str:
        return self.payload.get("destinationSku", "")

    @property
    def list_price(self) -> float:
        return self.payload.get("priceSale", 0)

    @property
    def sale_price(self) -> float:
        return self.payload.get("priceBase", 0)

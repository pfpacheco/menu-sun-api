from typing import Dict

from menu_sun_integration.presentations.inventory.abstract_inventory_response import AbstractInventoryResponse


class PernodInventoryResponse(AbstractInventoryResponse):
    def __init__(self, payload: Dict):
        super().__init__(payload)
        self.payload = payload

    @property
    def sku(self) -> str:
        return self.payload.get("destinationSku", "")

    @property
    def list_price(self) -> float:
        return self.payload.get("priceBase", "")

    @property
    def sale_price(self) -> float:
        return self.payload.get("priceSale", "")

    @property
    def inventory(self) -> int:
        return self.payload.get("availablestock", 0)

from typing import Dict

from menu_sun_integration.presentations.inventory.abstract_inventory_response import AbstractInventoryResponse


class BRFInventoryResponse(AbstractInventoryResponse):
    def __init__(self, payload: Dict):
        super().__init__(payload)

        self._logger.info(
            key="inventory_response",
            description="payload",
            payload=self._logger.dumps(payload))

        self._logger.info(
            key="inventory_response",
            description="inventory",
            payload=self)

    @property
    def sku(self) -> str:
        return self.payload.get("sku", "")

    @property
    def inventory(self) -> int:
        inventory: float = float(self.payload.get("stockCx", 0.0))
        return int(inventory)

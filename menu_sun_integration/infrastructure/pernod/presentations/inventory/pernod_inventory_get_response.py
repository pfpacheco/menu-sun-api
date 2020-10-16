from typing import Dict

from menu_sun_integration.infrastructure.pernod.presentations.inventory.pernod_inventory_response import \
    PernodInventoryResponse
from menu_sun_integration.presentations.inventory.abstract_inventory_get_response import AbstractInventoryGetResponse


class PernodInventoryGetResponse(AbstractInventoryGetResponse):
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
                    key="inventory_get_response",
                    description="inventory_found",
                    payload=self._logger.dumps(self.payload))
            else:
                self._logger.error(
                    key="inventory_get_response",
                    description="inventory_not_found",
                    payload=self._logger.dumps(self.payload))

        return result

    def get_inventories(self) -> [PernodInventoryResponse]:
        inventories_response = self.payload["itens"]
        products = list(map(lambda inventory: PernodInventoryResponse(payload=inventory),
                            inventories_response))

        return products

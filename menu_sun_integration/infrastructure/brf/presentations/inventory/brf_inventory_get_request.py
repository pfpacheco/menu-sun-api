from menu_sun_integration.presentations.inventory.abstract_inventory_get_request import AbstractInventoryGetRequest


class BRFInventoryGetRequest(AbstractInventoryGetRequest):
    def __init__(self, postal_code: str):
        self._postal_code = postal_code

    @property
    def payload(self):
        payload = f'stock/v1/stock?postalCode={self._postal_code}'

        self._logger.info(
            key="inventory_get_request",
            description="payload",
            payload=payload)

        return payload

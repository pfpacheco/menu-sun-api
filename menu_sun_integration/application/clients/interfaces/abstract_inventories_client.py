import abc

from menu_sun_integration.application.clients.interfaces.abstract_client import AbstractClient
from menu_sun_integration.presentations.inventory.abstract_inventory_get_request import AbstractInventoryGetRequest
from menu_sun_integration.presentations.inventory.abstract_inventory_get_response import AbstractInventoryGetResponse


class AbstractInventoriesClient(AbstractClient):
    @abc.abstractmethod
    def get_inventories(self, request: AbstractInventoryGetRequest) -> AbstractInventoryGetResponse:
        raise NotImplementedError

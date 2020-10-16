import abc


from menu_sun_integration.application.clients.interfaces.abstract_client import AbstractClient
from menu_sun_integration.presentations.inventory.abstract_inventory_by_sku_post_request import \
    AbstractInventoryBySkuPostRequest
from menu_sun_integration.presentations.inventory.abstract_inventory_get_response import AbstractInventoryGetResponse


class AbstractInventoryBySkuClient(AbstractClient):
    @abc.abstractmethod
    def get_inventory(self, request: AbstractInventoryBySkuPostRequest) -> AbstractInventoryGetResponse:
        raise NotImplemented

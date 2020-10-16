import abc

from menu_sun_integration.application.adapters.inventory_adapter import InventoryAdapter
from menu_sun_integration.application.services.interfaces.abstract_service import AbstractService


class AbstractInventoryService(AbstractService):
    _adapter: InventoryAdapter = None

    @abc.abstractmethod
    def update_inventory_from_seller(self) -> None:
        raise NotImplementedError

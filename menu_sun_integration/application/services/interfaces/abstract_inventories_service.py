import abc

from menu_sun_integration.application.adapters.inventories_adapter import InventoriesAdapter
from menu_sun_integration.application.services.interfaces.abstract_service import AbstractService


class AbstractInventoriesService(AbstractService):
    _adapter: InventoriesAdapter = None

    @abc.abstractmethod
    def update_inventories_from_seller(self) -> None:
        raise NotImplementedError

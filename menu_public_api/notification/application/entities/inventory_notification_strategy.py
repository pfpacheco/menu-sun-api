import abc
from typing import Dict, Optional

from menu_sun_api.domain.model.product.product_repository import ProductRepository


class InventoryStrategyInterface(abc.ABC):
    def __init__(self, product_service: ProductRepository):
        self._service = product_service

    @abc.abstractmethod
    def _translate_entity_notification(self, seller: dict, payload: dict) -> Optional[Dict]:
        pass

    def enqueue_entity(self, seller: dict, payload: dict) -> bool:
        pass

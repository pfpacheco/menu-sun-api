import abc
from typing import Dict, Optional


class OrderStrategyInterface(abc.ABC):

    @abc.abstractmethod
    def _translate_entity_notification(self, seller: dict, payload: dict) -> Optional[Dict]:
        pass

    def enqueue_entity(self, seller: dict, payload: dict) -> bool:
        pass

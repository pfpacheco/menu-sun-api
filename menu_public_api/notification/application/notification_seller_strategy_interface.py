import abc
from typing import Dict, Optional


class NotificationStrategyInterface(abc.ABC):

    @abc.abstractmethod
    def enqueue_notification(self, seller: dict, payload: dict) -> Optional[Dict]:
        pass

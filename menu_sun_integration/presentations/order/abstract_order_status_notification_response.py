import abc
from typing import Dict

from menu_sun_integration.presentations.interfaces.abstract_entity_response import AbstractEntityResponse
from menu_sun_integration.presentations.interfaces.abstract_presentation import AbstractPresentation


class AbstractStatusInfo(AbstractPresentation):
    def __init__(self, code: str, info: str):
        self.code = code
        self.information = info


class AbstractOrderStatusNotificationResponse(AbstractEntityResponse):
    def __init__(self, payload: Dict):
        self.payload = payload

    @property
    @abc.abstractmethod
    def status(self) -> AbstractStatusInfo:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def id(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def seller_order_id(self) -> str:
        raise NotImplementedError

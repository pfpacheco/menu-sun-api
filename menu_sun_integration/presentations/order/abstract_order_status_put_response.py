import abc
from typing import Dict

from menu_sun_integration.presentations.interfaces.abstract_entity_response import AbstractEntityResponse


class AbstractOrderStatusPutResponse(AbstractEntityResponse):
    def __init__(self, payload: Dict):
        self.payload = payload

    @abc.abstractmethod
    def published_date(self):
        raise NotImplementedError

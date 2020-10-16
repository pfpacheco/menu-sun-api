import abc
from typing import Dict, Optional

from menu_sun_integration.presentations.interfaces.abstract_entity_response import AbstractEntityResponse
from menu_sun_integration.presentations.interfaces.abstract_response import AbstractResponse
from menu_sun_integration.presentations.order.abstract_order_response import AbstractOrderResponse


class AbstractOrderPostResponse(AbstractResponse):
    def __init__(self, payload: Dict):
        self.payload = payload

    @abc.abstractmethod
    def succeeded(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get_order(self) -> Optional[AbstractOrderResponse]:
        raise NotImplementedError

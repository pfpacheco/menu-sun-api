import abc
from typing import Dict, Optional

from menu_sun_integration.presentations.interfaces.abstract_response import AbstractResponse
from menu_sun_integration.presentations.order.abstract_order_status_put_response import AbstractOrderStatusPutResponse


class AbstractOrderStatusDetailPutResponse(AbstractResponse):
    def __init__(self, payload: Dict):
        self.payload = payload

    @abc.abstractmethod
    def get_order(self) -> Optional[AbstractOrderStatusPutResponse]:
        raise NotImplementedError

    @abc.abstractmethod
    def succeeded(self) -> bool:
        raise NotImplementedError

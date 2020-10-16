import abc
from typing import Dict

from menu_sun_integration.presentations.interfaces.abstract_response import AbstractResponse
from menu_sun_integration.presentations.pricing.abstract_pricing_response import AbstractPricingResponse


class AbstractPricingDetailGetResponse(AbstractResponse):
    def __init__(self, payload: Dict):
        self.payload = payload

    @abc.abstractmethod
    def succeeded(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get_pricing(self) -> [AbstractPricingResponse]:
        raise NotImplementedError

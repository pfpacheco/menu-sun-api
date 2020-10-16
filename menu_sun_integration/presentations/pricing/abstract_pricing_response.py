import abc

from typing import Dict

from menu_sun_integration.presentations.interfaces.abstract_entity_response import AbstractEntityResponse


class AbstractPricingResponse(AbstractEntityResponse):
    def __init__(self, payload: Dict):
        self.payload = payload

    @property
    @abc.abstractmethod
    def sku(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def sale_price(self) -> float:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def list_price(self) -> float:
        raise NotImplementedError

    def __hash__(self):
        return hash(self.sku)

    def __eq__(self, other):
        if not hasattr(other, 'sku'):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.sku == other.sku


class AbstractPricesResponse(AbstractEntityResponse):
    def __init__(self, payload: Dict):
        self.payload = payload

    @property
    @abc.abstractmethod
    def prices(self) -> [AbstractPricingResponse]:
        raise NotImplementedError

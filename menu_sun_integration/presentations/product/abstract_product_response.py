import abc

from typing import Dict

from menu_sun_integration.presentations.interfaces.abstract_entity_response import AbstractEntityResponse


class AbstractProductResponse(AbstractEntityResponse):
    def __init__(self, payload: Dict):
        self.payload = payload

    @property
    @abc.abstractmethod
    def sku(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def weight(self) -> float:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def ean(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def description(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def brand(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def active(self) -> bool:
        raise NotImplementedError

    def __hash__(self):
        return hash(self.sku)

    def __eq__(self, other):
        if not hasattr(other, 'sku'):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.sku == other.sku


class AbstractProductsResponse(AbstractEntityResponse):
    def __init__(self, payload: Dict):
        self.payload = payload

    @property
    @abc.abstractmethod
    def products(self) -> [AbstractProductResponse]:
        raise NotImplementedError


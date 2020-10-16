import abc

from typing import Dict

from menu_sun_integration.presentations.interfaces.abstract_entity_response import AbstractEntityResponse


class AbstractCustomerPaymentTermsResponse(AbstractEntityResponse):
    def __init__(self, payload: Dict):
        self.payload = payload

    @property
    @abc.abstractmethod
    def deadline(self) -> int:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def description(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def payment_type(self) -> str:
        raise NotImplementedError


class AbstractCustomerResponse(AbstractEntityResponse):
    def __init__(self, payload: Dict):
        self.payload = payload

    @property
    @abc.abstractmethod
    def credit_limit(self) -> float:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def payment_terms(self) -> [AbstractCustomerPaymentTermsResponse]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def active(self) -> bool:
        raise NotImplementedError

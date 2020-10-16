import abc

from menu_sun_integration.presentations.interfaces.abstract_request import AbstractBaseRequestPostAction


class AbstractProductDefaultPricingBySkuPostRequest(AbstractBaseRequestPostAction):
    def __init__(self, sku: str):
        self.sku = sku

    @abc.abstractmethod
    def payload(self):
        raise NotImplementedError

    @abc.abstractmethod
    def resource(self) -> str:
        raise NotImplementedError

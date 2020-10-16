import abc

from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequestPostAction


class AbstractPricingDetailGetRequest(AbstractRequestPostAction):
    def __init__(self, document: str, sku: str):
        self.document = document
        self.sku = sku

    @abc.abstractmethod
    def payload(self):
        raise NotImplementedError

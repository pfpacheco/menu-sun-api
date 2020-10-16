import abc

from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequestPostAction


class AbstractCustomerPricingDetailGetRequest(AbstractRequestPostAction):
    def __init__(self, document: str):
        self.document = document

    @abc.abstractmethod
    def payload(self):
        raise NotImplementedError

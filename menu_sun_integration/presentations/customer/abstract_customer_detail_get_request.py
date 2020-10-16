import abc

from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequestPostAction


class AbstractCustomerDetailGetRequest(AbstractRequestPostAction):
    def __init__(self, cnpj: str = None):
        self._document = cnpj

    @property
    def document(self) -> str:
        return self._document

    @abc.abstractmethod
    def payload(self):
        raise NotImplementedError

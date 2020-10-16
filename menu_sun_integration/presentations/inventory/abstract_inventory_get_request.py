import abc

from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequestPostAction


class AbstractInventoryGetRequest(AbstractRequestPostAction):
    @abc.abstractmethod
    def payload(self):
        raise NotImplementedError

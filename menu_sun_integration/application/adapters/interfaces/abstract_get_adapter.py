import abc

from menu_sun_api.domain import Default
from menu_sun_integration.application.adapters.interfaces.abstract_adapter import AbstractAdapter
from menu_sun_integration.presentations.interfaces.abstract_response import AbstractResponse


class AbstractGetAdapter(AbstractAdapter):
    @abc.abstractmethod
    def get_from_seller(self, entity: Default) -> AbstractResponse:
        raise NotImplementedError


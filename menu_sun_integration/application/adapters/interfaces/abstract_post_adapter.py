import abc

from menu_sun_integration.application.adapters.interfaces.abstract_adapter import AbstractAdapter
from menu_sun_integration.presentations.interfaces.abstract_platform import AbstractPlatform
from menu_sun_integration.presentations.interfaces.abstract_response import AbstractResponse


class AbstractSendAdapter(AbstractAdapter):
    @abc.abstractmethod
    def send_to_seller(self, request: AbstractPlatform) -> AbstractResponse:
        raise NotImplementedError

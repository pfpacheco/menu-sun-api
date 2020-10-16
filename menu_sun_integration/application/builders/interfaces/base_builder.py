import abc

from menu_sun_integration.application.adapters.interfaces.abstract_post_adapter import AbstractAdapter
from menu_sun_integration.application.clients.interfaces.abstract_client import AbstractClient


class BaseBuilder(abc.ABC):
    @abc.abstractmethod
    def __init__(self, client: AbstractClient):
        self._client = client
        self._adapter: AbstractAdapter

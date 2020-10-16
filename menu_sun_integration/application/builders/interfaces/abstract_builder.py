import abc

from menu_sun_integration.application.adapters.interfaces.abstract_post_adapter import AbstractAdapter
from menu_sun_integration.application.clients.interfaces.abstract_client import AbstractClient
from menu_sun_integration.application.translators.interfaces.abstract_translator import AbstractTranslator


class AbstractBuilder(abc.ABC):
    def __init__(self, client: AbstractClient = None, translator: AbstractTranslator = None,
                 adapter: AbstractAdapter = None, session=None):
        self._client = client
        self._translator = translator
        self._adapter = adapter
        self._session = session

    @abc.abstractmethod
    def build_adapter(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def create_client(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def create_session(self, session) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def define_translator(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_adapter(self) -> AbstractAdapter:
        raise NotImplementedError

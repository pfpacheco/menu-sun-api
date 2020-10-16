import abc

from menu_sun_integration.application.adapters.interfaces.abstract_post_adapter import AbstractAdapter
from menu_sun_integration.application.builders.interfaces.abstract_builder import AbstractBuilder
from menu_sun_integration.application.repositories.order_repository import OrderRepository
from menu_sun_integration.infrastructure.ambev.contexts.promax_context_api import PromaxContextAPI
from menu_sun_integration.infrastructure.ambev.promax_client import PromaxClient


class PromaxBaseBuilder(AbstractBuilder):
    def __init__(self):
        super().__init__()
        self.order_repository = OrderRepository(context=PromaxContextAPI())

    def create_client(self) -> None:
        self._client = PromaxClient(order_repository=self.order_repository)

    def create_session(self, session) -> None:
        pass

    def get_adapter(self) -> AbstractAdapter:
        return self._adapter

    @abc.abstractmethod
    def define_translator(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def build_adapter(self) -> None:
        raise NotImplementedError

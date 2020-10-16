import abc

from menu_sun_integration.application.adapters.interfaces.abstract_adapter import AbstractAdapter
from menu_sun_integration.application.builders.interfaces.abstract_builder import AbstractBuilder
from menu_sun_integration.application.repositories.order_repository import OrderRepository
from menu_sun_integration.application.repositories.product_repository import ProductRepository
from menu_sun_integration.infrastructure.serbom.contexts.serbom_price_context_s3 import SerbomPriceS3Context
from menu_sun_integration.infrastructure.serbom.contexts.serbom_context_api import SerbomContextAPI
from menu_sun_integration.infrastructure.serbom.serbom_client import SerbomClient


class AryztaBaseBuilder(AbstractBuilder):
    def __init__(self):
        super().__init__()
        self.context_s3 = SerbomPriceS3Context(bucket="ARYZTA_BUCKET")
        self.serbom_context_api = SerbomContextAPI()
        self.order_repository = OrderRepository(context=self.serbom_context_api)
        self.product_repository = ProductRepository(context=self.context_s3)

    def create_client(self) -> None:
        self._client = SerbomClient(order_repository=self.order_repository, product_repository=self.product_repository)

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

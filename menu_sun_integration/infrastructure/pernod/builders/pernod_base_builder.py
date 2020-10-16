import abc

from menu_sun_api.domain.model.seller.seller_repository import SellerRepository
from menu_sun_integration.application.adapters.interfaces.abstract_post_adapter import AbstractAdapter
from menu_sun_integration.application.builders.interfaces.abstract_builder import AbstractBuilder
from menu_sun_integration.application.repositories.order_repository import OrderRepository
from menu_sun_integration.application.repositories.product_repository import ProductRepository
from menu_sun_integration.infrastructure.pernod.contexts.pernod_context_api import PernodContextAPI
from menu_sun_integration.infrastructure.pernod.contexts.pernod_product_context_api import PernodProductContextAPI
from menu_sun_integration.infrastructure.pernod.pernod_client import PernodClient


class PernodBaseBuilder(AbstractBuilder):
    def __init__(self):
        super().__init__()
        self.product_context_api = PernodProductContextAPI()
        self.context_api = PernodContextAPI(seller_repository=SellerRepository(self._session))

        self.order_repository = OrderRepository(context=self.context_api)
        self.product_repository = ProductRepository(context=self.product_context_api)

    def create_client(self) -> None:
        self._client = PernodClient(order_repository=self.order_repository, product_repository=self.product_repository)

    def create_session(self, session) -> None:
        self._session = session

    def get_adapter(self) -> AbstractAdapter:
        return self._adapter

    @abc.abstractmethod
    def define_translator(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def build_adapter(self) -> None:
        raise NotImplementedError

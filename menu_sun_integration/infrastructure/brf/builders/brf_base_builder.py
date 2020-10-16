import abc

from menu_sun_integration.application.adapters.interfaces.abstract_post_adapter import AbstractAdapter
from menu_sun_integration.application.builders.interfaces.abstract_builder import AbstractBuilder
from menu_sun_integration.application.repositories.customer_repository import CustomerRepository
from menu_sun_integration.application.repositories.order_repository import OrderRepository
from menu_sun_integration.application.repositories.pricing_repository import PricingRepository
from menu_sun_integration.application.repositories.product_repository import ProductRepository
from menu_sun_integration.infrastructure.brf.brf_client import BRFClient
from menu_sun_integration.infrastructure.brf.contexts.brf_context_api import BRFContextAPI


class BRFBaseBuilder(AbstractBuilder):
    def __init__(self):
        super().__init__()
        self.context_api = BRFContextAPI()
        self.customer_repository = CustomerRepository(context=self.context_api)
        self.order_repository = OrderRepository(context=self.context_api)
        self.product_repository = ProductRepository(context=self.context_api)
        self.pricing_repository = PricingRepository(context=self.context_api)

    def create_client(self) -> None:
        self._client = BRFClient(customer_repository=self.customer_repository, order_repository=self.order_repository,
                                 product_repository=self.product_repository, pricing_repository=self.pricing_repository)

    def get_adapter(self) -> AbstractAdapter:
        return self._adapter

    def create_session(self, session) -> None:
        self._session = session

    @abc.abstractmethod
    def define_translator(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def build_adapter(self) -> None:
        raise NotImplementedError

import abc

from menu_sun_integration.application.adapters.customer_adapter import CustomerAdapter
from menu_sun_integration.application.services.interfaces.abstract_service import AbstractService


class AbstractCustomerService(AbstractService):
    _adapter: CustomerAdapter = None

    @abc.abstractmethod
    def update_customer_from_seller(self) -> None:
        raise NotImplementedError

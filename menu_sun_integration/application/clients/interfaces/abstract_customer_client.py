import abc


from menu_sun_integration.application.clients.interfaces.abstract_client import AbstractClient
from menu_sun_integration.presentations.customer.abstract_customer_detail_get_request import \
    AbstractCustomerDetailGetRequest
from menu_sun_integration.presentations.customer.abstract_customer_detail_get_response import \
    AbstractCustomerDetailGetResponse


class AbstractCustomerClient(AbstractClient):
    @abc.abstractmethod
    def get_customer(self, request: AbstractCustomerDetailGetRequest) -> AbstractCustomerDetailGetResponse:
        raise NotImplementedError

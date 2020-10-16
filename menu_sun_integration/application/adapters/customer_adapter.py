from menu_sun_api.domain.model.customer.customer import Customer
from menu_sun_integration.application.adapters.interfaces.abstract_domain_adapter import AbstractDomainAdapter
from menu_sun_integration.application.adapters.interfaces.abstract_get_adapter import AbstractGetAdapter
from menu_sun_integration.application.clients.interfaces.abstract_customer_client import AbstractCustomerClient
from menu_sun_integration.application.translators.interfaces.abstract_customer_translator import \
    AbstractCustomerTranslator
from menu_sun_integration.presentations.customer.abstract_customer_detail_get_response import \
    AbstractCustomerDetailGetResponse
from menu_sun_integration.presentations.customer.abstract_customer_response import AbstractCustomerResponse


class CustomerAdapter(AbstractGetAdapter, AbstractDomainAdapter):
    def __init__(self, client: AbstractCustomerClient, translator: AbstractCustomerTranslator):
        self._client = client
        self._translator = translator

    def get_from_seller(self, customer: Customer) -> AbstractCustomerDetailGetResponse:
        request = self._translator.to_seller_get_format(customer)
        return self._client.get_customer(request)

    def get_domain(self, response: AbstractCustomerResponse) -> Customer:
        return self._translator.to_domain_format(response)







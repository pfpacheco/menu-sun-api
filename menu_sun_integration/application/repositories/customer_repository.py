from typing import Dict

from menu_sun_integration.application.context.ìnterfaces.abstract_get_post_context import AbstractGetPostContext
from menu_sun_integration.application.repositories.interfaces.abstract_customer_repository import \
    AbstractCustomerRepository
from menu_sun_integration.presentations.customer.abstract_customer_detail_get_request import \
    AbstractCustomerDetailGetRequest
from menu_sun_integration.presentations.customer.abstract_customer_post_request import AbstractCustomerPostRequest


class CustomerRepository(AbstractCustomerRepository):
    def __init__(self, context: AbstractGetPostContext):
        self.context = context

    def post(self, request: AbstractCustomerPostRequest) -> Dict:
        return self.context.post(request)

    def get(self, request: AbstractCustomerDetailGetRequest) -> Dict:
        return self.context.get(request)

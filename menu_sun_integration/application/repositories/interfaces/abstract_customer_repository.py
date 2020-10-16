import abc

from typing import Dict

from menu_sun_integration.presentations.customer.abstract_customer_detail_get_request import \
    AbstractCustomerDetailGetRequest
from menu_sun_integration.presentations.customer.abstract_customer_post_request import AbstractCustomerPostRequest


class AbstractCustomerRepository(abc.ABC):
    # TODO: Débito Técnico - Criar um objeto de retorno específico para o post do customer
    @abc.abstractmethod
    def post(self, request: AbstractCustomerPostRequest) -> Dict:
        raise NotImplemented

    @abc.abstractmethod
    def get(self, request: AbstractCustomerDetailGetRequest) -> Dict:
        raise NotImplemented

import abc
from typing import Dict, Optional

from menu_sun_integration.presentations.customer.abstract_customer_response import AbstractCustomerResponse
from menu_sun_integration.presentations.interfaces.abstract_response import AbstractResponse


class AbstractCustomerDetailGetResponse(AbstractResponse):
    def __init__(self, payload: Dict, document: str = None):
        self.document = document
        self.payload = payload

    @abc.abstractmethod
    def get_customer(self) -> Optional[AbstractCustomerResponse]:
        raise NotImplementedError


import abc

from menu_sun_api.domain import Default
from menu_sun_integration.presentations.order.abstract_order_detail_get_request import AbstractOrderDetailGetRequest


class AbstractTranslator(abc.ABC):
    @abc.abstractmethod
    def to_domain_format(self, entity: Default) -> AbstractOrderDetailGetRequest:
        raise NotImplementedError

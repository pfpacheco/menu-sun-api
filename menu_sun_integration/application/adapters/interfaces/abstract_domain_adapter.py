import abc

from menu_sun_integration.application.adapters.interfaces.abstract_adapter import AbstractAdapter
from menu_sun_integration.presentations.interfaces.abstract_entity_response import AbstractEntityResponse
from menu_sun_api.domain import Default


class AbstractDomainAdapter(AbstractAdapter):
    @abc.abstractmethod
    def get_domain(self, response: AbstractEntityResponse) -> Default:
        raise NotImplementedError


import abc

from typing import Dict

from menu_sun_integration.application.context.ìnterfaces.abstract_get_context import AbstractGetContext
from menu_sun_integration.application.context.ìnterfaces.abstract_post_context import AbstractPostContext


class AbstractGetPostContext(AbstractGetContext, AbstractPostContext):
    @abc.abstractmethod
    def get(self, request) -> Dict:
        return {}

    @abc.abstractmethod
    def post(self, request) -> Dict:
        raise NotImplemented

    @abc.abstractmethod
    def put(self, request) -> Dict:
        raise NotImplemented




import abc

from typing import Dict

from menu_sun_integration.application.context.ìnterfaces.abstract_context import AbstractContext


class AbstractPostContext(AbstractContext):
    @abc.abstractmethod
    def post(self, request) -> Dict:
        raise NotImplemented



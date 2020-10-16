import abc

from typing import Dict

from menu_sun_integration.application.context.ìnterfaces.abstract_context import AbstractContext


class AbstractGetContext(AbstractContext):
    @abc.abstractmethod
    def get(self, request) -> Dict:
        raise NotImplemented



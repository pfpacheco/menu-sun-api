import abc

from typing import Dict

from menu_sun_integration.application.context.ìnterfaces.abstract_context import AbstractContext


class AbstractPutContext(AbstractContext):
    @abc.abstractmethod
    def put(self, request) -> Dict:
        raise NotImplemented



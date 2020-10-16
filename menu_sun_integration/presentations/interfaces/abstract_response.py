import abc

from menu_sun_integration.presentations.interfaces.abstract_presentation import AbstractPresentation


class AbstractResponse(AbstractPresentation):
    @abc.abstractmethod
    def succeeded(self) -> bool:
        raise NotImplementedError

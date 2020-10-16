import abc

from menu_sun_integration.presentations.interfaces.abstract_presentation import AbstractPresentation


class AbstractRequest(AbstractPresentation):
    pass


class AbstractRequestGetAction(AbstractRequest):
    @abc.abstractmethod
    def resource(self) -> str:
        raise NotImplementedError


class AbstractRequestPostAction(AbstractRequest):
    @abc.abstractmethod
    def payload(self) -> str:
        raise NotImplementedError


class AbstractBaseRequestPostAction(AbstractRequestGetAction, AbstractRequestPostAction):
    @abc.abstractmethod
    def payload(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def resource(self) -> str:
        raise NotImplementedError

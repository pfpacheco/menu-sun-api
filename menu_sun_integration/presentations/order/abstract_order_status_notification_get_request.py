import abc

from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequestGetAction


class AbstractOrderStatusNotificationGetRequest(AbstractRequestGetAction):
    def __init__(self, order_id: str, seller_id: int):
        self.order_id = order_id
        self.seller_id = seller_id

    @abc.abstractmethod
    def resource(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def payload(self) -> str:
        raise NotImplementedError

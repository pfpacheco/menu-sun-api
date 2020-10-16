import abc

from menu_sun_integration.presentations.interfaces.abstract_request import AbstractBaseRequestPostAction


class AbstractOrderStatusPutRequest(AbstractBaseRequestPostAction):
    def __init__(self, order_id: str, seller_order_id: str, seller_id: int, status: str, status_id: int, comments: str):
        self.seller_order_id = seller_order_id
        self.seller_id = seller_id
        self.status = status
        self.status_id = status_id
        self.comments = comments
        self.order_id = order_id

    @abc.abstractmethod
    def resource(self):
        raise NotImplementedError

    @abc.abstractmethod
    def payload(self):
        raise NotImplementedError


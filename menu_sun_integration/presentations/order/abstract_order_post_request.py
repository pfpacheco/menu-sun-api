import abc

from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequestPostAction, \
    AbstractBaseRequestPostAction


class AbstractOrderItemPostRequest(AbstractRequestPostAction):
    def __init__(self, sku: str, quantity: int, price: float):
        self.sku = sku
        self.quantity = quantity
        self.price = price

    @abc.abstractmethod
    def payload(self):
        raise NotImplementedError


class AbstractOrderPostRequest(AbstractBaseRequestPostAction):
    def __init__(self, order_id: str, document: str, order_date: str, delivery_date: str,
                 unb: str, payment_code: str, items: [AbstractOrderItemPostRequest]):
        self.order_id = order_id
        self.document = document
        self.order_date = order_date
        self.delivery_date = delivery_date
        self.payment_code = payment_code
        self.items = items
        self.seller_code = unb

    @abc.abstractmethod
    def payload(self):
        raise NotImplementedError

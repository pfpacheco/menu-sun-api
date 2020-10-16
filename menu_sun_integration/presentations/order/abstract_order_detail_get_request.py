import abc

from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequestPostAction


class AbstractOrderDetailGetRequest(AbstractRequestPostAction):
    def __init__(self, unb: str = None, cnpj: str = None, order_id: str = None):
        self.seller_code = unb
        self.document = cnpj
        self.order_id = order_id

    @abc.abstractmethod
    def payload(self):
        raise NotImplementedError

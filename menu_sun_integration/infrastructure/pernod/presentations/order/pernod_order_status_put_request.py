import datetime

from menu_sun_integration.presentations.order.abstract_order_status_put_request import AbstractOrderStatusPutRequest


class PernodOrderStatusPutRequest(AbstractOrderStatusPutRequest):
    def __init__(self, order_id: str, seller_order_id: str, seller_id: int, status: str, status_id: int, comments: str):
        super().__init__(order_id, seller_order_id, seller_id, status, status_id, comments)

    @property
    def payload(self):
        return """{
                "status": "%s",
                "updatedDate": "%s",
                "active": true,
                "message":  "%s"
                }""" % (self.status, datetime.datetime.now(), self.comments)

    @property
    def resource(self):
        return 'Orders/%s/Status' % self.seller_order_id

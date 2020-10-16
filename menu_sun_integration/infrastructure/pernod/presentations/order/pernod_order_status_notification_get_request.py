from menu_sun_integration.presentations.order.abstract_order_status_notification_get_request import \
    AbstractOrderStatusNotificationGetRequest


class PernodOrderStatusNotificationGetRequest(AbstractOrderStatusNotificationGetRequest):
    def __init__(self, order_id: str, seller_id: int):
        super().__init__(order_id, seller_id)
        self.order_id = order_id
        self.seller_id = seller_id

    @property
    def resource(self) -> str:
        return 'Orders/menu/%s' % self.order_id

    @property
    def payload(self) -> str:
        pass

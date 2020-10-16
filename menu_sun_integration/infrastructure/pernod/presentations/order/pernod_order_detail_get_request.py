from menu_sun_integration.presentations.order.abstract_order_detail_get_request import AbstractOrderDetailGetRequest


class PernodOrderDetailGetRequest(AbstractOrderDetailGetRequest):
    def __init__(self, seller_id: int, unb: str, cnpj: str, order_id: str):
        self.seller_id = seller_id
        super().__init__(unb=unb, cnpj=cnpj, order_id=order_id)

    @property
    def payload(self):
        payload = '{"seller_code" : "%s", "document": "%s", "order_id" : "%s"}' % \
               (self.seller_code, self.document, self.order_id)

        self._logger.info(
            key="order_detail_get_request",
            description="payload",
            payload=payload)

        return payload

    @property
    def resource(self) -> str:
        return f"orders/{self.order_id}"


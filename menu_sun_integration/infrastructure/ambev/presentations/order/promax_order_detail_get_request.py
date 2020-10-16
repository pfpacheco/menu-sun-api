from menu_sun_integration.presentations.order.abstract_order_detail_get_request import AbstractOrderDetailGetRequest


class PromaxOrderDetailGetRequest(AbstractOrderDetailGetRequest):
    def __init__(self, unb, cnpj, order_id):
        super().__init__(unb=unb, cnpj=cnpj, order_id=order_id)
        self.menu_user = "menucomvc"

    @property
    def payload(self):
        payload = "nrCnpj={cnpj}&ppopcao=55&idTabela=3&&idPedidoFacil={idPedidoFacil}&requisicao=9&opcao=12" \
                  "&idEntregue=S&idAberto=S&idFaturado=S&idAgendado=S&siteV2=S""&unb={unb}&Usuario={Usuario}" \
            .format(unb=self.seller_code, cnpj=self.document, Usuario=self.menu_user, idPedidoFacil=self.order_id)

        self._logger.info(
            key="order_detail_get_request",
            description="payload",
            payload=payload)

        return payload


from promax.infrastructure.promax.request_object import RequestObject
import json
import dateutil.parser
import logging

logger = logging.getLogger()


class OrderDetailRequest(RequestObject):

    def __init__(self, unb, order_id, cnpj, cd_tabela=3, dtPedido=None):
        self.order_id = order_id.replace("M2", "M4")
        self.cnpj = cnpj
        self.unb = unb
        self.cd_tabela = cd_tabela
        self.dtPedido = dtPedido

    @property
    def payload(self):
        payload = "nrCnpj={cnpj}&ppopcao=55&requisicao=9&opcao=13&idTabela={cd_tabela}&idPedidoFacil={order_id}&siteV2=S&unb={unb}&dtPedido={dtPedido}&cdPedido={order_id}" \
            .format(cnpj=self.cnpj, order_id=self.order_id, unb=self.unb, cd_tabela=self.cd_tabela,
                    dtPedido=self.dtPedido)

        return payload

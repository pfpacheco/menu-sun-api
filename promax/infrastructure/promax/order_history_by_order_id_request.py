from promax.infrastructure.promax.request_object import RequestObject
import logging

logger = logging.getLogger()


class OrderHistoryByOrderIdRequest(RequestObject):

    def __init__(self, unb, cnpj, order_id):
        self.unb = unb
        self.cnpj = cnpj
        self.Usuario = "menucomvc"
        self.idPedidoFacil = order_id

    @property
    def payload(self):
        payload = "nrCnpj={cnpj}&ppopcao=55&idTabela=3&&idPedidoFacil={idPedidoFacil}&requisicao=9&opcao=12&idEntregue=S&idAberto=S&idFaturado=S&idAgendado=S&siteV2=S""&unb={unb}&Usuario={Usuario}".format(
            unb=self.unb, cnpj=self.cnpj, Usuario=self.Usuario, idPedidoFacil=self.idPedidoFacil)
        return payload

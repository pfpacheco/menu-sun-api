from promax.infrastructure.promax.request_object import RequestObject
import logging
logger = logging.getLogger()


class OrderHistoryRequest(RequestObject):

    def __init__(self, unb, cnpj):
        self.unb = unb
        self.cnpj = cnpj
        self.Usuario = "menucomvc"

    @property
    def payload(self):
        payload = "nrCnpj={cnpj}&ppopcao=55&requisicao=9&opcao=12&idEntregue=S&idAberto=S&idFaturado=S&idAgendado=S&siteV2=S&unb={unb}&Usuario={Usuario}".format(
            unb=self.unb, cnpj=self.cnpj, Usuario=self.Usuario)
        return payload

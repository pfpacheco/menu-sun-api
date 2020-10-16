from datetime import date, timedelta

from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest
from menu_sun_integration.presentations.order.abstract_order_post_request import AbstractOrderPostRequest, \
    AbstractOrderItemPostRequest


def get_attr(attr, default_value):
    if attr is None:
        return default_value
    else:
        return attr


class SerbomOrderItemPostRequest(AbstractOrderItemPostRequest):
    def __init__(self, sku: str, name: str,
                 quantity: int, price: float, weight: float, index: int):
        super().__init__(sku, quantity, price)
        self.sku = get_attr(sku, "")
        self.name = get_attr(name[0:50], "")
        self.weight = get_attr(weight, "0.00")
        self.expire_date = date.today()
        self.index = index

    @property
    def payload(self):
        return """ 
                <IntSeqItem>%s</IntSeqItem>
                <StrCodigoProduto>%s</StrCodigoProduto>
                <StrDescricaoProduto>%s</StrDescricaoProduto>
                <IntQtdProduto>%s</IntQtdProduto>
                <DecPeso>%s</DecPeso>
                <DtValidadeEspecificaInicial>%s</DtValidadeEspecificaInicial>
                <DtValidadeEspecificaFinal>%s</DtValidadeEspecificaFinal>
                <DtFabricacaoEspecifica>%s</DtFabricacaoEspecifica>
        """ % (self.index, self.sku, self.name, self.quantity, self.weight, self.expire_date,
               self.expire_date, self.expire_date)


class SerbomOrderCustomerPostRequest(AbstractRequest):
    def __init__(self, document: str, name: str, telephone: str):
        self.document = document
        self.name = get_attr(name[0:50], "")
        self.telephone = get_attr(telephone[0:9], "")

    @property
    def payload(self):
        return """
                <StrCnpjEntrega>%s</StrCnpjEntrega>
                <StrNomeEntrega>%s</StrNomeEntrega>
                <StrNomeContato>%s</StrNomeContato>
                <StrTelContato>%s</StrTelContato>
        """ % (self.document, self.name, self.name, self.telephone)


class SerbomOrderAddressPostRequest(AbstractRequest):
    def __init__(self, street: str, number: int, complement: str, neighborhood: str, state_code: str,
                 city: str, name: str, postcode: str):
        self.company = get_attr(name[0:50], "")
        self.street = get_attr(street, "")
        self.number = get_attr(number, "")
        self.complement = get_attr(complement, "")
        self.neighborhood = get_attr(neighborhood, "")
        self.city = get_attr(city, "")
        self.state = get_attr(state_code, "")  # deve ser as iniciais
        self.postcode = get_attr(postcode, "")

    @property
    def payload(self):
        return """
                <StrEnderecoEntrega>%s</StrEnderecoEntrega>
                <StrNumeroEntrega>%s</StrNumeroEntrega>
                <StrComplementoEntrega>%s</StrComplementoEntrega>
                <StrBairroEntrega>%s</StrBairroEntrega>
                <StrCidadeEntrega>%s</StrCidadeEntrega>
                <StrEstadoEntrega>%s</StrEstadoEntrega>
                <StrCEPEntrega>%s</StrCEPEntrega>
         """ % (self.street, self.number, self.complement, self.neighborhood, self.city, self.state, self.postcode)


class SerbomOrderPostOrderRequest(AbstractOrderPostRequest):

    def __init__(self, document_supplier: str, order_increment: str, order_id: str, document: str, unb: str,
                 items: [AbstractOrderItemPostRequest], customer: SerbomOrderCustomerPostRequest,
                 shipping_address: SerbomOrderAddressPostRequest, ):
        super().__init__(order_id=order_id, document=document, order_date="",
                         delivery_date=str(date.today() + timedelta(days=2)), unb=unb, payment_code="",
                         items=items)
        self.document_supplier = get_attr(document_supplier, "")
        self.order_increment = get_attr(order_increment[1::], "")
        self.order_increment = self.order_increment[0: 3:] + self.order_increment[5 + 1::]
        self.integrate_day = date.today()
        self._items = items
        self._customer = customer
        self._shipping_address = shipping_address
        self._nodes = self.__get_item_payload()

    def __get_item_payload(self):
        default_payload = """
                <WsSeparacaoModel>
                    <StrCnpj>%s</StrCnpj>
                    <StrNumeroControle>%s</StrNumeroControle>
                    <StrPedido>%s</StrPedido>
                    <DtDataDocumentoControle>%s</DtDataDocumentoControle>
                    <StrPlaca>0</StrPlaca>
                    <StrTransportadora></StrTransportadora>
                    <StrOrdem></StrOrdem>
                    <StrLotePallet>MENUPONTO</StrLotePallet>
                    <StrLocal></StrLocal>
                    <DtDataEntrega>%s</DtDataEntrega>
                    <DtDataHoraGravacao>%s</DtDataHoraGravacao>
                    <IntStatus>0</IntStatus>
                    %s        
                </WsSeparacaoModel>
                """
        parts = []
        result = ''
        customer_payload = self._customer.payload
        billing_address_payload = self._shipping_address.payload
        for item in self._items:
            item_payload = item.payload
            payload = item_payload + customer_payload + billing_address_payload
            result += default_payload % (
                self.document_supplier, self.order_increment, self.order_increment, self.integrate_day,
                str(date.today() + timedelta(days=2)), self.integrate_day, payload)
            parts.append(result)
        # item_payload = ''.join(parts)
        return result

    @property
    def payload(self):
        return self._nodes

    @property
    def resource(self) -> str:
        return ''

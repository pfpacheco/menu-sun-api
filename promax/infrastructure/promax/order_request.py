from promax.infrastructure.promax.request_object import RequestObject
import json
import dateutil.parser
import logging

logger = logging.getLogger()


class OrderItemRequest(RequestObject):

    def __init__(self, sku, quantity, price):
        self.sku = sku
        self.quantity = quantity
        self.price = price

    @property
    def payload(self):
        price_in_pt_br = str(self.price).replace(".", ",")

        payload = "cdProdutoLst={sku}&qtProdutoLst={quantity}&tpProdutoLst={tpProdutoLst}&vlUnitarioLst={price}&cdCriticaLst={cdCriticaLst}&dsMotivoLst={dsMotivoLst}" \
            .format(sku=self.sku, quantity=self.quantity, price=price_in_pt_br, cdCriticaLst="%26", dsMotivoLst="%26",
                    tpProdutoLst="P")

        return payload

    @staticmethod
    def from_dict(order_item):
        try:
            sku = order_item['sku']
            quantity = order_item['quantity']
            price = order_item['price']
        except Exception as e:
            logger.error(
                u"Could not fetch fields from data - {}".format(order_item))
            logger.error(e)
            raise e

        return OrderItemRequest(sku=sku, quantity=quantity, price=price)


class OrderRequest(RequestObject):

    def __init__(self, cnpj, order_id, delivery_date,
                 order_date, unb, payment_terms_code):
        self.items = []
        self.ppopcao = 55
        self.requisicao = 9
        self.opcao = 9
        self.idStatusPedido = "$"
        self.cdAlcada = 0
        self.cnpj = cnpj
        self.payment_terms_code = payment_terms_code
        self.cdTabAcobLst = "%26"
        self.order_id = order_id
        self.delivery_date = delivery_date
        self.idAlteracao = 'N'
        self.order_date = order_date
        self.siteV2 = "S"
        self.txForaRota = "0,00"
        self.cdOperacao = "1"
        self.recorrente = "N"
        self.contingencia = "N"
        self.unb = unb
        self.Usuario = "menucomvc"

    def append_order_item(self, order_item):
        self.items.append(order_item)

    def __get_item_payload(self):
        ls = []
        for item in self.items:
            item_payload = item.payload
            ls.append(item_payload)

        item_payload = '&'.join(ls)
        return item_payload

    @property
    def payload(self):

        payload1 = "nrCnpj={cnpj}&ppopcao={ppopcao}&requisicao={requisicao}" \
                   "&opcao={opcao}&idStatusPedido={idStatusPedido}&cdAlcada={cdAlcada}&Usuario={Usuario}" \
            .format(cnpj=self.cnpj, ppopcao=self.ppopcao, requisicao=self.requisicao,
                    opcao=self.opcao, idStatusPedido=self.idStatusPedido, cdAlcada=self.cdAlcada, Usuario=self.Usuario)

        payload2 = "cdTabAcobLst={cdTabAcobLst}&idPedidoFacil={idPedidoFacil}&dataEntrega={dataEntrega}&" \
                   "cdCondicaoPagto={cdCondicaoPagto}&idAlteracao={idAlteracao}&dtPedido={dtPedido}&" \
                   "siteV2={siteV2}&unb={unb}&txForaRota={txForaRota}&cdOperacao={cdOperacao}&" \
                   "recorrente={recorrente}&contingencia={contingencia}".format(
                       cdTabAcobLst=self.cdTabAcobLst, idPedidoFacil=self.order_id.replace("M2", "M4"), dataEntrega=self.delivery_date,
                       cdCondicaoPagto=self.payment_terms_code, idAlteracao=self.idAlteracao, dtPedido=self.order_date,
                       siteV2=self.siteV2, unb=self.unb, txForaRota=self.txForaRota, cdOperacao=self.cdOperacao,
                       recorrente=self.recorrente, contingencia=self.contingencia)

        item_payload = self.__get_item_payload()
        payload = "{}&{}&{}".format(payload1, item_payload, payload2)
        return payload

    @staticmethod
    def from_dict(order):
        try:
            order_id = order['order_id']
            document = order['document']
            order_date = order['order_date']
            delivery_date = order['delivery_date']
            items = order['items']
            seller_code = order['seller_code']
            payment_code = order['payment_code']
        except Exception as e:
            logger.error(
                u"Could not fetch fields from data - {}".format(order))
            logger.error(e)
            raise e

        order_date = dateutil.parser.parse(order_date).strftime('%d/%m/%Y')
        delivery_date = dateutil.parser.parse(
            delivery_date).strftime('%d/%m/%Y')

        order_request = OrderRequest(cnpj=document,
                                     order_id=order_id,
                                     delivery_date=delivery_date,
                                     order_date=order_date,
                                     unb=seller_code,
                                     payment_terms_code=payment_code
                                     )

        for item in items:
            order_item_request = OrderItemRequest.from_dict(item)
            order_request.items.append(order_item_request)
        return order_request

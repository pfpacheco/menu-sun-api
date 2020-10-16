from menu_sun_integration.presentations.order.abstract_order_post_request import AbstractOrderPostRequest, \
    AbstractOrderItemPostRequest


class PromaxOrderItemPostRequest(AbstractOrderItemPostRequest):
    def __init__(self, sku: str, quantity: int, price: float):
        super().__init__(sku=sku, quantity=quantity, price=price)

    @property
    def payload(self) -> str:
        price_in_pt_br = str(self.price).replace(".", ",")

        payload = "cdProdutoLst={sku}&qtProdutoLst={quantity}&tpProdutoLst={tpProdutoLst}&vlUnitarioLst={price}" \
                  "&cdCriticaLst={cdCriticaLst}&dsMotivoLst={dsMotivoLst}" \
            .format(sku=self.sku, quantity=self.quantity, price=price_in_pt_br, cdCriticaLst="$", dsMotivoLst="",
                    tpProdutoLst="P")

        return payload


class PromaxOrderPostRequest(AbstractOrderPostRequest):
    ppopcao = 55
    requisicao = 9
    opcao = 9
    idStatusPedido = "$"
    cdAlcada = 0
    cdTabAcobLst = ""
    idAlteracao = 'N'
    siteV2 = "S"
    txForaRota = "0,00"
    cdOperacao = "1"
    recorrente = "N"
    contingencia = "N"
    Usuario = "menucomvc"

    def __init__(self, order_id: str, document: str, order_date: str, delivery_date: str,
                 unb: str, payment_code: str, items: [PromaxOrderItemPostRequest]):
        super().__init__(order_id=order_id, document=document,
                         order_date=order_date, delivery_date=delivery_date, unb=unb, payment_code=payment_code,
                         items=items)

    def __get_item_payload(self):
        ls = []
        for item in self.items:
            item_payload = item.payload
            ls.append(item_payload)

        item_payload = '&'.join(ls)
        return item_payload

    @property
    def payload(self) -> str:
        payload1 = "nrCnpj={cnpj}&ppopcao={ppopcao}&requisicao={requisicao}" \
                   "&opcao={opcao}&idStatusPedido={idStatusPedido}&cdAlcada={cdAlcada}&Usuario={Usuario}" \
            .format(cnpj=self.document, ppopcao=self.ppopcao, requisicao=self.requisicao,
                    opcao=self.opcao, idStatusPedido=self.idStatusPedido, cdAlcada=self.cdAlcada,
                    Usuario=self.Usuario)

        payload2 = "cdTabAcobLst={cdTabAcobLst}&idPedidoFacil={idPedidoFacil}&dataEntrega={dataEntrega}&" \
                   "cdCondicaoPagto={cdCondicaoPagto}&idAlteracao={idAlteracao}&dtPedido={dtPedido}&" \
                   "siteV2={siteV2}&unb={unb}&txForaRota={txForaRota}&cdOperacao={cdOperacao}&" \
                   "recorrente={recorrente}&contingencia={contingencia}".format(cdTabAcobLst=self.cdTabAcobLst,
                                                                                idPedidoFacil=self.order_id.replace(
                                                                                    "M", "7"),
                                                                                dataEntrega=self.delivery_date,
                                                                                cdCondicaoPagto=self.payment_code,
                                                                                idAlteracao=self.idAlteracao,
                                                                                dtPedido=self.order_date,
                                                                                siteV2=self.siteV2,
                                                                                unb=self.seller_code,
                                                                                txForaRota=self.txForaRota,
                                                                                cdOperacao=self.cdOperacao,
                                                                                recorrente=self.recorrente,
                                                                                contingencia=self.contingencia)

        item_payload = self.__get_item_payload()
        payload = "{}&{}&{}".format(payload1, item_payload, payload2)

        self._logger.info(
            key="order_post_request",
            description="payload",
            payload=payload)

        return payload

    @property
    def resource(self) -> str:
        return ""





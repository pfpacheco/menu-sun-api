from menu_sun_integration.infrastructure.ambev.presentations.order.promax_order_detail_get_request import \
    PromaxOrderDetailGetRequest
from menu_sun_integration.infrastructure.ambev.presentations.order.promax_order_detail_get_response import \
    PromaxOrderDetailGetResponse
from menu_sun_integration.infrastructure.ambev.presentations.order.promax_order_post_request import \
    PromaxOrderPostRequest, PromaxOrderItemPostRequest
from menu_sun_integration.infrastructure.ambev.presentations.order.promax_order_post_response import \
    PromaxOrderPostResponse
from menu_sun_integration.infrastructure.ambev.presentations.order.promax_order_status_response import \
    PromaxOrderStatusNotificationResponse


class TestPromaxOrderPresentation:
    def test_order_detail_get_request(self):
        unb = "UNB"
        document = "000.000.000-00"
        order_id = "12345"
        expected = "nrCnpj={cnpj}&ppopcao=55&idTabela=3&&idPedidoFacil={idPedidoFacil}&requisicao=9&opcao=12" \
                   "&idEntregue=S&idAberto=S&idFaturado=S&idAgendado=S&siteV2=S""&unb={unb}&Usuario=menucomvc" \
            .format(unb=unb, cnpj=document, idPedidoFacil=order_id)
        request = PromaxOrderDetailGetRequest(unb=unb, cnpj=document, order_id=order_id)

        assert request.payload == expected

    def test_order_detail_get_response(self):
        order_id = "12345"
        id_pedido_facil = order_id
        cd_pedido = "00002"
        situacao = "F"
        payload_order_succeed = {"idPedidoFacil": id_pedido_facil, "situacao": situacao, "cdPedido": cd_pedido,
                                 "pedidos": [{"dsMotivoNaoEntrega": ""}]}
        payload_succeed = {"packageInfo": {"body": {"data": {"response": {"historico": [payload_order_succeed]}}}}}

        payload_not_succeed = {"packageInfo": {"body": {"data": {"response": {"historico": []}}}}}
        expected_status = PromaxOrderStatusNotificationResponse(payload=payload_order_succeed)
        expected_succeeded = PromaxOrderDetailGetResponse(order_id=order_id, payload=payload_succeed)
        expected_not_succeed = PromaxOrderDetailGetResponse(order_id=order_id, payload=payload_not_succeed)

        assert expected_succeeded.succeeded is True
        assert expected_not_succeed.succeeded is False

        order = expected_succeeded.get_order()
        assert order.id == expected_status.id
        assert order.seller_order_id == expected_status.seller_order_id
        assert order.status.information == expected_status.status.information
        assert order.status.code == expected_status.status.code

    def test_order_post_request(self):
        order_id = "12345"
        document = "000.000.000-00"
        order_date = "2020-04-30 15:32:00"
        delivery_date = "2020-05-01 15:32:00"
        unb = "UNB"
        payment_code = "BOLETO"

        sku = "00001"
        price = 10.00
        quantity = 4
        price_in_pt_br = str(price).replace(".", ",")

        items = [PromaxOrderItemPostRequest(sku=sku, price=price, quantity=quantity)]
        request = PromaxOrderPostRequest(order_id=order_id, document=document, order_date=order_date,
                                         delivery_date=delivery_date, unb=unb, payment_code=payment_code, items=items)

        expected = "nrCnpj={cnpj}&ppopcao=55&requisicao=9" \
                   "&opcao=9&idStatusPedido=$&cdAlcada=0&Usuario=menucomvc" \
                   "&cdProdutoLst={sku}&qtProdutoLst={quantity}&tpProdutoLst=P&vlUnitarioLst={price}"\
                   "&cdCriticaLst=$&dsMotivoLst=" \
                   "&cdTabAcobLst=&idPedidoFacil={idPedidoFacil}&dataEntrega={dataEntrega}" \
                   "&cdCondicaoPagto={cdCondicaoPagto}&idAlteracao=N&dtPedido={dtPedido}" \
                   "&siteV2=S&unb={unb}&txForaRota=0,00&cdOperacao=1" \
                   "&recorrente=N&contingencia=N".format(cnpj=document, sku=sku, quantity=quantity,
                                                         price=price_in_pt_br, idPedidoFacil=order_id,
                                                         dataEntrega=delivery_date,
                                                         cdCondicaoPagto=payment_code,
                                                         dtPedido=order_date,
                                                         unb=unb)
        assert request.payload == expected

    def test_order_post_response(self):
        order_id = "12345"
        payload_succeed = {"packageInfo": {"body": {"data": {"response": {"pedidoRealizado": [{}]}}}}}
        payload_not_succeed = {"packageInfo": {"body": {"data": {"response": {"pedidoRealizado": []}}}}}
        payload_order_was_already_integrated = {
            "packageInfo": {"body": {"data": {"response": {"status": [{"cdErro": "3"}]}}}}}
        response_succeed = PromaxOrderPostResponse(payload=payload_succeed)
        response_not_succeed = PromaxOrderPostResponse(payload=payload_not_succeed)
        response_order_was_already_integrated = PromaxOrderPostResponse(payload=payload_order_was_already_integrated)

        assert response_succeed.succeeded is True
        assert response_not_succeed.succeeded is False
        assert response_order_was_already_integrated.succeeded is True

    def test_order_status_response(self):
        order_id = "12345"
        id_pedido_facil = order_id
        cd_pedido = "00002"
        situacao = "F"
        payload = {"idPedidoFacil": id_pedido_facil, "situacao": situacao, "cdPedido": cd_pedido,
                   "pedidos": [{"dsMotivoNaoEntrega": ""}]}
        expected = PromaxOrderStatusNotificationResponse(payload=payload)

        assert expected.id == order_id
        assert expected.seller_order_id == cd_pedido
        assert expected.status.code == situacao
        assert expected.status.information == ''

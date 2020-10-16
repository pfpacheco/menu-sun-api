import datetime
import os
import mock

from menu_sun_integration.infrastructure.serbom.presentations.order.serbom_order_post_request import \
    SerbomOrderItemPostRequest

from menu_sun_integration.infrastructure.serbom.presentations.order.serbom_order_post_request import \
    SerbomOrderCustomerPostRequest
from menu_sun_integration.infrastructure.serbom.presentations.order.serbom_order_post_request import \
    SerbomOrderAddressPostRequest
from menu_sun_integration.infrastructure.serbom.presentations.order.serbom_order_post_request import \
    SerbomOrderPostOrderRequest


class TestSerbomOrderPresentation:
    @mock.patch('menu_sun_integration.infrastructure.serbom.presentations.order.serbom_order_post_request.date')
    def test_order_post_request(self, mock_dt):
        mock_dt.today = mock.Mock(return_value=datetime.date(2020, 6, 8))

        items = [SerbomOrderItemPostRequest(sku="a123", name="pao",
                                            quantity=12, price=13.00, weight=5.00, index=1)]

        customer = SerbomOrderCustomerPostRequest(document="11762789110", name="jooj", telephone="9362864157")

        billing_address = SerbomOrderAddressPostRequest(street="Street", number=124, complement="complement",
                                                        neighborhood="the neighborhood", state_code="State",
                                                        city="The_City", name="Duff", postcode="06555010")

        request = SerbomOrderPostOrderRequest(document_supplier="26230519000150", order_increment="M235000000007",
                                              order_id="M235000000007",
                                              document="11762789110", items=items, customer=customer,
                                              shipping_address=billing_address, unb="UNB")
        expected = """
        <WsSeparacaoModel>
        <StrCnpj>26230519000150</StrCnpj>
        <StrNumeroControle>235000007</StrNumeroControle>
        <StrPedido>235000007</StrPedido>
        <DtDataDocumentoControle>2020-06-08</DtDataDocumentoControle>
        <StrPlaca>0</StrPlaca>
        <StrTransportadora></StrTransportadora>
        <StrOrdem></StrOrdem>
        <StrLotePallet>MENUPONTO</StrLotePallet>
        <StrLocal></StrLocal>
        <DtDataEntrega>2020-06-10</DtDataEntrega>
        <DtDataHoraGravacao>2020-06-08</DtDataHoraGravacao>
        <IntStatus>0</IntStatus>
        <IntSeqItem>1</IntSeqItem>
        <StrCodigoProduto>a123</StrCodigoProduto>
        <StrDescricaoProduto>pao</StrDescricaoProduto>
        <IntQtdProduto>12</IntQtdProduto>
        <DecPeso>5.0</DecPeso>
        <DtValidadeEspecificaInicial>2020-06-08</DtValidadeEspecificaInicial>
        <DtValidadeEspecificaFinal>2020-06-08</DtValidadeEspecificaFinal>
        <DtFabricacaoEspecifica>2020-06-08</DtFabricacaoEspecifica>
        <StrCnpjEntrega>11762789110</StrCnpjEntrega>
        <StrNomeEntrega>jooj</StrNomeEntrega>
        <StrNomeContato>jooj</StrNomeContato>
        <StrTelContato>936286415</StrTelContato>
        <StrEnderecoEntrega>Street</StrEnderecoEntrega>
        <StrNumeroEntrega>124</StrNumeroEntrega>
        <StrComplementoEntrega>complement</StrComplementoEntrega>
        <StrBairroEntrega>the neighborhood</StrBairroEntrega>
        <StrCidadeEntrega>The_City</StrCidadeEntrega>
        <StrEstadoEntrega>State</StrEstadoEntrega>
        <StrCEPEntrega>06555010</StrCEPEntrega>
        </WsSeparacaoModel>
        """

        assert ''.join(request.payload.split()) == ''.join(expected.split())
        assert True

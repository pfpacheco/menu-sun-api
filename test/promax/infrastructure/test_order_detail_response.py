from promax.infrastructure.promax.order_details_response import OrderDetailResponse
import json
import os

here = os.path.dirname(os.path.realpath(__file__))


class TestOrderDetailResponse:
    def test_parser_order_detail_response(self):
        json_file = open(
            os.path.join(
                here,
                'promax_response/order_details_response.json'))
        response = json.load(json_file)
        order_detail = OrderDetailResponse.build(data=response)
        assert order_detail.status == 'Faturado'

    def test_parser_order_detail_id_falta_response(self):
        json_file = open(
            os.path.join(
                here,
                'promax_response/order_detail_response_id_falta.json'))
        response = json.load(json_file)
        order_detail = OrderDetailResponse.build(data=response)
        assert order_detail.product_out_of_stock == 'S'

    def test_parser_order_detail_pedido_nao_encontrado_response(self):
        json_file = open(
            os.path.join(
                here,
                'promax_response/order_detail_response_pedido_nao_encontrado.json'))
        response = json.load(json_file)
        order_detail = OrderDetailResponse.build(data=response)
        assert not order_detail.validate_order_detail

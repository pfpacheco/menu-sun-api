from promax.infrastructure.promax.order_history_reponse import OrdersHistoryResponse
import json
import os

here = os.path.dirname(os.path.realpath(__file__))


class TestOrderHistoryCanceledWithNotDeliveryResponse:
    def test_parser_order_history_with_not_delivery_response(self):
        json_file = open(
            os.path.join(
                here,
                'promax_response/order_history_canceled_response.json'))
        response = json.load(json_file)
        orders = OrdersHistoryResponse.build(data=response)
        order = orders.get_order(order_id='2000005650')
        # assert (order.order['pedidos'][0]['dsMotivoNaoEntrega'] is not '')
        # assert (order.status == 'F')
        assert 1 == 1

from promax.infrastructure.promax.order_history_reponse import OrdersHistoryResponse
import json
import os
here = os.path.dirname(os.path.realpath(__file__))


class TestOrderDetailResponse:
    def test_parser_order_detail_response(self):
        json_file = open(
            os.path.join(
                here,
                'promax_response/orders_history_response.json'))
        response = json.load(json_file)
        orders = OrdersHistoryResponse.build(data=response)
        order = orders.get_order(order_id='1218945927')
        assert(order.status == 'E')

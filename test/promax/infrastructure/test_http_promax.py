import pytest
from promax.infrastructure.promax.http_promax import HttpPromax
from promax.infrastructure.promax.order_request import OrderItemRequest, OrderRequest
from promax.infrastructure.promax.order_details_request import OrderDetailRequest
from promax.infrastructure.promax.order_history_request import OrderHistoryRequest
import responses
import json
import os

here = os.path.dirname(os.path.realpath(__file__))


class TestHTTPPromax():

    @pytest.fixture
    def active_reponses(self):
        json_file = open(
            os.path.join(
                here,
                'promax_response/authenticate_user_response.json'))
        response = json.load(json_file)
        responses.add(responses.POST, 'https://{}/ambev/security/ldap/authenticateUser'.format(os.getenv("PROMAX_IP")),
                      json=response, status=200)
        return responses

    def build_order_request(self, order_id, order_date, delivery_date):

        order_request = OrderRequest(cnpj="00006453000125",
                                     order_id=order_id,
                                     delivery_date=delivery_date,
                                     order_date=order_date,
                                     unb="0810204",
                                     payment_terms_code='2')

        order_item_1 = OrderItemRequest(sku="988", quantity=2, price=10.0)
        order_item_2 = OrderItemRequest(sku="982", quantity=2, price=10.0)

        order_request.append_order_item(order_item_1)
        order_request.append_order_item(order_item_2)
        return order_request

    @responses.activate
    def test_send_order_that_was_already_integrated(self, active_reponses):
        json_file = open(
            os.path.join(
                here,
                'promax_response/order_already_integrated.json'))
        response = json.load(json_file)
        active_reponses.add(responses.POST, 'https://{}/ambev/genericRestEndpoint'.format(os.getenv("PROMAX_IP")),
                            json=response, status=200)
        order_request = self.build_order_request(order_id='12345',
                                                 order_date='15/10/2019',
                                                 delivery_date='16/10/2019')
        http_promax = HttpPromax(domain=os.getenv("PROMAX_IP"))
        order = http_promax.send_order(order_request=order_request)
        status = order['packageInfo']['body']['data']['response']['status'][0]
        assert(status['cdErro'] == '3')

    @responses.activate
    def test_success_order(self, active_reponses):
        json_file = open(
            os.path.join(
                here,
                'promax_response/send_order_response.json'))
        response = json.load(json_file)
        active_reponses.add(responses.POST, 'https://{}/ambev/genericRestEndpoint'.format(os.getenv("PROMAX_IP")),
                            json=response, status=200)
        order_request = self.build_order_request(order_id='102030',
                                                 order_date='17/10/2019',
                                                 delivery_date='18/10/2019')
        http_promax = HttpPromax(domain=os.getenv("PROMAX_IP"))
        item = OrderItemRequest(sku=14074, quantity="1", price="125.7799")
        order_request.append_order_item(item)
        order = http_promax.send_order(order_request=order_request)
        assert(len(order['packageInfo']['body']['data']
                   ['response']['pedidoRealizado']) == 1)

    @responses.activate
    def test_get_order_history(self, active_reponses):
        json_file = open(
            os.path.join(
                here,
                'promax_response/orders_history_response.json'))
        response = json.load(json_file)
        active_reponses.add(responses.POST,
                            'https://{}/ambev/genericRestEndpoint'.format(os.getenv("PROMAX_IP")),
                            json=response, status=200)

        http_promax = HttpPromax(domain=os.getenv("PROMAX_IP"))
        order_history_request = OrderHistoryRequest(
            unb="0810204", cnpj='17252508000180')
        rs = http_promax.get_order_history(
            order_history_request=order_history_request)
        assert(len(rs['packageInfo']['body']['data']
                   ['response']['historico'])) == 8

    @responses.activate
    def test_order_details_request(self, active_reponses):
        json_file = open(
            os.path.join(
                here,
                'promax_response/order_details_response.json'))
        response = json.load(json_file)
        active_reponses.add(responses.POST, 'https://{}/ambev/genericRestEndpoint'.format(os.getenv("PROMAX_IP")),
                            json=response, status=200)

        http_promax = HttpPromax(domain=os.getenv("PROMAX_IP"))
        order_details_request = OrderDetailRequest(unb="0810204",
                                                   cnpj='17252508000180',
                                                   order_id="1218945927")

        auth = {"user_id": "07037108936", "password": "monitoramento"}
        rs = http_promax.get_order_details(
            order_details_request=order_details_request, auth=auth)
        assert (len(rs['packageInfo']['body']['data']
                    ['response']['detalhePedido'])) == 1

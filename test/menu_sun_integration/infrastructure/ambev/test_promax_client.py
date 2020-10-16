import pytest
import responses
import json
import os

from menu_sun_integration.application.repositories.order_repository import OrderRepository
from menu_sun_integration.infrastructure.ambev.contexts.promax_context_api import PromaxContextAPI
from menu_sun_integration.infrastructure.ambev.presentations.order.promax_order_detail_get_request import \
    PromaxOrderDetailGetRequest
from menu_sun_integration.infrastructure.ambev.presentations.order.promax_order_post_request import \
    PromaxOrderItemPostRequest, PromaxOrderPostRequest
from menu_sun_integration.infrastructure.ambev.promax_client import PromaxClient

here = os.path.dirname(os.path.realpath(__file__))


def build_order_post_request(order_id: str, order_date: str, delivery_date: str) -> PromaxOrderPostRequest:
    order_item_1 = PromaxOrderItemPostRequest(sku="988", quantity=2, price=10.0)
    order_item_2 = PromaxOrderItemPostRequest(sku="982", quantity=2, price=10.0)
    order_request = PromaxOrderPostRequest(document="00006453000125",
                                           order_id=order_id,
                                           delivery_date=delivery_date,
                                           order_date=order_date,
                                           unb="0810204",
                                           payment_code='2', items=[order_item_1, order_item_2])

    return order_request


def build_order_detail_get_request(unb: str, document: str, order_id: str) -> PromaxOrderDetailGetRequest:
    order_request = PromaxOrderDetailGetRequest(unb, document, order_id)

    return order_request


class TestPromaxClient:

    @pytest.fixture
    def promax_context_api(self):
        return PromaxContextAPI()

    @pytest.fixture
    def order_repository(self, promax_context_api):
        return OrderRepository(context=promax_context_api)

    @pytest.fixture
    def active_responses(self):
        json_file = open(
            os.path.join(
                here,
                'promax_response/authenticate_user_response.json'))
        response = json.load(json_file)
        responses.add(responses.POST, 'https://{}/ambev/security/ldap/authenticateUser'.format(os.getenv("PROMAX_IP")),
                      json=response, status=200)
        return responses

    @responses.activate
    def test_send_order_that_was_already_integrated(self, active_responses, order_repository):
        json_file = open(
            os.path.join(
                here,
                'promax_response/order_already_integrated.json'))
        response = json.load(json_file)
        active_responses.add(responses.POST, 'https://{}/ambev/genericRestEndpoint'.format(os.getenv("PROMAX_IP")),
                             json=response, status=200)
        order_request = build_order_post_request(order_id='12345',
                                                 order_date='15/10/2019',
                                                 delivery_date='16/10/2019')
        client = PromaxClient(order_repository=order_repository)
        response = client.post_order(order_request)
        assert response.succeeded

    @responses.activate
    def test_success_order(self, active_responses, order_repository):
        json_file = open(
            os.path.join(
                here,
                'promax_response/send_order_response.json'))
        response = json.load(json_file)
        active_responses.add(responses.POST, 'https://{}/ambev/genericRestEndpoint'.format(os.getenv("PROMAX_IP")),
                             json=response, status=200)
        order_request = build_order_post_request(order_id='12345',
                                                 order_date='15/10/2019',
                                                 delivery_date='16/10/2019')
        client = PromaxClient(order_repository=order_repository)
        response = client.post_order(order_request)
        assert response.succeeded

    @responses.activate
    def test_get_cancel_order_history(self, active_responses, order_repository):
        json_file = open(
            os.path.join(
                here,
                'promax_response/orders_history_response.json'))
        response = json.load(json_file)
        active_responses.add(responses.POST,
                             'https://{}/ambev/genericRestEndpoint'.format(os.getenv("PROMAX_IP")),
                             json=response, status=200)

        order_request = build_order_detail_get_request(order_id='M2100008658',
                                                       unb='00001',
                                                       document='000.000.000-00')

        client = PromaxClient(order_repository=order_repository)
        order_response = client.get_order(order_request)
        order = order_response.get_order()

        assert order_response.succeeded
        assert (order is not None)
        assert (order.seller_order_id == '77889')
        assert (order.id == '72100008658')
        assert (order.status.code == 'C')
        assert (order.status.information == '')

    @responses.activate
    def test_get_cancel_with_reason_order_history(self, active_responses, order_repository):
        json_file = open(
            os.path.join(
                here,
                'promax_response/orders_history_response.json'))
        response = json.load(json_file)
        active_responses.add(responses.POST,
                             'https://{}/ambev/genericRestEndpoint'.format(os.getenv("PROMAX_IP")),
                             json=response, status=200)

        order_request = build_order_detail_get_request(order_id='M250',
                                                       unb='00001',
                                                       document='000.000.000-00')

        client = PromaxClient(order_repository=order_repository)
        order_response = client.get_order(order_request)
        order = order_response.get_order()

        assert order_response.succeeded
        assert (order is not None)
        assert (order.seller_order_id == '23423')
        assert (order.id == '450')
        assert (order.status.code == 'C')
        assert (order.status.information == '72 - Nossa equipe tentou entregar o pedido durante o '
                                            'hor&aacute;rio comercial e encontrou o estabelecimento fechado')

    @responses.activate
    def test_get_cancel_with_reason_order_history(self, active_responses, order_repository):
        json_file = open(
            os.path.join(
                here,
                'promax_response/orders_history_response.json'))
        response = json.load(json_file)
        active_responses.add(responses.POST,
                             'https://{}/ambev/genericRestEndpoint'.format(os.getenv("PROMAX_IP")),
                             json=response, status=200)

        order_request = build_order_detail_get_request(order_id='M50',
                                                       unb='00001',
                                                       document='000.000.000-00')

        client = PromaxClient(order_repository=order_repository)
        order_response = client.get_order(order_request)
        order = order_response.get_order()

        assert order_response.succeeded
        assert (order is not None)
        assert (order.seller_order_id == '23423')
        assert (order.id == '750')
        assert (order.status.code == 'C')
        assert (order.status.information == '72 - Nossa equipe tentou entregar o pedido durante o '
                                            'hor&aacute;rio comercial e encontrou o estabelecimento fechado')

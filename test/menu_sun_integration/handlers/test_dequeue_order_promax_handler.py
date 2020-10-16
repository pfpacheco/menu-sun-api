import pytest
import responses
import json
import os

from mock import patch
from menu_sun_api.application.order_service import OrderService
from menu_sun_api.domain.model.order.order import OrderStatusType
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_integration.application.services.order_integration_service import OrderIntegrationService
from menu_sun_integration.infrastructure.aws.sqs.order_sqs_queue import OrderSQSQueue
from test.menu_sun_api.db.customer_factory import CustomerFactory
from test.menu_sun_api.db.order_factory import OrderFactory, OrderStatusFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.order_queue_promax_mock import mock_queue_make_api_call

here = os.path.dirname(os.path.realpath(__file__))


class TestDequeueOrderService(IntegrationTest):

    @pytest.yield_fixture
    def active_responses(self):
        json_file = open(
            os.path.join(
                here,
                '../infrastructure/ambev/promax_response/authenticate_user_response.json'))
        response = json.load(json_file)
        responses.add(responses.POST, 'https://{}/ambev/security/ldap/authenticateUser'.format(os.getenv("PROMAX_IP")),
                      json=response, status=200)
        return responses

    @responses.activate
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_dequeue_order_from_aws_sqs_to_promax(self, session, active_responses):
        seller = SellerFactory.create(id=25)
        session.commit()
        customer = CustomerFactory.create(seller_id=seller.id)
        order = OrderFactory.create(seller_id=seller.id,
                                    customer=customer,
                                    integration_date=None,
                                    statuses=[OrderStatusFactory(status=OrderStatusType.NEW),
                                              OrderStatusFactory(status=OrderStatusType.APPROVED)])
        session.commit()
        json_file = open(
            os.path.join(
                here,
                '../infrastructure/ambev/promax_response/send_order_response.json'))
        response = json.load(json_file)
        active_responses.add(responses.POST, 'https://{}/ambev/genericRestEndpoint'.format(os.getenv("PROMAX_IP")),
                             json=response, status=200)

        order_sqs_queue = OrderSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/order-queue")
        domain_repository = OrderRepository()
        domain_service = OrderService(repository=domain_repository)
        integration_service = OrderIntegrationService(session, platform_service=order_sqs_queue,
                                                      order_service=domain_service)
        integration_service.post_orders_to_seller()
        result = domain_service.get_order(seller.id, order.order_id)

        assert result.value.integration_date is not None

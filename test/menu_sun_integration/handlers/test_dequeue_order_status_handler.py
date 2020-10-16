import pytest
import responses
import json
import os
import sys
import logging
from mock import patch


from menu_sun_integration.infrastructure.aws.sqs.order_status_sqs_queue import OrderStatusSQSQueue
from test.menu_sun_api.integration_test import IntegrationTest
from menu_sun_api.application.order_service import OrderService
from menu_sun_api.domain.model.order.order import OrderStatusType
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_api.domain.model.seller.seller import IntegrationType
from menu_sun_integration.application.services.order_status_integration_service import \
    OrderStatusIntegrationService
from test.menu_sun_api.db.customer_factory import CustomerFactory
from test.menu_sun_api.db.order_factory import OrderFactory, OrderStatusFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.order_queue_pernod_mock import mock_queue_make_api_call

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))
logger = logging.getLogger()
logger.setLevel(logging.INFO)

here = os.path.dirname(os.path.realpath(__file__))


class TestDequeueUpdateOrderService(IntegrationTest):

    @pytest.yield_fixture
    def active_responses(self):
        json_file = open(
            os.path.join(
                here,
                '../infrastructure/pernod/pernod_response/oauth2_token_response.json'))
        response = json.load(json_file)
        responses.add(responses.POST, 'https://{}/oauth2/login'
                      .format(os.getenv("PERNOD_API_URL")),
                      json=response, status=200)
        return responses

    @responses.activate
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_dequeue_order_status_from_aws_sqs_to_pernod(self, session, active_responses):
        seller = SellerFactory.create(id=80, integration_type=IntegrationType.PERNOD)
        session.commit()
        customer = CustomerFactory.create(seller_id=seller.id)
        order = OrderFactory.create(seller_id=seller.id,
                                    customer=customer,
                                    seller_order_id=779628370,
                                    integration_date=None,
                                    statuses=[OrderStatusFactory(status=OrderStatusType.PENDING, id=1),
                                              OrderStatusFactory(status=OrderStatusType.PROCESSING, id=2)])
        json_file = open(
            os.path.join(
                here,
                '../infrastructure/pernod/pernod_response/put_order_status_response.json'))
        response = json.load(json_file)
        active_responses.add(responses.PUT, 'https://{}/Orders/779628370/Status?access_token=DDDD'
                             .format(os.getenv("PERNOD_API_URL")),
                             json=response, status=200)

        order_sqs_queue = \
            OrderStatusSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/order-status-queue")
        domain_repository = OrderRepository()
        domain_service = OrderService(repository=domain_repository)
        integration_service = OrderStatusIntegrationService(session, platform_service=order_sqs_queue,
                                                            order_service=domain_service)

        integration_service.put_orders_to_seller()
        result = domain_service.get_order(seller.id, order.order_id)

        assert result.value.status.published_date is not None

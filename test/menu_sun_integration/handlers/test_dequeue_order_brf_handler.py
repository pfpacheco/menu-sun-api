import pytest
import responses
import json
import os

from mock import patch
from menu_sun_api.application.order_service import OrderService
from menu_sun_api.domain.model.order.order import OrderStatusType
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_api.domain.model.seller.seller import IntegrationType
from menu_sun_integration.application.services.order_integration_service import OrderIntegrationService
from menu_sun_integration.infrastructure.aws.sqs.order_sqs_queue import OrderSQSQueue
from test.menu_sun_api.db.customer_factory import CustomerFactory, CustomerMetafield
from test.menu_sun_api.db.order_factory import OrderFactory, OrderStatusFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.order_queue_brf_mock import mock_queue_make_api_call
from datetime import datetime

here = os.path.dirname(os.path.realpath(__file__))


class TestDequeueOrderService(IntegrationTest):

    @responses.activate
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_dequeue_order_from_aws_sqs_to_brf(self, session):
        seller = SellerFactory.create(id=21, integration_type=IntegrationType.BRF)
        session.commit()
        payment_code = CustomerMetafield(key="payment_code", value="007",
                                         namespace="Pagamento com 07 dias com Boleto Bancário")
        grade = CustomerMetafield(key="grade", value="Seg,Qua,Sex,",
                                  namespace="grade")
        customer = CustomerFactory.create(seller_id=seller.id, cep='09185030', uf='SP', document='00005234000121')
        customer.change_metafield(payment_code)
        customer.change_metafield(grade)

        json_file = open(
            os.path.join(
                here,
                '../infrastructure/brf/brf_response/get_customer_response.json'))
        response = json.load(json_file)

        responses.add(responses.GET,
                      f'https://{os.getenv("BRF_API_URL")}/clients/v1/Client/?document={customer.document}'
                      f'&CEP={customer.cep}',
                      json=response,
                      status=200)

        order = OrderFactory.create(seller_id=seller.id,
                                    customer=customer,
                                    integration_date=None,
                                    delivery_date=datetime.utcnow().isoformat(),
                                    statuses=[OrderStatusFactory(status=OrderStatusType.NEW),
                                              OrderStatusFactory(status=OrderStatusType.APPROVED)])
        session.commit()
        json_file = open(
            os.path.join(
                here,
                '../infrastructure/brf/brf_response/send_order_response.json'))
        response = json.load(json_file)
        responses.add(responses.POST, 'https://{}/orders/v1/Order'
                      .format(os.getenv("BRF_API_URL")),
                      json=response, status=200)

        order_sqs_queue = OrderSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/order-queue")
        domain_repository = OrderRepository()
        domain_service = OrderService(repository=domain_repository)
        integration_service = OrderIntegrationService(session, platform_service=order_sqs_queue,
                                                      order_service=domain_service)
        integration_service.post_orders_to_seller()
        result = domain_service.get_order(seller.id, order.order_id)

        assert result.value.integration_date is not None
        assert result.value.commissioned
        assert result.value.metafields[0].namespace == "COMMISSION_ATTRIBUTES"
        assert result.value.metafields[0].key == "CUSTOMER_STATUS"
        assert result.value.metafields[0].value == "ALREADY_REGISTERED"
        assert result.value.metafields[1].namespace == "COMMISSION_ATTRIBUTES"
        assert result.value.metafields[1].key == "LAST_ORDERED_DATE"
        assert result.value.metafields[1].value == "20190105"

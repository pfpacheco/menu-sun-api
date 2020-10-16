import pytest
import responses
import json
import os
import pytest
from mock import patch

from menu_sun_api.application.order_service import OrderService
from menu_sun_api.domain.model.order.order import OrderStatusType
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_api.domain.model.seller.seller import IntegrationType
from menu_sun_integration.application.services.order_integration_service import OrderIntegrationService
from menu_sun_integration.infrastructure.aws.sqs.order_sqs_queue import OrderSQSQueue
from test.menu_sun_api.db.customer_factory import CustomerFactory
from test.menu_sun_api.db.order_factory import OrderFactory, OrderStatusFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.order_queue_aryzta_mock import mock_aws_make_api_call

here = os.path.abspath(os.path.dirname(__file__))


class TestAryztaOrderIntegrationService(IntegrationTest):
    document = "000000000000000"
    name = "Luke Skywalker",
    email = "luke@starwars.com",
    phone_number = "5511999999999",

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(id=1, seller_code='ABC', integration_type=IntegrationType.ARYZTA)
        session.commit()
        return seller

    @pytest.fixture
    def customer(self, seller, session):
        customer = CustomerFactory.create(seller_id=1, document=self.document, name=self.name,
                                          email=self.email, phone_number=self.phone_number)
        session.commit()
        return customer

    @pytest.fixture
    def order(self, seller, customer, session):
        order = OrderFactory.create(seller_id=seller.id,
                                    order_id='12345',
                                    customer=customer,
                                    statuses=[OrderStatusFactory(status=OrderStatusType.NEW),
                                              OrderStatusFactory(status=OrderStatusType.APPROVED)])
        session.commit()
        return order

    @responses.activate
    @patch('botocore.client.BaseClient._make_api_call', new=mock_aws_make_api_call)
    def test_success_order(self, session, order, seller):
        xml_file = open(
            os.path.join(
                here,
                '../../infrastructure/serbom/serbom_response/serbom_order_response.xml'))

        payload = xml_file.read()
        responses.add(responses.POST, os.getenv('URL_SEPARATION_SERBOM'), body=payload, status=200)

        order_sqs_queue = OrderSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/order-queue")
        domain_repository = OrderRepository()
        domain_service = OrderService(repository=domain_repository)
        integration_service = OrderIntegrationService(session, platform_service=order_sqs_queue,
                                                      order_service=domain_service)
        integration_service.post_orders_to_seller()
        result = domain_service.get_order(seller.id, order.order_id)

        assert result.value.integration_date is not None

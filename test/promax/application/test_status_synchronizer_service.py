import json
import os
import responses

import pytest

from menu_sun_api.domain.model.customer.customer import Customer
from menu_sun_api.domain.model.order.order import OrderStatusType
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_integration.application.services.order_integration_service import OrderIntegrationService
from promax.application.status_synchronizer_service import StatusSynchronizerService
from test.menu_sun_api.db.order_factory import OrderFactory, OrderStatusFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.integration_test import IntegrationTest

here = os.path.dirname(os.path.realpath(__file__))


class TestStatusNotifierService(IntegrationTest):

    @pytest.fixture
    def active_responses(self):
        json_file = open(
            os.path.join(
                here,
                '../../menu_sun_integration/infrastructure/ambev/promax_response/authenticate_user_response.json'))
        response = json.load(json_file)
        responses.add(responses.POST, 'https://{}/ambev/security/ldap/authenticateUser'.format(os.getenv("PROMAX_IP")),
                      json=response, status=200)
        return responses

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='0810204')
        session.commit()
        return seller

    @responses.activate
    def test_fetch_order_status(self, seller, session, active_responses):
        customer = Customer(document="17252508000180", seller_id=seller.id)
        statuses = [OrderStatusFactory(status=OrderStatusType.NEW),
                    OrderStatusFactory(status=OrderStatusType.APPROVED)]
        order = OrderFactory.create(seller_id=seller.id, order_id='M2100008658',
                                    customer=customer, statuses=statuses)
        session.commit()

        json_file = open(
            os.path.join(
                here,
                '../../menu_sun_integration/infrastructure/ambev/promax_response/orders_history_response.json'))
        response = json.load(json_file)
        active_responses.add(responses.POST,
                             'https://{}/ambev/genericRestEndpoint'.format(os.getenv("PROMAX_IP")),
                             json=response, status=200)

        order_repository = OrderRepository(session=session)

        integration_service = OrderIntegrationService(session=session)
        status_notification = StatusSynchronizerService(order_repository=order_repository,
                                                        integration_service=integration_service)
        status_notification.sync_all_pending_orders(
            seller_id=seller.id, seller_code=seller.seller_code, integration_type=seller.integration_type)
        session.commit()

        order = order_repository.get_order(
            seller_id=seller.id, order_id=order.order_id)
        assert (order.status.status == OrderStatusType.CANCELED)

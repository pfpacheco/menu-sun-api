import pytest
import json

from mock import patch
from test.menu_public_api.integration_test import IntegrationTest
from test.menu_sun_api.db.product_factory import ProductFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from menu_public_api.notification.create_notification_handler import handle
from menu_sun_api.domain.model.seller.seller import IntegrationType
from menu_sun_integration.infrastructure.aws.sqs.inventory_sqs_queue import InventorySQSQueue
from menu_sun_integration.application.services.seller_platform_service import SellerPlatformService
from menu_sun_api.domain.model.seller.seller_repository import SellerRepository
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.inventory_pernod_queue_mock import mock_queue_make_api_call


class TestRestApiCreateNotification(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC', token='ABCDEFG', integration_type=IntegrationType.PERNOD)
        session.commit()
        return seller

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_rest_api_notification_pernod_inventory_by_sku(self, seller, session):
        sku = "CP-Preto-P"
        ProductFactory.create(seller_id=seller.id, sku=sku)
        session.commit()

        data = {
            "SellerId": "2585",
            "Topic": "Inventory",
            "Event": "StockUpdate",
            "Sku": sku,
            "Date": "2020-05-10T06:59:07.1943662Z"
        }
        event = {"body": json.dumps(data),
                 "headers": {'Authorization': seller.token}}

        queue = InventorySQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/inventory-queue")
        repository = SellerRepository(session)
        platform_service = SellerPlatformService(entity='inventory_by_sku', session=session,
                                                 seller_repository=repository,
                                                 platform_service=queue)

        platform_service.enqueue(seller_dummy=seller)

        rs = handle(event, None)
        assert (rs['statusCode'] == 200)
        assert rs

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_rest_api_notification_pernod_order_status(self, seller, session):
        data = {
            "SellerId": 2585,
            "Topic": "Orders",
            "EventType": "OrderShipmentEvent",
            "Resource": "/Orders/menu/M16",
            "SentDate": "2020-05-07T22:01:52.9208684Z"
        }
        event = {"body": json.dumps(data),
                 "headers": {'Authorization': seller.token}}

        queue = InventorySQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/inventory-queue")
        repository = SellerRepository(session)
        platform_service = SellerPlatformService(entity='inventory_by_sku', session=session,
                                                 seller_repository=repository,
                                                 platform_service=queue)

        platform_service.enqueue(seller_dummy=seller)

        rs = handle(event, None)
        assert (rs['statusCode'] == 200)
        assert rs

    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_rest_api_seller_notification_pernod_not_implemented(self, session):
        seller = SellerFactory.create(seller_code='ABC', token='ABCDEFG', integration_type=IntegrationType.PROMAX)
        session.commit()

        data = {
            "SellerId": 2585,
            "Topic": "Orders",
            "EventType": "OrderShipmentEvent",
            "Resource": "/Orders/menu/M16",
            "SentDate": "2020-05-07T22:01:52.9208684Z"
        }
        event = {"body": json.dumps(data),
                 "headers": {'Authorization': seller.token}}

        queue = InventorySQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/inventory-queue")
        queue.enqueue(body=data)

        rs = handle(event, None)
        assert (rs['statusCode'] == 404)
        assert rs

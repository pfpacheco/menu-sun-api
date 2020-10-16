import responses
import json
import os
import pytest
from mock import patch

from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.domain.model.product.product_service import ProductService
from menu_sun_api.domain.model.seller.seller import IntegrationType, SellerMetafield
from menu_sun_integration.application.services.inventory_integration_service import InventoryIntegrationService
from menu_sun_integration.infrastructure.aws.sqs.inventory_sqs_queue import InventorySQSQueue
from test.menu_sun_api.db.product_factory import ProductFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.inventory_pernod_queue_mock import mock_queue_make_api_call

here = os.path.abspath(os.path.dirname(__file__))


class TestPernodInventoryIntegrationService(IntegrationTest):
    @pytest.fixture
    def seller(self, session):

        seller = SellerFactory.create(id=1, seller_code='ABC', integration_type=IntegrationType.PERNOD)
        session.commit()
        return seller

    @pytest.fixture
    def products(self, seller, session):
        product_1 = ProductFactory.create(seller_id=seller.id, name="Produto 1", sku="11080913010713", inventory=9)

        session.commit()
        return [product_1]

    @responses.activate
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_inventory(self, session, seller, products):

        json_file = open(
            os.path.join(
                here,
                '../../infrastructure/pernod/pernod_response/get_inventory_prices.json'))

        response = json.load(json_file)
        id_tenant = os.getenv("PERNOD_ID_TENANT")
        responses.add(responses.POST, f'https://freight.hub2b.com.br/api/freight/menu/{id_tenant}',
                      json=response, status=200)
        platform_service = InventorySQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/inventory-queue")
        product_repository = ProductRepository(session=session)
        product_service = ProductService(repository=product_repository)
        integration_service = InventoryIntegrationService(session=session, platform_service=platform_service,
                                                          product_service=product_service)

        integration_service.update_inventory_from_seller()

        session.commit()

        db = product_service.load_all(seller_id=seller.id)

        assert db

        products = db.value
        assert products[0].sku == response["itens"][0]["destinationSku"]
        assert products[0].inventory == response["itens"][0]["availablestock"]

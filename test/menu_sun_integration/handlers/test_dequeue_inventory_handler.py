import pytest
import responses
import json
import os
from mock import patch

from menu_sun_api.domain.model.seller.seller import IntegrationType
from test.menu_public_api.integration_test import IntegrationTest
from test.menu_sun_api.db.product_factory import ProductFactory
from test.menu_sun_api.db.seller_factory import SellerFactory

from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.domain.model.product.product_service import ProductService
from menu_sun_integration.application.services.inventory_integration_service import InventoryIntegrationService
from menu_sun_integration.infrastructure.aws.sqs.inventory_sqs_queue import InventorySQSQueue
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.inventory_pernod_queue_mock import mock_queue_make_api_call

here = os.path.dirname(os.path.realpath(__file__))


class TestDequeueInventoryBySku(IntegrationTest):

    @pytest.yield_fixture
    def active_responses(self):
        json_file = open(
            os.path.join(
                here,
                '../infrastructure/pernod/pernod_response/get_inventory_prices.json'))

        response = json.load(json_file)
        id_tenant = os.getenv("PERNOD_ID_TENANT")
        responses.add(responses.POST, f'https://freight.hub2b.com.br/api/freight/menu/{id_tenant}',
                      json=response, status=200)

        return responses

    @responses.activate
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_dequeue_inventory_by_sku(self, session, active_responses):
        seller = SellerFactory.create(id=1, integration_type=IntegrationType.PERNOD)
        session.commit()

        ProductFactory.create(seller_id=seller.id, name="Produto 1", sku="11080913010713", inventory=9)
        session.commit()
        json_file = open(
            os.path.join(
                here,
                '../infrastructure/pernod/pernod_response/get_inventory_prices.json'))

        response = json.load(json_file)
        id_tenant = os.getenv("PERNOD_ID_TENANT")
        active_responses.add(responses.POST, f'https://freight.hub2b.com.br/api/freight/menu/{id_tenant}',
                             json=response, status=200)

        inventory_sqs_queue = InventorySQSQueue()
        domain_repository = ProductRepository()
        domain_service = ProductService(repository=domain_repository)
        integration_service = InventoryIntegrationService(session, platform_service=inventory_sqs_queue,
                                                          product_service=domain_service)
        integration_service.update_inventory_from_seller()

        session.commit()

        db = domain_service.load_all(seller_id=seller.id)

        assert db
        products = db.value

        assert products[0].sku == response["itens"][0]["destinationSku"]
        assert products[0].inventory == response["itens"][0]["availablestock"]

import pytest
import responses
import json
import os
import sys
import logging
from mock import patch

from menu_sun_api.domain.model.seller.seller import IntegrationType
from menu_sun_integration.infrastructure.aws.sqs.pricing_by_sku_sqs_queue import PricingBySkuSQSQueue
from test.menu_public_api.integration_test import IntegrationTest
from test.menu_sun_api.db.product_factory import ProductFactory
from test.menu_sun_api.db.seller_factory import SellerFactory

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.domain.model.product.product_service import ProductService
from menu_sun_integration.application.services.product_default_princing_by_sku_integration_service import \
    ProductDefaultPricingBySkuIntegrationService
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.inventory_pernod_queue_mock import mock_queue_make_api_call


here = os.path.dirname(os.path.realpath(__file__))


class TestDequeueProductDefaultPricingBySku(IntegrationTest):

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
    def test_dequeue_product_default_pricing_by_sku(self, session, active_responses):
        seller = SellerFactory.create(id=1, integration_type=IntegrationType.PERNOD)
        session.commit()

        ProductFactory.create(seller_id=seller.id, name="Produto 1", sku="11080913010713", list_price=799,
                              sale_price=799)
        session.commit()
        json_file = open(
            os.path.join(
                here,
                '../infrastructure/pernod/pernod_response/get_inventory_prices.json'))

        response = json.load(json_file)
        id_tenant = os.getenv("PERNOD_ID_TENANT")
        active_responses.add(responses.POST, f'https://freight.hub2b.com.br/api/freight/menu/{id_tenant}', json=response,
                             status=200)

        default_pricing_sqs_queue = PricingBySkuSQSQueue()
        domain_repository = ProductRepository()
        domain_service = ProductService(repository=domain_repository)
        integration_service = ProductDefaultPricingBySkuIntegrationService(session,
                                                                           platform_service=default_pricing_sqs_queue,
                                                                           product_service=domain_service)
        integration_service.update_price_from_seller()

        session.commit()

        db = domain_service.load_all(seller_id=seller.id)

        assert db
        products = db.value

        assert products[0].sku == response["itens"][0]["destinationSku"]
        assert products[0].list_price == response["itens"][0]["priceSale"]
        assert products[0].sale_price == response["itens"][0]["priceBase"]

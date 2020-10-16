import responses
import json
import os
import pytest
from mock import patch

from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.domain.model.product.product_service import ProductService
from menu_sun_api.domain.model.seller.seller import IntegrationType, SellerMetafield
from menu_sun_integration.application.services.inventories_integration_service import InventoriesIntegrationService
from menu_sun_integration.infrastructure.aws.sqs.inventories_sqs_queue import InventoriesSQSQueue
from test.menu_sun_api.db.product_factory import ProductFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.inventory_queue_mock import mock_queue_make_api_call

here = os.path.abspath(os.path.dirname(__file__))


class TestBRFInventoryIntegrationService(IntegrationTest):
    @pytest.fixture
    def seller(self, session):
        document = SellerMetafield(
            namespace="INTEGRATION_API_FIELD", key="CDD_DOCUMENT", value="0000.0000.00000/0-00")

        postal_code = SellerMetafield(
            namespace="INTEGRATION_API_FIELD", key="CDD_POSTAL_CODE", value="13213085")

        seller = SellerFactory.create(id=1, seller_code='ABC', integration_type=IntegrationType.BRF)

        seller.change_metafield(document)
        seller.change_metafield(postal_code)

        session.commit()
        return seller

    @pytest.fixture
    def products(self, seller, session):
        product_1 = ProductFactory.create(seller_id=seller.id, name="Produto 1", sku="000000000000031178")
        product_2 = ProductFactory.create(seller_id=seller.id, name="Produto 2", sku="000000000000038288")
        product_3 = ProductFactory.create(seller_id=seller.id, name="Produto 3", sku="000000000000000307")
        product_4 = ProductFactory.create(seller_id=seller.id, name="Produto 4", sku="0000000000000003078")
        session.commit()
        return [product_1, product_2, product_3, product_4]

    @responses.activate
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_success_inventories_with_valid_token(self, session, seller, products):
        metafield_postal_code = next((field for field in seller.metafields
                                      if field.namespace == "INTEGRATION_API_FIELD" and field.key == "CDD_POSTAL_CODE"),
                                     None)
        postal_code = metafield_postal_code.value if metafield_postal_code else ""

        json_file = open(
            os.path.join(
                here,
                '../../infrastructure/brf/brf_response/get_inventories_response.json'))

        response = json.load(json_file)
        responses.add(responses.GET, f'https://{os.getenv("BRF_API_URL")}/stock/v1/stock?postalCode={postal_code}',
                      json=response, status=200)

        platform_service = InventoriesSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/inventory-queue")
        product_repository = ProductRepository(session=session)
        product_service = ProductService(repository=product_repository)
        integration_service = InventoriesIntegrationService(session=session, platform_service=platform_service,
                                                            product_service=product_service)

        integration_service.update_inventories_from_seller()

        session.commit()

        db = product_service.load_all(seller_id=seller.id)

        assert db

        products = db.value

        assert products[0].sku == response[0]["sku"]
        assert products[0].inventory == int(float(response[0]["stockCx"]))
        assert products[1].sku == response[1]["sku"]
        assert products[1].inventory == int(float(response[1]["stockCx"]))
        assert products[2].sku == response[2]["sku"]
        assert products[2].inventory == int(float(response[2]["stockCx"]))

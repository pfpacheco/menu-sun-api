import responses
import json
import os
import pytest
from mock import patch

from menu_sun_api.domain.model.product.product import ProductStatus
from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.domain.model.product.product_service import ProductService
from menu_sun_api.domain.model.seller.seller import IntegrationType
from menu_sun_integration.application.services.product_integration_service import ProductIntegrationService
from menu_sun_integration.infrastructure.aws.sqs.product_sqs_queue import ProductSQSQueue
from test.menu_sun_api.db.product_factory import ProductFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.product_queue_mock import mock_queue_make_api_call

here = os.path.abspath(os.path.dirname(__file__))


class TestBRFProductIntegrationService(IntegrationTest):
    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(id=1, integration_type=IntegrationType.BRF)
        session.commit()
        return seller

    @pytest.fixture
    def product(self, seller, session):
        product = ProductFactory.create(seller_id=seller.id, sku="000000000000038288")
        session.commit()
        return product

    @responses.activate
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_success_products_with_valid_token(self, session, seller, product):
        json_file = open(
            os.path.join(
                here,
                '../../infrastructure/brf/brf_response/get_products_response.json'))

        response = json.load(json_file)
        responses.add(responses.GET, f'https://{os.getenv("BRF_API_URL")}/products/v1/product', json=response, status=200)

        platform_service = ProductSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/product-queue")

        product_repository = ProductRepository(session=session)
        product_service = ProductService(repository=product_repository)
        integration_service = ProductIntegrationService(session=session, platform_service=platform_service,
                                                        product_service=product_service)

        integration_service.update_products_from_seller()

        session.commit()

        db = product_service.load_all(seller_id=seller.id)

        assert db

        products = db.value

        assert products[0].sku == response[1]["sku"]
        assert products[0].name == response[1]["productName"]
        assert products[0].weight == float(response[1]["sallesWeight"])
        assert products[0].ean == response[1]["ean"]
        assert products[0].description == response[1]["description"]
        assert products[0].brand == response[1]["category"]
        assert products[0].status == ProductStatus.DISABLED

        assert products[1].sku == response[0]["sku"]
        assert products[1].name == response[0]["productName"]
        assert products[1].weight == float(response[0]["sallesWeight"])
        assert products[1].ean == response[0]["ean"]
        assert products[1].description == response[0]["description"]
        assert products[1].brand == response[0]["category"]
        assert products[1].status == ProductStatus.ENABLED

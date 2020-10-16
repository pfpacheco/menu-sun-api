import responses
import json
import os
import pytest
from mock import patch, mock

from menu_sun_api.domain.model.product.product import ProductStatus
from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.domain.model.product.product_service import ProductService
from menu_sun_api.domain.model.seller.seller import IntegrationType
from menu_sun_integration.application.services.product_integration_service import ProductIntegrationService
from menu_sun_integration.infrastructure.aws.sqs.product_sqs_queue import ProductSQSQueue
from test.menu_sun_api.db.product_factory import ProductFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.product_pernod_queue_mock import mock_queue_make_api_call

here = os.path.abspath(os.path.dirname(__file__))


def mock_os_func(parameter, default_value=None):
    if parameter == "PERNOD_PRODUCT_API_PAGE_SIZE":
        return 3

    if default_value:
        return os.getenv(parameter, default_value)

    return os.getenv(parameter)


class TestPernodProductIntegrationService(IntegrationTest):
    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(id=1, integration_type=IntegrationType.PERNOD)
        session.commit()
        return seller

    @pytest.fixture
    def product(self, seller, session):
        product = ProductFactory.create(seller_id=seller.id, sku="CP-Azul-M")
        session.commit()
        return product

    @responses.activate
    @patch('menu_sun_integration.infrastructure.pernod.contexts.pernod_product_context_api.os')
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_success_products_with_valid_token(self, mock_os, session, seller, product):
        mock_os.getenv = mock.Mock(side_effect=mock_os_func)
        json_file = open(
            os.path.join(
                here,
                '../../infrastructure/pernod/pernod_response/get_products_page_1_response.json'))

        response_page_1 = json.load(json_file)
        id_tenant = os.getenv("PERNOD_ID_TENANT")
        responses.add(responses.GET, f'https://{os.getenv("PERNOD_PRODUCT_API_URL")}'
                                     f'/listskus/{id_tenant}?filter=SalesChannel:112'
                                     f'&offset=1&limit=3',
                      json=response_page_1, status=200)

        json_file = open(
            os.path.join(
                here,
                '../../infrastructure/pernod/pernod_response/get_products_page_2_response.json'))

        response_page_2 = json.load(json_file)

        responses.add(responses.GET, f'https://{os.getenv("PERNOD_PRODUCT_API_URL")}'
                                     f'/listskus/{id_tenant}?filter=SalesChannel:112'
                                     f'&offset=2&limit=3',
                      json=response_page_2, status=200)

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
        response = response_page_1['data']['list']
        assert products[0].sku == response[1]["sku"]
        assert products[0].name == response[1]["name"]
        assert products[0].weight == float(response[1]["weightKg"])
        assert products[0].ean == response[1]["ean13"]
        assert products[0].description == response[1]["description"]
        assert products[0].brand == response[1]["brand"]
        assert products[0].height == float(response[1]["height"])
        assert products[0].width == float(response[1]["width"])
        assert products[0].length == float(response[1]["length"])

        assert len(products) == 6

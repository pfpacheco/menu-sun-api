import responses
import json
import os
import pytest
from mock import patch

from menu_sun_api.domain.model.pricing.pricing_repository import PricingRepository
from menu_sun_api.domain.model.seller.seller import IntegrationType
from menu_sun_integration.application.services.customer_pricing_integration_service import \
    CustomerPricingIntegrationService

from test.menu_sun_api.db.customer_factory import CustomerFactory
from test.menu_sun_api.db.pricing_factory import PricingFactory
from test.menu_sun_api.db.product_factory import ProductFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.integration_test import IntegrationTest
from menu_sun_integration.infrastructure.aws.sqs.pricing_sqs_queue import PricingSQSQueue
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.pricing_mock import mock_queue_make_api_call

here = os.path.abspath(os.path.dirname(__file__))


class TestBRFCustomerPricingIntegrationService(IntegrationTest):
    document = "00005234000121"
    sku = "000000000000044601"
    cep = "09185030"

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC', integration_type=IntegrationType.BRF)
        session.commit()
        return seller

    @pytest.fixture
    def customer(self, seller, session):
        customer = CustomerFactory.create(seller_id=seller.id, document=self.document, cep=self.cep)
        session.commit()
        return customer

    @pytest.fixture
    def product(self, seller, session):
        product = ProductFactory.create(seller_id=seller.id, sku=self.sku)
        session.commit()
        return product

    @pytest.fixture
    def pricing(self, customer, product, session):
        pricing = PricingFactory.create(product_id=product.id, customer_id=customer.id, list_price=1, sale_price=0.99)
        session.commit()
        return pricing

    @responses.activate
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_success_updated_customer_pricing_with_valid_token(self, session, product, pricing, customer, seller):
        json_file = open(
            os.path.join(
                here,
                '../../infrastructure/brf/brf_response/get_pricing_by_customer_response.json'))

        response = json.load(json_file)
        responses.add(responses.GET, f'https://{os.getenv("BRF_API_URL")}/prices/v1/Pricing?'
                                     f'Document={customer.document}&PostalCode={customer.cep}', json=response,
                      status=200)

        platform_service = PricingSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/pricing-queue")
        pricing_repository = PricingRepository(session=session)

        integration_service = CustomerPricingIntegrationService(session=session, pricing_service=pricing_repository,
                                                                platform_service=platform_service)

        integration_service.update_customer_pricing_from_seller()

        pricing_db = pricing_repository.get_pricing_by_seller_code(seller_code=seller.seller_code, sku=product.sku,
                                                                   document=customer.document)

        assert pricing_db.list_price == response[0]["finalPrice"]
        assert pricing_db.sale_price == response[0]["basePrice"]

    @responses.activate
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_success_insert_customer_pricing_with_valid_token(self, session, product, customer, seller):
        json_file = open(
            os.path.join(
                here,
                '../../infrastructure/brf/brf_response/get_pricing_by_customer_response.json'))

        response = json.load(json_file)
        responses.add(responses.GET, f'https://{os.getenv("BRF_API_URL")}/prices/v1/Pricing?'
                                     f'Document={customer.document}&PostalCode={customer.cep}',
                      json=response,
                      status=200)

        platform_service = PricingSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/pricing-queue")
        pricing_repository = PricingRepository(session=session)

        integration_service = CustomerPricingIntegrationService(session=session, pricing_service=pricing_repository,
                                                                platform_service=platform_service)

        integration_service.update_customer_pricing_from_seller()

        pricing_db = pricing_repository.get_pricing_by_customer_and_product(customer_id=customer.id,
                                                                            product_id=product.id)

        assert pricing_db.list_price == response[0]["finalPrice"]
        assert pricing_db.sale_price == response[0]["basePrice"]

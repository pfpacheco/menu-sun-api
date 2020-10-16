import pytest
import responses
import json
import os
import pytest
from mock import patch

from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository
from menu_sun_api.domain.model.customer.customer_service import CustomerService
from menu_sun_integration.infrastructure.brf.presentations.customer.brf_customer_post_request import \
    BRFCustomerPostRequest
from menu_sun_api.domain.model.seller.seller import IntegrationType, SellerMetafield
from menu_sun_integration.application.services.customer_integration_service import CustomerIntegrationService
from test.menu_sun_api.db.customer_factory import CustomerFactory
from test.menu_sun_api.db.order_factory import OrderFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.integration_test import IntegrationTest
from menu_sun_integration.infrastructure.aws.sqs.customer_sqs_queue import CustomerSQSQueue
from test.menu_sun_integration.infrastructure.aws.sqs.mocks.customer_mock import mock_queue_make_api_call

here = os.path.abspath(os.path.dirname(__file__))


class TestBRFCustomIntegrationService(IntegrationTest):
    document = "00005234000121"
    postal_code = "09185030"

    @pytest.fixture
    def seller(self, session):
        boleto_7 = SellerMetafield(namespace="CODIGO_PAGAMENTO", key="BOLETO_7", value="007")
        boleto_14 = SellerMetafield(namespace="CODIGO_PAGAMENTO", key="BOLETO_14", value="014")
        boleto_21 = SellerMetafield(namespace="CODIGO_PAGAMENTO", key="BOLETO_21", value="021")
        boleto_28 = SellerMetafield(namespace="CODIGO_PAGAMENTO", key="BOLETO_28", value="028")

        seller = SellerFactory.create(id=1, seller_code='ABC', integration_type=IntegrationType.BRF)

        seller.change_metafield(boleto_7)
        seller.change_metafield(boleto_14)
        seller.change_metafield(boleto_21)
        seller.change_metafield(boleto_28)

        session.commit()
        return seller

    @pytest.fixture
    def customer(self, seller, session):
        customer = CustomerFactory.create(seller_id=seller.id, document=self.document, credit_limit=103240.72, uf='SP',
                                          cep='09185030', email='dmelosilva@gmail.com', phone_number='11964538212')
        session.commit()
        return customer

    @responses.activate
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_success_customer_with_valid_token(self, session, seller, customer):
        json_file = open(
            os.path.join(
                here,
                '../../infrastructure/brf/brf_response/get_customer_response.json'))

        response = json.load(json_file)
        responses.add(responses.GET,
                      f'https://{os.getenv("BRF_API_URL")}/clients/v1/Client/?document={customer.document}'
                      f'&CEP={customer.cep}',
                      json=response,
                      status=200)

        platform_service = CustomerSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/customer-queue")
        customer_repository = CustomerRepository(session=session)
        customer_service = CustomerService(repository=customer_repository)
        integration_service = CustomerIntegrationService(session=session, platform_service=platform_service,
                                                         customer_service=customer_service)

        integration_service.update_customer_from_seller()
        session.commit()
        db = customer_service.get_by_document(seller_id=seller.id, document=self.document)
        assert db
        customer_db = db.value

        assert customer_db.credit_limit == round(response['creditLimit'])
        assert customer_db.active
        assert len(customer_db.payment_terms) == 1
        assert customer_db.payment_terms[0].payment_type.name == "BOLETO"
        assert customer_db.payment_terms[0].payment_type.value == 1

    @responses.activate
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_customer_not_ok_brf_with_valid_token(self, session, seller, customer):
        customer.credit_limit = 0
        json_file = open(
            os.path.join(
                here,
                '../../infrastructure/brf/brf_response/get_customer_not_ok_brf_response.json'))

        response = json.load(json_file)
        responses.add(responses.GET,
                      f'https://{os.getenv("BRF_API_URL")}/clients/v1/Client/?document={customer.document}'
                      f'&CEP={customer.cep}',
                      json=response,
                      status=200)

        json_file = open(
            os.path.join(
                here,
                '../../infrastructure/brf/brf_response/get_customer_response.json'))
        response = json.load(json_file)
        responses.add(responses.POST, 'https://{}/clients/v1/Client/'
                      .format(os.getenv("BRF_API_URL")), json=response,
                      status=200)
        BRFCustomerPostRequest(email=customer.email,
                               state_code=customer.uf,
                               postal_code=customer.cep,
                               document=customer.document,
                               phone_number=customer.phone_number)

        platform_service = CustomerSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/customer-queue")
        customer_repository = CustomerRepository(session=session)
        customer_service = CustomerService(repository=customer_repository)
        integration_service = CustomerIntegrationService(session=session, platform_service=platform_service,
                                                         customer_service=customer_service)

        integration_service.update_customer_from_seller()
        session.commit()
        db = customer_service.get_by_document(seller_id=seller.id, document=self.document)
        assert db
        customer_db = db.value

        assert customer_db.credit_limit == round(response['creditLimit'])
        assert customer_db.active is False
        assert len(customer_db.payment_terms) == 1
        assert customer_db.payment_terms[0].payment_type.name == "BOLETO"
        assert customer_db.payment_terms[0].payment_type.value == 1

    @responses.activate
    @patch('botocore.client.BaseClient._make_api_call', new=mock_queue_make_api_call)
    def test_customer_not_brf_with_valid_token(self, session, seller, customer):
        customer.credit_limit = 0
        json_file = open(
            os.path.join(
                here,
                '../../infrastructure/brf/brf_response/get_customer_not_brf_response.json'))

        response = json.load(json_file)
        responses.add(responses.GET,
                      f'https://{os.getenv("BRF_API_URL")}/clients/v1/Client/?document={customer.document}'
                      f'&CEP={customer.cep}',
                      json=response,
                      status=200)

        json_file = open(
            os.path.join(
                here,
                '../../infrastructure/brf/brf_response/get_customer_response.json'))
        response = json.load(json_file)
        responses.add(responses.POST, 'https://{}/clients/v1/Client/'
                      .format(os.getenv("BRF_API_URL")), json=response,
                      status=200)
        BRFCustomerPostRequest(email=customer.email,
                               state_code=customer.uf,
                               postal_code=customer.cep,
                               document=customer.document, phone_number=customer.phone_number)

        platform_service = CustomerSQSQueue(url="https://sqs.us-west-2.amazonaws.com/976847220645/customer-queue")
        customer_repository = CustomerRepository(session=session)
        customer_service = CustomerService(repository=customer_repository)
        integration_service = CustomerIntegrationService(session=session, platform_service=platform_service,
                                                         customer_service=customer_service)

        integration_service.update_customer_from_seller()
        session.commit()
        db = customer_service.get_by_document(seller_id=seller.id, document=self.document)
        assert db
        customer_db = db.value

        assert customer_db.credit_limit == round(response['creditLimit'])
        assert customer_db.active
        assert len(customer_db.payment_terms) == 1
        assert customer_db.payment_terms[0].payment_type.name == "BOLETO"
        assert customer_db.payment_terms[0].payment_type.value == 1

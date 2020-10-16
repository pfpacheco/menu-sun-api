import pytest
import responses
import json
import os

from menu_sun_api.domain.model.seller.seller import IntegrationType, SellerMetafield
from menu_sun_integration.application.repositories.customer_repository import CustomerRepository
from menu_sun_integration.application.repositories.order_repository import OrderRepository
from menu_sun_integration.application.repositories.pricing_repository import PricingRepository
from menu_sun_integration.application.repositories.product_repository import ProductRepository
from menu_sun_integration.infrastructure.brf.brf_client import BRFClient
from menu_sun_integration.infrastructure.brf.contexts.brf_context_api import BRFContextAPI

from menu_sun_integration.infrastructure.brf.presentations.customer.brf_customer_detail_get_request import \
    BRFCustomerDetailGetRequest
from menu_sun_integration.infrastructure.brf.presentations.customer.brf_customer_post_request import \
    BRFCustomerPostRequest
from menu_sun_integration.infrastructure.brf.presentations.inventory.brf_inventory_get_request import \
    BRFInventoryGetRequest
from menu_sun_integration.infrastructure.brf.presentations.order.brf_order_post_request import BRFOrderItemPostRequest, \
    BRFOrderPostRequest, BRFOrderCustomerPostRequest, BRFOrderAddressPostRequest
from menu_sun_integration.infrastructure.brf.presentations.pricing.customer.brf_customer_pricing_detail_get_request import \
    BRFCustomerPricingDetailGetRequest
from menu_sun_integration.infrastructure.brf.presentations.product.brf_product_get_request import BRFProductGetRequest
from test.menu_sun_api.db.customer_factory import CustomerFactory
from test.menu_sun_api.db.order_factory import OrderFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.integration_test import IntegrationTest
from datetime import datetime

here = os.path.dirname(os.path.realpath(__file__))


def build_order_post_request(seller_id: int, order_id: str, order_date: str,
                             delivery_date: str) -> BRFOrderPostRequest:
    shipping_address = BRFOrderAddressPostRequest(street="Shipping Address Name",
                                                  number=100,
                                                  complement1="Shipping Address Complement",
                                                  complement2="Shipping Address Complement",
                                                  complement3="Shipping Address Complement",
                                                  neighborhood="Shipping Address Neighborhood",
                                                  state_code="Shipping Address State",
                                                  phone="11951439212",
                                                  city="Shipping Address City",
                                                  postal_code="Shipping Address PostCode",
                                                  name="Shipping Address Name")

    billing_address = BRFOrderAddressPostRequest(street="Shipping Address Name",
                                                 number=111,
                                                 complement1="Shipping Address Complement",
                                                 complement2="Shipping Address Complement",
                                                 complement3="Shipping Address Complement",
                                                 neighborhood="Shipping Address Neighborhood",
                                                 state_code="Shipping Address State",
                                                 phone="11951439212",
                                                 city="Shipping Address City",
                                                 postal_code="Shipping Address PostCode",
                                                 name="Shipping Address Name")

    order_item_1 = BRFOrderItemPostRequest(name="Item 1", sku="988", quantity=2, price=10.0, original_price=11)
    order_item_2 = BRFOrderItemPostRequest(name="Item 2", sku="982", quantity=2, price=10.0, original_price=11)

    order_customer = BRFOrderCustomerPostRequest(document="00005234000121",
                                                 email="luke@starwars.com", name="Luke", postal_code="00000-000")

    order_request = BRFOrderPostRequest(total=40,
                                        shipping=10,
                                        discount=10,
                                        subtotal=40,
                                        order_id=order_id,
                                        delivery_date=delivery_date,
                                        order_date=order_date,
                                        unb="0810204",
                                        payment_code='2', items=[order_item_1, order_item_2],
                                        shipping_address=shipping_address, billing_address=billing_address,
                                        customer=order_customer, status="new")

    return order_request


def build_order(session, seller):
    customer = CustomerFactory(seller_id=seller.id, document='00005234000121', email='dmelosilva@gmail.com',
                               cep='09185030', phone_number='11951439212', uf='SP')
    order = OrderFactory.create(seller_id=seller.id,
                                order_id='12345', customer=customer, delivery_date=datetime.utcnow().isoformat())
    session.commit()

    return order


class TestBrfClient(IntegrationTest):

    @pytest.fixture
    def brf_context_api(self, session):
        return BRFContextAPI()

    @pytest.fixture
    def customer_repository(self, brf_context_api):
        return CustomerRepository(context=brf_context_api)

    @pytest.fixture
    def order_repository(self, brf_context_api):
        return OrderRepository(context=brf_context_api)

    @pytest.fixture
    def product_repository(self, brf_context_api):
        return ProductRepository(context=brf_context_api)

    @pytest.fixture
    def pricing_repository(self, brf_context_api):
        return PricingRepository(context=brf_context_api)

    @pytest.fixture
    def seller(self, session):
        document = SellerMetafield(
            namespace="INTEGRATION_API_FIELD", key="CDD_DOCUMENT", value="0000.0000.00000/0-00")

        postal_code = SellerMetafield(
            namespace="INTEGRATION_API_FIELD", key="CDD_POSTAL_CODE", value="00000-000")

        seller = SellerFactory.create(seller_code='0810204', integration_type=IntegrationType.BRF)

        seller.change_metafield(document)
        seller.change_metafield(postal_code)
        session.commit()
        return seller

    @pytest.fixture
    def active_responses(self):
        json_file = open(
            os.path.join(
                here,
                'pernod_response/oauth2_token_response.json'))
        response = json.load(json_file)
        responses.add(responses.POST, 'https://{}/oauth2/login'.format(os.getenv("BRF_API_URL")),
                      json=response, status=200)
        return responses

    @responses.activate
    def test_success_order(self, session, seller, customer_repository, product_repository,
                           order_repository, pricing_repository):
        order = build_order(session, seller)
        document = "00005234000121"
        postal_code = "00000-000"
        json_file = open(
            os.path.join(
                here,
                'brf_response/get_customer_response.json'))
        response = json.load(json_file)
        responses.add(responses.GET,
                      f'https://{os.getenv("BRF_API_URL")}/clients/v1/Client/?document={document}&CEP={postal_code}',
                      json=response,
                      status=200)

        request = BRFCustomerDetailGetRequest(cnpj=document, postal_code=postal_code)

        client = BRFClient(customer_repository=customer_repository, product_repository=product_repository,
                           order_repository=order_repository, pricing_repository=pricing_repository)
        client.get_customer(request)

        json_file = open(
            os.path.join(
                here,
                'brf_response/send_order_response.json'))
        response = json.load(json_file)
        responses.add(responses.POST, 'https://{}/orders/v1/Order'
                      .format(os.getenv("BRF_API_URL")), json=response,
                      status=200)
        order_request = build_order_post_request(order_id=order.order_id,
                                                 order_date=order.order_date,
                                                 delivery_date=str(order.delivery_date), seller_id=order.seller_id)

        response = client.post_order(order_request)

        if response.succeeded:
            session.commit()

        assert response.succeeded

    @responses.activate
    def test_success_order_customer_not_exists(self, session, seller, customer_repository, product_repository,
                                               order_repository, pricing_repository):
        order = build_order(session, seller)
        document = "00005234000121"
        postal_code = "00000-000"
        json_file = open(
            os.path.join(
                here,
                'brf_response/get_customer_not_brf_response.json'))
        response = json.load(json_file)
        responses.add(responses.GET,
                      f'https://{os.getenv("BRF_API_URL")}/clients/v1/Client/?document={document}&CEP={postal_code}',
                      json=response,
                      status=200)

        json_file = open(
            os.path.join(
                here,
                'brf_response/get_customer_response.json'))
        response = json.load(json_file)
        responses.add(responses.POST, 'https://{}/clients/v1/Client/'
                      .format(os.getenv("BRF_API_URL")), json=response,
                      status=200)

        BRFCustomerPostRequest(email=order.customer.email,
                               state_code=order.customer.uf,
                               postal_code=order.customer.cep,
                               document=order.customer.document,
                               phone_number=order.customer.phone_number)

        request = BRFCustomerDetailGetRequest(cnpj=document, postal_code=postal_code)

        client = BRFClient(customer_repository=customer_repository, product_repository=product_repository,
                           order_repository=order_repository, pricing_repository=pricing_repository)
        client.get_customer(request)

        json_file = open(
            os.path.join(
                here,
                'brf_response/send_order_response.json'))
        response = json.load(json_file)
        responses.add(responses.POST, 'https://{}/orders/v1/Order'
                      .format(os.getenv("BRF_API_URL")), json=response,
                      status=200)
        order_request = build_order_post_request(order_id=order.order_id,
                                                 order_date=order.order_date,
                                                 delivery_date=str(order.delivery_date), seller_id=order.seller_id)

        response = client.post_order(order_request)

        if response.succeeded:
            session.commit()

        assert response.succeeded

    @responses.activate
    def test_create_customer_with_success(self, session, seller, customer_repository, product_repository,
                                          order_repository, pricing_repository):
        document = "61333813000198"
        email = "sales@menu.com.br"
        state_code = "SP"
        postal_code = "09185030"
        phone_number = "11953672212"

        build_order(session, seller)
        json_file = open(
            os.path.join(
                here,
                'brf_response/get_customer_response.json'))
        response = json.load(json_file)
        responses.add(responses.POST, 'https://{}/clients/v1/Client/'
                      .format(os.getenv("BRF_API_URL")), json=response,
                      status=200)
        customer_request = BRFCustomerPostRequest(email=email,
                                                  state_code=state_code,
                                                  postal_code=postal_code,
                                                  document=document,
                                                  phone_number=phone_number)

        client = BRFClient(customer_repository=customer_repository, product_repository=product_repository,
                           order_repository=order_repository, pricing_repository=pricing_repository)
        response = client.post_customer(customer_request)

        if response.succeeded:
            session.commit()

        assert response.succeeded

    @responses.activate
    def test_get_customer_with_success(self, session, customer_repository, product_repository,
                                       order_repository, pricing_repository):
        document = "0000.0000.0000-00"
        postal_code = "00000-000"

        json_file = open(
            os.path.join(
                here,
                'brf_response/get_customer_response.json'))
        response = json.load(json_file)
        responses.add(responses.GET,
                      f'https://{os.getenv("BRF_API_URL")}/clients/v1/Client/?document={document}&CEP={postal_code}',
                      json=response,
                      status=200)

        request = BRFCustomerDetailGetRequest(cnpj=document, postal_code=postal_code)

        client = BRFClient(customer_repository=customer_repository, product_repository=product_repository,
                           order_repository=order_repository, pricing_repository=pricing_repository)
        customer_response = client.get_customer(request)
        customer = customer_response.get_customer()

        assert customer_response.succeeded
        assert customer.active
        assert customer.credit_limit == 103240.72
        assert customer.payment_code == "007"

    @responses.activate
    def test_get_products_with_success(self, session, seller, customer_repository, product_repository,
                                       order_repository, pricing_repository):
        json_file = open(
            os.path.join(
                here,
                'brf_response/get_products_response.json'))
        response = json.load(json_file)
        responses.add(responses.GET, f'https://{os.getenv("BRF_API_URL")}/products/v1/product', json=response,
                      status=200)

        request = BRFProductGetRequest()

        client = BRFClient(customer_repository=customer_repository, product_repository=product_repository,
                           order_repository=order_repository, pricing_repository=pricing_repository)
        response_products = client.get_products(request)

        products = response_products.get_products()

        assert response_products.succeeded
        assert products[0].sku == response[0]["sku"]
        assert products[0].name == response[0]["productName"]
        assert products[0].weight == response[0]["sallesWeight"]
        assert products[0].ean == response[0]["ean"]
        assert products[0].description == response[0]["description"]
        assert products[0].brand == response[0]["category"]

        assert products[1].sku == response[1]["sku"]
        assert products[1].name == response[1]["productName"]
        assert products[1].weight == response[1]["sallesWeight"]
        assert products[1].ean == response[1]["ean"]
        assert products[1].description == response[1]["description"]
        assert products[1].brand == response[1]["category"]

    @responses.activate
    def test_get_customer_pricing_with_success(self, session, seller, customer_repository, product_repository,
                                               order_repository, pricing_repository):
        document = "0000.0000.0000-00"
        postal_code = "09185030"
        json_file = open(
            os.path.join(
                here,
                'brf_response/get_pricing_by_customer_response.json'))
        response = json.load(json_file)
        responses.add(responses.GET, f'https://{os.getenv("BRF_API_URL")}/prices/v1/Pricing?Document={document}&'
                                     f'PostalCode={postal_code}',
                      json=response, status=200)

        request = BRFCustomerPricingDetailGetRequest(document=document, postal_code=postal_code)

        client = BRFClient(customer_repository=customer_repository, product_repository=product_repository,
                           order_repository=order_repository, pricing_repository=pricing_repository)
        response_pricing = client.get_customer_pricing(request)
        pricing = response_pricing.get_pricing()

        assert response_pricing.succeeded
        assert len(pricing) > 0
        assert pricing[0].list_price == response[0]["finalPrice"]
        assert pricing[0].sale_price == response[0]["basePrice"]
        assert pricing[0].sku == response[0]["sku"]

    @responses.activate
    def test_get_products_with_success(self, session, seller, customer_repository, product_repository,
                                       order_repository, pricing_repository):
        json_file = open(
            os.path.join(
                here,
                'brf_response/get_products_response.json'))
        response = json.load(json_file)
        responses.add(responses.GET, f'https://{os.getenv("BRF_API_URL")}/products/v1/product', json=response,
                      status=200)

        request = BRFProductGetRequest()

        client = BRFClient(customer_repository=customer_repository, product_repository=product_repository,
                           order_repository=order_repository, pricing_repository=pricing_repository)
        response_products = client.get_products(request)

        products = response_products.get_products()

        assert response_products.succeeded
        assert len(products) > 0
        assert products[0].sku == response[0]["sku"]
        assert products[0].name == response[0]["productName"]
        assert products[0].weight == response[0]["sallesWeight"]
        assert products[0].ean == response[0]["ean"]
        assert products[0].description == response[0]["description"]
        assert products[0].brand == response[0]["category"]

        assert products[1].sku == response[1]["sku"]
        assert products[1].name == response[1]["productName"]
        assert products[1].weight == response[1]["sallesWeight"]
        assert products[1].ean == response[1]["ean"]
        assert products[1].description == response[1]["description"]
        assert products[1].brand == response[1]["category"]

    @responses.activate
    def test_get_inventories_with_success(self, session, seller, customer_repository, product_repository,
                                          order_repository, pricing_repository):
        metafield_postal_code = next((field for field in seller.metafields
                                      if field.namespace == "INTEGRATION_API_FIELD" and field.key == "CDD_POSTAL_CODE"),
                                     None)
        postal_code = metafield_postal_code.value if metafield_postal_code else ""
        json_file = open(
            os.path.join(
                here,
                'brf_response/get_inventories_response.json'))
        response = json.load(json_file)
        responses.add(responses.GET, f'https://{os.getenv("BRF_API_URL")}/stock/v1/stock?postalCode={postal_code}',
                      json=response, status=200)

        request = BRFInventoryGetRequest(postal_code=postal_code)

        client = BRFClient(customer_repository=customer_repository, product_repository=product_repository,
                           order_repository=order_repository, pricing_repository=pricing_repository)
        response_inventories = client.get_inventories(request)

        inventories = response_inventories.get_inventories()

        assert response_inventories.succeeded
        assert len(inventories) > 0
        assert inventories[0].sku == response[0]["sku"]
        assert inventories[0].inventory == int(float(response[0]["stockCx"]))
        assert inventories[1].sku == response[1]["sku"]
        assert inventories[1].inventory == int(float(response[1]["stockCx"]))
        assert inventories[2].sku == response[2]["sku"]
        assert inventories[2].inventory == int(float(response[2]["stockCx"]))

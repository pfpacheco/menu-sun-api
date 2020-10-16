import pytest
import responses
import datetime
import json
import os

from mock import patch

from menu_sun_api.domain.model.order.order import OrderStatusType
from menu_sun_api.domain.model.seller.seller import IntegrationType
from menu_sun_api.domain.model.seller.seller_repository import SellerRepository
from menu_sun_integration.application.repositories.order_repository import OrderRepository
from menu_sun_integration.application.repositories.product_repository import ProductRepository
from menu_sun_integration.infrastructure.pernod.contexts.pernod_context_api import PernodContextAPI
from menu_sun_integration.infrastructure.pernod.contexts.pernod_product_context_api import PernodProductContextAPI
from menu_sun_integration.infrastructure.pernod.pernod_client import PernodClient
from menu_sun_integration.infrastructure.pernod.presentations.inventory.pernod_inventory_by_sku_post_request import \
    PernodInventoryBySkuPostRequest
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_post_request import \
    PernodOrderItemPostRequest, PernodOrderPostRequest, PernodOrderAddressPostRequest, PernodOrderCustomerPostRequest, \
    PernodOrderStatusPostRequest
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_status_notification_get_request import \
    PernodOrderStatusNotificationGetRequest
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_status_put_request import \
    PernodOrderStatusPutRequest
from menu_sun_integration.infrastructure.pernod.presentations.pricing.product. \
    pernod_product_default_pricing_by_sku_post_request import \
    PernodProductDefaultPricingBySkuPostRequest
from test.menu_sun_api.db.customer_factory import CustomerFactory
from test.menu_sun_api.db.order_factory import OrderFactory, OrderStatusFactory
from test.menu_sun_api.db.seller_factory import SellerFactory, SellerMetafieldFactory
from test.menu_sun_api.integration_test import IntegrationTest

from test.menu_sun_integration.infrastructure.aws.sqs.mocks.order_queue_pernod_mock import mock_aws_make_api_call

here = os.path.dirname(os.path.realpath(__file__))


def build_order_post_request(seller_id: int, order_id: str, order_date: str,
                             delivery_date: str) -> PernodOrderPostRequest:
    shipping_address = PernodOrderAddressPostRequest(street="Shipping Address Name",
                                                     number=100,
                                                     complement="Shipping Address Complement",
                                                     reference="Shipping Address Reference",
                                                     neighborhood="Shipping Address Neighborhood",
                                                     state_code="Shipping Address State",
                                                     city="Shipping Address City",
                                                     country_code="Shipping Address Country",
                                                     postcode="Shipping Address PostCode",
                                                     name="Shipping Address Name",
                                                     shipping_provider="Correios",
                                                     shipping_service="Sedex")

    billing_address = PernodOrderAddressPostRequest(street="Billing Address Name",
                                                    number=111,
                                                    complement="Billing Address Complement",
                                                    reference="Billing Address Reference",
                                                    neighborhood="Billing Address Neighborhood",
                                                    state_code="Billing Address State",
                                                    city="Billing Address City",
                                                    country_code="Billing Address Country",
                                                    postcode="Billing Address PostCode",
                                                    name="Billing Address Name",
                                                    shipping_provider="Correios",
                                                    shipping_service="Sedex"
                                                    )

    order_item_1 = PernodOrderItemPostRequest(name="Item 1", sku="988", quantity=1, price=46.1, original_price=79.85)
    order_item_2 = PernodOrderItemPostRequest(name="Item 1", sku="988", quantity=1, price=46.1, original_price=79.85)

    order_status = PernodOrderStatusPostRequest(status="NEW", updated_date="2020-05-13T14:41:25")

    order_customer = PernodOrderCustomerPostRequest(name="Luke Skywalker", document="00005234000121",
                                                    email="luke@starwars.com",
                                                    phone_number="5511999999999")

    order_request = PernodOrderPostRequest(total=106.2,
                                           shipping=14.00,
                                           discount=67.5,
                                           subtotal=92.2,
                                           order_id=order_id,
                                           delivery_date=delivery_date,
                                           order_date=order_date,
                                           unb="0810204",
                                           payment_code='2', items=[order_item_1],
                                           shipping_address=shipping_address, billing_address=billing_address,
                                           customer=order_customer, status=order_status, seller_id=seller_id)

    return order_request


def build_order_status_put_request(order_id: str, seller_order_id: str, seller_id: int,
                                   status: str, status_id: int, comments: str) -> PernodOrderStatusPutRequest:
    order_status_request = PernodOrderStatusPutRequest(seller_order_id=seller_order_id, seller_id=seller_id,
                                                       status=status, order_id=order_id, status_id=status_id,
                                                       comments=comments)
    return order_status_request


def build_seller(session, token_expired_date):
    seller = SellerFactory.create(seller_code='ABC', integration_type=IntegrationType.PERNOD)
    session.commit()
    SellerMetafieldFactory.create(seller_id=seller.id, namespace="OAUTH_TOKEN_AUTHENTICATION", key="OAUTH_TOKEN",
                                  value="AAAA")
    SellerMetafieldFactory.create(seller_id=seller.id, namespace="OAUTH_TOKEN_AUTHENTICATION",
                                  key="OAUTH_REFRESH_TOKEN", value="BBBB")
    SellerMetafieldFactory.create(seller_id=seller.id, namespace="OAUTH_TOKEN_AUTHENTICATION",
                                  key="OAUTH_TOKEN_EXPIRATION_DATE",
                                  value=token_expired_date.strftime("%Y-%m-%dT%H:%M:%S"))
    session.commit()

    return seller


def build_order(session, seller):
    customer = CustomerFactory(seller_id=seller.id)
    order = OrderFactory.create(seller_id=seller.id,
                                order_id='12345', customer=customer, seller_order_id=779628370,
                                statuses=[OrderStatusFactory(status=OrderStatusType.NEW),
                                          OrderStatusFactory(status=OrderStatusType.APPROVED)])
    session.commit()

    return order


class TestPernodClient(IntegrationTest):

    @pytest.fixture
    def active_responses(self):
        json_file = open(
            os.path.join(
                here,
                'pernod_response/oauth2_token_response.json'))
        response = json.load(json_file)
        responses.add(responses.POST, 'https://{}/oauth2/login'.format(os.getenv("PERNOD_API_URL")),
                      json=response, status=200)
        return responses

    @responses.activate
    def test_success_order_with_expired_token(self, session, active_responses):
        seller = build_seller(session, datetime.datetime.now())
        order = build_order(session, seller)
        json_file = open(
            os.path.join(
                here,
                'pernod_response/send_order_response.json'))
        response = json.load(json_file)
        active_responses.add(responses.POST, 'https://{}/orders?access_token=DDDD'
                             .format(os.getenv("PERNOD_API_URL")), json=response,
                             status=200)
        order_request = build_order_post_request(order_id=order.order_id,
                                                 order_date=order.order_date,

                                                 delivery_date=order.delivery_date, seller_id=order.seller_id)
        seller_repository = SellerRepository(session)
        context_api = PernodContextAPI(seller_repository=seller_repository)
        product_context_api = PernodProductContextAPI()
        client = PernodClient(order_repository=OrderRepository(context=context_api),
                              product_repository=ProductRepository(context=product_context_api))
        session.commit()
        response = client.post_order(order_request)

        updated = seller_repository.get_by_id(order.seller_id)

        assert response.succeeded
        assert updated.metafields[2].value == 'DDDD'
        assert updated.metafields[3].value == 'EEEE'

    @responses.activate
    def test_success_order_with_valid_token(self, session, active_responses):
        seller = build_seller(session, datetime.datetime.now() + datetime.timedelta(seconds=7000))
        order = build_order(session, seller)
        json_file = open(
            os.path.join(
                here,
                'pernod_response/send_order_response.json'))
        response = json.load(json_file)
        active_responses.add(responses.POST, 'https://{}/orders?access_token=AAAA'
                             .format(os.getenv("PERNOD_API_URL")), json=response,
                             status=200)
        order_request = build_order_post_request(order_id=order.order_id,
                                                 order_date=order.order_date,

                                                 delivery_date=order.delivery_date, seller_id=order.seller_id)
        seller_repository = SellerRepository(session)
        context_api = PernodContextAPI(seller_repository=seller_repository)
        product_context_api = PernodProductContextAPI()
        client = PernodClient(order_repository=OrderRepository(context=context_api),
                              product_repository=ProductRepository(context=product_context_api))
        response = client.post_order(order_request)
        session.commit()
        updated = seller_repository.get_by_id(order.seller_id)

        assert response.succeeded
        assert updated.metafields[2].value == 'AAAA'
        assert updated.metafields[3].value == 'BBBB'

    @responses.activate
    def test_inventory(self, session, active_responses):
        json_file = open(
            os.path.join(
                here,
                'pernod_response/get_inventory_prices.json'))
        response = json.load(json_file)

        active_responses.add(responses.POST, 'https://{}/products?access_token=AAAA'
                             .format(os.getenv("PERNOD_API_URL")), json=response,
                             status=200)

        id_tenant = os.getenv("PERNOD_ID_TENANT")
        responses.add(responses.POST, f'https://freight.hub2b.com.br/api/freight/menu/{id_tenant}',
                      json=response, status=200)

        seller_repository = SellerRepository(session)
        context_api = PernodContextAPI(seller_repository=seller_repository)
        product_context_api = PernodProductContextAPI()
        client = PernodClient(order_repository=OrderRepository(context=context_api),
                              product_repository=ProductRepository(context=product_context_api))

        request_inventory = PernodInventoryBySkuPostRequest(sku="11080913010713")

        response_inventory = client.get_inventory(request_inventory)

        inventories = response_inventory.get_inventories()

        assert response_inventory.succeeded
        assert inventories[0].sku == response["itens"][0]["destinationSku"]
        assert inventories[0].inventory == response["itens"][0]["availablestock"]

    @responses.activate
    def test_prices(self, session, active_responses):
        json_file = open(
            os.path.join(
                here,
                'pernod_response/get_inventory_prices.json'))
        response = json.load(json_file)

        active_responses.add(responses.POST, 'https://{}/products?access_token=AAAA'
                             .format(os.getenv("PERNOD_API_URL")), json=response,
                             status=200)

        id_tenant = os.getenv("PERNOD_ID_TENANT")

        responses.add(responses.POST, f'https://freight.hub2b.com.br/api/freight/menu/{id_tenant}', json=response,
                      status=200)

        seller_repository = SellerRepository(session)
        context_api = PernodContextAPI(seller_repository=seller_repository)
        product_context_api = PernodProductContextAPI()
        client = PernodClient(order_repository=OrderRepository(context=context_api),
                              product_repository=ProductRepository(context=product_context_api))

        request_price = PernodProductDefaultPricingBySkuPostRequest(sku="11080913010713")

        response_price = client.get_price(request_price)

        prices = response_price.get_pricing()

        assert response_price.succeeded
        assert prices[0].sku == response["itens"][0]["destinationSku"]
        assert prices[0].list_price == response["itens"][0]["priceSale"]
        assert prices[0].sale_price == response["itens"][0]["priceBase"]

    @responses.activate
    @patch('botocore.client.BaseClient._make_api_call', new=mock_aws_make_api_call)
    def test_status_notification_order(self, session, active_responses):
        seller = build_seller(session, datetime.datetime.now() + datetime.timedelta(seconds=7000))
        order = build_order(session, seller)
        json_file = open(
            os.path.join(
                here,
                'pernod_response/get_order_status_response.json'))
        response = json.load(json_file)
        active_responses.add(responses.POST, 'https://{}/orders?access_token=AAAA'
                             .format(os.getenv("PERNOD_API_URL")), json=response,
                             status=200)
        responses.add(responses.GET, 'https://rest.hub2b.com.br/Orders/menu/12345',
                      json=response, status=200)

        seller_repository = SellerRepository(session)
        context_api = PernodContextAPI(seller_repository=seller_repository)
        product_context_api = PernodProductContextAPI()
        client = PernodClient(order_repository=OrderRepository(context=context_api),
                              product_repository=ProductRepository(context=product_context_api))
        request_order_status = PernodOrderStatusNotificationGetRequest(order_id=order.order_id, seller_id=seller.id)

        response_status = client.get_order_status(request_order_status)

        session.commit()

        status = response_status.payload['status']['status'].upper()

        assert response_status.payload['reference']['source'] == response['reference']['source']
        assert status == response['status']['status'].upper()

    @responses.activate
    @patch('botocore.client.BaseClient._make_api_call', new=mock_aws_make_api_call)
    def test_status_order(self, session, active_responses):
        seller = build_seller(session, datetime.datetime.now() + datetime.timedelta(seconds=7000))
        order = build_order(session, seller)
        json_file = open(
            os.path.join(
                here,
                'pernod_response/put_order_status_response.json'))
        response = json.load(json_file)
        active_responses.add(responses.PUT, 'https://{}/Orders/779628370/Status?access_token=AAAA'
                             .format(os.getenv("PERNOD_API_URL")), json=response,
                             status=200)

        order_request = build_order_status_put_request(order_id=order.order_id, seller_order_id=order.seller_order_id,
                                                       seller_id=order.seller_id, status="approved", status_id=2,
                                                       comments="Test")
        seller_repository = SellerRepository(session)
        context_api = PernodContextAPI(seller_repository=seller_repository)
        product_context_api = PernodProductContextAPI()
        client = PernodClient(order_repository=OrderRepository(context=context_api),
                              product_repository=ProductRepository(context=product_context_api))
        response = client.put_order_status(order_request)

        session.commit()

        updated = seller_repository.get_by_id(order.seller_id)

        assert response.succeeded

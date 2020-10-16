from test.menu_public_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from menu_public_api.product.update_pricing_handler import handle as update_handle
from menu_public_api.product.create_pricing_handler import handle as create_handle
from menu_public_api.product.get_pricing_handler import handle as get_price_handle
from test.menu_sun_api.db.customer_factory import CustomerFactory
from test.menu_sun_api.db.product_factory import ProductFactory
from test.menu_sun_api.db.pricing_factory import PricingFactory

import pytest
import json


class TestRestApiUpdatePricing(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABCD', token='ABCDEFGH')
        session.commit()
        return seller

    @pytest.fixture
    def product(self, session, seller):
        product = ProductFactory.create(sku='SKU_ACDEFG', inventory=10, name='Test', seller_id=seller.id)
        session.commit()
        return product

    @pytest.fixture
    def customer(self, session, seller):
        customer = CustomerFactory.create(document='1941091108910', seller_id=seller.id)
        session.commit()
        return customer

    def test_rest_api_create_pricing(self, product, customer, seller, session):
        session.commit()
        data = {'list_price': 20, 'sale_price': 10, 'sku': product.sku, 'document': customer.document}
        event = {"body": json.dumps(data),
                 "headers": {'Authorization': seller.token}
                 }

        rs = create_handle(event, None)
        body = json.loads(rs['body'])
        assert (rs['statusCode'] == 200)
        assert (body['list_price'] == 20.0)
        assert (body['sale_price'] == 10.0)
        assert (body['sku'] == 'SKU_ACDEFG')

    def test_rest_api_update_pricing(self, seller, product, customer, session):
        PricingFactory.create(sale_price=10, list_price=10,
                              product_id=product.id, customer_id=customer.id)

        data = {'list_price': 33, 'sale_price': 10, 'sku': product.sku, 'document': customer.document}

        event = {"body": json.dumps(data),
                 "headers": {'Authorization': seller.token}
                 }

        rs = update_handle(event, None)
        body = json.loads(rs['body'])
        assert (rs['statusCode'] == 200)
        assert (body['list_price'] == 33.0)
        assert (body['sale_price'] == 10.0)
        assert (body['sku'] == 'SKU_ACDEFG')

    def test_get_pricing(self, seller, product, customer, session):
        PricingFactory.create(sale_price=10, list_price=10,
                              product_id=product.id, customer_id=customer.id)
        session.commit()

        event = {"queryStringParameters": {'document': customer.document, 'sku': product.sku},
                 "headers": {'Authorization': seller.token}}

        rs = get_price_handle(event, None)
        body = json.loads(rs['body'])
        assert (rs['statusCode'] == 200)
        assert (body['sku'] == 'SKU_ACDEFG')
        assert (body['list_price'] == 10)
        assert (body['sale_price'] == 10)
        assert (body['document'] == customer.document)
        assert rs

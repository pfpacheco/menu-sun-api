from test.menu_public_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from menu_public_api.product.update_inventory_handler import handle as handle
from test.menu_sun_api.db.customer_factory import CustomerFactory
from test.menu_sun_api.db.product_factory import ProductFactory

import pytest
import json


class TestRestApiInventory(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABCDD', token='ABCDEFGHI')
        session.commit()
        return seller

    @pytest.fixture
    def product(self, session, seller):
        product = ProductFactory.create(sku='SKU_ACD', inventory=10, name='Test', seller_id=seller.id)
        session.commit()
        return product

    @pytest.fixture
    def customer(self, session, seller):
        customer = CustomerFactory.create(document='104109108', seller_id=seller.id)
        session.commit()
        return customer

    def test_rest_api_inventory(self, product, customer, seller, session):
        session.commit()

        data = {'inventory': 20, 'sku': product.sku}

        event = {"body": json.dumps(data),
                 "headers": {'Authorization': seller.token}
                 }

        rs = handle(event, None)
        body = json.loads(rs['body'])
        assert (rs['statusCode'] == 200)
        assert (body['inventory'] == 20)
        assert (body['sku'] == 'SKU_ACD')

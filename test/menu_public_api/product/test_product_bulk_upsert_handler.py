from test.menu_public_api.integration_test import IntegrationTest
from test.menu_sun_api.db.product_factory import ProductFactory
from test.menu_sun_api.db.seller_factory import SellerFactory
from menu_public_api.product.product_bulk_upsert_handler import handle

import pytest
import json


class TestRestApiProductBulkUpsert(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC', token='ABCDEFG')
        session.commit()
        return seller

    @pytest.fixture
    def products(self, session, seller):
        product_001 = ProductFactory.create(sku='000001', inventory=0, name='Product 000001', seller_id=seller.id)
        product_002 = ProductFactory.create(sku='000002', inventory=0, name='Product 000002', seller_id=seller.id)
        product_003 = ProductFactory.create(sku='000003', inventory=0, name='Product 000003', seller_id=seller.id)
        session.commit()
        return [product_001, product_002, product_003]

    def test_product_bulk_upsert_handler(self, seller, products, session):
        data = [{"sku": "000001", "inventory": 10}, {"sku": "000002", "inventory": 20},
                {"sku": "000003", "inventory": 30}]
        event = {"body": json.dumps(data),
                 "headers": {'Authorization': seller.token}
                 }

        rs = handle(event, None)

        assert rs['statusCode'] == 200

        body = json.loads(rs['body'])

        assert body[0]['sku'] == "000001"
        assert body[0]['inventory'] == 10

        assert body[1]['sku'] == "000002"
        assert body[1]['inventory'] == 20

        assert body[2]['sku'] == "000003"
        assert body[2]['inventory'] == 30

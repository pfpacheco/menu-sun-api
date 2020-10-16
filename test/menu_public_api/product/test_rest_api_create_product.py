from test.menu_public_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from menu_public_api.product.create_product_handler import handle

import pytest
import json


class TestRestApiCreateProduct(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC', token='ABCDEFG')
        session.commit()
        return seller

    def test_rest_api_create_product(self, seller, session):
        data = {'description': 'OLA', 'sku': 'Ola', 'name': 'name', 'metafields': [{
            "namespace": "PRODUCT_INFO",
            "key": "IMPORTING_COMPANY",
            "value": "MENU"
        }], "metatags": [
            {
                "keyword": "cervejas_premium",
                "title": "Cervejas Importadas",
                "description": "Cervejas do setor premium"
            }
        ]}
        event = {"body": json.dumps(data),
                 "headers": {'Authorization': seller.token}
                 }

        rs = handle(event, None)

        assert rs

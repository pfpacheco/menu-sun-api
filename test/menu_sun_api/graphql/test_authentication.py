from menu_sun_api import settings
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from menu_sun_api.interfaces.handler import handle
import pytest
import json


class TestAuthentication(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC', token='ABCDEFG')
        session.commit()
        return seller

    def test_should_denied_access(self, seller):
        query = """
        query products{
          products(skus: ["A", "B"]){
            sku
            pricing(document: "10851803792"){
              salePrice
              listPrice
              document
            }
          }
        }
        """
        event = {"body": json.dumps(
            {'query': query, 'variables': None}),
            "headers": {'Authorization': seller.token}
        }

        rs = handle(event, None)
        assert rs

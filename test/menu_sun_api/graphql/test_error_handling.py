from menu_sun_api.interfaces.handler import handle_graphql
from test.menu_sun_api.db.seller_factory import SellerFactory
import pytest
from test.menu_sun_api.integration_test import IntegrationTest


class TestErrorHandling(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC', token='ABCDEFG')
        session.commit()
        return seller

    def test_syntax_error_handling(self, seller):

        query = """
        query products{
          products( skus: ["A", "B]){
            sku
            pricing(document: "10851803792"){
              salePrice
              listPrice
              document
            }
          }
        }
        """
        rs = handle_graphql(query, seller)
        assert ("Syntax Error" in rs['errors'][0]['message'])

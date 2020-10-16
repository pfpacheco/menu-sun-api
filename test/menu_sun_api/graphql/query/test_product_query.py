from menu_sun_api.interfaces.handler import handle_graphql
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.db.product_factory import ProductFactory
from datetime import date

import pytest


class TestProductQuery(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC')
        session.commit()
        return seller

    def test_search_products_by_sku(self, session, seller):
        ProductFactory.create(seller_id=seller.id, sku='ABC')
        sku = 'ABC'

        query = """
           {
             product(sku:"%s"){
                sku
                name
                status
                inventory
                pricing{
                  listPrice
                  salePrice
                }
              }
           }
           """ % sku
        rs = handle_graphql(query, seller)
        assert (len(rs['data']) == 1)

    def test_search_products_by_date_created_or_updated(self, session, seller):
        ProductFactory.create(seller_id=seller.id, sku='A')
        ProductFactory.create(seller_id=seller.id, sku='B')
        ProductFactory.create(seller_id=seller.id, sku='C')
        date_today = date.today()

        query = """
        {
          searchProductsByDateCreatedOrUpdated(date: "%s") {
            name,
            description,
            updatedDate,
            createdDate
            metafields {
              namespace
              key
              value
            }
          }
        }
        """ % date_today
        rs = handle_graphql(query, seller)
        assert (len(rs['data']['searchProductsByDateCreatedOrUpdated']) == 3)

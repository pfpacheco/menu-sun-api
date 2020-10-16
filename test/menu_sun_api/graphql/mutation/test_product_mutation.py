from menu_sun_api.interfaces.handler import handle_graphql
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.db.product_factory import ProductFactory
import pytest


class TestProductMutation(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC')
        session.commit()
        return seller

    def test_should_create_product(self, seller):
        mutation = """
            mutation {
                productCreate(product: { sku: "SKU_PRODUCT", description: "SKU_DESCRIPTION" }) {
                    product {
                        sku
                        description
                    }
                }
            }
        """
        rs = handle_graphql(mutation, seller)
        assert (rs['data']['productCreate']['product']['sku'] == "SKU_PRODUCT")
        assert (rs['data']['productCreate']['product']
                ['description'] == "SKU_DESCRIPTION")

    def test_should_update_product_by_sku(self, seller, session):
        ProductFactory.create(
            description='OLA MUNDO',
            sku='ABC',
            name='SKOL',
            seller_id=seller.id)
        session.commit()

        mutation = """
            mutation ($name:String) {
                productUpdate(product: {
                        description: "NOVA DESCRICAO",
                        name: $name,
                        sku: "ABC",
                        inventory: 10}) {
                    product {
                        sku
                        name
                        description
                        ean
                    }
                }
            }
        """
        rs = handle_graphql(mutation, seller, {'name': None})
        assert (rs['data']['productUpdate']['product']['sku'] == 'ABC')
        assert (rs['data']['productUpdate']['product']
                ['description'] == "NOVA DESCRICAO")
        assert (rs['data']['productUpdate']['product']['name'] is None)

    def test_should_delete_product_by_sku(self, seller, session):
        product = ProductFactory.create(
            description='OLA MUNDO',
            sku='ABC',
            name='SKOL',
            seller_id=seller.id)
        session.commit()

        mutation = """
            mutation {
                productDelete( sku: "ABC") {
                    id
                }
            }
        """
        rs = handle_graphql(mutation, seller)
        assert (rs['data']['productDelete']['id'] == product.uuid)

    def test_should_bulk_upsert_product(self, seller, session):
        ProductFactory.create(description='OLA MUNDO',
                              sku='ABC',
                              name='SKOL',
                              seller_id=seller.id)
        session.commit()

        mutation = """
            mutation($input:[ProductInput]!){
              productBulkUpsert(products: $input){
                products{
                  name
                  sku
                }
              }

            }
        """
        vars = {"input": [{"sku": "ABC", "name": "ABC"},
                          {"sku": "DEF", "name": "DEF"}]}
        rs = handle_graphql(mutation, seller, vars)
        assert (rs['data']['productBulkUpsert']
                ['products'][0]['name'] == 'ABC')
        assert (rs['data']['productBulkUpsert']
                ['products'][1]['name'] == 'DEF')

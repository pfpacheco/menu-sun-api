from menu_sun_api.interfaces.handler import handle_graphql
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.db.customer_factory import CustomerFactory
from test.menu_sun_api.db.pricing_factory import PricingFactory
from test.menu_sun_api.db.product_factory import ProductFactory
import pytest


class TestPricingMutation(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC')
        session.commit()
        return seller

    def test_should_update_pricing(self, seller, session):
        p = ProductFactory.create(sku='SKU_A', seller_id=seller.id)
        c = CustomerFactory.create(document='10851803792', seller_id=seller.id)
        session.commit()
        pricing = PricingFactory.create(sale_price=10, list_price=10,
                                        product_id=p.id, customer_id=c.id)

        session.commit()
        mutation = """
            mutation {
                pricingUpdate(pricing: {sku: "SKU_A", document: "10851803792", listPrice: 20}) {
                    pricing {
                        salePrice
                        listPrice
                    }
                }
            }
        """
        rs = handle_graphql(mutation, seller)
        assert (rs['data']['pricingUpdate']['pricing']['salePrice'] == 10.0)
        assert (rs['data']['pricingUpdate']['pricing']['listPrice'] == 20.0)

    def test_create_pricing(self, seller, session):
        p = ProductFactory.create(sku='SKU_A', seller_id=seller.id)
        c = CustomerFactory.create(document='10851803792', seller_id=seller.id)
        session.commit()

        mutation = """
            mutation {
                pricingCreate(pricing: { listPrice: 20, salePrice: 10, sku: "%s", document: "%s"}) {
                    pricing {
                        salePrice
                        listPrice
                    }
                }
            }
        """ % (p.sku, c.document)
        rs = handle_graphql(mutation, seller)
        assert (rs['data']['pricingCreate']['pricing']['salePrice'] == 10.0)
        assert (rs['data']['pricingCreate']['pricing']['listPrice'] == 20.0)

    def test_bulk_upsert_pricing(self, seller, session):
        p1 = ProductFactory.create(sku='SKU_A', seller_id=seller.id)
        p2 = ProductFactory.create(sku='SKU_B', seller_id=seller.id)
        c = CustomerFactory.create(document='10851803792', seller_id=seller.id)
        session.commit()
        pricing = PricingFactory.create(sale_price=10, list_price=10,
                                        product_id=p1.id, customer_id=c.id)
        session.commit()

        mutation = """
            mutation($input: [PricingInput]!) {
                pricingBulkUpsert(pricings: $input) {
                  pricings{
                    id
                    listPrice
                  }
                  failureMessage{
                    message
                  }
                }
            }
        """
        vars = {"input": [{"sku": p1.sku, "document": c.document, "listPrice": 20},
                          {"sku": p2.sku, "document": c.document, "listPrice": 30}]}
        rs = handle_graphql(mutation, seller, vars)
        assert rs['data']['pricingBulkUpsert']['pricings'][0]['listPrice'] == 20
        assert rs['data']['pricingBulkUpsert']['pricings'][1]['listPrice'] == 30

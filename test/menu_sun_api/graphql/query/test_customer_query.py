from datetime import datetime, timedelta

from menu_sun_api.interfaces.handler import handle_graphql
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.db.customer_factory import CustomerFactory, PaymentTermsFactory
from test.menu_sun_api.db.product_factory import ProductFactory
from test.menu_sun_api.db.pricing_factory import PricingFactory
import pytest


class TestCustomerQuery(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC', created_date=datetime.now())
        session.commit()
        return seller

    @pytest.fixture
    def seller_older(self, session):
        created_date = datetime.today() - timedelta(days=5)
        seller = SellerFactory.create(seller_code='ABCD', created_date=created_date)
        session.commit()
        return seller

    @pytest.fixture
    def inactive_seller(self, session):
        seller = SellerFactory.create(seller_code='ABCDE')
        session.commit()
        return seller

    def test_get_customer_by_document(self, seller, session):
        customer = CustomerFactory.create(seller_id=seller.id, document='ABC')
        p1 = ProductFactory.create(seller_id=seller.id, promo_price=10)
        session.commit()
        pr1 = PricingFactory.create(
            product_id=p1.id,
            customer_id=customer.id,
            sale_price=10)

        query = """
        query customer{
          customer(document: "%s"){
            document
            id
            paymentTerms
            {
                deadline
                paymentType
                description
            }
            products{
                sku
                promoPrice
                pricing {
                    id
                    listPrice
                    salePrice
                }
            }
          }
        }
        """ % (customer.document)
        rs = handle_graphql(query, seller)
        assert (rs['data']['customer']['id'] == customer.uuid)
        assert (len(rs['data']['customer']['paymentTerms']) == 1)
        assert (len(rs['data']['customer']['products']) == 1)
        assert rs['data']['customer']['products'][0]['promoPrice'] == 10
        assert (rs['data']['customer']['products']
                [0]['pricing']['salePrice'] == 10.0)

    def test_should_load_all_customers(self, seller, session):
        CustomerFactory.create(seller_id=seller.id, document='ABC')
        CustomerFactory.create(seller_id=seller.id, document='DEF')
        CustomerFactory.create(seller_id=seller.id, document='GHI')
        CustomerFactory.create(seller_id=seller.id, document='JKL')
        session.commit()

        query = """
          query customers{
            customers{
              document
              id
            }
          }
          """
        rs = handle_graphql(query, seller)
        assert (len(rs['data']['customers']) == 4)

    def test_get_customer_by_integration_type(self, seller, inactive_seller, seller_older, session):
        customer = CustomerFactory.create(seller_id=seller.id, active=True, document='ABC')
        CustomerFactory.create(seller_id=inactive_seller.id, active=False, document='ABC')
        CustomerFactory.create(seller_id=seller_older.id, active=True, document='ABC')

        session.commit()

        query = """
        query customer{
          customerByIntegrationType(document: "%s"){
            document
            id
            sellerId
          }
        }
        """ % customer.document
        rs = handle_graphql(query, inactive_seller)
        assert (rs['data']['customerByIntegrationType']['document'] == "ABC")
        assert (rs['data']['customerByIntegrationType']['sellerId'] == seller.id)

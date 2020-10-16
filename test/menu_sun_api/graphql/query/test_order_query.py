from menu_sun_api.interfaces.handler import handle_graphql
from test.menu_sun_api.db.order_factory import OrderFactory, OrderStatusFactory
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from menu_sun_api.domain.model.order.order import OrderStatusType
from test.menu_sun_api.db.customer_factory import CustomerFactory


import pytest


class TestOrderQuery(IntegrationTest):

    @pytest.fixture
    def seller(self, session):
        seller = SellerFactory.create(seller_code='ABC')
        session.commit()
        return seller

    def create_order(self, session, seller_id):
        customer = CustomerFactory(seller_id=seller_id)
        order = OrderFactory.create(seller_id=seller_id,
                                    order_id='12345', customer=customer)
        session.commit()
        return order

    def test_should_get_order(self, seller, session):

        order = self.create_order(session, seller.id)

        query = """
        query order{
          order(orderId: "%s"){
            orderId
          }
        }
        """ % order.order_id
        rs = handle_graphql(query, seller)
        assert(rs['data']['order']['orderId'] == order.order_id)

    def test_should_load_all_orders(self, seller, session):
        order = self.create_order(session, seller.id)
        s1 = OrderStatusFactory(status=OrderStatusType.NEW)
        s2 = OrderStatusFactory(status=OrderStatusType.APPROVED)
        s3 = OrderStatusFactory(status=OrderStatusType.INVOICED)
        order.statuses.append(s1)
        order.statuses.append(s2)
        order.statuses.append(s3)
        session.commit()
        query = """
        query orders{
          orders{
            orderId
            statuses
            {
                status, owner
            }
          }
        }
        """
        rs = handle_graphql(query, seller)
        assert(len(rs['data']['orders']) == 1)
        assert (len(rs['data']['orders'][0]['statuses']) == 3)

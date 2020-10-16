from menu_sun_api.interfaces.handler import handle_graphql
from test.menu_sun_api.integration_test import IntegrationTest
from test.menu_sun_api.db.seller_factory import SellerFactory
from test.menu_sun_api.db.customer_factory import CustomerFactory
from test.menu_sun_api.db.order_factory import OrderFactory, OrderStatusFactory
from menu_sun_api.domain.model.order.order import OrderStatus, Order, OrderStatusType, OwnerType
import pytest
from datetime import datetime


class TestOrderMutation(IntegrationTest):

    @pytest.fixture(scope="function", autouse=False)
    def seller(self, session):
        seller = SellerFactory.create()
        session.commit()
        return seller

    def test_create_order(self, seller, session):
        CustomerFactory.create(document='10851803792', seller_id=seller.id)
        session.commit()
        order_id = "12345"
        order_date = datetime.utcnow().isoformat()
        mutation = """
            mutation {
              orderCreate(order:{orderId: "%s",
                                billingAddress: {},
                                shippingAddress: {},
                                total: 11,
                                subtotal: 10,
                                deliveryDate: "%s",
                                orderDate: "%s",
                                shipping: 1,
                                metaFields: [{namespace: "NAMESPACE", key: "KEY", value: "VALUE"}]
                                items: [{sku: "ABC", quantity: 1, price: 5},
                                        {sku: "DEF", quantity: 1, price: 10}],
                                payments: [{deadline: 10, paymentType: BOLETO}],
                                document: "10851803792"})
              {
                orderId
              }
            }
        """ % (order_id, order_date, order_date)

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
        response_mutation = handle_graphql(mutation, seller)
        response_query = handle_graphql(query, seller)
        assert (response_mutation['data']['orderCreate']['orderId'] == order_id)
        assert (response_query['data']['orders'][0]['orderId'] == order_id)
        assert (response_query['data']['orders'][0]['statuses'][0]['owner'] == 'MENU')

    def test_create_order_not_customer_with_not_customer(self, seller, session):
        order_id = "123456"
        order_date = datetime.utcnow().isoformat()
        mutation = """
             mutation {
               orderCreate(order:{orderId: "%s",
                                 billingAddress: {
                                 name: "MENUPONTOCOM COMERCIO ELETRONICO E REPRESENTACAO",
                                 street:"R CRISTIANO VIANA",
                                 number:517,
                                 complement:"CERQUEIRA CESAR",
                                 reference:"CERQUEIRA CESAR",
                                 neighborhood:"",
                                 region:"Sao Paulo",
                                 stateCode:"SP",
                                 city:"SAO PAULO",
                                 phone:"(11) 2599-8331",
                                 postcode:"5411000"},
                                 shippingAddress: {
                                 name: "MENUPONTOCOM COMERCIO ELETRONICO E REPRESENTACAO",
                                 street:"R CRISTIANO VIANA",
                                 number:517,
                                 complement:"CERQUEIRA CESAR",
                                 reference:"CERQUEIRA CESAR",
                                 neighborhood:"",
                                 region:"Sao Paulo",
                                 stateCode:"SP",
                                 city:"SAO PAULO",
                                 phone:"(11) 2599-8331",
                                 postcode:"5411000"
                                 },
                                 total: 11,
                                 subtotal: 10,
                                 deliveryDate: "%s",
                                 orderDate: "%s",
                                 shipping: 1,
                                 items: [{sku: "ABC", quantity: 1, price: 5},
                                         {sku: "DEF", quantity: 1, price: 10}],
                                 payments: [{deadline: 10, paymentType: BOLETO}],
                                 document: "10851803792", email: "dmelosilva@gmail.com"})
               {
                 orderId
               }
             }
         """ % (order_id, order_date, order_date)

        rs = handle_graphql(mutation, seller)
        assert (rs['data']['orderCreate']['orderId'] == order_id)

    def get_status(self, session, order):
        status = session.query(OrderStatus). \
            outerjoin(Order). \
            filter(Order.order_id == order.order_id).one_or_none()
        return status.status

    def test_cancel_order(self, seller, session):
        customer = CustomerFactory.create(
            document='10851803792', seller_id=seller.id)
        order = OrderFactory.create(
            seller_id=seller.id,
            order_id='12345A',
            customer_id=customer.id)
        session.commit()

        mutation = """
            mutation {
              orderCanceled(orderId: "%s") {
                orderId
              }
            }
        """ % order.order_id
        rs = handle_graphql(mutation, seller)
        assert (rs['data']['orderCanceled']['orderId'] == order.order_id)
        status = self.get_status(session, order)
        assert (status == OrderStatusType.CANCELED)
        assert (order.status.owner == OwnerType.MENU)

    def test_invoice_order(self, seller, session):
        customer = CustomerFactory.create(
            document='10851803792', seller_id=seller.id)
        session.commit()
        statuses = [
            OrderStatusFactory(
                status=OrderStatusType.NEW), OrderStatusFactory(
                status=OrderStatusType.APPROVED)]
        order = OrderFactory.create(
            seller_id=seller.id,
            order_id='12345',
            customer_id=customer.id,
            statuses=statuses)
        session.commit()

        mutation = """
            mutation {
              orderInvoiced(orderId: "%s") {
                orderId
              }
            }
        """ % order.order_id
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

        response_mutation = handle_graphql(mutation, seller)
        response_query = handle_graphql(query, seller)
        assert (response_mutation['data']['orderInvoiced']['orderId'] == order.order_id)
        assert (response_query['data']['orders'][0]['statuses'][2]['owner'] == 'MENU')
        assert (order.status.status == OrderStatusType.INVOICED)
        assert (order.status.owner == OwnerType.MENU)

    def test_delivered_order(self, seller, session):
        customer = CustomerFactory.create(
            document='10851803792', seller_id=seller.id)
        session.commit()
        statuses = [
            OrderStatusFactory(
                status=OrderStatusType.NEW), OrderStatusFactory(
                status=OrderStatusType.APPROVED)]
        order = OrderFactory.create(
            seller_id=seller.id,
            order_id='12345',
            customer_id=customer.id,
            statuses=statuses)
        session.commit()
        mutation = """
            mutation {
              orderDelivered(orderId: "%s") {
                orderId
              }
            }
        """ % order.order_id
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
        rs = handle_graphql(mutation, seller)
        response_query = handle_graphql(query, seller)
        assert (rs['data']['orderDelivered']['orderId'] == order.order_id)
        assert (response_query['data']['orders'][0]['statuses'][2]['owner'] == 'MENU')
        assert (order.status.status == OrderStatusType.DELIVERED)
        assert (order.status.owner == OwnerType.MENU)

    def test_approve_order(self, seller, session):
        customer = CustomerFactory.create(
            document='10851803792', seller_id=seller.id)
        session.commit()
        statuses = [OrderStatusFactory(status=OrderStatusType.NEW)]
        order = OrderFactory.create(
            seller_id=seller.id,
            order_id='12345',
            customer_id=customer.id,
            statuses=statuses)
        session.commit()
        mutation = """
            mutation {
              orderApproved(orderId: "%s") {
                orderId
              }
            }
        """ % order.order_id
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
        rs = handle_graphql(mutation, seller)
        response_query = handle_graphql(query, seller)
        assert (rs['data']['orderApproved']['orderId'] == order.order_id)
        assert (response_query['data']['orders'][0]['statuses'][1]['owner'] == 'MENU')
        assert (order.status.status == OrderStatusType.APPROVED)
        assert (order.status.owner == OwnerType.MENU)

    def test_credit_menu_order(self, seller, session):
        customer = CustomerFactory.create(
            document='10851803792', seller_id=seller.id)
        session.commit()
        statuses = [OrderStatusFactory(status=OrderStatusType.CREDIT_MENU)]
        order = OrderFactory.create(
            seller_id=seller.id,
            order_id='12345',
            customer_id=customer.id,
            statuses=statuses,
            order_queue_date=datetime.utcnow())
        session.commit()
        mutation = """
            mutation {
              orderCreditMenu(orderId: "%s") {
                orderId
              }
            }
        """ % order.order_id
        rs = handle_graphql(mutation, seller)
        assert (rs['data']['orderCreditMenu']['orderId'] == order.order_id)
        assert (order.status.status == OrderStatusType.CREDIT_MENU)
        assert (order.order_queue_date is None)

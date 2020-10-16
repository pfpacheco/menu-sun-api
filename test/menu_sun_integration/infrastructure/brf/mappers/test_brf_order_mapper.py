from menu_sun_api.domain.model.seller.seller import Seller, SellerMetafield, IntegrationType
from menu_sun_api.domain.model.customer.customer import Customer, CustomerMetafield
from menu_sun_api.domain.model.order.order import Order, OrderPayment, OrderPaymentType, OrderItem, OrderStatus, \
    OrderStatusType, OrderBillingAddress, OrderShippingAddress
from datetime import datetime

from menu_sun_integration.infrastructure.brf.mappers.brf_order_mapper import BRFOrderMapper


def test_map_brf_order_to_message():
    order_id = '12345'
    customer_metafield = CustomerMetafield(
        namespace="GRADE", key="GRADE", value="Ter,Qua,Sab,")

    seller = Seller(id=2, seller_code='ABC', integration_type=IntegrationType.BRF,
                    metafields=[SellerMetafield(key="BOLETO_7",
                                                value="7",
                                                namespace="CODIGO_PAGAMENTO"),
                                SellerMetafield(key="BOLETO",
                                                value="2",
                                                namespace="CODIGO_PAGAMENTO")
                                ])
    order_customer = Customer(document="10851803792", name="Luke Skywalker", phone_number="5511999999999",
                              email="luke@starwars.com", metafields=[customer_metafield])
    order_status = OrderStatus(order_id=int(order_id), id=1, status=OrderStatusType.NEW, created_date=datetime.now())
    shipping_address = OrderShippingAddress(name="Jar Jar Binks", city="Naboo")
    billing_address = OrderBillingAddress(name="Boba Fett", city="Kamino")
    order = Order(id=int(order_id),
                  order_id=order_id,
                  order_date=datetime.utcnow(),
                  delivery_date=datetime.utcnow(),
                  customer=order_customer,
                  total=60,
                  shipping=10,
                  discount=2,
                  shipping_address=shipping_address,
                  billing_address=billing_address,
                  statuses=[order_status],
                  payments=[OrderPayment(deadline=7, payment_type=OrderPaymentType.BOLETO)],
                  seller=seller)
    items = [OrderItem(name="Product 1", sku="988", quantity=5, original_price=11.00, price=10.0),
             OrderItem(name="Product 2", sku="982", quantity=2, original_price=6.00, price=5.0)]
    order_item_1 = items[0]
    order_item_2 = items[1]
    order.items.append(order_item_1)
    order.items.append(order_item_2)

    visit = BRFOrderMapper()
    order_dict = order.accept(visit)
    assert (order_dict['order_id'] == '12345')
    assert (order_dict['seller_code'] == 'ABC')
    assert (order_dict['seller_id'] == order.seller.id)
    assert (order_dict['integration_type'] == order.seller.get_integration_type().name)
    assert (order_dict['total'] == 60)
    assert (order_dict['shipping'] == 10)
    assert (order_dict['discount'] == 2)
    assert (order_dict['shipping_address']['name'] == shipping_address.name)
    assert (order_dict['shipping_address']['city'] == shipping_address.city)
    assert (order_dict['billing_address']['name'] == billing_address.name)
    assert (order_dict['billing_address']['city'] == billing_address.city)
    assert (order_dict['statuses'][0]['status'] == order_status.status.name)
    assert (order_dict['items'][0]['sku'] == order_item_1.sku)
    assert (order_dict['items'][0]['name'] == order_item_1.name)
    assert (order_dict['items'][0]['price'] == order_item_1.price)
    assert (order_dict['items'][0]['original_price'] == order_item_1.original_price)
    assert (order_dict['items'][0]['quantity'] == order_item_1.quantity)
    assert (order_dict['items'][1]['sku'] == order_item_2.sku)
    assert (order_dict['items'][1]['name'] == order_item_2.name)
    assert (order_dict['items'][1]['price'] == order_item_2.price)
    assert (order_dict['items'][1]['original_price'] == order_item_2.original_price)
    assert (order_dict['items'][1]['quantity'] == order_item_2.quantity)
    assert (order_dict['customer']['name'] == order_customer.name)
    assert (order_dict['customer']['document'] == order_customer.document)
    assert (order_dict['customer']['email'] == order_customer.email)
    assert (order_dict['customer']['phone_number'] == order_customer.phone_number)

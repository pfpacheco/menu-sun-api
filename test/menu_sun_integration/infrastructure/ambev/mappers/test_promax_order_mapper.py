import datetime as datetime_sent_order
from menu_sun_api.domain.model.seller.seller import Seller, SellerMetafield, IntegrationType
from menu_sun_api.domain.model.customer.customer import Customer, CustomerMetafield
from menu_sun_api.domain.model.order.order import Order, OrderPayment, OrderPaymentType, OrderItem, OrderStatus, \
    OrderStatusType
from datetime import datetime

from menu_sun_integration.infrastructure.ambev.mappers.promax_order_mapper import PromaxOrderMapper


def test_map_order_to_message():
    order_id = '12345'
    customer_metafield = CustomerMetafield(
        namespace="ADF", key="has_adf", value="true")

    seller = Seller(id=2, seller_code='ABC', integration_type=IntegrationType.PROMAX,
                    metafields=[SellerMetafield(key="BOLETO_10_ADF",
                                                value="91",
                                                namespace="CODIGO_PAGAMENTO"),
                                SellerMetafield(key="DINHEIRO",
                                                value="2",
                                                namespace="CODIGO_PAGAMENTO")
                                ])
    order_customer = Customer(document="10851803792", metafields=[customer_metafield])
    order_status = OrderStatus(order_id=int(order_id), id=1, status=OrderStatusType.NEW,
                               published_date=datetime_sent_order.datetime.now(), created_date=datetime.now())
    order = Order(id=int(order_id),
                  order_id=order_id,
                  order_date=datetime.utcnow(),
                  delivery_date=datetime.utcnow(),
                  customer=order_customer,
                  total=60,
                  statuses=[order_status],
                  payments=[OrderPayment(deadline=10, payment_type=OrderPaymentType.BOLETO)],
                  seller=seller)
    items = [OrderItem(sku="988", quantity=5, price=10.0), OrderItem(sku="982", quantity=2, price=5.0)]
    order_item_1 = items[0]
    order_item_2 = items[1]
    order.items.append(order_item_1)
    order.items.append(order_item_2)

    visit = PromaxOrderMapper()
    order_dict = order.accept(visit)
    assert (order_dict['order_id'] == '12345')
    assert(order_dict['seller_code'] == 'ABC')
    assert (order_dict['document'] == order_customer.document)
    assert (order_dict['seller_id'] == order.seller.id)
    assert (order_dict['integration_type'] == order.seller.get_integration_type().name)
    assert (order_dict['payment_code'] == "91")
    assert (order_dict['statuses'][0]['status'] == order_status.status.name)
    assert (order_dict['items'][0]['sku'] == order_item_1.sku)
    assert (order_dict['items'][0]['price'] == order_item_1.price)
    assert (order_dict['items'][0]['quantity'] == order_item_1.quantity)
    assert (order_dict['items'][1]['sku'] == order_item_2.sku)
    assert (order_dict['items'][1]['price'] == order_item_2.price)
    assert (order_dict['items'][1]['quantity'] == order_item_2.quantity)

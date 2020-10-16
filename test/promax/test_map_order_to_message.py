from menu_sun_api.domain.model.seller.seller import Seller, SellerMetafield, IntegrationType
from menu_sun_api.domain.model.customer.customer import Customer, CustomerMetafield
from menu_sun_api.domain.model.order.order import Order, OrderPaymentType, OrderItem, \
    OrderPayment
from datetime import datetime
from promax.application.map_order import MapOrderToMessage


def test_map_order_to_message():

    customer_metafield = CustomerMetafield(
        namespace="ADF", key="has_adf", value="true")

    seller = Seller(seller_code='ABC', integration_type=IntegrationType.PROMAX,
                    metafields=[SellerMetafield(key="BOLETO_10_ADF",
                                                value="91",
                                                namespace="CODIGO_PAGAMENTO"),
                                SellerMetafield(key="DINHEIRO",
                                                value="2",
                                                namespace="CODIGO_PAGAMENTO")
                                ])
    order_customer = Customer(document="10851803792", metafields=[customer_metafield]
                              )
    order = Order(order_id='12345',
                  order_date=datetime.utcnow(),
                  delivery_date=datetime.utcnow(),
                  customer=order_customer,
                  payments=[OrderPayment(deadline=10,
                                         payment_type=OrderPaymentType.BOLETO)
                            ],
                  seller=seller)
    order_item_1 = OrderItem(sku="988", quantity=2, price=10.0)
    order_item_2 = OrderItem(sku="982", quantity=2, price=10.0)
    order.items.append(order_item_1)
    order.items.append(order_item_2)

    visit = MapOrderToMessage()
    order_dict = order.accept(visit)
    assert(order_dict['seller_code'] == 'ABC')
    assert(order_dict['payment_code'] == "91")
    assert (order_dict['document'] == order_customer.document)

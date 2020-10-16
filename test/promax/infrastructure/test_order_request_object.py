from menu_sun_api.domain.model.order.order import Order, OrderItem,\
    OrderShippingAddress, OrderBillingAddress, OrderPayment, OrderPaymentType

from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_api.domain.model.customer.customer import Customer
from promax.infrastructure.promax.order_request import OrderRequest
from datetime import datetime
from menu_sun_api.domain.model.seller.seller import SellerMetafield
from promax.application.map_order import MapOrderToMessage


class TestOrderRequestObject():

    def test_should_build_order_from_json(self):
        seller = Seller(seller_code='ABC', metafields=[SellerMetafield(key="BOLETO_10",
                                                                       value="91",
                                                                       namespace="CODIGO_PAGAMENTO"),
                                                       SellerMetafield(key="DINHEIRO",
                                                                       value="2",
                                                                       namespace="CODIGO_PAGAMENTO")
                                                       ])
        order_customer = Customer(document="10851803792")
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

        mapper = MapOrderToMessage()
        order_dict = order.accept(mapper)

        order_request = OrderRequest.from_dict(order_dict)
        payload = order_request.payload
        assert(payload)

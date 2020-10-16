from datetime import datetime
import dateutil.parser

from menu_sun_api.domain import Default
from menu_sun_api.domain.model.order.order import Order, OrderMetafield
from menu_sun_integration.application.translators.interfaces.abstract_order_translator import AbstractOrderTranslator
from menu_sun_integration.infrastructure.brf.presentations.order.brf_order_post_request import \
    BRFOrderPostRequest, BRFOrderItemPostRequest, BRFOrderAddressPostRequest, BRFOrderCustomerPostRequest
from menu_sun_integration.infrastructure.brf.presentations.order.brf_order_response import BRFOrderResponse
from menu_sun_integration.infrastructure.brf.specification.commissioned.last_ordered_date_specification import \
    LastOrderedDateSpecification
from menu_sun_integration.infrastructure.brf.specification.commissioned.new_user_specification import \
    NewUserSpecification
from menu_sun_integration.presentations.order.abstract_order_detail_get_request import AbstractOrderDetailGetRequest
from menu_sun_integration.presentations.order.order_sqs_platform import OrderDetailSQSPlatform, OrderStatusSQSPlatform


class BRFOrderTranslator(AbstractOrderTranslator):
    def to_seller_send_format(self, order: OrderDetailSQSPlatform) -> BRFOrderPostRequest:
        order_date = dateutil.parser.parse(order.order_date).strftime('%Y-%m-%dT%H:%M:%S%Z')

        statuses = order.statuses[len(order.statuses)-1]

        status = (statuses or [OrderStatusSQSPlatform.from_dict(
            {"status": "", "updated_date": {order_date}})])

        order_items = [BRFOrderItemPostRequest(sku=item.sku, quantity=item.quantity, price=item.price, name=item.name,
                                               original_price=item.original_price)
                       for item in order.items]

        shipping_address = BRFOrderAddressPostRequest(street=order.shipping_address.street,
                                                      number=order.shipping_address.number,
                                                      complement1=order.shipping_address.complement,
                                                      complement2=order.shipping_address.reference,
                                                      complement3=order.shipping_address.reference,
                                                      neighborhood=order.shipping_address.neighborhood,
                                                      state_code=order.shipping_address.state_code,
                                                      city=order.shipping_address.city,
                                                      postal_code=order.shipping_address.postcode,
                                                      phone=order.customer.phone_number,
                                                      name=order.shipping_address.name)

        billing_address = BRFOrderAddressPostRequest(street=order.billing_address.street,
                                                     number=order.billing_address.number,
                                                     complement1=order.billing_address.complement,
                                                     complement2=order.billing_address.reference,
                                                     complement3=order.billing_address.reference,
                                                     neighborhood=order.billing_address.neighborhood,
                                                     state_code=order.billing_address.state_code,
                                                     city=order.billing_address.city,
                                                     postal_code=order.billing_address.postcode,
                                                     phone=order.customer.phone_number,
                                                     name=order.billing_address.name)

        order_customer = BRFOrderCustomerPostRequest(document=order.customer.document,
                                                     email=order.customer.email, name=order.customer.name,
                                                     postal_code=order.customer.cep)

        order_request = BRFOrderPostRequest(order_id=order.order_id, order_date=order_date,
                                            delivery_date=order.delivery_date, unb=order.seller_code, items=order_items,
                                            total=order.total, subtotal=order.subtotal, shipping=order.shipping,
                                            discount=order.discount, shipping_address=shipping_address,
                                            billing_address=billing_address, payment_code=order.payment_code,
                                            customer=order_customer, status=status.status)
        return order_request

    def to_seller_get_format(self, entity: Default, **kwargs) -> AbstractOrderDetailGetRequest:
        pass

    def to_domain_format(self, response: BRFOrderResponse) -> Order:
        metafield_customer_status = OrderMetafield(namespace='COMMISSION_ATTRIBUTES',
                                                   key="CUSTOMER_STATUS",
                                                   value=response.customer_status)

        metafield_last_ordered_date = OrderMetafield(namespace='COMMISSION_ATTRIBUTES',
                                                     key="LAST_ORDERED_DATE",
                                                     value=response.last_ordered_date.strftime('%Y%m%d'))

        must_be_commissioned = NewUserSpecification() | LastOrderedDateSpecification()
        return Order(integration_date=datetime.utcnow(), commissioned=must_be_commissioned.is_satisfied_by(response),
                     metafields=[metafield_customer_status, metafield_last_ordered_date])

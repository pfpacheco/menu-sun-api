from datetime import datetime

import dateutil.parser

from menu_sun_api.domain.model.order.order import Order, OrderMetafield
from menu_sun_integration.application.translators.interfaces.abstract_order_translator import AbstractOrderTranslator
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_detail_get_request import \
    PernodOrderDetailGetRequest
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_post_request import \
    PernodOrderPostRequest, PernodOrderItemPostRequest, PernodOrderAddressPostRequest, PernodOrderCustomerPostRequest, \
    PernodOrderStatusPostRequest
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_response import PernodOrderResponse
from menu_sun_integration.presentations.order.order_sqs_platform import OrderDetailSQSPlatform, OrderStatusSQSPlatform
from menu_sun_integration.shared.specification.always_commissioned_specification import AlwaysComissionedSpecification


class PernodOrderTranslator(AbstractOrderTranslator):
    def __init__(self):
        super().__init__()

    def to_seller_send_format(self, order: OrderDetailSQSPlatform) -> PernodOrderPostRequest:
        order_date = dateutil.parser.parse(order.order_date).strftime('%Y-%m-%dT%H:%M:%S%Z')
        delivery_date = dateutil.parser.parse(order.delivery_date).strftime('%Y-%m-%dT%H:%M:%S%Z')

        status_sorted = sorted(order.statuses, key=lambda item: item.updated_date, reverse=True)
        status = (status_sorted[:1] or [OrderStatusSQSPlatform.from_dict(
            {"status": "", "updated_date": {order_date}})])[0]

        order_items = [PernodOrderItemPostRequest(sku=item.sku, quantity=item.quantity, price=item.price,
                                                  name=item.name, original_price=item.original_price)
                       for item in order.items]

        shipping_address = PernodOrderAddressPostRequest(street=order.shipping_address.street,
                                                         number=order.shipping_address.number,
                                                         complement=order.shipping_address.complement,
                                                         reference=order.shipping_address.reference,
                                                         neighborhood=order.shipping_address.neighborhood,
                                                         state_code=order.shipping_address.state_code,
                                                         city=order.shipping_address.city,
                                                         country_code=order.shipping_address.country_code,
                                                         postcode=order.shipping_address.postcode,
                                                         name=order.shipping_address.name,
                                                         shipping_service=order.shipping_address.shipping_service,
                                                         shipping_provider=order.shipping_address.shipping_provider)

        billing_address = PernodOrderAddressPostRequest(street=order.billing_address.street,
                                                        number=order.billing_address.number,
                                                        complement=order.billing_address.complement,
                                                        reference=order.billing_address.reference,
                                                        neighborhood=order.billing_address.neighborhood,
                                                        state_code=order.billing_address.state_code,
                                                        city=order.billing_address.city,
                                                        country_code=order.billing_address.country_code,
                                                        postcode=order.billing_address.postcode,
                                                        name=order.billing_address.name,
                                                        shipping_service=order.shipping_address.shipping_service,
                                                        shipping_provider=order.shipping_address.shipping_provider)

        order_customer = PernodOrderCustomerPostRequest(name=order.customer.name, document=order.customer.document,
                                                        email=order.customer.email,
                                                        phone_number=order.customer.phone_number)

        order_status = PernodOrderStatusPostRequest(status=status.status, updated_date=status.updated_date)

        order_request = PernodOrderPostRequest(order_id=order.order_id, order_date=order_date,
                                               delivery_date=delivery_date, unb=order.seller_code, items=order_items,
                                               total=order.total, subtotal=order.subtotal, shipping=order.shipping,
                                               discount=order.discount, shipping_address=shipping_address,
                                               billing_address=billing_address, payment_code=order.payment_code,
                                               customer=order_customer,
                                               status=order_status, seller_id=order.seller_id)
        return order_request

    def to_seller_get_format(self, order: Order) -> PernodOrderDetailGetRequest:
        return PernodOrderDetailGetRequest(unb=order.seller.seller_code, cnpj=order.customer.document,
                                           order_id=order.order_id, seller_id=order.seller_id)

    def to_domain_format(self, response: PernodOrderResponse) -> Order:
        metafield_general_status = OrderMetafield(namespace='COMMISSION_ATTRIBUTES',
                                                  key="GENERAL_RULE",
                                                  value="ALWAYS_TRUE")
        must_be_commissioned = AlwaysComissionedSpecification()
        return Order(integration_date=datetime.utcnow(), commissioned=must_be_commissioned.is_satisfied_by(response),
                     metafields=[metafield_general_status], seller_order_id=response.seller_order_id)

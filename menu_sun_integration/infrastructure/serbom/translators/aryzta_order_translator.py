import os
from datetime import datetime
from menu_sun_api.domain import Default
from menu_sun_api.domain.model.order.order import Order
from menu_sun_integration.application.translators.interfaces.abstract_order_translator import AbstractOrderTranslator
from menu_sun_integration.infrastructure.serbom.presentations.order.serbom_order_post_request import \
    SerbomOrderPostOrderRequest, SerbomOrderItemPostRequest, SerbomOrderCustomerPostRequest, \
    SerbomOrderAddressPostRequest
from menu_sun_integration.infrastructure.serbom.presentations.order.serbom_order_response import SerbomOrderResponse
from menu_sun_integration.presentations.order.abstract_order_detail_get_request import AbstractOrderDetailGetRequest
from menu_sun_integration.presentations.order.order_sqs_platform import OrderDetailSQSPlatform


class AryztaOrderTranslator(AbstractOrderTranslator):

    def __init__(self):
        super().__init__()
        self.document_supplier = os.getenv('DOCUMENT_ARYZTA', "57016578000900")

    def to_seller_send_format(self, entity: OrderDetailSQSPlatform) -> SerbomOrderPostOrderRequest:
        customer = SerbomOrderCustomerPostRequest(document=entity.customer.document, name=entity.customer.name,
                                                  telephone=entity.customer.phone_number)

        items = [
            SerbomOrderItemPostRequest(sku=item.sku, name=item.name,
                                       quantity=item.quantity,
                                       price=item.price, weight=0, index=index)
            for index, item in enumerate(entity.items)]

        billing_address = SerbomOrderAddressPostRequest(street=entity.shipping_address.street,
                                                        number=entity.shipping_address.number,
                                                        complement=entity.shipping_address.complement,
                                                        neighborhood=entity.shipping_address.neighborhood,
                                                        state_code=entity.shipping_address.state_code,
                                                        city=entity.shipping_address.city,
                                                        name=entity.shipping_address.name,
                                                        postcode=entity.shipping_address.postcode)

        request_order = SerbomOrderPostOrderRequest(document_supplier=self.document_supplier,
                                                    order_increment=entity.order_id, order_id=entity.order_id,
                                                    document=entity.customer.document,
                                                    unb=entity.seller_code, items=items,
                                                    customer=customer, shipping_address=billing_address)

        return request_order

    def to_domain_format(self, response: SerbomOrderResponse) -> Order:
        return Order(integration_date=datetime.utcnow())

    def to_seller_get_format(self, entity: Default, **kwargs) -> AbstractOrderDetailGetRequest:
        raise NotImplementedError

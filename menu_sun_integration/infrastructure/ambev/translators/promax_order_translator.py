import dateutil.parser
from datetime import datetime, date

import pytz

from menu_sun_api.domain.model.order.order import Order
from menu_sun_integration.application.translators.interfaces.abstract_order_translator import AbstractOrderTranslator
from menu_sun_integration.infrastructure.ambev.presentations.order.promax_order_detail_get_request import \
    PromaxOrderDetailGetRequest
from menu_sun_integration.infrastructure.ambev.presentations.order.promax_order_post_request import \
    PromaxOrderPostRequest, PromaxOrderItemPostRequest
from menu_sun_integration.infrastructure.ambev.presentations.order.promax_order_response import PromaxOrderResponse
from menu_sun_integration.presentations.order.order_sqs_platform import OrderDetailSQSPlatform


class PromaxOrderTranslator(AbstractOrderTranslator):
    def to_seller_send_format(self, order: OrderDetailSQSPlatform) -> PromaxOrderPostRequest:
        order_items = [PromaxOrderItemPostRequest(item.sku, item.quantity, item.price) for item in order.items]

        tz = pytz.timezone('America/Sao_Paulo')

        order_date_parse = dateutil.parser.parse(order.order_date)
        order_date = pytz.utc.localize(order_date_parse).astimezone(tz).strftime('%d/%m/%Y')

        delivery_date_parse = dateutil.parser.parse(order.delivery_date)
        delivery_date = pytz.utc.localize(delivery_date_parse).astimezone(tz).strftime('%d/%m/%Y')

        order_request = PromaxOrderPostRequest(order.order_id, order.document, order_date, delivery_date,
                                               order.seller_code, order.payment_code, order_items)
        return order_request

    def to_seller_get_format(self, order: Order) -> PromaxOrderDetailGetRequest:
        order_id = order.order_id.replace("M", "7")
        return PromaxOrderDetailGetRequest(order.seller.seller_code, order.customer.document, order_id)

    def to_domain_format(self, response: PromaxOrderResponse) -> Order:
        return Order(integration_date=datetime.utcnow())

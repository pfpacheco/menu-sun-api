from datetime import datetime
from menu_sun_api.domain.model.order.order import Order, OrderStatus, OrderStatusType

from menu_sun_integration.application.translators.interfaces.abstract_order_status_translator import \
    AbstractOrderStatusTranslator

from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_status_put_request import \
    PernodOrderStatusPutRequest
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_status_put_response import \
    PernodOrderStatusPutResponse
from menu_sun_integration.presentations.order.order_status_sqs_platform import OrderStatusDetailSQSPlatform


class PernodOrderStatusTranslator(AbstractOrderStatusTranslator):

    def to_seller_put_format(self, order: OrderStatusDetailSQSPlatform) -> PernodOrderStatusPutRequest:
        status = order.status
        if status == 'PENDING_INVOICE':
            status = 'APPROVED'
        return PernodOrderStatusPutRequest(seller_order_id=order.seller_order_id, seller_id=order.seller_id,
                                           status=status, status_id=order.status_id,
                                           order_id=order.order_id, comments=order.comments)

    def to_domain_format(self, response: PernodOrderStatusPutResponse) -> Order:
        status = OrderStatus(id=response.status_id, published_date=response.published_date())
        return Order(updated_date=datetime.utcnow(),
                     statuses=[status])

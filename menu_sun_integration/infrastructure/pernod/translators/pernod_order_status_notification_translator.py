from datetime import datetime
from menu_sun_api.domain.model.order.order import Order, OrderStatus, OrderMetafield, OrderStatusType
from menu_sun_integration.application.translators.interfaces.abstract_order_status_notification_translator import \
    AbstractOrderStatusNotificationTranslator
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_status_notification_get_request import \
    PernodOrderStatusNotificationGetRequest
from menu_sun_integration.infrastructure.pernod.presentations.order.pernod_order_status_notification_response import \
    PernodOrderStatusNotificationResponse


class PernodOrderStatusNotificationTranslator(AbstractOrderStatusNotificationTranslator):

    def to_seller_get_format(self, order: Order) -> PernodOrderStatusNotificationGetRequest:
        return PernodOrderStatusNotificationGetRequest(order_id=order.order_id, seller_id=order.seller_id)

    def to_domain_format(self, response: PernodOrderStatusNotificationResponse) -> Order:
        if response.status.code.upper() == 'COMPLETED' or response.status.code.upper() == 'SHIPPED':
            status_code = 'COMPLETE'
        elif response.status.code.upper() == 'DELIVERED':
            status_code = 'ENTREGUE'
        else:
            status_code = response.status.code.upper()

        status = OrderStatus(status=OrderStatusType.get_value(status_code),
                             comments=response.status.information)
        
        return Order(updated_date=datetime.utcnow(),
                     statuses=[status])

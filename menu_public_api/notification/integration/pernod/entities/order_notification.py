import json
from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_api.domain.model.order.order import Order
from menu_sun_integration.shared.mappers.factory_mapper import FactoryMapper
from menu_sun_integration.infrastructure.aws.sqs.order_status_notification_sqs_queue import OrderStatusNotificationSQSQueue
from menu_public_api.notification.application.entities.order_notification_strategy import OrderStrategyInterface


class PernodOrderNotification(OrderStrategyInterface):

    def _translate_entity_notification(self, seller: Seller, payload: dict) -> str:
        resource_list = payload['Resource'].split('/')
        order_id = resource_list[-1]
        seller_mapper = FactoryMapper.get_instance().get_mapper(
            integration_type=seller.integration_type.name,
            entity="seller")

        order_notification_mapper = FactoryMapper.get_instance().get_mapper(
            integration_type=seller.integration_type.name,
            entity="order_notification")

        order = Order(order_id=order_id, seller_id=seller.id)

        seller_dict = seller.accept(seller_mapper)
        order_dict = order.accept(order_notification_mapper)
        enqueue_dict = {**order_dict, **seller_dict}
        body = json.dumps(enqueue_dict)

        return body

    def enqueue_entity(self, seller: Seller, payload: dict) -> bool:
        body = self._translate_entity_notification(seller, payload)
        queue = OrderStatusNotificationSQSQueue()

        if queue.enqueue(body=body) is None:
            return False
        return True

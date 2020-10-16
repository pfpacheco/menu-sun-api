from typing import Optional

from menu_sun_api.domain.model.seller.seller import Seller

from menu_public_api.notification.application.notification_seller_strategy_interface \
    import NotificationStrategyInterface
from menu_public_api.notification.application.mapper.notification_entities_factory \
    import FactoryNotificationEntitiesMapper


class PernodNotification(NotificationStrategyInterface):

    def enqueue_notification(self, seller: Seller, payload: dict) -> Optional:
        pernod_entity_notification = FactoryNotificationEntitiesMapper.get_instance().get_mapper(
            integration_type='PERNOD', entity=payload['Topic'])
        pernod_notification = pernod_entity_notification.enqueue_entity(seller=seller, payload=payload)

        return pernod_notification

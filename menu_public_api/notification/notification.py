from typing import Optional, Dict

from menu_public_api.notification.application.notification_seller_strategy_interface \
    import NotificationStrategyInterface


class Notification(NotificationStrategyInterface):

    def __init__(self, notification_stategy_interface: NotificationStrategyInterface):
        self.__notification_stategy_interface = notification_stategy_interface

    def enqueue_notification(self, seller: dict, payload: dict) -> Optional[Dict]:
        return self.__notification_stategy_interface.enqueue_notification(seller=seller, payload=payload)

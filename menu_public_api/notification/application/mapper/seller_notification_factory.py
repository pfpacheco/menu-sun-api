from typing import Optional
from menu_public_api.notification.integration.pernod.pernod_notification import PernodNotification
from menu_sun_integration.application.mappers.interfaces.abstract_mapper import AbstractMapper


class FactorySellerNotification:
    __instance = None

    @staticmethod
    def get_instance():
        if FactorySellerNotification.__instance is None:
            FactorySellerNotification()
        return FactorySellerNotification.__instance

    def __init__(self):
        if FactorySellerNotification.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self._notification = {"PERNOD": PernodNotification()}

            FactorySellerNotification.__instance = self

    def get_notification(self, integration_type: str) -> Optional[AbstractMapper]:
        notification = self._notification.get(integration_type)
        return notification

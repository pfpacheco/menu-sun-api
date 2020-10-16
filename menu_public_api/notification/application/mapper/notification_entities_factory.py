from typing import Optional
from menu_public_api.notification.integration.pernod.entities.inventory_notification import PernodInventoryNotification
from menu_public_api.notification.integration.pernod.entities.order_notification import PernodOrderNotification
from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_integration.application.mappers.interfaces.abstract_mapper import AbstractMapper


class FactoryNotificationEntitiesMapper:
    __instance = None

    @staticmethod
    def get_instance():
        if FactoryNotificationEntitiesMapper.__instance is None:
            FactoryNotificationEntitiesMapper()
        return FactoryNotificationEntitiesMapper.__instance

    def __init__(self):
        if FactoryNotificationEntitiesMapper.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self._mappers = {"PERNOD": {"Orders": PernodOrderNotification(),
                                        "Inventory": PernodInventoryNotification(product_service=ProductRepository())}
                             }

            FactoryNotificationEntitiesMapper.__instance = self

    def get_mapper(self, integration_type: str, entity: str) -> Optional[AbstractMapper]:
        mappers = self._mappers.get(integration_type)
        return mappers.get(entity)

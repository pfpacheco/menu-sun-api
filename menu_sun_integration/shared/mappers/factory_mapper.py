from typing import Optional

from menu_sun_integration.application.mappers.base_customer_mapper import BaseCustomerMapper
from menu_sun_integration.application.mappers.base_seller_mapper import BaseSellerMapper
from menu_sun_integration.application.mappers.interfaces.abstract_mapper import AbstractMapper
from menu_sun_integration.infrastructure.ambev.mappers.promax_order_mapper import PromaxOrderMapper
from menu_sun_integration.infrastructure.pernod.mappers.pernod_order_mapper import PernodOrderMapper
from menu_sun_integration.infrastructure.pernod.mappers.pernod_order_status_mapper import PernodOrderStatusMapper
from menu_sun_integration.infrastructure.pernod.mappers.pernod_product_mapper import PernodProductNotificationMapper
from menu_sun_integration.infrastructure.pernod.mappers.pernod_order_notification_mapper import \
    PernodOrderNotificationMapper
from menu_sun_integration.infrastructure.brf.mappers.brf_order_mapper import BRFOrderMapper
from menu_sun_integration.infrastructure.serbom.mappers.serbom_order_mapper import SerbomOrderMapper


class FactoryMapper:
    __instance = None

    @staticmethod
    def get_instance():
        if FactoryMapper.__instance is None:
            FactoryMapper()
        return FactoryMapper.__instance

    def __init__(self):
        if FactoryMapper.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self._mappers = {"BRF": {"customer": BaseCustomerMapper(),
                                     "customer_pricing": BaseCustomerMapper(),
                                     "order": BRFOrderMapper(),
                                     "inventory": BaseSellerMapper(),
                                     "product_default_pricing": BaseSellerMapper(),
                                     "product": BaseSellerMapper(),
                                     "seller": BaseSellerMapper(),
                                     },
                             "PERNOD": {"order": PernodOrderMapper(),
                                        "order_notification": PernodOrderNotificationMapper(),
                                        "product_notification": PernodProductNotificationMapper(),
                                        "order_status": PernodOrderStatusMapper(),
                                        "order_status_notification": PernodOrderMapper(),
                                        "product": BaseSellerMapper(),
                                        "inventory_by_sku": BaseSellerMapper(),
                                        "product_default_pricing_by_sku": BaseSellerMapper(),
                                        "seller": BaseSellerMapper(),
                                        },
                             "PROMAX": {"order": PromaxOrderMapper()},
                             "ARYZTA": {"order": SerbomOrderMapper(), 
                                        "product_default_pricing": BaseSellerMapper()},
                             "BENJAMIN": {"order": SerbomOrderMapper(),
                                          "product_default_pricing": BaseSellerMapper()}
                             }

            FactoryMapper.__instance = self

    def register_mapper(self, integration_type: str, entity: str, mapper: AbstractMapper):
        self._mappers[integration_type] = {entity: mapper}

    def get_mapper(self, integration_type: str, entity: str) -> Optional[AbstractMapper]:
        mappers = self._mappers.get(integration_type)
        return mappers.get(entity)

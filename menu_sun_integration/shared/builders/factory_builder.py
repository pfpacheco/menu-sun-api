from typing import Optional

from menu_sun_integration.application.builders.interfaces.abstract_builder import AbstractBuilder
from menu_sun_integration.application.builders.not_implemented_builder import NotImplementedBuilder
from menu_sun_integration.infrastructure.ambev.builders.promax_order_builder import PromaxOrderBuilder
from menu_sun_integration.infrastructure.brf.builders.brf_customer_builder import BRFCustomerBuilder
from menu_sun_integration.infrastructure.brf.builders.brf_customer_pricing_builder import BRFCustomerPricingBuilder
from menu_sun_integration.infrastructure.brf.builders.brf_inventory_builder import BRFInventoryBuilder
from menu_sun_integration.infrastructure.brf.builders.brf_order_builder import BRFOrderBuilder
from menu_sun_integration.infrastructure.brf.builders.brf_product_builder import BRFProductBuilder
from menu_sun_integration.infrastructure.brf.builders.brf_product_default_price_builder import \
    BRFProductDefaultPricingBuilder
from menu_sun_integration.infrastructure.pernod.builders.pernod_inventory_builder import PernodInventoryBuilder
from menu_sun_integration.infrastructure.pernod.builders.pernod_order_builder import PernodOrderBuilder
from menu_sun_integration.infrastructure.pernod.builders.pernod_product_builder import PernodProductBuilder
from menu_sun_integration.infrastructure.pernod.builders.pernod_product_default_price_builder import \
    PernodProductDefaultPricingBuilder
from menu_sun_integration.infrastructure.pernod.builders.pernod_order_status_notification_builder import\
    PernodOrderStatusNotificationBuilder
from menu_sun_integration.infrastructure.pernod.builders.pernod_order_status_builder import \
    PernodOrderStatusBuilder
from menu_sun_integration.infrastructure.serbom.builders.aryzta_order_builder import AryztaOrderBuilder
from menu_sun_integration.infrastructure.serbom.builders.aryzta_product_default_pricing_builder import \
    AryztaProductDefaultPricingBuilder
from menu_sun_integration.infrastructure.serbom.builders.benjamin_order_builder import BenjaminOrderBuilder
from menu_sun_integration.infrastructure.serbom.builders.benjamin_product_default_pricing_builder import \
    BenjaminProductDefaultPricingBuilder


class FactoryBuilder:
    __instance = None

    @staticmethod
    def get_instance():
        if FactoryBuilder.__instance is None:
            FactoryBuilder()
        return FactoryBuilder.__instance

    def __init__(self):
        if FactoryBuilder.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self._builder = {'PROMAX': {'order': PromaxOrderBuilder()},
                             'PERNOD': {'order': PernodOrderBuilder(),
                                        'order_status_notification': PernodOrderStatusNotificationBuilder(),
                                        'order_status': PernodOrderStatusBuilder(),
                                        'product': PernodProductBuilder(),
                                        'inventory_by_sku': PernodInventoryBuilder(),
                                        'product_default_pricing_by_sku': PernodProductDefaultPricingBuilder()},
                             'BRF': {'order': BRFOrderBuilder(), 'customer': BRFCustomerBuilder(),
                                     'product': BRFProductBuilder(),
                                     'customer_pricing': BRFCustomerPricingBuilder(),
                                     'product_default_pricing': BRFProductDefaultPricingBuilder(),
                                     'inventory': BRFInventoryBuilder()},
                             'ARYZTA': {'order': AryztaOrderBuilder(),
                                        'product_default_pricing': AryztaProductDefaultPricingBuilder()},
                             'BENJAMIN': {'order': BenjaminOrderBuilder(),
                                          'product_default_pricing': BenjaminProductDefaultPricingBuilder()}}
            FactoryBuilder.__instance = self

    def register_builder(self, integration_type: str, entity: str, builder: AbstractBuilder):
        self._builder[integration_type] = {entity: builder}

    def get_builder(self, integration_type: str, entity: str) -> Optional[AbstractBuilder]:
        _builders = self._builder.get(integration_type)

        if not _builders:
            return NotImplementedBuilder()

        return _builders.get(entity)

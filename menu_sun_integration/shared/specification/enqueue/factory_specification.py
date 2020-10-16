from typing import Optional

from menu_sun_api.shared.specification import Specification
from menu_sun_integration.infrastructure.serbom.specification.enqueue.serbom_order_specification_base import \
    SerbomOrderSpecificationBase
from menu_sun_integration.shared.specification.enqueue.customer_specification_base import CustomerSpecificationBase
from menu_sun_integration.shared.specification.enqueue.order_specification_base import OrderSpecificationBase
from menu_sun_integration.shared.specification.enqueue.order_status_specification_credit_menu_base import OrderStatusSpecificationCreditMenuBase
from menu_sun_integration.shared.specification.enqueue.order_specification_credit_hybrid_base import \
    OrderSpecificationCreditHybridBase
from menu_sun_integration.shared.specification.enqueue.order_specification_credit_menu_base import \
    OrderSpecificationCreditMenuBase
from menu_sun_integration.shared.specification.enqueue.order_specification_credit_pre_approved_base import \
    OrderSpecificationCreditPreApprovedBase
from menu_sun_integration.shared.specification.enqueue.order_specification_credit_seller_base import \
    OrderSpecificationCreditSellerBase
from menu_sun_integration.shared.specification.enqueue.seller_specification_base import SellerSpecificationBase


class FactorySpecification:
    __instance = None

    @staticmethod
    def get_instance():
        if FactorySpecification.__instance is None:
            FactorySpecification()

        return FactorySpecification.__instance

    def __init__(self):
        if FactorySpecification.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self._specifications = {
                "BRF": {"customer": CustomerSpecificationBase(),
                        "customer_pricing": CustomerSpecificationBase(),
                        "order": OrderSpecificationCreditHybridBase(),
                        "inventory": SellerSpecificationBase(),
                        "product_default_pricing": SellerSpecificationBase(),
                        "product": SellerSpecificationBase(),
                        },
                "PERNOD": {"order": OrderSpecificationCreditMenuBase(),
                           "order_status_notification": OrderSpecificationBase(),
                           "order_status": OrderStatusSpecificationCreditMenuBase(),
                           "product": SellerSpecificationBase(),
                           "product_default_pricing_by_sku": SellerSpecificationBase(),
                           "inventory_by_sku": SellerSpecificationBase()
                           },
                "PROMAX": {"order": OrderSpecificationCreditPreApprovedBase()},
                "ARYZTA": {"order": SerbomOrderSpecificationBase(),
                           "product_default_pricing": SellerSpecificationBase()},
                "BENJAMIN": {"order": OrderSpecificationCreditSellerBase(),
                             "product_default_pricing": SellerSpecificationBase()}
            }
            FactorySpecification.__instance = self

    def register_specification(self, integration_type: str, entity: str, specification: Specification):
        self._specifications[integration_type] = {entity: specification}

    def get_specification(self, integration_type: str, entity: str) -> Optional[Specification]:
        specifications = self._specifications.get(integration_type)
        if not specifications:
            return None

        return specifications.get(entity)

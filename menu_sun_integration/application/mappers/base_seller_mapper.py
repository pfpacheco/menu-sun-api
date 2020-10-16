from typing import Optional, Dict

from menu_sun_api.domain.model.seller.seller import Seller, SellerMetafield
from menu_sun_integration.application.mappers.interfaces.abstract_mapper import AbstractMapper


class BaseSellerMapper(AbstractMapper):
    def visit(self, entity) -> Optional[Dict]:
        if isinstance(entity, Seller):

            if entity.metafields:
                metafields = [i.accept(self) for i in entity.metafields]
            else:
                metafields = []

            return {"seller_id": entity.id, "seller_code": entity.seller_code,
                    "seller_metafields": metafields, "integration_type": entity.get_integration_type().name}

        if isinstance(entity, SellerMetafield):
            return {
                "namespace": entity.namespace,
                "key": entity.key,
                "value": entity.value
            }

        return None

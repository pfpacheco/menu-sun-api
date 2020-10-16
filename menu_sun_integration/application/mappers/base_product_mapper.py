from typing import Optional, Dict

from menu_sun_api.domain.model.product.product import Product
from menu_sun_integration.application.mappers.interfaces.abstract_mapper import AbstractMapper


class BaseProductMapper(AbstractMapper):
    def visit(self, entity) -> Optional[Dict]:
        if isinstance(entity, Product):
            return {"sku": entity.sku}

        return None

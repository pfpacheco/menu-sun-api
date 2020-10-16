from menu_sun_api.domain.model.product.product import Product
from menu_sun_integration.application.mappers.base_product_mapper import BaseProductMapper


class PernodProductNotificationMapper(BaseProductMapper):
    def __init__(self, base_mapper: BaseProductMapper = BaseProductMapper()):
        self._base_mapper = base_mapper

    def visit(self, entity):

        if isinstance(entity, Product):
            general_message = self._base_mapper.visit(entity)
            pernod_message = {
                "sku": entity.sku,
                "seller_id": entity.seller_id,
            }

            return {**general_message, **pernod_message}

        return None

import json
import logging

from menu_sun_api.domain.model.product.product import Product
from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.domain.model.seller.seller import Seller
from menu_public_api.notification.application.entities.inventory_notification_strategy import InventoryStrategyInterface
from menu_sun_integration.shared.mappers.factory_mapper import FactoryMapper
from menu_sun_integration.infrastructure.aws.sqs.inventory_sqs_queue import InventorySQSQueue

logger = logging.getLogger()


class PernodInventoryNotification(InventoryStrategyInterface):
    def __init__(self, product_service: ProductRepository):
        super().__init__(product_service=product_service)

    def _translate_entity_notification(self, seller: Seller, payload: dict) -> str:
        sku = payload['Sku']
        product = self._service.get_by_sku(seller_id=seller.id, sku=sku)

        if not product:
            return ""

        seller_mapper = FactoryMapper.get_instance().get_mapper(
            integration_type=seller.integration_type.name,
            entity="seller")

        product_mapper = FactoryMapper.get_instance().get_mapper(
            integration_type=seller.integration_type.name,
            entity="product_notification")

        product = Product(sku=sku, seller_id=seller.id)
        product_dict = product.accept(product_mapper)

        seller_dict = seller.accept(seller_mapper)
        enqueue_dict = {**product_dict, **seller_dict}
        body = json.dumps(enqueue_dict)

        return body

    def enqueue_entity(self, seller: Seller, payload: dict) -> bool:
        body = self._translate_entity_notification(seller, payload)
        if not body:
            return False

        queue = InventorySQSQueue()

        if queue.enqueue(body=body) is None:
            return False
        return True

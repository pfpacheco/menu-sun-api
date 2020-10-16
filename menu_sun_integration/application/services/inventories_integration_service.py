from typing import Callable

from menu_sun_api.domain.model.product.product import Product
from menu_sun_api.domain.model.product.product_service import ProductService
from menu_sun_api.domain.model.seller.seller import Seller, SellerMetafield
from menu_sun_integration.application.adapters.inventories_adapter import InventoriesAdapter
from menu_sun_integration.application.services.interfaces.abstract_inventories_service import AbstractInventoriesService
from menu_sun_integration.infrastructure.aws.sqs.interfaces.abstract_inventories_platform_queue import \
    AbstractInventoriesPlatformQueue
from menu_sun_integration.presentations.inventory.abstract_inventory_response import AbstractInventoryResponse
from menu_sun_integration.presentations.seller.abstract_seller_platform import AbstractSellerMessagePlatform


class InventoriesIntegrationService(AbstractInventoriesService):
    def __init__(self, session=None, platform_service: AbstractInventoriesPlatformQueue = None,
                 adapter: InventoriesAdapter = None, product_service: ProductService = None):
        super().__init__(entity='inventory', platform_service=platform_service, adapter=adapter,
                         domain_service=product_service,
                         session=session)

    def __update_products(self, products_in_database: [Product]) -> Callable:
        def __update(updates: AbstractInventoryResponse) -> Product:
            try:
                [product] = (item for item in products_in_database if updates.sku == item.sku)
                product.update(self._adapter.get_domain(updates))

                self._logger.info(entity_id=updates.sku,
                                  key='inventories_integration_service', description="inventories_updated_from_seller",
                                  payload=product)

                return product

            except Exception as e:
                self._logger.error(entity_id=updates.sku,
                                   key='inventories_integration_service', description="inventories_not_updated_from_seller",
                                   payload=e)

        return __update

    def __mark_as_processed(self, message: AbstractSellerMessagePlatform):
        self._logger.update_entity("inventories_by_seller")

        seller = message.body
        has_processed = self._platform_service.processed(message.identifier)
        if has_processed:
            self._logger.info(entity_id=seller.seller_id, key='inventories_integration_service',
                              description="inventories_queue_message_processed", payload=seller)
        else:
            self._logger.error(entity_id=seller.seller_id, key='inventories_integration_service',
                               description="inventories_queue_message_not_processed", payload=seller)

        return has_processed

    def update_inventories_from_seller(self) -> None:
        inventories_messages = self._platform_service.dequeue()
        for inventory_message in inventories_messages:
            inventory = inventory_message.body
            super().bind_adapter(inventory.integration_type)
            super().bind_logger(integration_type=inventory.integration_type, entity="inventories_by_seller",
                                seller_id=inventory.seller_id, seller_code=inventory.seller_code,
                                entity_id=inventory.seller_id)
            if not self._adapter:
                self._logger.warn(key='inventories_integration_service', description="adapter_not_implemented",
                                  payload=inventory)

                self.__mark_as_processed(inventory_message)

                continue

            metafields = map(lambda metafield: SellerMetafield(namespace=metafield.namespace,
                                                               key=metafield.key, value=metafield.value),
                             inventory.seller_metafields)

            inventory_response = self._adapter.get_from_seller(Seller(id=inventory.seller_id,
                                                                      metafields=list(metafields)))
            if not inventory_response.succeeded:
                self._logger.warn(key='inventories_integration_service', description="inventories_not_found_from_seller",
                                  payload=inventory_response)

                self.__mark_as_processed(inventory_message)

                continue

            self._logger.update_entity("product")

            try:

                inventories_in_response = inventory_response.get_inventories()
                products_in_database = set(self._domain_service.load_all(seller_id=inventory.seller_id).value)

                # UPDATE ALL PRODUCTS
                products_to_update = products_in_database.intersection(inventories_in_response)
                update_product = self.__update_products(products_in_database)

                entities_to_update = list(map(lambda product_to_update: update_product(updates=product_to_update),
                                              products_to_update))

                self._session.bulk_save_objects(entities_to_update)
                self._session.commit()

                self.__mark_as_processed(inventory_message)

            except Exception as e:
                self._session.rollback()
                self._logger.update_entity("inventories_by_seller")
                self._logger.error(entity_id=inventory.seller_id,
                                   key='inventories_integration_service',
                                   description="inventories_integration_service_error", payload=e)

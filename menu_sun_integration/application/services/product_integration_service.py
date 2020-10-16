from typing import Callable

from menu_sun_api.domain.model.product.product import Product
from menu_sun_api.domain.model.product.product_service import ProductService
from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_integration.application.adapters.product_adapter import ProductAdapter
from menu_sun_integration.application.services.interfaces.abstract_product_service import AbstractProductService
from menu_sun_integration.infrastructure.aws.sqs.interfaces.abstract_product_platform_queue import \
    AbstractProductPlatformQueue
from menu_sun_integration.presentations.product.abstract_product_response import AbstractProductResponse
from menu_sun_integration.presentations.seller.abstract_seller_platform import AbstractSellerMessagePlatform


class ProductIntegrationService(AbstractProductService):
    def __init__(self, session=None, platform_service: AbstractProductPlatformQueue = None,
                 adapter: ProductAdapter = None, product_service: ProductService = None):
        super().__init__('product', platform_service=platform_service, adapter=adapter, domain_service=product_service,
                         session=session)

    def __insert_product(self, seller_id: int, product_response: AbstractProductResponse) -> Product:
        try:
            product = self._adapter.get_domain(product_response)
            product.seller_id = seller_id
            self._logger.info(entity_id=product_response.sku, key='product_integration_service',
                              description="product_inserted_from_seller", payload=product_response)

            return product

        except Exception as e:
            self._logger.error(entity_id=product_response.sku, key='product_integration_service',
                               description="product_not_inserted_from_seller", payload=e)

    def __update_products(self, products_in_database: [Product]) -> Callable:
        def __update(updates: AbstractProductResponse) -> Product:
            try:
                [product] = (item for item in products_in_database if updates.sku == item.sku)

                product.update(self._adapter.get_domain(updates))

                self._logger.info(entity_id=updates.sku,
                                  key='product_integration_service', description="product_updated_from_seller",
                                  payload=updates)

                return product

            except Exception as e:
                self._logger.error(entity_id=updates.sku,
                                   key='product_integration_service', description="product_not_updated_from_seller",
                                   payload=e)

        return __update

    def __mark_as_processed(self, message: AbstractSellerMessagePlatform):
        self._logger.update_entity("product_by_seller")

        seller = message.body
        has_processed = self._platform_service.processed(message.identifier)
        if has_processed:
            self._logger.info(entity_id=seller.seller_id,
                              key='product_integration_service', description="product_queue_message_processed",
                              payload=seller)
        else:
            self._logger.error(entity_id=seller.seller_id,
                               key='product_integration_service', description="product_queue_message_not_processed",
                               payload=seller)
        return has_processed

    def update_products_from_seller(self) -> None:
        products_messages = self._platform_service.dequeue()
        for product_message in products_messages:
            product = product_message.body
            super().bind_adapter(product.integration_type)
            super().bind_logger(integration_type=product.integration_type, entity="product_by_seller",
                                seller_id=product.seller_id, seller_code=product.seller_code,
                                entity_id=product.seller_id)

            if not self._adapter:
                self._logger.warn(key='product_integration_service', description="adapter_not_implemented",
                                  payload=product)
                self.__mark_as_processed(product_message)

                continue

            product_response = self._adapter.get_from_seller(Seller(id=product.seller_id))
            if not product_response.succeeded:
                self._logger.warn(key='product_integration_service', description="products_not_found_into_seller",
                                  payload=product_response)

                self.__mark_as_processed(product_message)
                continue

            self._logger.update_entity("product")

            try:

                products_in_response = product_response.get_products()
                products_in_database = set(self._domain_service.load_all(seller_id=product.seller_id).value)

                products_to_insert = (set(products_in_response).difference(products_in_database))
                # ADD ALL NEW PRODUCTS

                entities_to_insert = list(map(lambda product_to_insert:
                                              self.__insert_product(seller_id=product.seller_id,
                                                                    product_response=product_to_insert),
                                              products_to_insert))

                self._session.bulk_save_objects(entities_to_insert)
                self._session.commit()
                # UPDATE ALL PRODUCTS
                products_to_update = products_in_database.intersection(products_in_response)
                update_product = self.__update_products(products_in_database)

                entities_to_update = list(map(lambda product_to_update: update_product(updates=product_to_update),
                                              products_to_update))

                self._session.bulk_save_objects(entities_to_update)
                self._session.commit()

                self.__mark_as_processed(product_message)

            except Exception as e:
                self._session.rollback()
                self._logger.update_entity("product_by_seller")
                self._logger.error(entity_id=product.seller_id,
                                   key='product_integration_service', description="product_integration_service_error",
                                   payload=e)


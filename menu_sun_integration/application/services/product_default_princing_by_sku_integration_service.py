from typing import Callable

from menu_sun_api.domain.model.product.product import Product
from menu_sun_api.domain.model.product.product_service import ProductService
from menu_sun_integration.application.adapters.product_default_pricing_by_sku_adapter import \
    ProductDefaultPricingBySkuAdapter
from menu_sun_integration.application.services.interfaces.abstract_product_default_pricing_by_sku_service import \
    AbstractProductDefaultPricingBySkuService
from menu_sun_integration.infrastructure.aws.sqs.interfaces.abstract_default_pricing_by_sku_plataform_queue import \
    AbstractDefaultPricingBySkuPlatformQueue
from menu_sun_integration.presentations.pricing.abstract_pricing_response import AbstractPricingResponse
from menu_sun_integration.presentations.seller.abstract_seller_platform import \
    AbstractSellerMessagePlatform


class ProductDefaultPricingBySkuIntegrationService(AbstractProductDefaultPricingBySkuService):
    def __init__(self, session=None, platform_service: AbstractDefaultPricingBySkuPlatformQueue = None,
                 adapter: ProductDefaultPricingBySkuAdapter = None, product_service: ProductService = None):
        super().__init__('product_default_pricing_by_sku', platform_service=platform_service, adapter=adapter,
                         domain_service=product_service,
                         session=session)

    def __mark_as_processed(self, message: AbstractSellerMessagePlatform):
        self._logger.update_entity("product_default_pricing_by_sku")
        pricing = message.body
        has_processed = self._platform_service.processed(message.identifier)
        if has_processed:
            self._logger.info(entity_id=pricing.seller_id, key='product_default_pricing_by_sku_integration_service',
                              description="product_default_pricing_by_sku_message_processed", payload=pricing)
        else:
            self._logger.error(entity_id=pricing.seller_id, key='product_default_pricing__by_sku_integration_service',
                               description="product_default_pricing_by_sku_queue_message_not_processed", payload=pricing)
        return has_processed

    def __update_products(self, products_in_database: [Product]) -> Callable:

        def __update(updates: AbstractPricingResponse) -> Product:
            try:
                [product] = (item for item in products_in_database if updates.sku == item.sku)
                product.update(self._adapter.get_domain(updates))
                self._logger.info(entity_id=updates.sku,
                                  key='product_default_pricing_by_sku_integration_service',
                                  description="product__updated_from_seller", payload=product)

                return product

            except Exception as e:
                self._logger.error(entity_id=updates.sku,
                                   key='product_default_pricing_by_sku_integration_service',
                                   description="product_not_updated_from_seller", payload=e)

        return __update

    def update_price_from_seller(self) -> None:
        default_pricing_messages = self._platform_service.dequeue()
        for default_pricing_message in default_pricing_messages:
            pricing = default_pricing_message.body
            super().bind_adapter(pricing.integration_type)
            super().bind_logger(integration_type=pricing.integration_type, entity="product_default_pricing_by_sku",
                                seller_id=pricing.seller_id, seller_code=pricing.seller_code,
                                entity_id=pricing.sku)

            if not self._adapter:
                self._logger.warn(key='product_default_pricing_by_sku_integration_service',
                                  description="adapter_not_implemented", payload=pricing)
                self.__mark_as_processed(default_pricing_message)
                continue

            default_pricing_response = self._adapter.get_from_seller(Product(sku=pricing.sku))
            if not default_pricing_response.succeeded:
                self._logger.info(key='product_default_pricing_by_sku_integration_service',
                                  description="pricing_not_found_from_seller", payload=pricing)

                self.__mark_as_processed(default_pricing_message)
                continue

            self._logger.update_entity("product")

            try:

                prices_in_response = default_pricing_response.get_pricing()
                products_in_database = set(self._domain_service.load_all(seller_id=pricing.seller_id).value)

                # UPDATE ALL PRODUCTS
                products_to_update = products_in_database.intersection(prices_in_response)
                update_product = self.__update_products(products_in_database)

                entities_to_update = list(map(lambda product_to_update: update_product(updates=product_to_update),
                                              products_to_update))

                self._session.bulk_save_objects(entities_to_update)
                self._session.commit()

                self.__mark_as_processed(default_pricing_message)

            except Exception as e:
                self._session.rollback()
                self._logger.update_entity("product_pricing_by_sku")
                self._logger.error(entity_id=pricing.seller_id,
                                   key='product_default_pricing_by_sku_integration_service',
                                   description="product_default_pricing_by_sku_integration_service_error", payload=e)

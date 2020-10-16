from menu_sun_api.domain.model.customer.customer import Customer
from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository
from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.domain.model.pricing.pricing import Pricing
from menu_sun_api.domain.model.pricing.pricing_repository import PricingRepository
from menu_sun_integration.application.adapters.customer_pricing_adapter import CustomerPricingAdapter
from menu_sun_integration.application.services.interfaces.abstract_customer_pricing_service import \
    AbstractPricingByCustomerService
from menu_sun_integration.infrastructure.aws.sqs.interfaces.abstract_pricing_platform_queue import \
    AbstractPricingPlatformQueue
from menu_sun_integration.presentations.customer.abstract_customer_message_platform import \
    AbstractCustomerMessagePlatform


class CustomerPricingIntegrationService(AbstractPricingByCustomerService):
    def __init__(self, session=None, platform_service: AbstractPricingPlatformQueue = None,
                 adapter: CustomerPricingAdapter = None, pricing_service: PricingRepository = None):
        super().__init__('customer_pricing', platform_service=platform_service, domain_service=pricing_service,
                         session=session, adapter=adapter)

    def __update_pricing(self, pricing: Pricing, pricing_updates: Pricing):
        try:
            pricing.update(pricing_updates)

            self._logger.info(key='customer_pricing_integration_service', description="pricing_updated_from_seller",
                              payload=pricing)

            self._session.commit()

            return True
        except Exception as e:
            self._session.rollback()
            self._logger.error(key='customer_pricing_integration_service',
                               description="pricing_not_updated_from_seller",
                               payload=e)
            return False

    def __insert_pricing(self, customer_id: int, product_id: int, pricing: Pricing):
        try:
            pricing.customer_id = customer_id
            pricing.product_id = product_id

            self._domain_service.add(pricing)

            self._logger.info(key='customer_pricing_integration_service', description="pricing_inserted_from_seller",
                              payload=pricing)

            self._session.commit()

            return True
        except Exception as e:
            self._session.rollback()
            self._logger.error(key='customer_pricing_integration_service',
                               description="pricing_not_inserted_from_seller",
                               payload=e)

            return False

    def __mark_as_processed(self, message: AbstractCustomerMessagePlatform):
        self._logger.update_entity("customer_pricing")

        customer = message.body
        has_processed = self._platform_service.processed(message.identifier)
        if has_processed:
            self._logger.info(entity_id=customer.document, key='customer_pricing_integration_service',
                              description="customer_pricing_queue_message_processed", payload=customer)
        else:
            self._logger.error(entity_id=customer.document, key='customer_pricing_integration_service',
                               description="customer_pricing_message_not_processed", payload=customer)
        return has_processed

    def update_customer_pricing_from_seller(self) -> None:
        pricing_messages = self._platform_service.dequeue()
        for pricing_message in pricing_messages:
            pricing = pricing_message.body
            super().bind_adapter(pricing.integration_type)
            super().bind_logger(integration_type=pricing.integration_type, entity="customer_pricing",
                                seller_id=pricing.seller_id, seller_code=pricing.seller_code,
                                entity_id=pricing.document)

            customer_repository = CustomerRepository(session=self._session)
            customer = customer_repository.get_by_document_and_seller_code(seller_code=pricing.seller_code,
                                                                           document=pricing.document)

            if not self._adapter:
                self._logger.warn(key='customer_pricing_integration_service', description="adapter_not_implemented",
                                  payload=pricing)

                self.__mark_as_processed(pricing_message)

                continue

            pricing_response = self._adapter.get_from_seller(
                customer=Customer(document=pricing.document, cep=customer.cep))

            if not pricing_response.succeeded:
                self._logger.warn(key='customer_pricing_integration_service',
                                  description="pricing_not_found_from_seller",
                                  payload=pricing_response)
                self.__mark_as_processed(pricing_message)
                continue

            self._logger.update_entity("pricing")

            prices_in_response = set(pricing_response.get_pricing())

            for price_to_insert in prices_in_response:
                product_repository = ProductRepository(session=self._session)
                product = product_repository.get_by_sku_and_seller_code(seller_code=pricing.seller_code,
                                                                        sku=price_to_insert.sku)
                if product:
                    pricing_updates = self._adapter.get_domain(price_to_insert)
                    pricing_to_rs = self._domain_service.get_pricing_by_seller_code(seller_code=pricing.seller_code,
                                                                                    sku=price_to_insert.sku,
                                                                                    document=pricing.document)
                    if pricing_to_rs:
                        self.__update_pricing(pricing=pricing_to_rs, pricing_updates=pricing_updates)
                    else:
                        self.__insert_pricing(customer_id=customer.id, product_id=product.id, pricing=pricing_updates)

                self.__mark_as_processed(pricing_message)

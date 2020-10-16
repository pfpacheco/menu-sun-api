from menu_sun_api.domain.model.customer.customer import Customer
from menu_sun_api.domain.model.customer.customer_service import CustomerService
from menu_sun_integration.application.adapters.customer_adapter import CustomerAdapter
from menu_sun_integration.application.services.interfaces.abstract_customer_service import AbstractCustomerService
from menu_sun_integration.infrastructure.aws.sqs.interfaces.abstract_customer_platform_queue import \
    AbstractCustomerPlatformQueue
from menu_sun_integration.presentations.customer.abstract_customer_message_platform import \
    AbstractCustomerMessagePlatform


class CustomerIntegrationService(AbstractCustomerService):
    def __init__(self, session=None, platform_service: AbstractCustomerPlatformQueue = None,
                 adapter: CustomerAdapter = None, customer_service: CustomerService = None):
        super().__init__('customer', platform_service=platform_service, adapter=adapter,
                         domain_service=customer_service,
                         session=session)

    def __mark_as_processed(self, message: AbstractCustomerMessagePlatform):
        customer = message.body
        has_processed = self._platform_service.processed(message.identifier)
        if has_processed:
            self._logger.info(key='customer_integration_service',
                              description="customer_queue_message_processed", payload=customer)
        else:
            self._logger.error(key='customer_integration_service',
                               description="customer_queue_message_not_processed", payload=customer)
        return has_processed

    def __update_customer(self, customer: Customer, customer_updated: Customer):
        try:
            for payment in customer_updated.payment_terms:
                customer.value.change_payment_terms(payment)

            for metafield in customer_updated.metafields:
                customer.value.change_metafield(metafield)
            customer.value.update(customer_updated)
            self._session.commit()
            return True
        except Exception as e:
            self._session.rollback()
            return False

    def update_customer_from_seller(self) -> None:
        customer_messages = self._platform_service.dequeue()
        for customer_message in customer_messages:
            customer = customer_message.body
            super().bind_adapter(customer.integration_type)
            super().bind_logger(integration_type=customer.integration_type, entity="customer",
                                seller_id=customer.seller_id, seller_code=customer.seller_code,
                                entity_id=customer.document)

            customer_by_document = self._domain_service.get_by_document_and_seller_code(
                seller_code=customer.seller_code,
                document=customer.document)
            customer_response_by_document = customer_by_document.value

            if not self._adapter:
                self._logger.warn(key='customer_integration_service', description="adapter_not_implemented",
                                  payload=customer)
                self.__mark_as_processed(customer_message)
                continue

            customer_response = self._adapter.get_from_seller(
                Customer(id=customer_response_by_document.id,
                         document=customer_response_by_document.document,
                         cep=customer_response_by_document.cep,
                         seller_id=customer.seller_id))

            if not customer_response.succeeded:
                self._logger.info(key='customer_integration_service', description="customer_not_found_from_seller",
                                  payload=customer)

                self.__mark_as_processed(customer_message)

                continue

            customer_response = customer_response.get_customer()
            customer_updated = self._adapter.get_domain(customer_response)

            result = self.__update_customer(customer_by_document, customer_updated)

            if result:
                self._logger.info(key='customer_integration_service', description="customer_updated_from_seller",
                                  payload=customer)
            else:
                self._logger.error(key='customer_integration_service', description="customer_not_updated_from_seller",
                                   payload=customer)

            self.__mark_as_processed(customer_message)

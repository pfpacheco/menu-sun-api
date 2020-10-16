import json

from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository
from menu_sun_api.domain.model.response.failure_response import FailureResponse
from menu_sun_integration.application.services.interfaces.abstract_platform_service import AbstractPlatformService
from menu_sun_api.domain.model.response.success_response import SuccessResponse
from menu_sun_integration.infrastructure.aws.sqs.interfaces.abstract_platform_queue import AbstractPlatformQueue
from menu_sun_integration.shared.mappers.factory_mapper import FactoryMapper
from menu_sun_integration.shared.specification.enqueue.factory_specification import FactorySpecification


class CustomerPlatformService(AbstractPlatformService):
    def __init__(self, platform_service: AbstractPlatformQueue, customer_repository: CustomerRepository,
                 session, entity: str = 'customer'):
        super().__init__(entity, platform_service=platform_service, repository=customer_repository, session=session)

    def enqueue(self, seller):
        super().bind_logger(integration_type=seller.integration_type.name, entity="customer",
                            seller_id=seller.id, seller_code=seller.seller_code,
                            entity_id=seller.id)

        specification = FactorySpecification.get_instance().get_specification(
            integration_type=seller.integration_type.name,
            entity=self._entity)

        msgs = []

        if not specification:
            self._logger.warn(key='customer_platform_service', description="specification_not_implemented",
                              payload=seller)
            return

        customers = self._repository.filter_by_specification(seller_id=seller.id, specification=specification)

        if customers:
            for customer in customers:
                try:
                    self._logger.update_entity("customer")
                    customer_mapper = FactoryMapper.get_instance().get_mapper(
                        integration_type=seller.integration_type.name,
                        entity=self._entity)
                    seller_mapper = FactoryMapper.get_instance().get_mapper(
                        integration_type=seller.integration_type.name,
                        entity="seller")

                    customer_dict = customer.accept(customer_mapper)
                    seller_dict = seller.accept(seller_mapper)

                    enqueue_dict = {**customer_dict, **seller_dict}
                    body = json.dumps(enqueue_dict)

                    self._logger.info(entity_id=customer.document,
                                      key='customer_platform_service', description="enqueue_customer",
                                      payload=enqueue_dict)

                    message_id = self._platform_service.enqueue(body=body)
                    if not message_id:
                        return FailureResponse()
                    else:
                        msgs.append(message_id)
                        self._logger.info(entity_id=customer.document,
                                          key='customer_platform_service', description="enqueued_customer",
                                          payload=enqueue_dict)
                except Exception as e:
                    self._logger.error(entity_id=customer.document,
                                       key='customer_platform_service',
                                       description="enqueue_customer_error_exception_detail",
                                       payload=e)

        return SuccessResponse(msgs)

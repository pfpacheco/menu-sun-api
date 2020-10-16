import json
from datetime import datetime

from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_api.domain.model.response.failure_response import FailureResponse
from menu_sun_integration.application.services.interfaces.abstract_platform_service import AbstractPlatformService
from menu_sun_api.domain.model.response.success_response import SuccessResponse
from menu_sun_integration.infrastructure.aws.sqs.interfaces.abstract_platform_queue import AbstractPlatformQueue
from menu_sun_integration.shared.mappers.factory_mapper import FactoryMapper
from menu_sun_integration.shared.specification.enqueue.factory_specification import FactorySpecification


class OrderStatusPlatformService(AbstractPlatformService):
    def __init__(self, platform_service: AbstractPlatformQueue, order_repository: OrderRepository):
        super().__init__('order_status', platform_service=platform_service, repository=order_repository,
                         session=None)

    def enqueue(self, seller):
        super().bind_logger(integration_type=seller.integration_type.name, entity="order_status",
                            seller_id=seller.id, seller_code=seller.seller_code,
                            entity_id=seller.id)

        specification = FactorySpecification.get_instance().get_specification(
            integration_type=seller.integration_type.name,
            entity=self._entity)

        msgs = []

        if not specification:
            self._logger.warn(key='order_status_platform_service', description="specification_not_implemented",
                              payload=seller)
            return

        orders = self._repository.filter_by_specification(seller_id=seller.id, specification=specification)

        if orders:
            for order in orders:
                try:

                    mapper = FactoryMapper.get_instance().get_mapper(integration_type=seller.integration_type.name,
                                                                     entity=self._entity)
                    order_dict = order.accept(mapper)

                    self._logger.info(entity_id=order.order_id,
                                      key='order_status_platform_service_body_dict_to_json',
                                      description="order_status_platform_service_body",
                                      payload="dict to json ---> {0}".format(order_dict))
                    body = json.dumps(order_dict)
                    self._logger.info(entity_id=order.order_id,
                                      key='order_status_platform_service', description="enqueue_order",
                                      payload=order_dict)

                    message_id = self._platform_service.enqueue(body=body)
                    if not message_id:
                        return FailureResponse()
                    else:
                        msgs.append(message_id)

                        self._logger.info(entity_id=order.order_id,
                                          key='order_status_platform_service', description="enqueued_order_status",
                                          payload=order_dict)

                except Exception as e:
                    self._logger.error(entity_id=order.order_id,
                                       key='order_status_platform_service',
                                       description="enqueue_order_status_error_exception_detail",
                                       payload=e)
        return SuccessResponse(msgs)

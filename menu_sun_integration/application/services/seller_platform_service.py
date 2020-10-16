import json

from menu_sun_api.domain.model.response.failure_response import FailureResponse
from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_api.domain.model.seller.seller_repository import SellerRepository
from menu_sun_integration.application.services.interfaces.abstract_platform_service import AbstractPlatformService
from menu_sun_api.domain.model.response.success_response import SuccessResponse
from menu_sun_integration.infrastructure.aws.sqs.interfaces.abstract_platform_queue import AbstractPlatformQueue
from menu_sun_integration.shared.mappers.factory_mapper import FactoryMapper
from menu_sun_integration.shared.specification.enqueue.factory_specification import FactorySpecification


class SellerPlatformService(AbstractPlatformService):
    def __init__(self, platform_service: AbstractPlatformQueue, seller_repository: SellerRepository,
                 session, entity: str = 'seller'):
        super().__init__(entity, platform_service=platform_service, repository=seller_repository, session=session)

    def enqueue(self, seller_dummy: Seller):
        super().bind_logger(integration_type=seller_dummy.integration_type.name, entity="seller",
                            seller_id=seller_dummy.id, seller_code=seller_dummy.seller_code,
                            entity_id=seller_dummy.id)

        specification = FactorySpecification.get_instance().get_specification(
            integration_type=seller_dummy.integration_type.name,
            entity=self._entity)

        msgs = []

        if not specification:
            self._logger.warn(key='seller_platform_service', description="specification_not_implemented",
                              payload=seller_dummy)
        else:
            sellers = self._repository.filter_by_specification(seller_id=seller_dummy.id, specification=specification)

            if sellers:
                for seller in sellers:
                    try:
                        seller_mapper = FactoryMapper.get_instance().get_mapper(
                            integration_type=seller.integration_type.name,
                            entity=self._entity)

                        seller_dict = seller.accept(seller_mapper)

                        enqueue_dict = seller_dict
                        body = json.dumps(enqueue_dict)

                        self._logger.info(key='seller_platform_service', description="enqueue_seller",
                                          payload=enqueue_dict)
                        message_id = self._platform_service.enqueue(body=body)
                        if not message_id:
                            return FailureResponse()
                        else:
                            msgs.append(message_id)
                            self._logger.info(key='seller_platform_service', description="enqueued_seller",
                                              payload=enqueue_dict)
                    except Exception as e:
                        self._logger.error(key='seller_platform_service',
                                           description="enqueue_seller_error_exception_detail",
                                           payload=e)
        return SuccessResponse(msgs)

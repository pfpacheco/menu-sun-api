from menu_sun_api.application.order_service import OrderService
from menu_sun_api.domain.model.order.order import Order
from menu_sun_integration.application.adapters.order_adapter import OrderAdapter
from menu_sun_integration.infrastructure.aws.sqs.interfaces.abstract_order_platform_queue import \
    AbstractOrderPlatformQueue
from menu_sun_integration.presentations.interfaces.abstract_order_message_platform import AbstractOrderMessagePlatform
from menu_sun_integration.application.services.interfaces.abstract_order_service import AbstractOrderService
from menu_sun_integration.presentations.order.abstract_order_detail_get_response import AbstractOrderDetailGetResponse
from menu_sun_integration.presentations.order.abstract_order_response import AbstractOrderResponse


class OrderIntegrationService(AbstractOrderService):
    def __init__(self, session=None, platform_service: AbstractOrderPlatformQueue = None,
                 adapter: OrderAdapter = None, order_service: OrderService = None):
        super().__init__('order', platform_service=platform_service, adapter=adapter, domain_service=order_service,
                         session=session)

    def __update(self, order: Order, updates: AbstractOrderResponse):
        try:
            order_updates = self._adapter.get_domain(updates)
            order.update(order_updates)
            for metafield in order_updates.metafields:
                order.change_metafield(metafield)
            self._logger.info(key='order_integration_service', description="order_updated_from_seller",
                              payload=order)

            self._session.commit()
            return True
        except Exception as e:
            self._logger.error(key='order_integration_service', description="order_not_updated_from_seller",
                               payload=e)

            return False

    def __mark_as_processed(self, message: AbstractOrderMessagePlatform):
        order = message.body
        has_processed = self._platform_service.processed(message.identifier)
        if has_processed:
            self._logger.info(key='order_integration_service', description="order_queue_message_processed",
                              payload=order)
        else:
            self._logger.error(key='order_integration_service', description="order_queue_message_not_processed",
                               payload=order)
        return has_processed

    def post_orders_to_seller(self) -> None:
        order_messages = self._platform_service.dequeue()
        for order_message in order_messages:
            order = order_message.body
            super().bind_adapter(order.integration_type)
            super().bind_logger(integration_type=order.integration_type, entity="order",
                                seller_id=order.seller_id, seller_code=order.seller_code,
                                entity_id=order.order_id)

            if not self._adapter:
                self._logger.warn(key='order_integration_service', description="adapter_not_implemented",
                                  payload=order)
                return None

            order_response = self._adapter.send_to_seller(order)

            if order_response.succeeded:
                order_to_update = self._domain_service.get_order(seller_id=order.seller_id, order_id=order.order_id)
                has_integrated = self.__update(order=order_to_update.value, updates=order_response.get_order())
                if has_integrated:
                    self.__mark_as_processed(order_message)

    def get_order_from_seller(self, order: Order) \
            -> AbstractOrderDetailGetResponse:
        super().bind_adapter(order.seller.get_integration_type().name)
        return self._adapter.get_from_seller(order)

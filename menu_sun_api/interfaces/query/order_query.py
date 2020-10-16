import graphene
import os
import sys
import logging
import json

from graphene import ObjectType

from menu_sun_api.interfaces.definition.order import Order
from menu_sun_api.application.order_service import OrderService
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_integration.application.services.order_integration_service import OrderIntegrationService
from promax.application.status_synchronizer_service import StatusSynchronizerService

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../menu_sun_api/vendored"))

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class OrderQuery(ObjectType):
    orders = graphene.List(Order, offset=graphene.Int(), limit=graphene.Int())
    order = graphene.Field(Order, order_id=graphene.String(required=True))
    pending_orders = graphene.List(
        Order, offset=graphene.Int(), limit=graphene.Int())
    load_orders_to_integrated_by_order_id = graphene.Field(
        Order, orderId=graphene.String(required=True))

    def resolve_order(parent, info, order_id, **kwargs):
        repository = OrderRepository()
        order_service = OrderService(repository)
        seller = info.context.get('seller')
        order = order_service.get_order(seller_id=seller.id, order_id=order_id)
        return order.value

    def resolve_orders(self, info, **kwargs):
        repository = OrderRepository()
        offset = kwargs.get('offset')
        limit = kwargs.get('limit')
        order_service = OrderService(repository)
        seller = info.context.get('seller')
        orders = order_service.load_all(
            seller_id=seller.id, limit=limit, offset=offset)
        return orders.value

    def resolve_load_orders_to_integrated_by_order_id(
            self, info, orderId, **kwargs):
        global session
        try:

            session = Session()
            seller = info.context.get('seller')
            order_repository = OrderRepository()
            integration_service = OrderIntegrationService(session=session)
            status_sync = StatusSynchronizerService(integration_service=integration_service,
                                                    order_repository=order_repository)

            logger.info('Syncronizing orders_to_integrated_by_order_id...')
            status_sync.sync_all_pending_orders_by_order_id(seller_id=seller.id,
                                                            seller_code=seller.seller_code,
                                                            integration_type=seller.integration_type,
                                                            order_id=orderId)

            session.commit()
            order_service = OrderService(order_repository)
            order = order_service.get_order(
                seller_id=seller.id, order_id=orderId)

            return order.value
        except Exception as e:
            logger.error(e)
            session.rollback()
            raise

        finally:
            session.close()

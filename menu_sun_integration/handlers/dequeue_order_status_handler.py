import os
import sys
import logging

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from menu_sun_integration.application.services.order_status_integration_service import \
    OrderStatusIntegrationService
from menu_sun_integration.infrastructure.aws.sqs.order_status_sqs_queue import OrderStatusSQSQueue
from menu_sun_api.application.order_service import OrderService
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_api.infrastructure.connection_factory import Session


def handler(event, context):
    session = Session()

    try:
        order_status_sqs_queue = OrderStatusSQSQueue()
        domain_repository = OrderRepository()
        domain_service = OrderService(repository=domain_repository)
        integration_service = OrderStatusIntegrationService(session, platform_service=order_status_sqs_queue,
                                                            order_service=domain_service)
        integration_service.put_orders_to_seller()

    except Exception as e:
        logger.error(str(e))
        session.rollback()
        raise
    finally:
        session.close()

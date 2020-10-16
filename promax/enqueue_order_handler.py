import logging
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../menu_sun_api/vendored"))

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from promax.application.order_integration_service import OrderIntegrationService
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.seller.seller_repository import SellerRepository
from promax.infrastructure.sqs.order_queue import OrderQueue
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_api.application.order_service import OrderService


def handler(event, context):
    session = Session()
    try:
        order_queue_url = os.getenv("ORDER_QUEUE_URL")
        order_queue = OrderQueue(queue_url=order_queue_url)

        order_service = OrderService(OrderRepository(session))
        seller_repository = SellerRepository()
        order_integration_service = OrderIntegrationService(order_service=order_service,
                                                            order_queue=order_queue)

        sellers = seller_repository.load_all_sellers()
        logger.info('Enqueuing orders...')
        for seller in sellers:
            logger.info('Checking order for seller id [{}]'.format(seller.id))
            order_integration_service.enqueue_pending_orders(
                seller_id=seller.id)
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()

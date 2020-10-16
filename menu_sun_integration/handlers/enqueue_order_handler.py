import logging
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_integration.application.services.order_platform_service import OrderPlatformService
from menu_sun_integration.infrastructure.aws.sqs.order_sqs_queue import OrderSQSQueue
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.seller.seller_repository import SellerRepository


def handler(event, context):
    session = Session()
    try:
        queue = OrderSQSQueue()
        seller_repository = SellerRepository()
        platform_service = OrderPlatformService(session=session, order_repository=OrderRepository(session),
                                                platform_service=queue)

        sellers = seller_repository.load_all_sellers()
        logger.info('Enqueuing orders...')
        for seller in sellers:
            logger.info('Checking order for seller id [{}]'.format(seller.id))
            platform_service.enqueue(seller=seller)
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()

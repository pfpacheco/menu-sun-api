import logging
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from menu_sun_integration.application.services.seller_platform_service import SellerPlatformService
from menu_sun_integration.infrastructure.aws.sqs.product_sqs_queue import ProductSQSQueue
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.seller.seller_repository import SellerRepository


def handler(event, context):
    session = Session()
    try:
        queue = ProductSQSQueue()
        seller_repository = SellerRepository(session)
        platform_service = SellerPlatformService(entity='product', session=session, seller_repository=seller_repository,
                                                 platform_service=queue)

        sellers = seller_repository.load_all_sellers()
        logger.info('Enqueuing orders...')
        for seller in sellers:
            logger.info('Checking product for seller id [{}]'.format(seller.id))
            platform_service.enqueue(seller)
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()

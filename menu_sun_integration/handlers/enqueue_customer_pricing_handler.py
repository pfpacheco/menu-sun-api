import logging
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository
from menu_sun_integration.application.services.customer_platform_service import CustomerPlatformService
from menu_sun_integration.infrastructure.aws.sqs.pricing_sqs_queue import PricingSQSQueue
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.seller.seller_repository import SellerRepository


def handler(event, context):
    session = Session()
    try:
        queue = PricingSQSQueue()
        seller_repository = SellerRepository(session)
        platform_service = CustomerPlatformService(entity="customer_pricing", session=session,
                                                   customer_repository=CustomerRepository(session),
                                                   platform_service=queue)

        sellers = seller_repository.load_all_sellers()
        logger.info('Enqueuing pricings...')
        for seller in sellers:
            logger.info('Checking pricing for seller id [{}]'.format(seller.id))
            platform_service.enqueue(seller)
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()

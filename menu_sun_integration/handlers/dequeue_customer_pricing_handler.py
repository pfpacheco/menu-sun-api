import os
import sys
import logging

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.pricing.pricing_repository import PricingRepository
from menu_sun_integration.infrastructure.aws.sqs.pricing_sqs_queue import PricingSQSQueue
from menu_sun_integration.application.services.customer_pricing_integration_service import \
    CustomerPricingIntegrationService


def handler(event, context):
    session = Session()

    try:
        pricing_sqs_queue = PricingSQSQueue()
        domain_repository = PricingRepository()
        pricing_service = CustomerPricingIntegrationService(session=session, pricing_service=domain_repository,
                                                            platform_service=pricing_sqs_queue)

        pricing_service.update_customer_pricing_from_seller()

    except Exception as e:
        logger.error(str(e))
        session.rollback()
        raise
    finally:
        session.close()

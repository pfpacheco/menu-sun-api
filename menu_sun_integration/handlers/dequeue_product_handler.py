import os
import sys
import logging

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.domain.model.product.product_service import ProductService
from menu_sun_integration.application.services.product_integration_service import ProductIntegrationService
from menu_sun_integration.infrastructure.aws.sqs.product_sqs_queue import ProductSQSQueue


def handler(event, context):
    session = Session()

    try:
        product_sqs_queue = ProductSQSQueue()
        domain_repository = ProductRepository()
        domain_service = ProductService(repository=domain_repository)
        integration_service = ProductIntegrationService(session, platform_service=product_sqs_queue,
                                                        product_service=domain_service)
        integration_service.update_products_from_seller()

    except Exception as e:
        logger.error(str(e))
        session.rollback()
        raise
    finally:
        session.close()

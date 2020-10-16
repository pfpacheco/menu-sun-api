import os
import sys
import logging

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository
from menu_sun_api.domain.model.customer.customer_service import CustomerService
from menu_sun_integration.application.services.customer_integration_service import CustomerIntegrationService
from menu_sun_integration.infrastructure.aws.sqs.customer_sqs_queue import CustomerSQSQueue


def handler(event, context):
    session = Session()

    try:
        customer_sqs_queue = CustomerSQSQueue()
        domain_repository = CustomerRepository()
        domain_service = CustomerService(repository=domain_repository)
        integration_service = CustomerIntegrationService(session, platform_service=customer_sqs_queue,
                                                         customer_service=domain_service)
        integration_service.update_customer_from_seller()

    except Exception as e:
        logger.error(str(e))
        session.rollback()
        raise
    finally:
        session.close()

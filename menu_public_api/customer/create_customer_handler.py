import json
import os
import sys
import logging

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))

from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository
from menu_sun_api.command.customer.customer_create_command import CustomerCreateCommand, \
    CustomerCreateCommandHandler
from menu_sun_api.interfaces.authenticator import Authenticator

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event, context):
    session = Session()
    customer = json.loads(event['body'])
    logger.info(event)
    seller = Authenticator.authenticate(event)
    customer_repository = CustomerRepository(session)
    command = CustomerCreateCommand(customer=customer,
                                    seller_id=seller.id)
    handler = CustomerCreateCommandHandler(
        customer_repository=customer_repository,
        session=session)

    res = handler.execute(command)

    if res:
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    'document': res.value.document,
                    'email': res.value.email,
                    'name': res.value.name,
                    'credit_limit': res.value.credit_limit,
                    'phone_number': res.value.phone_number,
                }
            ),
        }
    else:
        return {
            "statusCode": 404
        }

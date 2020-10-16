import json
import os
import sys
import logging

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))

from menu_sun_api.application.customer_service import CustomerService
from menu_sun_api.domain.model.customer.customer_repository import CustomerRepository
from menu_sun_api.interfaces.authenticator import Authenticator

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event, context):
    logger.info(event)
    seller = Authenticator.authenticate(event)
    document = json.loads(event['queryStringParameters']['document'])
    repository = CustomerRepository()
    customer_service = CustomerService(repository)
    customer = customer_service.get_by_document(seller_id=seller.id, document=document)

    if customer.value:
        order_json = {
            "statusCode": 200,
            "body": json.dumps(
                {

                    'document': customer.value.document,
                    'email': customer.value.email,
                    'name': customer.value.name,
                    'credit_limit': customer.value.credit_limit,
                    'phone_number': customer.value.phone_number,
                }
            ),
        }

        return order_json
    else:
        return {"statusCode": 404}

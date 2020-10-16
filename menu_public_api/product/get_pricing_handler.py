import json
import os
import sys
import logging

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))

from menu_sun_api.domain.model.pricing.pricing_repository import PricingRepository
from menu_sun_api.interfaces.authenticator import Authenticator

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event, context):
    logger.info(event)
    seller = Authenticator.authenticate(event)
    repository = PricingRepository()
    pricing = repository.get_pricing(seller_id=seller.id,
                                     document=event['queryStringParameters']['document'],
                                     sku=event['queryStringParameters']['sku'])

    if pricing:
        order_json = {
            "statusCode": 200,
            "body": json.dumps(
                {
                    'sku': event['queryStringParameters']['sku'],
                    'document': event['queryStringParameters']['document'],
                    'list_price': pricing.list_price,
                    'sale_price': pricing.sale_price,
                }
            ),
        }

        return order_json
    else:
        return {"statusCode": 404}

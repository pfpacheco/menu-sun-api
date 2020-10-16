import json
import os
import sys
import logging

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))

from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.interfaces.authenticator import Authenticator

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event, context):
    logger.info(event)
    seller = Authenticator.authenticate(event)
    repository = ProductRepository()
    product = repository.get_by_sku(seller_id=seller.id,
                                    sku=event['queryStringParameters']['sku'])
    logger.info({"seller_id": seller.id, "sku": event['queryStringParameters']['sku']})
    logger.info(product)
    if product:
        product_json = {
            "statusCode": 200,
            "body": json.dumps(
                product.to_dict()
            ),
        }

        return product_json
    else:
        return {"statusCode": 404}

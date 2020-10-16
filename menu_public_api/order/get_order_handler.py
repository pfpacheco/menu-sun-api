import json
import os
import sys
import logging

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))

from menu_sun_api.application.order_service import OrderService
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_api.interfaces.authenticator import Authenticator

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event, context):

    logger.info(event)
    seller = Authenticator.authenticate(event)
    order_id = event['queryStringParameters']['order_id']

    if order_id:

        repository = OrderRepository()
        order_service = OrderService(repository)
        order = order_service.get_order(seller_id=seller.id, order_id=order_id)

        if order.value:
            order_json = {
                "statusCode": 200,
                "body": json.dumps(
                    order.value.to_dict()
                ),
            }

            return order_json
        else:
            return {"statusCode": 404}

    return {"statusCode": 422}

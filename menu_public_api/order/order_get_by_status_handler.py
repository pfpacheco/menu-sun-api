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
    status = event['queryStringParameters']['status']

    try:

        if status:

            repository = OrderRepository()
            order_service = OrderService(repository)
            orders = order_service.list_orders_by_status(seller_id=seller.id, status=status)
            body = json.dumps([])
            if orders.value:
                body = json.dumps(list(map(lambda order: order.to_dict(), orders.value)))

            return {
                "statusCode": 200,
                "body": body,
            }

        return {"statusCode": 422}
    except Exception as e:
        return {"statusCode": 500, "exception": e}

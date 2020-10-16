import json
import os
import sys
import logging


here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))

from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.command.product.product_create_command import ProductCreateCommand, \
    ProductCreateCommandHandler
from menu_sun_api.interfaces.authenticator import Authenticator


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event, context):
    session = Session()
    product = json.loads(event['body'])
    logger.info(event)
    seller = Authenticator.authenticate(event)
    product_repository = ProductRepository(session)
    command = ProductCreateCommand(product=product,
                                   seller_id=seller.id)
    handler = ProductCreateCommandHandler(
        product_repository=product_repository,
        session=session)

    res = handler.execute(command)

    if res:
        return {
            "statusCode": 200,
            "body": json.dumps(
                res.value.to_dict()
            ),
        }
    else:
        return {
            "statusCode": 404
        }

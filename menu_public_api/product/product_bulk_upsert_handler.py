import json
import os
import sys
import logging


here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))

from menu_sun_api.command.product.product_bulk_upsert_command import ProductBulkUpsertCommandHandler, \
    ProductBulkUpsertCommand
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.product.product_repository import ProductRepository
from menu_sun_api.interfaces.authenticator import Authenticator

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event, context):
    session = Session()
    product_list = json.loads(event['body'])
    logger.info(event)
    seller = Authenticator.authenticate(event)
    product_repository = ProductRepository(session)
    command = ProductBulkUpsertCommand(product_list=product_list,
                                       seller_id=seller.id)
    handler = ProductBulkUpsertCommandHandler(
        product_repository=product_repository,
        session=session)

    res = handler.execute(command)

    if res:
        return {
            "statusCode": 200,
            "body": json.dumps(list(map(lambda product: product.to_dict(), res.value))),
        }
    else:
        return {
            "statusCode": 404
        }

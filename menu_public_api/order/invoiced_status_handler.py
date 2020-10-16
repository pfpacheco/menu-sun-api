import json
import os
import sys
import logging

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))

from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.command.order.order_invoice_command import OrderInvoiceCommand, OrderInvoiceCommandHandler
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_api.interfaces.authenticator import Authenticator
from menu_sun_api.domain.model.order.order import OwnerType

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event, context):
    session = Session()
    logger.info(event)
    seller = Authenticator.authenticate(event)
    body = json.loads(event['body'])
    order_repository = OrderRepository()
    command = OrderInvoiceCommand(seller_id=seller.id, order_id=body.get('order_id'))
    handler = OrderInvoiceCommandHandler(order_repository=order_repository, session=session, owner=OwnerType.SELLER)

    rs = handler.execute(command)
    if rs:
        return {
            "statusCode": 200,
            "body": json.dumps(body),
        }
    else:
        return {
            "statusCode": 404}

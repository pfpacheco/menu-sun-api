import json
import os
import sys
import logging


here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))

from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.pricing.pricing_repository import PricingRepository
from menu_sun_api.command.pricing.pricing_update_command import PricingUpdateCommandHandler, \
    PricingUpdateCommand
from menu_sun_api.interfaces.authenticator import Authenticator

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event, context):
    session = Session()
    pricing = json.loads(event['body'])
    logger.info(event)
    seller = Authenticator.authenticate(event)
    pricing_repository = PricingRepository(session)
    command = PricingUpdateCommand(pricing=pricing,
                                   seller_id=seller.id)

    handler = PricingUpdateCommandHandler(
        pricing_repository=pricing_repository,
        session=session)

    res = handler.execute(command)

    if res:
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    'list_price': res.value.list_price,
                    'sale_price': res.value.sale_price,
                    'sku': pricing.get('sku'),
                    'document': pricing.get('document')
                }
            ),
        }
    else:
        return {
            "statusCode": 404
        }

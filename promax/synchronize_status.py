import logging
import os
import sys

from menu_sun_integration.application.services.order_integration_service import OrderIntegrationService

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../menu_sun_api/vendored"))

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from promax.infrastructure.promax.http_promax import HttpPromax
from promax.infrastructure.promax.promax_service import PromaxService
from promax.application.status_synchronizer_service import StatusSynchronizerService
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.seller.seller_repository import SellerRepository
from menu_sun_api.domain.model.order.order_repository import OrderRepository


def handler(event, context):
    session = Session()
    try:

        promax_ip = os.getenv("PROMAX_IP")
        promax_password = os.getenv('PROMAX_PASSWORD')
        promax_userid = os.getenv('PROMAX_USER_ID')
        http_promax = HttpPromax(domain=promax_ip)
        order_repository = OrderRepository()

        integration_service = OrderIntegrationService(session=session)

        status_sync = StatusSynchronizerService(integration_service=integration_service,
                                                order_repository=order_repository)
        seller_repository = SellerRepository()
        sellers = seller_repository.load_all_sellers()
        logger.info('Syncronizing orders status...')
        for seller in sellers:
            status_sync.sync_all_pending_orders(seller_id=seller.id,
                                                seller_code=seller.seller_code,
                                                integration_type=seller.get_integration_type().name)
        session.commit()
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()

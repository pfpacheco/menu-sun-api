from menu_sun_api.infrastructure.connection_factory import Session
from promax.application.order_integration_service import OrderIntegrationService
from promax.infrastructure.promax.http_promax import HttpPromax
from promax.infrastructure.promax.promax_service import PromaxService
from promax.infrastructure.sqs.order_queue import OrderQueue
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_api.application.order_service import OrderService
import logging
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../menu_sun_api/vendored"))

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    session = Session()
    try:
        order_queue_url = os.getenv("ORDER_QUEUE_URL")
        promax_ip = os.getenv("PROMAX_IP")
        promax_password = os.getenv('PROMAX_PASSWORD')
        promax_userid = os.getenv('PROMAX_USER_ID')
        order_queue = OrderQueue(queue_url=order_queue_url)

        http_promax = HttpPromax(domain=promax_ip)
        promax_service = PromaxService(http_promax=http_promax)
        order_repository = OrderRepository()
        order_service = OrderService(order_repository)
        integration_service = OrderIntegrationService(order_service=order_service,
                                                      order_queue=order_queue)
        integration_service.integrate_orders(promax_service=promax_service,
                                             auth={'user_id': promax_userid, 'password': promax_password})
    except Exception as e:
        logger.error(str(e))
        session.rollback()
        raise
    finally:
        session.close()

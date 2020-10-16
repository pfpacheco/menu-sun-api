import logging
import json
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../vendored"))

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from menu_sun_api.infrastructure.webhoook import Webhook
from menu_sun_api.domain.model.seller.seller_repository import SellerRepository
from menu_sun_api.domain.model.order.order_repository import OrderRepository
from menu_sun_api.infrastructure.connection_factory import Session


def handler(event, context):
    session = Session()
    try:
        url = os.getenv("ORDER_STATUS_WEBHOOK")
        bearer_token_callback = os.getenv("BEARER_TOKEN")
        header = {'Authorization': "Bearer " + bearer_token_callback}
        urls = []
        if url:
            urls.append(url)

        seller_repository = SellerRepository()

        sellers = seller_repository.load_all_sellers()
        order_repository = OrderRepository(session=session)
        logger.info('Publishing order status...')
        for seller in sellers:
            orders = order_repository.load_orders_on_wms(seller_id=seller.id)
            for order in orders:
                unpublished_statuses = order.list_unpublished_statuses()
                for status in unpublished_statuses:
                    for url in urls:
                        payload = {
                            'status': status.status.name,
                            'order_id': order.order_id}
                        rs = Webhook.notify(
                            url=url, payload=payload, headers=header)
                        if rs.status_code == 200:
                            logger.info('Order status [{}] for order [{}] published.'.format(order.order_id,
                                                                                             status.status.name))
                            status.set_as_published()
                            session.commit()
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()

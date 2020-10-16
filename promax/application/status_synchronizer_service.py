from typing import Optional

from menu_sun_api.domain.model.order.order import Order, OwnerType
from menu_sun_api.domain.model.seller.seller import IntegrationType
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_integration.application.services.order_integration_service import OrderIntegrationService
from menu_sun_integration.presentations.order.abstract_order_status_notification_response import AbstractOrderStatusNotificationResponse

import logging
import json

logger = logging.getLogger()


def fetch_order_status(integration_service, order: Order) -> \
        Optional[AbstractOrderStatusNotificationResponse]:
    try:
        order_status_response = integration_service.get_order_from_seller(order)
        order_status = order_status_response.get_order() if order_status_response.succeeded else None

        if order:
            msg = {"seller_code": order.seller.seller_code,
                   "order_id": order.order_id,
                   "document": order.customer.document,
                   "status": str(order_status),
                   "key": 'fetch_order_status'}
            logger.info(json.dumps(msg))

        return order_status

    except Exception as e:
        logger.error(e)
        raise e


def update_order_status(integration_service, orders: [Order]):
    for order in orders:
        order_status = fetch_order_status(integration_service=integration_service, order=order)

        if order_status:
            order.link_seller_order_id(order_status.seller_order_id)

            if order_status.status.code == "F":
                order.invoice(owner=OwnerType.SELLER)
            elif order_status.status.code == "E":
                order.delivery(owner=OwnerType.SELLER)
            elif order_status.status.code == "C":
                order.cancel(comments=order_status.status.information, owner=OwnerType.SELLER)

            return order


class StatusSynchronizerService:

    def __init__(self, order_repository, integration_service):
        self.order_repository = order_repository
        self.integration_service = integration_service

    def sync_all_pending_orders(self, seller_id: str, seller_code: str, integration_type: IntegrationType):
        orders = self.order_repository.load_orders_on_wms(seller_id)
        logger.info('Total pending orders by {} {} {}: {}'.format(seller_id, seller_code, integration_type,
                                                                  len(orders)))
        update_order_status(integration_service=self.integration_service, orders=orders)

    def sync_all_pending_orders_by_order_id(
            self, seller_id: str, seller_code: str, integration_type: IntegrationType, order_id: str):
        orders = self.order_repository.load_order_by_order_id(
            seller_id, order_id)

        logger.info('Total pending orders by {} {} {} {}: {}'.format(seller_id, seller_code, integration_type, order_id,
                                                                     len(orders)))
        update_order_status(integration_service=self.integration_service, orders=orders)

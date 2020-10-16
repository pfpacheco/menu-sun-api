from promax.infrastructure.promax.order_request import OrderRequest
import json
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.domain.model.response.failure_response import FailureResponse
from menu_sun_api.domain.model.response.success_response import SuccessResponse
from promax.shared.order_logger import OrderLogger
from promax.application.map_order import MapOrderToMessage
import logging

logger = logging.getLogger()


class OrderIntegrationService():

    def __init__(self, order_service, order_queue):
        self.order_service = order_service
        self.order_queue = order_queue

    def integrate_orders(self, promax_service, auth):
        messages = self.order_queue.receive_messages()
        for m in messages:
            message_body = m['Body']
            receipt_handle = m['ReceiptHandle']
            order = json.loads(message_body)
            seller_id = order['seller_id']
            order_id = order['order_id']
            OrderLogger.info(
                order_id=order_id,
                key='integrating_order',
                payload=order)
            order_request = OrderRequest.from_dict(order)
            rs = promax_service.send_order(order_request, auth)
            if (rs):
                rs = self.order_service.mark_order_as_integrated(
                    seller_id=seller_id, order_id=order_id)
                OrderLogger.info(
                    order_id=order_id,
                    key='mark_as_integrated',
                    payload=order)
                Session().commit()
                if (rs):
                    self.order_queue.ack_message(receipt_handle)
                    OrderLogger.info(
                        order_id=order_id,
                        key='order_queue_ack',
                        payload=order)

    def enqueue_pending_orders(self, seller_id):
        import json
        from datetime import datetime

        msgs = []
        rs = self.order_service.load_pending_orders(seller_id)
        if (rs):
            ls = rs.value
            for order in ls:
                try:
                    mapper = MapOrderToMessage()
                    order_dict = order.accept(mapper)
                    body = json.dumps(order_dict)
                    OrderLogger.info(
                        order_id=order_dict['order_id'],
                        key='enqueue_order',
                        payload=order_dict)
                    message_id = self.order_queue.send_message(body=body)
                    if not message_id:
                        return FailureResponse()
                    else:
                        order.order_queue_date = datetime.utcnow()
                        Session().commit()
                        msgs.append(message_id)
                        OrderLogger.info(
                            order_id=order_dict['order_id'],
                            key='order_queued',
                            payload=order_dict)
                except Exception as e:
                    logger.error(e)
        return SuccessResponse(msgs)

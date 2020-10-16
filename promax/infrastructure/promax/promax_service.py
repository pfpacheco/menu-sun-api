import logging
import json
from promax.shared.order_logger import OrderLogger
from promax.infrastructure.promax.order_details_response import OrderDetailResponse
from promax.infrastructure.promax.order_history_reponse import OrdersHistoryResponse
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class PromaxService():

    def __init__(self, http_promax):
        self.http_promax = http_promax

    def __check_if_order_was_already_integrated(self, data):
        try:
            cd_erro = data['packageInfo']['body']['data']['response']['status'][0]['cdErro']
            ret = (cd_erro == "3")
        except Exception:
            ret = False
        return ret

    def __check_success(self, data):
        try:
            rs = data['packageInfo']['body']['data']['response']['pedidoRealizado']
            ret = (len(rs) == 1)
        except Exception:
            ret = False
        return ret

    def send_order(self, order_request, auth={}):
        order_id = order_request.order_id
        data = self.http_promax.send_order(
            order_request=order_request, auth=auth)
        rs = self.__check_success(data)
        if rs:
            OrderLogger.info(
                order_id=order_id,
                key="order_integrated",
                payload=data)
        else:
            rs = self.__check_if_order_was_already_integrated(data)
            if rs:
                OrderLogger.warn(
                    order_id=order_id,
                    key="order_already_integrated",
                    payload=data)
            else:
                OrderLogger.error(order_id=order_id,
                                  key="order_integration_error",
                                  payload=data)
        return rs

    def get_order_details(self, order_details_request, auth={}):
        data = self.http_promax.get_order_details(order_details_request=order_details_request,
                                                  auth=auth)
        order_response = OrderDetailResponse.build(data)
        if order_response:
            return order_response
        else:
            OrderLogger.error(
                order_id=order_details_request.order_id,
                key='error_fetching_status',
                payload=data)
            return None

    def __log_error_history(self, document, key, payload):
        msg = {"document": document, "key": key, "payload": payload}
        logger.error(json.dumps(msg))

    def get_orders_history(self, request, auth={}):
        data = self.http_promax.get_order_history(order_history_request=request,
                                                  auth=auth)
        orders = OrdersHistoryResponse.build(data)
        if (orders):
            return orders
        else:
            self.__log_error_history(
                document=request.cnpj,
                key='error_feching_order_history',
                payload=data)
            return None

    def get_order_history_by_order_id(self, request, auth={}):
        data = self.http_promax.get_order_history(order_history_request=request,
                                                  auth=auth)
        orders = OrdersHistoryResponse.build(data)

        if orders:
            return orders
        else:
            self.__log_error_history(
                document=request.cnpj,
                key='error_feching_order_history_by_order_id',
                payload=data)
            return None

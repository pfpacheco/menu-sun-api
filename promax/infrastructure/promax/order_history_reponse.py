import logging

logger = logging.getLogger()


class OrderHistory:

    def __init__(self, order):
        self.order = order

    @property
    def status(self):
        return self.order['situacao']

    @property
    def id(self):
        return str(self.order['idPedidoFacil'])

    @property
    def promax_order_id(self):
        return int(self.order['cdPedido'])


class OrdersHistoryResponse:

    def __init__(self, data):
        self.data = data
        self.orders_list = []
        for order_data in data:
            order = OrderHistory(order=order_data)
            self.orders_list.append(order)

    @classmethod
    def build(cls, data):
        try:
            history = data['packageInfo']['body']['data']['response']['historico']
            ret = OrdersHistoryResponse(data=history)
        except Exception:
            ret = None
        return ret

    def get_order(self, order_id):

        for order in self.orders_list:
            order_id_change = order_id.replace('M2', 'M4')
            if order.id == order_id_change.replace("M", ""):
                return order
        return None

class OrderDetailResponse():

    def __init__(self, order):
        self.order = order

    @classmethod
    def build(cls, data):
        ret = None
        try:
            ret = OrderDetailResponse(
                data['packageInfo']['body']['data']['response'])
        except Exception:
            ret = None
        return ret

    @property
    def status(self):
        return self.order['detalhePedido'][0]['dsSituacaoPedido']

    @property
    def validate_order_detail(self):
        if 'status' in self.order:
            return False

    @property
    def product_out_of_stock(self):

        for produto in self.order['produtos']:
            if produto['idFalta'] == 'S':
                return produto['idFalta']

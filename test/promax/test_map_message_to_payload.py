from promax.infrastructure.promax.order_request import OrderRequest, OrderItemRequest
from datetime import datetime


def test_map_order_to_message():

    items = [{"sku": "972", "price": 30.99, "quantity": 1}]
    message = {"order_id": "50",
               "document": "10851803792",
               "order_date": datetime.utcnow().isoformat(),
               'delivery_date': datetime.utcnow().isoformat(),
               'seller_code': "MOOCA",
               'payment_code': 2,
               "items": items
               }

    rs = OrderRequest.from_dict(message)
    payload = rs.payload
    assert(payload)

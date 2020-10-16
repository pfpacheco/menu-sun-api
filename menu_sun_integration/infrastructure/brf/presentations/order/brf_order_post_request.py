from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest, AbstractRequestPostAction
from menu_sun_integration.presentations.order.abstract_order_post_request import AbstractOrderPostRequest, \
    AbstractOrderItemPostRequest


def get_attr(attr, default_value):
    if attr is None:
        return default_value
    else:
        return attr


class BRFOrderAddressPostRequest(AbstractRequestPostAction):
    def __init__(self, street: str, number: int, complement1: str, complement2: str, complement3: str,
                 neighborhood: str, state_code: str, phone: str,
                 city: str, postal_code: str, name: str):
        self.street = get_attr(street, "")
        self.number = get_attr(number, 0)
        self.complement1 = get_attr(complement1, "")
        self.complement2 = get_attr(complement2, "")
        self.complement3 = get_attr(complement3, "")
        self.neighborhood = get_attr(neighborhood, "")
        self.state_code = get_attr(state_code, "")
        self.phone = get_attr(phone, "")
        self.city = get_attr(city, "")
        self.postal_code = get_attr(postal_code, "")
        self.name = get_attr(name, "")

    @property
    def payload(self):
        return """
               {
                    "name": "%s",
                    "street": "%s",
                    "number":"%s",
                    "complement1": "%s",
                    "complement2": "%s",
                    "complement3": "%s",
                    "neighborhood":"%s",
                    "stateCode": "%s",
                    "city": "%s",
                    "phone": "%s",
                    "postalCode": "%s"
                }
               """ % (self.name, self.street, self.number, self.complement1, self.complement2, self.complement3,
                      self.neighborhood, self.state_code, self.city, self.phone, self.postal_code)


class BRFOrderCustomerPostRequest(AbstractRequestPostAction):
    def __init__(self, document: str, name: str, email: str, postal_code: str):
        self.document = get_attr(document, "")
        self.email = get_attr(email, "")
        self.name = get_attr(name, "")
        self.postal_code = get_attr(postal_code, "")

    @property
    def payload(self):
        return """
              "document": "%s",
              "name": "%s",
              "email": "%s"
        """ % (self.document, self.name, self.email)


class BRFOrderItemPostRequest(AbstractOrderItemPostRequest):
    def __init__(self, name: str, sku: str, quantity: int, price: float,
                 original_price: float):
        super().__init__(sku=get_attr(sku, ""),
                         quantity=get_attr(quantity, 0), price=get_attr(price, 0.0))

        self.name = get_attr(name.translate(str.maketrans({"'": None})), "")
        self.original_price = get_attr(original_price, 0.0)
        self.discount = round((self.original_price or self.price) - self.price, 2)

    @property
    def payload(self):
        return """
                 {
                  "sku": "%s",
                  "description": "%s",
                  "ean": "%s",
                  "price": "%s",
                  "originalPrice": "%s",
                  "quantity": "%s"

                }
            """ % (self.sku, self.name, "", self.price, self.original_price, self.quantity)


class BRFOrderPostRequest(AbstractOrderPostRequest):
    def __init__(self, order_id: str, order_date: str, delivery_date: str,
                 unb: str, payment_code: str, items: [BRFOrderItemPostRequest], total: float, subtotal: float,
                 shipping: float, discount: float, shipping_address: BRFOrderAddressPostRequest,
                 billing_address: BRFOrderAddressPostRequest, customer: BRFOrderCustomerPostRequest,
                 status: str):
        super().__init__(order_id, "", order_date, delivery_date, unb, payment_code, items)

        self.interface_id = 'MENU'
        self.total = get_attr(total, 0.0)
        self.subtotal = get_attr(subtotal, 0.0)
        self.shipping = get_attr(shipping, 0.0)
        self.discount = get_attr(discount, 0.0)
        self.shipping_address = shipping_address
        self.billing_address = billing_address
        self.customer = customer
        self.status = status
        self.products = self.__get_item_payload()

    def __get_item_payload(self):
        parts = []
        for item in self.items:
            item_payload = item.payload
            parts.append(item_payload)

        item_payload = ','.join(parts)
        return item_payload

    @property
    def payload(self) -> str:
        return """
             {
                "interfaceId": "%s",
                "orderId": "%s",
                "sellerCode": "%s",
                %s,
                "deliveryDate":"%s",
                "orderDate": "%s",
                "paymentCode": "%s",
                "billingAddress":%s,
                "shippingAddress": %s,
                "status":"%s",
                "items": [%s]
            }
      """ % (self.interface_id, self.order_id, self.seller_code, self.customer.payload, self.delivery_date,
             self.order_date, self.payment_code, self.billing_address.payload, self.shipping_address.payload,
             self.status, self.products)

    @property
    def resource(self) -> str:
        return "orders/v1/Order"

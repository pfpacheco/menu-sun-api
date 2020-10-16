import os

from menu_sun_integration.presentations.interfaces.abstract_request import AbstractRequest, AbstractRequestPostAction
from menu_sun_integration.presentations.order.abstract_order_post_request import AbstractOrderPostRequest, \
    AbstractOrderItemPostRequest


def get_attr(attr, default_value):
    if attr is None:
        return default_value
    else:
        return attr


class PernodOrderAddressPostRequest(AbstractRequestPostAction):
    def __init__(self, street: str, number: int, complement: str, reference: str,
                 neighborhood: str, state_code: str,  shipping_provider: str, shipping_service: str,
                 city: str, country_code: str, postcode: str, name: str):
        self.street = get_attr(street, "")
        self.number = get_attr(number, 0)
        self.complement = get_attr(complement, "")
        self.reference = get_attr(reference, "")
        self.neighborhood = get_attr(neighborhood, "")
        self.state_code = get_attr(state_code, "")
        self.city = get_attr(city, "")
        self.country_code = get_attr(country_code, "")
        self.postcode = get_attr(postcode, "")
        self.name = get_attr(name, "")
        self.shipping_provider = get_attr(shipping_provider, "")
        self.shipping_service = get_attr(shipping_service, "")

    @property
    def payload(self):
        return """
               {
                    "address": "%s",
                    "neighborhood": "%s",
                    "city":"%s",
                    "state": "%s",
                    "country": "%s",
                    "zipCode": "%s",
                    "additionalInfo":"%s",
                    "reference": "%s",
                    "number": %s
                }
               """ % (self.street, self.neighborhood, self.city, self.state_code, self.country_code, self.postcode,
                      self.complement, self.reference, self.number)


class PernodOrderStatusPostRequest(AbstractRequestPostAction):
    def __init__(self, status: str, updated_date: str):
        self.real_status = get_attr(status, "")
        self.order_status = "pending"
        self.updated_date = get_attr(updated_date, "")

    @property
    def payload(self):
        return """
            {
                "status": "%s",
                "updatedDate": "%s",
                "message" : "Menu Status - %s",
                "active": true
            }
        """ % (self.order_status, self.updated_date, self.real_status)


class PernodOrderCustomerPostRequest(AbstractRequest):
    def __init__(self, name: str, document: str, email: str, phone_number: str):
        self.name = get_attr(name, "")
        self.document = get_attr(document, "")
        self.email = get_attr(email, "")
        self.phone_number = get_attr(phone_number, "")

    @property
    def payload(self):
        return """
            {
                "name": "%s",
                "documentNumber": "%s",
                "email": "%s",
                "mobileNumber": "%s"
            }
        """ % (self.name, self.document, self.email, self.phone_number)


class PernodOrderItemPostRequest(AbstractOrderItemPostRequest):
    def __init__(self, name: str, sku: str, quantity: int, price: float, original_price: float):
        super().__init__(sku=get_attr(sku, ""),
                         quantity=get_attr(quantity, 0), price=get_attr(price, 0.0))

        self.name = get_attr(name.translate(str.maketrans({"'": None})), "")
        self.original_price = get_attr(original_price, 0.0)
        self.discount = round((self.original_price or self.price) - self.price, 2)
        self.shipping_cost = 0.00

    @property
    def payload(self):
        return """
                 {
                  "sku": "%s",
                  "name": "%s",
                  "quantity": %s,
                  "price": %s,
                  "discount": %s,
                  "shippingCost": %s
                }
            """ % (self.sku, self.name, self.quantity, self.original_price, self.discount, self.shipping_cost)


class PernodOrderPostRequest(AbstractOrderPostRequest):
    def __init__(self, seller_id: str, order_id: str, order_date: str, delivery_date: str,
                 unb: str, payment_code: str, items: [PernodOrderItemPostRequest], total: float,
                 subtotal: float, shipping: float, discount: float, shipping_address: PernodOrderAddressPostRequest,
                 billing_address: PernodOrderAddressPostRequest, customer: PernodOrderCustomerPostRequest,
                 status: PernodOrderStatusPostRequest):
        super().__init__(order_id=order_id, document="",
                         order_date=order_date, delivery_date=delivery_date, unb=unb, payment_code=payment_code,
                         items=items)
        self.seller_id = seller_id
        self.shipping = get_attr(shipping, 0.0)
        self.discount = get_attr(discount, 0.0)
        self.shipping_address = shipping_address
        self.billing_address = billing_address
        self.id_tenant = os.getenv("PERNOD_ID_TENANT")
        self.store = "Menu"
        self.system_source = self.store
        self.shipping_responsible = "seller"
        self.shipping_per_item = self.shipping / len(list(self.items))
        self.shipping_provider = get_attr(shipping_address.shipping_provider, "")
        self.shipping_service = get_attr(shipping_address.shipping_service, "")
        self.installments = 1
        self.customer = customer
        self.status = status
        self.receiver_name = get_attr(self.shipping_address.name, "")
        self.products = self.__get_item_payload()
        self.total_discount = self.__get_item_total_discount() + self.discount
        self.subtotal = get_attr(subtotal, 0.0)
        self.total = get_attr(total, 0.0)

    def __get_item_payload(self):
        parts = []
        for item in self.items:
            item.shipping_cost = round(get_attr(self.shipping_per_item, 0.0), 2)
            item_payload = item.payload
            parts.append(item_payload)

        item_payload = ','.join(parts)
        return item_payload

    def __get_item_total_discount(self):
        item_discount = 0
        for item in self.items:
            item_discount += item.discount*item.quantity
        return item_discount

    @property
    def payload(self) -> str:
        payload = """
            {
              "reference": {
                "idTenant": %s,
                "store": "%s",
                "source": "%s",
                "system": {
                  "source": "%s"
                }
              },
              "shipping": {
                "responsible": "seller",
                "receiverName":"%s",
                "estimatedDeliveryDate": "%s",
                "provider": "%s",
                "service": "%s",
                "price": %s,
                "address": %s
              },
              "payment": {
                "method": "%s",
                "purchaseDate": "%s",
                "approvedDate": "%s",
                "totalAmount": %s,
                "totalAmountPlusShipping":%s,
                "totalDiscount": %s,
                "installments": %s,
                "address": %s
              },
              "status": %s,
              "customer": %s,
              "createdDate": "%s",
              "products": [%s]
            }
        """ % (self.id_tenant, self.store, self.order_id, self.system_source, self.receiver_name, self.delivery_date,
               self.shipping_provider, self.shipping_service, self.shipping,
               self.shipping_address.payload, self.payment_code, self.order_date, self.order_date,
               self.subtotal, self.total, self.total_discount, self.installments, self.billing_address.payload,
               self.status.payload, self.customer.payload, self.order_date, self.products)

        self._logger.info(
            key="order_post_request",
            description="payload",
            payload=payload)

        return payload

    @property
    def resource(self) -> str:
        return f"orders"

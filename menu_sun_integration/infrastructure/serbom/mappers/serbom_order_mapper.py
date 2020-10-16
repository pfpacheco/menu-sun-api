from menu_sun_api.domain.model.customer.customer import Customer
from menu_sun_api.domain.model.order.order import Order, OrderBillingAddress, OrderShippingAddress
from menu_sun_integration.application.mappers.base_order_mapper import BaseOrderMapper


class SerbomOrderMapper(BaseOrderMapper):
    def __init__(self, base_mapper: BaseOrderMapper = BaseOrderMapper()):
        self._base_mapper = base_mapper

    def visit(self, entity):

        if isinstance(entity, Order):
            shipping_address = entity.shipping_address.accept(self)
            billing_address = entity.billing_address.accept(self)
            customer = entity.customer.accept(self)

            general_message = self._base_mapper.visit(entity)
            aryzta_message = {
                "shipping_address": shipping_address,
                "billing_address": billing_address,
                "shipping": entity.shipping,
                "total": entity.total,
                "subtotal": entity.subtotal,
                "discount": entity.discount,
                "customer": customer
            }

            return {**general_message, **aryzta_message}

        if isinstance(entity, OrderShippingAddress) or isinstance(entity, OrderBillingAddress):
            return {
                "name": entity.name,
                "street": str(entity.street),
                "neighborhood": entity.neighborhood,
                "city": entity.city,
                "state_code": entity.state_code,
                "country_code": entity.country_code,
                "postcode": entity.postcode,
                "complement": entity.complement,
                "reference": entity.reference,
                "number": str(entity.number)
            }

        if isinstance(entity, Customer):
            return {"name": entity.name,
                    "document": entity.document,
                    "phone_number": entity.phone_number,
                    "email": entity.email
                    }

        return None

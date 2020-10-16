from menu_sun_api.domain.model.customer.customer import Customer
from menu_sun_api.domain.model.order.order import Order, OrderBillingAddress, OrderShippingAddress, OrderPayment
from menu_sun_integration.application.mappers.base_order_mapper import BaseOrderMapper


class PernodOrderMapper(BaseOrderMapper):
    def __init__(self, base_mapper: BaseOrderMapper = BaseOrderMapper()):
        self._base_mapper = base_mapper

    def visit(self, entity):

        if isinstance(entity, Order):
            shipping_address = entity.shipping_address.accept(self)
            shipping_provider = next(
                (field.value for field in entity.metafields if field.namespace == "INTEGRATION_API_FIELD"
                 and field.key == "DELIVERY_PROVIDER"), "")
            shipping_service = next(
                (field.value for field in entity.metafields if field.namespace == "INTEGRATION_API_FIELD"
                 and field.key == "DELIVERY_SERVICE"), "")

            payment = [i.accept(self) for i in entity.payments]
            payment_code = (payment[0]['payment_type'] if payment else '')

            shipping_address['shipping_provider'] = shipping_provider

            shipping_address['shipping_service'] = shipping_service

            billing_address = entity.billing_address.accept(self)
            customer = entity.customer.accept(self)
            general_message = self._base_mapper.visit(entity)
            pernod_message = {
                "shipping_address": shipping_address,
                "billing_address": billing_address,
                "shipping": entity.shipping,
                "total": entity.total,
                "subtotal": entity.subtotal,
                "discount": entity.discount,
                "customer": customer,
                "payment_code": payment_code
            }

            return {**general_message, **pernod_message}

        if isinstance(entity, OrderShippingAddress) or isinstance(entity, OrderBillingAddress):
            shipping_provider = None
            shipping_service = None
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
                "number": str(entity.number),
                "shipping_provider": shipping_provider,
                "shipping_service": shipping_service
            }

        if isinstance(entity, Customer):
            return {"name": entity.name,
                    "document": entity.document,
                    "phone_number": entity.phone_number,
                    "email": entity.email
                    }

        if isinstance(entity, OrderPayment):
            return {"payment_type": entity.payment_type.name}
        return None

from menu_sun_api.domain.model.order.order import Order, OrderItem, \
    OrderPayment, OrderStatusType, OrderMetafield, OrderBillingAddress, OrderShippingAddress, OrderStatus
from menu_sun_api.domain.model.seller.seller import Seller, SellerMetafield
from menu_sun_api.domain.model.customer.customer import Customer, CustomerMetafield

from promax.shared.order_logger import OrderLogger


class MapOrderToMessage():

    def lookup_payment_code(self, lookup_table, key):
        for item in lookup_table:
            if (item['key'] == key):
                return item['value']

    def __has_adf(self, metafields):
        for item in metafields:
            if item["namespace"] == "ADF" and item['key'] == 'has_adf':
                return True if item['value'] == 'true' else False
        return False

    def visit(self, entity):

        if isinstance(entity, Order):

            items = [i.accept(self) for i in entity.items]
            statuses = [i.accept(self) for i in entity.statuses]
            seller = entity.seller.accept(self)
            payments = [i.accept(self) for i in entity.payments]
            customer = entity.customer.accept(self)
            # shipping_address = entity.shipping_address.accept(self)
            # billing_address = entity.billing_address.accept(self)

            has_adf = self.__has_adf(customer['metafields'])

            if len(payments) != 1:
                OrderLogger.error(
                    order_id=entity.order_id,
                    key='payment_list_empty',
                    payload=entity)
                raise Exception('The payment list must equanl to one')

            payment = payments[0]
            payment_code_table = [
                d for d in seller['metafields'] if d['namespace'] == 'CODIGO_PAGAMENTO']

            if has_adf:
                key = "{}_{}_ADF".format(
                    payment['payment_type'], payment['deadline'])
            else:
                key = "{}_{}".format(
                    payment['payment_type'],
                    payment['deadline'])

            payment_code = self.lookup_payment_code(
                lookup_table=payment_code_table, key=key)
            if not payment_code:
                payload = {"key": key, "lookup_table": payment_code_table}
                OrderLogger.error(
                    order_id=entity.order_id,
                    key='payment_code_not_found',
                    payload=payload)
                raise Exception('Could not find payment code [{}]'.format(key))

            rs = {
                "order_id": entity.order_id,
                "items": items,
                "customer": customer,
                "statuses": statuses,
                "order_date": entity.order_date.isoformat(),
                "delivery_date": entity.delivery_date.isoformat(),
                "shipping": entity.shipping,
                "total": entity.total,
                "subtotal": entity.subtotal,
                "discount": entity.discount,
                "seller_code": entity.seller.seller_code,
                "payment_code": payment_code,
                "document": entity.customer.document,
                "seller_id": entity.seller.id,
                "integration_type": entity.seller.get_integration_type().name,
                # "shipping_address": shipping_address,
                # "billing_address": billing_address,
            }
            return rs

        if isinstance(entity, OrderItem):
            return {"sku": entity.sku,
                    "name": entity.name,
                    "ean": entity.ean,
                    "ncm": entity.ncm,
                    "price": entity.price,
                    "original_price": entity.original_price,
                    "quantity": entity.quantity
                    }

        if isinstance(entity, OrderPayment):
            return {"deadline": entity.deadline,
                    "payment_type": entity.payment_type.name}

        if isinstance(entity, OrderStatus):
            return {"status": str(entity.status),
                    "comments": entity.comments,
                    "updated_date": entity.updated_date
                    }

        if isinstance(entity, CustomerMetafield):
            return {"key": entity.key,
                    "value": entity.value,
                    "namespace": entity.namespace
                    }

        if isinstance(entity, Customer):
            if (entity.metafields):
                metafields = [i.accept(self) for i in entity.metafields]
            else:
                metafields = []
            return {"metafields": metafields, "document": entity.document, "name": entity.name,
                    "phone_number": entity.phone_number, "email": entity.email}

        if isinstance(entity, Seller):
            metafields = [i.accept(self) for i in entity.metafields]
            return {"seller_code": entity.seller_code,
                    "uuid": entity.uuid,
                    "metafields": metafields,
                    "id": entity.id,
                    "integration_type": entity.get_integration_type().name}

        if isinstance(entity, SellerMetafield):
            return {"namespace": entity.namespace,
                    "key": entity.key,
                    "value": entity.value}

        if isinstance(entity, OrderShippingAddress):
            return {
                "name": entity.name,
                "address": {"street": str(entity.street),
                            "neighborhood": entity.neighborhood,
                            "city": entity.city,
                            "state_code": entity.state_code,
                            "country_code": entity.country_code,
                            "postcode": entity.postcode,
                            "complement": entity.complement,
                            "reference": entity.reference,
                            "number": str(entity.number)}
            }

        if isinstance(entity, OrderBillingAddress):
            return {
                "name": entity.name,
                "address": {"street": str(entity.street),
                            "neighborhood": entity.neighborhood,
                            "city": entity.city,
                            "state_code": entity.state_code,
                            "country_code": entity.country_code,
                            "postcode": entity.postcode,
                            "complement": entity.complement,
                            "reference": entity.reference,
                            "number": str(entity.number)}
            }

        return None

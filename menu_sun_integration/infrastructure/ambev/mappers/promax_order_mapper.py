import dateutil.parser
from datetime import datetime
from menu_sun_api.domain.model.customer.customer import CustomerMetafield, Customer
from menu_sun_api.domain.model.order.order import Order, OrderItem, OrderPayment, OrderStatus
from menu_sun_api.domain.model.seller.seller import Seller, SellerMetafield
from menu_sun_integration.application.mappers.base_order_mapper import BaseOrderMapper


class PromaxOrderMapper:
    def __init__(self, base_mapper: BaseOrderMapper = BaseOrderMapper()):
        self._base_mapper = base_mapper

    @staticmethod
    def lookup_payment_code(lookup_table, key):
        for item in lookup_table:
            if item['key'] == key:
                return item['value']

    @staticmethod
    def __has_adf(metafields):
        for item in metafields:
            if item["namespace"] == "ADF" and item['key'] == 'has_adf':
                return True if item['value'] == 'true' else False
        return False

    def visit(self, entity):

        if isinstance(entity, Order):
            seller = entity.seller.accept(self)
            payments = [i.accept(self) for i in entity.payments]
            customer = entity.customer.accept(self)
            statuses = [i.accept(self) for i in entity.statuses]


            has_adf = self.__has_adf(customer['metafields'])

            if len(payments) != 1:
                raise Exception('The payment list must equal to one')

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

            payment_code = self.lookup_payment_code(lookup_table=payment_code_table, key=key)

            if not payment_code:
                payload = {"key": key, "lookup_table": payment_code_table}
                raise Exception('Could not find payment code [{}]'.format(key))

            general_message = self._base_mapper.visit(entity)

            promax_message = {
                "payment_code": payment_code,
                "document": entity.customer.document,
                "statuses": statuses
            }

            return {**general_message, **promax_message}

        if isinstance(entity, OrderPayment):
            return {"deadline": entity.deadline,
                    "payment_type": entity.payment_type.name}

        if isinstance(entity, CustomerMetafield):
            return {"key": entity.key,
                    "value": entity.value,
                    "namespace": entity.namespace
                    }

        if isinstance(entity, Customer):
            if entity.metafields:
                metafields = [i.accept(self) for i in entity.metafields]
            else:
                metafields = []
            return {"metafields": metafields, "document": entity.document}

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

        if isinstance(entity, OrderStatus):
            return self._base_mapper.visit(entity)

        return None

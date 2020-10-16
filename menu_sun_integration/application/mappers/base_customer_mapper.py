from typing import Optional, Dict

from menu_sun_api.domain.model.customer.customer import Customer, PaymentTerms, CustomerMetafield
from menu_sun_integration.application.mappers.interfaces.abstract_mapper import AbstractMapper


class BaseCustomerMapper(AbstractMapper):
    def visit(self, entity) -> Optional[Dict]:
        if isinstance(entity, Customer):
            payment_terms = [i.accept(self) for i in entity.payment_terms]

            if entity.metafields:
                metafields = [i.accept(self) for i in entity.metafields]
            else:
                metafields = []

            return {"payment_terms": payment_terms, "customer_metafields": metafields, "document": entity.document,
                    "cep": entity.cep, "uf": entity.uf}

        if isinstance(entity, PaymentTerms):
            return {
                "deadline": entity.deadline,
                "description": entity.description,
                "payment_type": entity.payment_type.name
            }

        if isinstance(entity, CustomerMetafield):
            return {
                "namespace": entity.namespace,
                "key": entity.key,
                "value": entity.value
            }

        return None

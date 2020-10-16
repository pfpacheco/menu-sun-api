from typing import Optional, Dict

from menu_sun_api.domain.model.customer.customer import Customer, PaymentTerms
from menu_sun_integration.application.mappers.interfaces.abstract_mapper import AbstractMapper


class BRFCustomerMapper(AbstractMapper):
    def visit(self, entity) -> Optional[Dict]:
        if isinstance(entity, Customer):
            payment_term = entity.payment_terms[0].accept(self) \
                if entity.payment_terms and len(entity.payment_terms) > 0 else {}

            return {
                "payment_term": payment_term,
                "document": entity.document,
                "postal_code": entity.uf
            }

        if isinstance(entity, PaymentTerms):
            return {
                "deadline": entity.deadline,
                "description": entity.description,
                "payment_type": entity.payment_type.name
            }

        return None

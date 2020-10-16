from typing import Dict

from menu_sun_integration.presentations.customer.abstract_customer_response import AbstractCustomerResponse, \
    AbstractCustomerPaymentTermsResponse


class BRFCustomerPaymentTermsResponse(AbstractCustomerPaymentTermsResponse):
    def __init__(self, payload: Dict):
        super().__init__(payload)

    @property
    def deadline(self) -> int:
        return self.payload.get("paymentCode", "")

    @property
    def description(self) -> str:
        return self.payload.get("paymentDescription", "")

    @property
    def payment_type(self) -> str:
        return "BOLETO"


class BRFCustomerResponse(AbstractCustomerResponse):
    def __init__(self, payload: Dict):
        super().__init__(payload)

    @property
    def credit_limit(self) -> float:
        return self.payload.get("creditLimit", 0)

    @property
    def payment_code(self) -> str:
        return self.payload.get("paymentCode", "")

    @property
    def grade(self) -> str:
        return self.payload.get("grade", "")

    @property
    def cdd(self) -> str:
        return self.payload.get("cdd", "")

    @property
    def payment_description(self) -> str:
        return self.payload.get("paymentDescription", "")

    @property
    def last_billing_date(self) -> str:
        return self.payload.get("lastBillingDate", "")

    @property
    def active(self) -> bool:
        status_code = self.payload.get("customerCode", "")
        return True if (status_code != "05" and self.cdd is not None) else False

    def is_new(self) -> bool:
        status_code = self.payload.get("customerCode", "")
        return True if status_code == "99" else False

    @property
    def payment_terms(self) -> [AbstractCustomerPaymentTermsResponse]:
        payment_terms = [BRFCustomerPaymentTermsResponse(self.payload)]
        return payment_terms

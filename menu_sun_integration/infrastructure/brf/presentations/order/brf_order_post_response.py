from datetime import datetime

from typing import Dict

from menu_sun_integration.infrastructure.brf.presentations.customer.brf_customer_response import BRFCustomerResponse
from menu_sun_integration.infrastructure.brf.presentations.order.brf_order_response import BRFOrderResponse
from menu_sun_integration.presentations.order.abstract_order_post_response import AbstractOrderPostResponse


class BRFOrderPostResponse(AbstractOrderPostResponse):
    def __init__(self, customer: BRFCustomerResponse, payload: Dict):
        super().__init__(payload)
        self._customer = customer

    def customer_status(self) -> str:
        return "NEW" if self._customer.payload['customerCode'] == "99" else "ALREADY_REGISTERED"

    def last_ordered_date(self) -> datetime:
        return datetime.strptime(self._customer.payload['lastBillingDate'], '%Y%m%d') \
            if self._customer.payload['lastBillingDate'] else datetime.utcnow()

    @property
    def succeeded(self) -> bool:
        result = False
        try:
            has_succeeded = self.payload.get('errors', [])
            result = not (len(has_succeeded) >= 1)
        except Exception:
            result = False
        finally:
            if result:
                self._logger.info(
                    key="order_post_response",
                    description="order_integrated",
                    payload=self._logger.dumps(self.payload))
            else:
                self._logger.error(
                    key="order_post_response",
                    description="order_not_integrated",
                    payload=self._logger.dumps(self.payload))

        return result

    def get_order(self) -> BRFOrderResponse:
        return BRFOrderResponse(customer_status=self.customer_status(), last_ordered_date=self.last_ordered_date())


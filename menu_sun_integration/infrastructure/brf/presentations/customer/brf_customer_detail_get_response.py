from typing import Dict

from menu_sun_integration.infrastructure.brf.presentations.customer.brf_customer_response import BRFCustomerResponse
from menu_sun_integration.presentations.customer.abstract_customer_detail_get_response import \
    AbstractCustomerDetailGetResponse


class BRFCustomerDetailGetResponse(AbstractCustomerDetailGetResponse):
    def __init__(self, payload: Dict):
        super().__init__(payload=payload)

    @property
    def succeeded(self) -> bool:
        result = False
        try:
            result = self.payload is not None
        except Exception:
            result = False
        finally:
            if result:
                self._logger.info(
                    key="customer_detail_get_response",
                    description="customer_found",
                    payload=self._logger.dumps(self.payload))
            else:
                self._logger.error(
                    key="customer_detail_get_response",
                    description="customer_not_found",
                    payload=self._logger.dumps(self.payload))

        return result

    def get_customer(self) -> BRFCustomerResponse:
        return BRFCustomerResponse(payload=self.payload)

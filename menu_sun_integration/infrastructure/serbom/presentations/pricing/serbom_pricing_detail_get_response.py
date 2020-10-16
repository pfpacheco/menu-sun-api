from typing import Dict

from menu_sun_integration.infrastructure.serbom.presentations.pricing.serbom_pricing_response import \
    SerbomPricingResponse
from menu_sun_integration.presentations.pricing.abstract_pricing_detail_get_response import \
    AbstractPricingDetailGetResponse


class SerbomPricingDetailGetResponse(AbstractPricingDetailGetResponse):
    def __init__(self, payload: Dict):
        super().__init__(payload=payload)

    @property
    def succeeded(self) -> bool:
        result = False
        try:
            result = len(self.payload) >= 1
        except Exception:
            result = False
        finally:
            if result:
                self._logger.info(
                    key="pricing_get_response",
                    description="pricing_found",
                    payload=self._logger.dumps(self.payload))
            else:
                self._logger.error(
                    key="pricing_get_response",
                    description="pricing_not_found",
                    payload=self._logger.dumps(self.payload))

        return result

    def get_pricing(self) -> [SerbomPricingResponse]:
        prices_response = self.payload
        prices = list(map(lambda price: SerbomPricingResponse(payload=price),
                          prices_response))

        return prices

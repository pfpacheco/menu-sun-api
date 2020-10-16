from typing import Dict

from menu_sun_integration.infrastructure.brf.presentations.pricing.brf_pricing_response import BRFPricingResponse
from menu_sun_integration.presentations.pricing.abstract_pricing_detail_get_response import \
    AbstractPricingDetailGetResponse


class BRFPricingDetailGetResponse(AbstractPricingDetailGetResponse):
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

    def get_pricing(self) -> [BRFPricingResponse]:
        prices_response = self.payload
        prices = list(map(lambda price: BRFPricingResponse(payload=price),
                          prices_response))

        return prices

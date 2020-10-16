from menu_sun_integration.application.adapters.customer_pricing_adapter import CustomerPricingAdapter
from menu_sun_integration.infrastructure.brf.builders.brf_base_builder import BRFBaseBuilder
from menu_sun_integration.infrastructure.brf.translators.brf_customer_pricing_translator import \
    BRFCustomerPricingTranslator


class BRFCustomerPricingBuilder(BRFBaseBuilder):
    def define_translator(self) -> None:
        self._translator = BRFCustomerPricingTranslator()

    def build_adapter(self) -> None:
        self._adapter = CustomerPricingAdapter(client=self._client, translator=self._translator)

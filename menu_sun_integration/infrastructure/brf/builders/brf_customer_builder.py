from menu_sun_integration.application.adapters.customer_adapter import CustomerAdapter
from menu_sun_integration.infrastructure.brf.builders.brf_base_builder import BRFBaseBuilder
from menu_sun_integration.infrastructure.brf.translators.brf_customer_translator import BRFCustomerTranslator


class BRFCustomerBuilder(BRFBaseBuilder):
    def define_translator(self) -> None:
        self._translator = BRFCustomerTranslator()

    def build_adapter(self) -> None:
        self._adapter = CustomerAdapter(client=self._client, translator=self._translator)

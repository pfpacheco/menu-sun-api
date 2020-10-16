from menu_sun_integration.application.adapters.order_adapter import OrderAdapter
from menu_sun_integration.infrastructure.serbom.builders.aryzta_base_builder import AryztaBaseBuilder
from menu_sun_integration.infrastructure.serbom.translators.aryzta_order_translator import AryztaOrderTranslator


class AryztaOrderBuilder(AryztaBaseBuilder):
    def create_session(self, session) -> None:
        pass

    def define_translator(self) -> None:
        self._translator = AryztaOrderTranslator()

    def build_adapter(self) -> None:
        self._adapter = OrderAdapter(client=self._client, translator=self._translator)

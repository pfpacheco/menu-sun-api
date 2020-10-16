from menu_sun_integration.application.adapters.order_adapter import OrderAdapter
from menu_sun_integration.infrastructure.ambev.builders.promax_base_builder import PromaxBaseBuilder
from menu_sun_integration.infrastructure.ambev.translators.promax_order_translator import PromaxOrderTranslator


class PromaxOrderBuilder(PromaxBaseBuilder):
    def create_session(self, session) -> None:
        pass

    def define_translator(self) -> None:
        self._translator = PromaxOrderTranslator()

    def build_adapter(self) -> None:
        self._adapter = OrderAdapter(client=self._client, translator=self._translator)

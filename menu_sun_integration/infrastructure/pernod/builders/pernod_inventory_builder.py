from menu_sun_integration.application.adapters.inventory_adapter import InventoryAdapter
from menu_sun_integration.infrastructure.pernod.builders.pernod_base_builder import PernodBaseBuilder
from menu_sun_integration.infrastructure.pernod.translators.pernod_inventory_translator import PernodInventoryTranslator


class PernodInventoryBuilder(PernodBaseBuilder):
    def define_translator(self) -> None:
        self._translator = PernodInventoryTranslator()

    def build_adapter(self) -> None:
        self._adapter = InventoryAdapter(client=self._client, translator=self._translator)
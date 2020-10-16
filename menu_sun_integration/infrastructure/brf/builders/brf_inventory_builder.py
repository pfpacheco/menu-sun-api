from menu_sun_integration.application.adapters.inventories_adapter import InventoriesAdapter
from menu_sun_integration.infrastructure.brf.builders.brf_base_builder import BRFBaseBuilder
from menu_sun_integration.infrastructure.brf.translators.brf_inventory_translator import BRFInventoryTranslator


class BRFInventoryBuilder(BRFBaseBuilder):
    def define_translator(self) -> None:
        self._translator = BRFInventoryTranslator()

    def build_adapter(self) -> None:
        self._adapter = InventoriesAdapter(client=self._client, translator=self._translator)

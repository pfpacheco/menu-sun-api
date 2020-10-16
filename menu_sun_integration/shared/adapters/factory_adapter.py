from typing import Optional

from menu_sun_integration.application.adapters.interfaces.abstract_post_adapter import AbstractAdapter
from menu_sun_integration.application.builders.integration_director import IntegrationDirector
from menu_sun_integration.shared.builders.factory_builder import FactoryBuilder


class FactoryAdapter:
    __instance = None

    @staticmethod
    def get_instance(session):
        if FactoryAdapter.__instance is None:
            FactoryAdapter(session)
        return FactoryAdapter.__instance

    def __init__(self, session):
        if FactoryAdapter.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self._adapters = {}
            self._session = session
            FactoryAdapter.__instance = self

    def register_adapter(self, integration_type: str, entity: str, adapter: AbstractAdapter):
        self._adapters[integration_type] = {entity: adapter}

    def get_adapter(self, integration_type: str, entity: str) -> Optional[AbstractAdapter]:
        adapters = self._adapters.get(integration_type)
        adapter = adapters.get(entity, None) if adapters else None

        has_to_build = True if not adapters or not adapter else False

        if has_to_build:
            builder = FactoryBuilder.get_instance().get_builder(integration_type, entity)
            integration_director = IntegrationDirector(builder=builder, session=self._session)
            integration_director.build_adapter()
            adapter = integration_director.get_adapter()
            self.register_adapter(integration_type, entity, adapter)
            return adapter

        return adapter

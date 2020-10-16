from menu_sun_integration.application.adapters.interfaces.abstract_adapter import AbstractAdapter
from menu_sun_integration.infrastructure.aws.sqs.interfaces.abstract_platform_queue import AbstractPlatformQueue
from menu_sun_integration.shared.adapters.factory_adapter import FactoryAdapter
from menu_sun_integration.shared.loggers.interfaces.abstract_logger import AbstractLogger


class AbstractService(AbstractLogger):
    def __init__(self, entity: str, adapter: AbstractAdapter, domain_service,
                 platform_service: AbstractPlatformQueue = None, session=None):
        super().__init__(entity)
        self._adapter = adapter
        self._domain_service = domain_service
        self._platform_service = platform_service
        self._session = session
        self._logger = None

    def bind_adapter(self, integration_type: str):
        adapter = FactoryAdapter.get_instance(self._session).get_adapter(integration_type, self._entity)
        self._adapter = adapter



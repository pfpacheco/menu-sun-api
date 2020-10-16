import abc

from menu_sun_api.domain.db_repository import DBRepository
from menu_sun_integration.infrastructure.aws.sqs.interfaces.abstract_platform_queue import AbstractPlatformQueue
from menu_sun_integration.shared.loggers.interfaces.abstract_logger import AbstractLogger


class AbstractPlatformService(AbstractLogger):
    def __init__(self, entity: str, platform_service: AbstractPlatformQueue, repository: DBRepository, session):
        super().__init__(entity)
        self._repository = repository
        self._platform_service = platform_service
        self._session = session

    @abc.abstractmethod
    def enqueue(self, seller_id):
        raise NotImplementedError

    @property
    def platform_service(self):
        return self._platform_service

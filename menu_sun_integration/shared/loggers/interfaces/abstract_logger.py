import abc

from menu_sun_integration.shared.loggers.logger import Logger


class AbstractLogger(abc.ABC):
    def __init__(self, entity: str):
        self._entity = entity
        self._logger = Logger()

    def bind_logger(self, integration_type: str, entity: str, seller_id: int, seller_code: str, entity_id):
        self._logger = Logger().setup(entity=entity, integration_type=integration_type, seller_id=seller_id,
                                      seller_code=seller_code, entity_id=entity_id)

"""
Singleton Design Pattern

Intent: Lets you ensure that a class has only one instance, while providing a
global access point to this instance.
"""
import logging
import json
from threading import Lock
from typing import Optional

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def info(msg):
    logger.info(msg)


class LoggerMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """
    _instance = None
    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    def __call__(cls, *args, **kwargs):
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if not cls._instance:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Logger(metaclass=LoggerMeta):
    """
    We'll use this property to prove that our Singleton really works.
    """

    def __init__(self) -> None:
        self.entity = None
        self.integration_type = None
        self.seller_code = None
        self.seller_id = None
        self.entity_id = None

    def setup(self, entity: str = None, integration_type: str = None, seller_id: int = None,
              seller_code: str = None, entity_id: str = None):
        self.entity = entity
        self.integration_type = integration_type
        self.seller_code = seller_code
        self.seller_id = seller_id
        self.entity_id = entity_id

        return self

    def update_entity(self, entity: str):
        self.entity = entity

    def update_entity_id(self, entity_id):
        self.entity_id = entity_id

    # def set_context(self, entity: str, entity_id=None):
    #     self.entity = entity
    #     self.entity = entity_id if entity_id else self.entity_id if self.entity_id else ""

    def __format_msg(self, key: str, payload: str, description: str, integration: str = None, entity_id=None):
        msg = {}
        integration_value = integration if integration else self.integration_type if self.integration_type else ""
        entity_id_value = entity_id if entity_id else self.entity_id if self.entity_id else ""
        if integration_value:
            msg = {"integration": integration_value}

        msg.update({"seller_id": self.seller_id, "seller_code": self.seller_code,
                    self.entity: entity_id_value, "key": key, "description": description, "payload": str(payload)})

        return msg

    @staticmethod
    def dumps(payload=None):
        return json.dumps(payload)

    def info(self, key: str, description: str, payload, entity_id=None):
        logger.info(self.__format_msg(key=key, description=description, entity_id=entity_id, payload=payload))

    def error(self, key: str, description: str, payload, entity_id=None):
        logger.error(self.__format_msg(key=key, description=description, entity_id=entity_id, payload=payload))

    def warn(self, key: str, description: str, payload, entity_id=None):
        logger.warning(self.__format_msg(key=key, description=description, entity_id=entity_id, payload=payload))


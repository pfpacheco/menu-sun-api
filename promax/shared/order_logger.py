import logging
import json
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class OrderLogger():

    @classmethod
    def info(cls, order_id, key=None, payload=None):
        msg = {"order_id": order_id, "key": key, "payload": payload}
        msg_str = json.dumps(msg)
        logger.info(msg_str)

    @classmethod
    def error(cls, order_id, key=None, payload=None):
        msg = {"order_id": order_id, "key": key, "payload": payload}
        logger.error(json.dumps(msg))

    @classmethod
    def warn(cls, order_id, key=None, payload=None):
        msg = {"order_id": order_id, "key": key, "payload": payload}
        logger.warning(json.dumps(msg))

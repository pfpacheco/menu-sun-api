import abc
import json

from menu_sun_integration.shared.loggers.logger import Logger

PRIMITIVE = (int, str, bool, float)


def is_primitive(thing):
    return isinstance(thing, PRIMITIVE)


class AbstractPresentation(abc.ABC):
    _logger = Logger()

    @classmethod
    def from_dict(cls, source):
        obj = cls()
        for key, value in source.items():
            if hasattr(obj, key) and is_primitive(value):
                setattr(obj, key, value)
        return obj

    def __str__(self):
        text = json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
        return text.replace('\n', '')

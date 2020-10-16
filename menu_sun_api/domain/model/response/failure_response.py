import enum
import os

import i18n

config = os.path.join(os.path.dirname(__file__))
i18n.load_path.append(os.path.join(config, './'))


class FailureResponseCategory(enum.Enum):
    INFO = 'INFO'
    ERROR = 'ERROR'
    VALIDATION = 'VALIDATION'
    WARNING = 'WARNING'


class FailureResponse(object):

    def __init__(self, category=None, target=None, key=None, args=[]):
        self.category = category
        self.target = target
        self.key = key
        self.args = args

    # def message(self):
    #     return self.load_message(self.key, self.args)

    @staticmethod
    def load_message(key, args=None):
        locale = FailureResponse._get_app_locale()
        message = i18n.t('messages.' + key, locale=locale)
        if args:
            i18n_args = map(
                lambda arg: i18n.t(
                    'messages.' + str(arg),
                    default=arg,
                    locale=locale),
                args)
            message = message.format(*i18n_args)
        return message

    @classmethod
    def _get_app_locale(cls):
        return 'pt'

    def _format_message(self, msg):
        if isinstance(msg, Exception):
            return "{}: {}".format(msg.__class__.__name__, "{}".format(msg))
        return msg

    def __bool__(self):
        return False

    # @classmethod
    # def build_system_error(cls, message=None):
    #     return ResponseFailure()
    #
    #         cls(cls.SYSTEM_ERROR, message)

    @property
    def value(self):
        return self.load_message(self.key, self.args)

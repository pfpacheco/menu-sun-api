# import enum
# import i18n
#
#
#
# class ResponseCategory(enum.Enum):
#     INFO = 'INFO'
#     SYSTEM_ERROR = 'ERROR'
#     VALIDATION_ERROR = 'VALIDATION_ERROR'
#     PARAMETERS_ERROR = 'PARAMETERS_ERROR'
#
#
# class ResponseFailure(object):
#
#     def __init__(self, category=None, target=None, key=None, args=[]):
#         self.category = category
#         self.target = target
#         self.key = key
#         self.args = args
#
#     def message(self):
#         return self.load_message(self.key, self.args)
#
#     @staticmethod
#     def load_message(key, args=None):
#         locale = ResponseFailure._get_app_locale()
#         message = i18n.t('messages.' + key, locale=locale)
#         if args:
#             i18n_args = map(lambda arg: i18n.t('messages.' + str(arg), default=arg, locale=locale), args)
#             message = message.format(*i18n_args)
#         return message
#
#     @classmethod
#     def _get_app_locale(cls):
#         return 'pt'
#
#     def _format_message(self, msg):
#         if isinstance(msg, Exception):
#             return "{}: {}".format(msg.__class__.__name__, "{}".format(msg))
#         return msg
#
#     def __bool__(self):
#         return False
#
#     @classmethod
#     def build_system_error(cls, message=None):
#         return ResponseFailure()
#
#             cls(cls.SYSTEM_ERROR, message)
#
#     # @property
#     # def value(self):
#     #     return {'type': self.type, 'message': self.message}
#
#
#
#     # @classmethod
#     # def build_resource_error(cls, message=None):
#     #     return cls(cls.RESOURCE_ERROR, message)
#     #
#
#     #
#     # @classmethod
#     # def build_parameters_error(cls, message=None):
#     #     return cls(cls.PARAMETERS_ERROR, message)
#     #
#     # @classmethod
#     # def build_from_invalid_request_object(cls, invalid_request_object):
#     #     message = "\n".join(["{}: {}".format(err['parameter'], err['message'])
#     #                          for err in invalid_request_object.errors])
#     #     return cls.build_parameters_error(message)

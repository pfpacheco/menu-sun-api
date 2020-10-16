import traceback

from graphql.error import GraphQLError
from graphql.error import format_error as format_graphql_error
from graphql.error.located_error import GraphQLLocatedError
from graphql.error.syntax_error import GraphQLSyntaxError

from menu_sun_api.interfaces.custom_exceptions import ResponseError
from menu_sun_api.shared.str_converters import to_kebab_case, dict_key_to_camel_case


class ErrorFormatter:

    def __init__(self, debug=False):
        self.debug = debug

    def encode_code(self, code):
        if code is None:
            return None
        return to_kebab_case(code)

    def encode_params(self, params):
        if params is None:
            return None
        return dict_key_to_camel_case(params)

    def format_internal_error(self, error: Exception):
        message = 'Internal server error'
        code = 'internal-server-error'
        if self.debug:
            params = {
                'exception': type(error).__name__,
                'message': str(error),
                'trace': traceback.format_list(traceback.extract_tb(error.__traceback__)),
            }
            return {
                'code': code,
                'message': message,
                'params': params,
            }
        return {
            'code': code,
            'message': message,
        }

    def format_response_error(self, error):
        return {
            'message': error.message,
            'code': self.encode_code(error.code),
            'params': self.encode_params(error.params),
        }

    def format_use_case_to_response_error(self, exc):
        return {
            'message': exc.message,
            'code': self.encode_code(exc.key),
            'params': None,
        }

    def format_located_error(self, error):
        if isinstance(error.original_error, GraphQLLocatedError):
            return self.format_located_error(error.original_error)
        if isinstance(error.original_error, ResponseError):
            return self.format_response_error(error.original_error)
        return self.format_internal_error(error.original_error)

    def format_error(self, error):
        try:
            if isinstance(error, GraphQLLocatedError):
                return self.format_located_error(error)
            if isinstance(error, GraphQLSyntaxError):
                return format_graphql_error(error)
            if isinstance(error, GraphQLError):
                return format_graphql_error(error)
            return self.format_internal_error(error)
        except Exception as e:
            return self.format_internal_error(e)

class ResponseError(Exception):
    def __init__(self, message, code=None, params=None):
        super().__init__(message)
        self.message = str(message)
        self.code = code
        self.params = params


class AuthenticationException(Exception):
    def __init__(self, messages):
        self.messages = messages


class AuthorizationException(Exception):
    def __init__(self, messages):
        self.messages = messages

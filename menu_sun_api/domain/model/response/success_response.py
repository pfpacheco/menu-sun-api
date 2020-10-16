class SuccessResponse(object):
    SUCCESS = 'SUCCESS'

    def __init__(self, value=None):
        self.type = self.SUCCESS
        self.value = value

    def __nonzero__(self):
        return True

    __bool__ = __nonzero__

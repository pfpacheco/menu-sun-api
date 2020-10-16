from menu_sun_api.domain.model.response.success_response import SuccessResponse
from menu_sun_api.domain.model.response.failure_response import FailureResponse
from menu_sun_api.domain.model.customer.customer import Customer


class Command(object):

    def validate(self):
        raise NotImplementedError()


class TransactionCommandHandler(object):

    def __init__(self, session):
        self.session = session

    def execute(self, command):
        try:
            command.validate()
            rs = self.process_request(command)
            self.session.commit()
            return rs
        except Exception as exc:
            self.session.rollback()
            raise exc

    def process_request(self, command):
        raise NotImplementedError(
            "process_request() not implemented by UseCase class")

import abc

from menu_sun_integration.presentations.interfaces.abstract_request import AbstractBaseRequestPostAction


class AbstractCustomerPostRequest(AbstractBaseRequestPostAction):
    def __init__(self, document: str, email: str = None, name: str = None):
        self._document = document
        self._email = email
        self._name = name

    @property
    def document(self):
        return self._document

    @property
    def email(self):
        return self._email

    @property
    def name(self):
        return self._name

    @abc.abstractmethod
    def payload(self):
        raise NotImplementedError

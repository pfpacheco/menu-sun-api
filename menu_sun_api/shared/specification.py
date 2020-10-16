from abc import abstractmethod

from sqlalchemy.sql.elements import BinaryExpression


class Specification:
    description = 'No description provided.'

    @abstractmethod
    def is_satisfied_by(self, seller_id: int) -> BinaryExpression:
        raise NotImplementedError

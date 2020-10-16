import abc

from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_api.infrastructure.connection_factory import Session
from menu_sun_api.shared.specification import Specification


class DBRepository:

    def __init__(self, clazz, session=None):
        if session:
            self.session = session
        else:
            self.session = Session()
        self.clazz = clazz

    def add(self, entity):
        self.session.add(entity)
        return entity

    def load_all(self, seller_id, offset=None, limit=None):
        query = self.session.query(self.clazz). \
            outerjoin(Seller). \
            filter(Seller.id == seller_id). \
            order_by(self.clazz.id)
        query = query.offset(offset) if offset else query
        query = query.limit(limit) if limit else query

        return query.all()

    @abc.abstractmethod
    def filter_by_specification(self, seller_id: int, specification: Specification):
        raise NotImplementedError()

from menu_sun_api.domain.db_repository import DBRepository
from menu_sun_api.domain.model.seller.seller import Seller, SellerMetafield, IntegrationType
from sqlalchemy import and_

from menu_sun_api.shared.specification import Specification


class SellerRepository(DBRepository):

    def __init__(self, session=None):
        super().__init__(Seller, session)

    def get_seller_by_token(self, token):
        rs = self.session.query(Seller).filter(Seller.token == token). \
            one_or_none()
        return rs

    def get_seller_by_seller_code(self, seller_code):
        rs = self.session.query(Seller).filter(Seller.seller_code == seller_code). \
            one_or_none()
        return rs

    def get_seller_by_integration_type(self, integration_type):
        rs = self.session.query(Seller).filter(Seller.integration_type == integration_type). \
            all()
        return rs

    def load_all_sellers(self):
        return self.session.query(Seller).all()

    def get_by_id(self, seller_id):
        rs = self.session.query(Seller).filter(Seller.id == seller_id). \
            one_or_none()
        return rs

    def get_metafield(self, seller_id, namespace, key):
        rs = self.session.query(Seller). \
            outerjoin(SellerMetafield). \
            filter(and_(Seller.id == seller_id,
                        SellerMetafield.key == key,
                        SellerMetafield.namespace == namespace)).one_or_none()
        return rs

    def filter_by_specification(self, seller_id: int, specification: Specification):
        query = self.session.query(Seller)
        return query.filter(specification.is_satisfied_by(seller_id)).all()

from menu_sun_api.domain.db_repository import DBRepository
from menu_sun_api.domain.model.product.product import Product
from menu_sun_api.domain.model.seller.seller import Seller
from sqlalchemy import or_, and_, func

from menu_sun_api.shared.specification import Specification


class ProductRepository(DBRepository):

    def __init__(self, session=None):
        super().__init__(Product, session)

    def search_products(self, seller_id, skus=[]):
        condition = [Seller.id == seller_id]
        query = self.session.query(Product) \
            .outerjoin(Seller)

        if skus:
            condition.append(Product.sku.in_(skus))
        ls = query.filter(*condition).all()
        return ls

    def get_by_uuid(self, uuid):
        record = self.session.query(Product). \
            filter(Product.uuid == uuid).one_or_none()
        return record

    def get_products_by_created_date_or_update(self, date, seller_id):
        condition = [Product.seller_id == seller_id]
        record = self.session.query(Product). \
            filter(or_(Product.created_date >= date,
                       date <= Product.updated_date))
        return record.filter(*condition).all()

    def get_by_sku(self, seller_id, sku):
        condition = [Seller.id == seller_id]
        record = self.session.query(Product). \
            outerjoin(Seller)

        if sku:
            condition.append(Product.sku == sku)
        return record.filter(*condition).one_or_none()

    def get_by_sku_and_seller_code(self, seller_code, sku):
        condition = [Seller.seller_code == seller_code]
        record = self.session.query(Product). \
            outerjoin(Seller)

        if sku:
            condition.append(Product.sku == sku)
        return record.filter(*condition).one_or_none()

    def delete_by_sku(self, seller_id, sku):
        record = self.get_by_sku(seller_id, sku)
        if record:
            self.session.delete(record)
        return record

    def filter_by_specification(self, seller_id: int, specification: Specification):
        query = self.session.query(Product)
        return query.filter(specification.is_satisfied_by(seller_id)).all()

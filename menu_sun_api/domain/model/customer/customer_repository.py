from menu_sun_api.domain.db_repository import DBRepository
from menu_sun_api.domain.model.customer.customer import Customer, CustomerMetafield, PaymentTerms, PaymentType
from menu_sun_api.domain.model.seller.seller import Seller
from sqlalchemy import and_

from menu_sun_api.shared.specification import Specification


class CustomerRepository(DBRepository):

    def __init__(self, session=None):
        super().__init__(Customer, session)

    def search_customers(self, seller_id, documents=[]):
        condition = [Seller.id == seller_id]
        query = self.session.query(Customer) \
            .outerjoin(Seller)

        if documents:
            condition.append(Customer.document.in_(documents))

        ls = query.filter(*condition).all()
        return ls

    def get_by_document(self, seller_id, document):
        condition = [Seller.id == seller_id]
        query = self.session.query(Customer) \
            .outerjoin(Seller)

        condition.append(Customer.document == document)
        return query.filter(*condition).one_or_none()

    def get_by_document_and_seller_code(self, seller_code, document):
        condition = [Seller.seller_code == seller_code]
        query = self.session.query(Customer) \
            .outerjoin(Seller)

        if document:
            condition.append(Customer.document == document)
        return query.filter(*condition).one_or_none()

    def get_by_document_and_seller_integration(self, integration_type, document):
        condition = [Seller.integration_type == integration_type]
        query = self.session.query(Customer) \
            .outerjoin(Seller)

        if document:
            condition.append(Customer.document == document)
        return query.filter(*condition).one_or_none()

    def get_by_uuid(self, uuid):
        record = self.session.query(Customer). \
            filter(Customer.uuid == uuid).one_or_none()
        return record

    def delete(self, seller_id, document):
        customer = self.get_by_document(seller_id=seller_id, document=document)
        if customer:
            self.session.delete(customer)
        return customer

    def get_metafield(self, seller_id, document, namespace, key):
        metafield = self.session.query(CustomerMetafield).\
            outerjoin(Customer).filter(and_(Customer.document == document,
                                            Customer.seller_id == seller_id,
                                            CustomerMetafield.namespace == namespace,
                                            CustomerMetafield.key == key)).one_or_none()
        return metafield

    def get_payment_term(self, seller_id, document, payment_type):
        payment_term = self.session.query(PaymentTerms).\
            outerjoin(Customer).filter(and_(Customer.document == document,
                                            Customer.seller_id == seller_id,
                                            PaymentTerms.payment_type == payment_type
                                            )).one_or_none()
        return payment_term

    def get_by_integration(self, integration_type, document):
        condition = [Seller.integration_type == integration_type]
        query = self.session.query(Customer) \
            .outerjoin(Seller)

        condition.append(Customer.active)
        condition.append(Customer.document == document)

        return query.filter(*condition).order_by(Seller.created_date.desc()).first()

    def filter_by_specification(self, seller_id: int, specification: Specification):
        query = self.session.query(Customer)
        return query.filter(specification.is_satisfied_by(seller_id)).all()

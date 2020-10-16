from menu_sun_api.domain.model.response.failure_response import FailureResponse, FailureResponseCategory
from menu_sun_api.domain.model.response.success_response import SuccessResponse


class CustomerService:

    def __init__(self, repository):
        self.repository = repository

    def load_all_customers(self, seller_id, offset=None, limit=None):
        ls = self.repository.load_all(
            seller_id=seller_id, offset=offset, limit=limit)
        return SuccessResponse(ls)

    def search_by_documents(self, seller_id, documents):
        products = self.repository.search_customers(seller_id,
                                                    documents)
        return SuccessResponse(products)

    def load_by_uuid(self, uuid):
        customer = self.repository.get_by_uuid(uuid=uuid)
        return SuccessResponse(customer)

    def get_by_document(self, seller_id, document):
        customer = self.repository.get_by_document(
            seller_id=seller_id, document=document)
        return SuccessResponse(customer)

    def get_by_document_and_seller_code(self, seller_code, document):
        customer = self.repository.get_by_document_and_seller_code(seller_code, document)
        return SuccessResponse(customer)

    def create_customer(self, customer_domain):
        self.repository.add(customer_domain)

        # should check if the customer exists
        return SuccessResponse(customer_domain)

    def update_customer(self, seller_id, document, customer):
        customer_db = self.repository.get_by_document(
            seller_id=seller_id, document=document)
        if not customer_db:
            rs = FailureResponse(FailureResponseCategory.ERROR,
                                 key='customer_not_found',
                                 args=[document]
                                 )
            return rs
        customer_db.update(customer)
        customer_db.update_metafields(customer.metafields)
        return SuccessResponse(customer_db)

    def delete_customer(self, seller_id, document):
        customer = self.repository.delete(
            seller_id=seller_id, document=document)
        if customer:
            return SuccessResponse(value=customer)
        return FailureResponse()

    def get_by_integration(self, integration_type, document):
        customer = self.repository.get_by_integration(
            integration_type=integration_type, document=document)
        return SuccessResponse(customer)

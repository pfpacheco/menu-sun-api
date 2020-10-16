from menu_sun_api.domain.model.response.success_response import SuccessResponse
import logging

logger = logging.getLogger()


class CustomerService:

    def __init__(self, repository):
        self.repository = repository

    def get_by_document(self, seller_id, document):
        customer = self.repository.get_by_document(seller_id=seller_id,
                                                   document=document)
        return SuccessResponse(customer)

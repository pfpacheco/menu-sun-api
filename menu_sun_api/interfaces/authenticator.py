from menu_sun_api.domain.model.seller.seller_repository import SellerRepository
from menu_sun_api.infrastructure.connection_factory import Session
from .custom_exceptions import AuthorizationException
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Authenticator(object):

    @staticmethod
    def authenticate(event):

        try:
            token = event['headers'].get('Authorization')
            token_replace = token.replace('Bearer', '').strip()
            logger.info(token_replace.strip())
            seller = Authenticator.__auth_by_token(token_replace)
            logger.info(seller)
            if not seller:
                logger.warning("Token [{}] not authorized")
                logger.warning(event)
                raise AuthorizationException('Seller was not found')
            return seller
        except BaseException:
            raise AuthorizationException('Forbidden')

    @staticmethod
    def __auth_by_token(token):
        repository = SellerRepository(Session())
        return repository.get_seller_by_token(token)

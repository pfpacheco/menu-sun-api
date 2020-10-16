import json
import logging
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../vendored"))


logger = logging.getLogger()
logger.setLevel(logging.INFO)

from menu_sun_api.domain.model.seller.seller import Seller
from menu_sun_api.interfaces.graphql_entrypoint import GraphqlEntryPoint
from menu_sun_api.interfaces.error_formatter import ErrorFormatter
from menu_sun_api.infrastructure.connection_factory import Session  # nopep8
from menu_sun_api.interfaces.authenticator import Authenticator  # nopep8
from menu_sun_api.interfaces.graphql_decorator import GraphQLDecorator  # nopep8


def handle_graphql(query, seller: Seller, variables=None) -> dict:
    result = GraphqlEntryPoint().execute(query=query,
                                         seller=seller,
                                         variables=variables)

    if result.errors:
        error_formatter = ErrorFormatter()
        Session().rollback()
        error_msg = str(result.errors)
        logger.error("Error resolving query: %s", str(error_msg))
        errors = [error_formatter.format_error(e) for e in result.errors]
        body = {'errors': errors}
    elif result.data:
        Session().commit()
        body = {'data': result.data}
    else:
        Session().rollback()
        logger.error("Result without data or errors")
        body = {'errors': [{'message': 'Internal Server Error'}]}

    return body


@GraphQLDecorator()
def handle(event, context):
    logger.info(event)
    seller = Authenticator.authenticate(event)
    body = json.loads(event['body'])
    query = body.get('query')
    variables = body.get('variables')
    return handle_graphql(query=query, seller=seller, variables=variables)

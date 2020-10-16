import json
import logging
import os
import sys
import traceback

from menu_sun_api.infrastructure.connection_factory import Session
from .custom_exceptions import AuthorizationException

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../vendored"))

logger = logging.getLogger()


class GraphQLDecorator:

    def __call__(self, f):
        def run(event, context):
            headers = {
                "Access-Control-Allow-Origin": "*"
            }

            try:
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(f(event, context))
                }

            except AuthorizationException as e:
                traceback.print_exc()
                logger.error(e)
                return {
                    'statusCode': 403,
                    'headers': headers,
                    'body': json.dumps('Unauthorized')
                }

            except Exception as e:
                traceback.print_exc()
                error_msg = str(e)
                logger.error("Unexpected exception: %s", error_msg)
                Session().rollback()

                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({'errors': [{'message': error_msg}]})
                }
            finally:
                Session().close()

        return run

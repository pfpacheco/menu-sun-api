import json
import os
import sys
import logging

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../menu_sun_api/vendored"))

from menu_public_api.notification.notification import Notification
from menu_public_api.notification.application.mapper.seller_notification_factory import FactorySellerNotification
from menu_sun_api.interfaces.authenticator import Authenticator

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle(event, context):
    logger.info(event)
    seller = Authenticator.authenticate(event)
    data = json.loads(event['body'])
    notification_instance = FactorySellerNotification.get_instance().get_notification(
        integration_type=seller.integration_type.name)

    if notification_instance:

        notification = Notification(notification_instance)
        notification_enqueue = notification.enqueue_notification(seller=seller, payload=data)

        if notification_enqueue:
            return {
                "statusCode": 200,
                "body": json.dumps(
                    {
                        'message': "MESSAGE RECEIVED"
                    }
                ),
            }
        else:
            return {
                "statusCode": 404
            }
    else:

        return {
            "statusCode": 404,
            "body": json.dumps(
                {
                    'message': "INTEGRATION FOR THIS SELLER IS NOT IMPLEMENTED"
                }
            ),
        }

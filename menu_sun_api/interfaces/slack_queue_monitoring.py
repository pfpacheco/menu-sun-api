import logging
import requests
import json
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../vendored"))


logger = logging.getLogger()


def handle(event, context):
    webhook_url = 'https://hooks.slack.com/services/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'
    payload = json.loads(event['body'])
    response = requests.post(
        webhook_url,
        json=payload
    )

    http_reply = {
        "statusCode": 200,
        "body": response.text
    }

    return http_reply

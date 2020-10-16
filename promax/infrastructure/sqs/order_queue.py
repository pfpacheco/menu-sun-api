import boto3
import logging
import json
logger = logging.getLogger()


class OrderQueue:

    def __init__(self, queue_url=None):
        self.client = boto3.client('sqs')
        self.queue_url = queue_url

    def receive_messages(self):
        response = self.client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=5,
            VisibilityTimeout=30
        )
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        if status_code != 200:
            raise Exception(response)
        if 'Messages' in response:
            return response['Messages']
        else:
            return []

    def send_message(self, body):
        response = self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=body
        )
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Exception(json.dumps(response))
        return response['MessageId']

    def ack_message(self, receipt_handle):
        response = self.client.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handle
        )
        rs = (response['ResponseMetadata']['HTTPStatusCode'] == 200)
        if not rs:
            raise Exception(json.dumps(rs))
        return rs

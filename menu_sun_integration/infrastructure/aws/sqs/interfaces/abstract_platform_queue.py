import abc
import boto3
import json

from menu_sun_integration.presentations.interfaces.abstract_message_platform import AbstractMessagePlatform


class AbstractPlatformQueue(abc.ABC):
    def __init__(self, url: str, max_number_of_messages: int = 10, visibility_timeout: int = 120):
        self.client = boto3.client('sqs')
        self.queue_url = url
        self.max_number_of_messages = max_number_of_messages
        self.visibility_timeout = visibility_timeout

    def enqueue(self, body: str) -> str:
        response = self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=body
        )
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Exception(json.dumps(response))
        return response['MessageId']

    def processed(self, identifier: str) -> bool:
        response = self.client.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=identifier
        )
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Exception(json.dumps(response))
        return True

    @abc.abstractmethod
    def map_payload(self, payload) -> AbstractMessagePlatform:
        pass

    def dequeue(self) -> [AbstractMessagePlatform]:
        response = self.client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=self.max_number_of_messages,
            VisibilityTimeout=self.visibility_timeout
        )
        status_code = response['ResponseMetadata']['HTTPStatusCode']

        if status_code != 200:
            raise Exception(response)
        if 'Messages' in response:
            return map(self.map_payload, response['Messages'])
        else:
            return []

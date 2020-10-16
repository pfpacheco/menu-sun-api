import abc
import csv

import boto3

from typing import Dict

from menu_sun_integration.application.context.ìnterfaces.abstract_get_context import AbstractGetContext


class ContextS3(AbstractGetContext):
    def __init__(self, bucket_name: str):
        super().__init__(base_url=bucket_name)
        self.client = boto3.client('s3')

    @abc.abstractmethod
    def parser(self, file) -> [Dict]:
        raise

    def get(self, request) -> Dict:
        body = {}
        s3_object = self.client.get_object(Bucket=self.base_url, Key=request.payload)
        self._logger.info(key="context_s3_get", description="s3_object",
                          payload=s3_object)
        if not s3_object:
            self._logger.warn(key="context_s3_get", description=f'response_payload_failed(url="{self.base_url}")',
                              payload="There is no file here!")
            return body

        body = s3_object["Body"].read().decode('utf-8').split()

        self._logger.info(key="context_s3_get", description='s3_object_body',
                          payload=body)

        if not body:
            self._logger.warn(key="context_s3_get", description=f'response_payload_failed(url="{self.base_url}")',
                              payload="There is no file here!")

            return body

        return self.parser(body)

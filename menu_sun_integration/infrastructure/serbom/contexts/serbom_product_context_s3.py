import csv
import os

from typing import Dict
from menu_sun_integration.infrastructure.context.context_s3 import ContextS3


class SerbomProductS3Context(ContextS3):

    def __init__(self, bucket):
        super().__init__(os.getenv(bucket))

    def parser(self, file) -> [Dict]:
        fieldnames = [
            'description', 'sku', 'inventory', 'brand',
            'cost', 'ean', 'height', 'length',
            'name', 'ncm',  'status', 'weight',
            'width', 'list_price', 'sale_price', 'promo_price'
        ]
        dict_reader = csv.DictReader(file, fieldnames=fieldnames, delimiter=";")
        result = list(dict_reader)
        self._logger.info(key="serbom_s3_context", description='parser',
                          payload=result)
        return result

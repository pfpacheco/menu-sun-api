import csv

from mock import patch
from typing import Dict

from menu_sun_integration.infrastructure.context.context_s3 import ContextS3
from menu_sun_integration.infrastructure.serbom.presentations.pricing.product.\
    serbom_product_default_pricing_detail_get_request import SerbomProductDefaultPricingDetailGetRequest
from test.menu_sun_integration.infrastructure.aws.s3.mocks.pricing.pricing_mock import mock_s3_bucket_make_api_call


class ContextS3Fake(ContextS3):
    def parser(self, file) -> [Dict]:
        fieldnames = ['sku', 'price']
        dict_reader = csv.DictReader(file, fieldnames=fieldnames, delimiter=";")
        return list(dict_reader)


@patch('botocore.client.BaseClient._make_api_call', new=mock_s3_bucket_make_api_call)
def test_context_s3():
    context = ContextS3Fake(bucket_name="menu-aryzta-dev")
    result = context.get(request=SerbomProductDefaultPricingDetailGetRequest())
    assert len(result) == 4
    assert result[0]["sku"] == "525200073"
    assert result[0]["price"] == "77,999989"
    assert result[3]["sku"] == "525200075"
    assert result[3]["price"] == "77,999989"

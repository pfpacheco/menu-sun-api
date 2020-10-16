
from mock import patch

from menu_sun_integration.infrastructure.serbom.contexts.serbom_price_context_s3 import SerbomPriceS3Context
from menu_sun_integration.infrastructure.serbom.presentations.pricing.product.\
    serbom_product_default_pricing_detail_get_request import SerbomProductDefaultPricingDetailGetRequest
from test.menu_sun_integration.infrastructure.aws.s3.mocks.pricing.pricing_mock import mock_s3_bucket_make_api_call


@patch('botocore.client.BaseClient._make_api_call', new=mock_s3_bucket_make_api_call)
def test_serbom_context_s3():
    context = SerbomPriceS3Context(bucket="ARYZTA_BUCKET")
    result = context.get(request=SerbomProductDefaultPricingDetailGetRequest())
    assert len(result) == 4
    assert result[0]["sku"] == "525200073"
    assert result[0]["price"] == "77,999989"
    assert result[3]["sku"] == "525200075"
    assert result[3]["price"] == "77,999989"

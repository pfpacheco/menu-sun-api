import pytest

from menu_sun_integration.presentations.metafield.metafield_sql_platform import MetafieldSQSPlatform
from menu_sun_integration.presentations.seller.seller_sqs_platform import SellerDetailSQSPlatform, \
    SellerSQSMessagePlatform


class TestCustomerSQSPlatform:

    @pytest.fixture
    def seller_raw_from_platform(self):
        payload = {
            "ReceiptHandle": "AAAAA",
            "Body": {
                "integration_type": "BRF",
                "seller_id": 1,
                "seller_code": "AAAA",
                "seller_metafields": [{
                    "namespace": "Seller Namespace 1",
                    "key": "Seller Key 1",
                    "value": "Seller VALUE 1"
                }, {
                    "namespace": "Seller Namespace 2",
                    "key": "Seller Key 2",
                    "value": "Seller VALUE 2"
                }
                ]
            }
        }
        return payload

    def test_mapping_seller_from_platform_to_domain(self, seller_raw_from_platform):
        receipt_handle = seller_raw_from_platform.get("ReceiptHandle", {})
        body = seller_raw_from_platform.get("Body", {})

        seller_detail = SellerDetailSQSPlatform.from_dict(body)
        seller_metafield = [MetafieldSQSPlatform.from_dict(item) for item in body.get('seller_metafields', {})]

        seller_detail.seller_metafields = seller_metafield

        seller_platform = SellerSQSMessagePlatform(receipt_handle=receipt_handle, body=seller_detail)

        seller = seller_platform.body
        raw = seller_raw_from_platform["Body"]

        assert seller.integration_type == raw["integration_type"]
        assert seller.seller_id == raw["seller_id"]
        assert seller.seller_code == raw["seller_code"]
        assert seller.seller_metafields[0].namespace == raw["seller_metafields"][0]["namespace"]
        assert seller.seller_metafields[0].key == raw["seller_metafields"][0]["key"]
        assert seller.seller_metafields[0].value == raw["seller_metafields"][0]["value"]
        assert seller.seller_metafields[1].namespace == raw["seller_metafields"][1]["namespace"]
        assert seller.seller_metafields[1].key == raw["seller_metafields"][1]["key"]
        assert seller.seller_metafields[1].value == raw["seller_metafields"][1]["value"]

import pytest

from menu_sun_integration.presentations.customer.customer_sqs_platform import CustomerSQSMessagePlatform, \
    CustomerDetailSQSPlatform, CustomerPaymentTermSQSPlatform
from menu_sun_integration.presentations.metafield.metafield_sql_platform import MetafieldSQSPlatform


class TestCustomerSQSPlatform:

    @pytest.fixture
    def customer_raw_from_platform(self):
        payload = {
            "ReceiptHandle": "AAAAA",
            "Body": {
                "document": "00005234000121",
                "customer_metafields": [{
                    "namespace": "Customer Namespace 1",
                    "key": "Customer Key 1",
                    "value": "Customer VALUE 1"
                }, {
                    "namespace": "Customer Namespace 2",
                    "key": "Customer Key 2",
                    "value": "Customer VALUE 2"
                }
                ],
                "payment_terms": [{
                    "deadline": 5,
                    "description": "Payment 5",
                    "payment_type": "BOLETO"
                }, {
                    "deadline": 10,
                    "description": "Payment 10",
                    "payment_type": "CHEQUE"
                }
                ],
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

    def test_mapping_customer_from_platform_to_domain(self, customer_raw_from_platform):
        receipt_handle = customer_raw_from_platform.get("ReceiptHandle", {})
        body = customer_raw_from_platform.get("Body", {})

        customer_detail = CustomerDetailSQSPlatform.from_dict(body)
        customer_metafield = [MetafieldSQSPlatform.from_dict(item) for item in body.get('customer_metafields', {})]
        seller_metafield = [MetafieldSQSPlatform.from_dict(item) for item in body.get('seller_metafields', {})]
        payment_terms = [CustomerPaymentTermSQSPlatform.from_dict(item) for item in body.get('payment_terms', {})]

        customer_detail.customer_metafields = customer_metafield
        customer_detail.seller_metafields = seller_metafield
        customer_detail.payment_terms = payment_terms

        customer_platform = CustomerSQSMessagePlatform(receipt_handle=receipt_handle, body=customer_detail)

        customer = customer_platform.body
        raw = customer_raw_from_platform["Body"]

        assert customer.document == raw["document"]
        assert customer.customer_metafields[0].namespace == raw["customer_metafields"][0]["namespace"]
        assert customer.customer_metafields[0].key == raw["customer_metafields"][0]["key"]
        assert customer.customer_metafields[0].value == raw["customer_metafields"][0]["value"]
        assert customer.customer_metafields[1].namespace == raw["customer_metafields"][1]["namespace"]
        assert customer.customer_metafields[1].key == raw["customer_metafields"][1]["key"]
        assert customer.customer_metafields[1].value == raw["customer_metafields"][1]["value"]
        assert customer.payment_terms[0].deadline == raw["payment_terms"][0]["deadline"]
        assert customer.payment_terms[0].deadline == raw["payment_terms"][0]["deadline"]
        assert customer.payment_terms[0].deadline == raw["payment_terms"][0]["deadline"]
        assert customer.integration_type == raw["integration_type"]
        assert customer.seller_id == raw["seller_id"]
        assert customer.seller_code == raw["seller_code"]
        assert customer.seller_metafields[0].namespace == raw["seller_metafields"][0]["namespace"]
        assert customer.seller_metafields[0].key == raw["seller_metafields"][0]["key"]
        assert customer.seller_metafields[0].value == raw["seller_metafields"][0]["value"]
        assert customer.seller_metafields[1].namespace == raw["seller_metafields"][1]["namespace"]
        assert customer.seller_metafields[1].key == raw["seller_metafields"][1]["key"]
        assert customer.seller_metafields[1].value == raw["seller_metafields"][1]["value"]

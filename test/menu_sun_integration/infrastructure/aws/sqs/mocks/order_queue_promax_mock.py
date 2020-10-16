def mock_queue_make_api_call(self, operation_name, kwarg):
    if operation_name == 'SendMessage':
        return {'MD5OfMessageBody': 'a836c42e687e8a08e66a794a5dacd8c1',
                'MessageId': '85e8a505-2ba4-4fa3-a93c-cc30bf5e65e7',
                'ResponseMetadata': {'RequestId': '7313c686-bca3-5d79-9295-90a51d270c9c',
                                     'HTTPStatusCode': 200,
                                     'HTTPHeaders': {
                                         'x-amzn-requestid': '7313c686-bca3-5d79-9295-90a51d270c9c',
                                         'date': 'Fri, 18 Oct 2019 11:17:24 GMT',
                                         'content-type': 'text/xml', 'content-length': '378'},
                                     'RetryAttempts': 0}}
    if operation_name == 'ReceiveMessage':
        return {'Messages': [{'MessageId': '92de7972-f8e5-4998-a182-3977455f8cb0',
                              'ReceiptHandle': 'AQEBWvhuG9mMCVO0LE7k'
                                               '+flexfAzfGFn4yGRI5Xm60pwu1RwlGot4GqWveL1tOYmUTM63bwR+OFj5CL'
                                               '/e1ZchKlZ0DTF6rc9Q+pyNdbIKckaVrfgbYySsZDkr68AtoWzFoIf0U68SUO83ys0ydK'
                                               '+TSHgpw38zKICpupwccqe67HDu2Vve6ATFtjHa10+w3fU6l63NRFnmNeDjuDw'
                                               '/uq86s0puouRFHQmoeNlLg'
                                               '/5wjlT1excIDKxlIvJFBoc420ZgxulvIOcblqUxcGIG6Ah6x3aJw27q14vT'
                                               '+0wRi9aoQ8dG0ys57OeWjlRRG3UII1J5uiShet9F15CKF3GZatNEZOOXkIqdQO'
                                               '+lMHIhwMt7wls2EMtVO4KFIdWokzIFhidzfAHMTANCoAD26gUsp2Z9UyZaA==',
                              'MD5OfBody': 'a836c42e687e8a08e66a794a5dacd8c1',
                              'Body': '{"order_id": "12345",  "order_date": "2020-04-13T14:41:25", '
                                      '"delivery_date": "2020-04-14T14:41:25", "seller_code": "0810204",'
                                      ' "payment_code": "2", "document": "00005234000121",'
                                      ' "seller_id": 25, "integration_type": "PROMAX", '
                                      ' "items" : [{ "sku": "0001", "price" :10.00, "quantity": 1 }],'
                                      ' "total" : 31.80,"discount": 10.00, "shipping": 10.00,"subtotal": 21.80,'
                                      ' "billing_address" : {"name": "Boba Fett", "city":"Kamino"}}'},
                             ],
                'ResponseMetadata': {'RequestId': '0ffbdfb3-809f-539e-84dd-899024785f25',
                                     'HTTPStatusCode': 200,
                                     'HTTPHeaders': {
                                         'x-amzn-requestid': '0ffbdfb3-809f-539e-84dd-899024785f25',
                                         'date': 'Fri, 18 Oct 2019 11:31:51 GMT',
                                         'content-type': 'text/xml',
                                         'content-length': '892'}, 'RetryAttempts': 0}}
    if operation_name == 'DeleteMessage':
        return {'MD5OfMessageBody': 'a836c42e687e8a08e66a794a5dacd8c1',
                'ResponseMetadata': {'RequestId': '7313c686-bca3-5d79-9295-90a51d270c9c',
                                     'HTTPStatusCode': 200,
                                     'HTTPHeaders': {
                                         'x-amzn-requestid': '7313c686-bca3-5d79-9295-90a51d270c9c',
                                         'date': 'Fri, 18 Oct 2019 11:17:24 GMT',
                                         'content-type': 'text/xml', 'content-length': '378'},
                                     'RetryAttempts': 0}}


class S3Object:
    def read(self):
        return b'525200073;77,999989\n525200074;77,999989\n525200072;77,999989\n525200075;77,999989\n'


def mock_s3_bucket_make_api_call(self, operation_name, kwarg):
    if operation_name == 'GetObject':
        return {'Body': S3Object()}

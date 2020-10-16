
class S3Object:
    def read(self):
        return b'2019-10-24 00:00:00;2019-12-09 18:47:19;1;1;COLORADO CAUIM 016 ONE WAY 600ML CX C-12 ARTE;15348;12;;' \
               b'COLORADO CAUIM 016;;;;;COLORADO CAUIM 016 ONE WAY 600ML CX C-12 ARTE;;;;;;;\n'


def mock_s3_bucket_make_api_call(self, operation_name, kwarg):
    if operation_name == 'GetObject':
        return {'Body': S3Object()}

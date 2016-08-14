import os

AWS_STORAGE_BUCKET_NAME = 'staginghopestarterimageupload'
AWS_BUCKET_UPLOAD_PREFIX='uploads/'
AWS_BUCKET_UPLOAD_CDN='d2uc1tz5ijwlrf.cloudfront.net'
AWS_BUCKET_REGION=os.getenv('S3_REGION', 'eu-west-1')
AWS_VERIFY=True

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_S3_SECURE_URLS = True # use https
AWS_QUERYSTRING_AUTH = False
AWS_S3_HOST = 's3-eu-west-1.amazonaws.com'
# see http://developer.yahoo.com/performance/rules.html#expires
AWS_HEADERS = {
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}



BROKEN_IMAGE_URL = 'https://{}/images/medium/broken_image.png'.format(AWS_BUCKET_UPLOAD_CDN)

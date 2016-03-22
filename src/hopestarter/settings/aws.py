import os

AWS_BUCKET_UPLOAD='staginghopestarterimageupload'
AWS_BUCKET_UPLOAD_PREFIX='uploads/'
AWS_BUCKET_UPLOAD_CDN='d2uc1tz5ijwlrf.cloudfront.net'
AWS_BUCKET_REGION=os.getenv('S3_REGION', 'eu-west-1')
AWS_VERIFY=True

AWS_QUERYSTRING_AUTH = False


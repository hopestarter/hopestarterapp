import sys
import re
import boto3

from botocore.exceptions import ClientError

from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from hopebase.log import logger


class S3URLValidator(RegexValidator):
    message = 'Enter a valid S3 URL'
    lbl = '[a-z0-9][a-z0-9-]*[a-z0-9]'
    regex = re.compile(r'^s3://(' + lbl + '(?:\.' + lbl + ')*)/(.*)')


    def __call__(self, value):
        bucket_name, key_name = self.get_bucket_and_key(value)
        if bucket_name is None:
            raise ValidationError(self.message)
        elif bucket_name not in [settings.AWS_BUCKET_UPLOAD]:
            raise ValidationError("Invalid bucket name in URL")
        bucket = boto3.resource('s3', verify=settings.AWS_VERIFY).Bucket(bucket_name)
        key = bucket.Object(key_name)
        try:
            metadata = key.metadata
        except:
            c, v, t = sys.exc_info()
            if isinstance(v, ClientError):
                logger.exception("Invalid key URL")
                raise ValidationError, "Invalid key URL", t
            raise


    @classmethod
    def get_bucket_and_key(cls, url):
        match = cls.regex.search(url)
        if not match or len(match.groups()) != 2:
            return (None, None)
        return (match.group(1), match.group(2))


    @classmethod
    def get_public_url(cls, url, size='medium'):
        _, key_name = cls.get_bucket_and_key(url)
        if key_name is None:
            return settings.BROKEN_IMAGE_URL
        return 'https://{}/images/{}/{}'.format(
            settings.AWS_BUCKET_UPLOAD_CDN, size, key_name)

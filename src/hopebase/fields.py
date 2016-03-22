from __future__ import unicode_literals
import sys
import boto3
from botocore.exceptions import ClientError

from django.conf import settings

from rest_framework.exceptions import ValidationError
from rest_framework import fields

from hopebase.log import logger
from hopebase.validators import ProfilePictureValidator


class ProfileURLField(fields.CharField):
    default_error_messages = {
        'invalid': 'Enter a valid URL.'
    }

    def get_bucket_and_key(self, url):
        match = ProfilePictureValidator.regex.search(url)
        return (match.group(1), match.group(2))

    def __init__(self, *args, **kwargs):
        super(ProfileURLField, self).__init__(*args, **kwargs)
        validator = ProfilePictureValidator(
            message=self.error_messages['invalid'])
        self.validators.append(validator)

    def to_internal_value(self, data):
        bucket_name, key_name = self.get_bucket_and_key(data)
        if bucket_name not in [settings.AWS_BUCKET_UPLOAD]:
            raise ValidationError("Invalid bucket name in URL")
        bucket = boto3.resource('s3', verify=False).Bucket(bucket_name)
        key = bucket.Object(key_name)
        try:
            metadata = key.metadata
        except:
            c, v, t = sys.exc_info()
            if isinstance(v, ClientError):
                logger.exception("Invalid key URL")
                raise ValidationError, "Invalid key URL", t
            raise
        return data

    def to_representation(self, url):
        _, key_name = self.get_bucket_and_key(url)
        return 'https://{}/images/medium/{}'.format(
            settings.AWS_BUCKET_UPLOAD_CDN, key_name)

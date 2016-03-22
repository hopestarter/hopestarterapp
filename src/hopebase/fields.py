from __future__ import unicode_literals
import sys

from django.conf import settings

from rest_framework import fields

from hopebase.validators import S3URLValidator


class ProfileURLField(fields.CharField):
    default_error_messages = {
        'invalid': 'Enter a valid URL.'
    }


    def __init__(self, *args, **kwargs):
        super(ProfileURLField, self).__init__(*args, **kwargs)
        validator = S3URLValidator(
            message=self.error_messages['invalid'])
        self.validators.append(validator)

    def to_representation(self, url):
        _, key_name = S3URLValidator.get_bucket_and_key(url)
        if key_name is None:
            return settings.BROKEN_IMAGE_URL
        return 'https://{}/images/medium/{}'.format(
            settings.AWS_BUCKET_UPLOAD_CDN, key_name)

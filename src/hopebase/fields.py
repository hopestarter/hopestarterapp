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
        return S3URLValidator.get_public_url(url)

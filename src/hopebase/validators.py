import re

from rest_framework.fields import RegexValidator
from django.conf import settings


class ProfilePictureValidator(RegexValidator):
    message = 'Enter a valid S3 URL'
    lbl = '[a-z0-9][a-z0-9-]*[a-z0-9]'
    regex = re.compile(r'^s3://' + lbl + '(?:\.' + lbl + ')*/.*')

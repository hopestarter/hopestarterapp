import sys
import re

from django.core.validators import RegexValidator


class ProfilePictureValidator(RegexValidator):
    message = 'Enter a valid S3 URL'
    lbl = '[a-z0-9][a-z0-9-]*[a-z0-9]'
    regex = re.compile(r'^s3://(' + lbl + '(?:\.' + lbl + ')*)/(.*)')

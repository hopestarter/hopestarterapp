from django.conf import settings

from rest_framework import fields

from hopebase.validators import ProfilePictureValidator


class ProfileURLField(fields.CharField):
    default_error_messages = {
        'invalid': 'Enter a valid URL.'
    }

    def __init__(self, *args, **kwargs):
        super(ProfileURLField, self).__init__(*args, **kwargs)
        validator = ProfilePictureValidator(
            message=self.error_messages['invalid'])
        self.validators.append(validator)

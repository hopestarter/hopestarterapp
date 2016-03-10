import uuid

from django.conf import settings


def generate_upload_prefix():
    return settings.AWS_BUCKET_UPLOAD_PREFIX + str(uuid.uuid4()) + "/"

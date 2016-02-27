import boto3
import uuid
import json

from django.conf import settings

from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

from hopecollector import serializers
from hopebase import permissions
from hopespace.models import LocationMark


class LocationMarkSubmitView(generics.CreateAPIView):
    permission_classes = [getattr(permissions, p) for p in settings.LOCATION_PERMS]
    required_scopes = ['set-location']
    model = LocationMark
    serializer_class = serializers.LocationMarkSerializer


@api_view(['POST'])
def upload_image(request):
    bname = settings.AWS_BUCKET_UPLOAD
    bprefix = settings.AWS_BUCKET_UPLOAD_PREFIX + str(uuid.uuid4()) + "/"
    barn = "arn:aws:s3:::" + bname
    bpolicy = json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "s3:ListAllMyBuckets",
                "Resource": "arn:aws:s3:::*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucket",
                    "s3:GetBucketLocation"
                    ],
                "Resource": barn
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject",
                    "s3:GetObject",
                    "s3:DeleteObject"
                    ],
                "Resource": "{}/{}*".format(barn, bprefix)
            }
        ]
    })

    client = boto3.client('sts')
    response = client.get_federation_token(
        Name=request.user.username,
        Policy=bpolicy,
        DurationSeconds=900
    )
    return Response({
        "credentials": response['Credentials'],
        "bucket": {
            "name": bname,
            "prefix": bprefix,
            "region" : settings.AWS_BUCKET_REGION
        }
    });

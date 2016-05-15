import boto3
import json

from django.conf import settings

from rest_framework import generics, mixins
from rest_framework.filters import DjangoFilterBackend, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import api_view

from hopecollector import serializers, filters
from hopecollector.utils import generate_upload_prefix
from hopebase import permissions
from hopespace.models import LocationMark


class LocationMarkView(generics.ListAPIView):
    permission_classes = [getattr(permissions, p) for p in settings.LOCATION_PERMS]
    queryset = LocationMark.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = filters.LocationMarkFilterSet
    ordering_fields = ('created',)
    ordering = ('-created',)
    serializer_class = serializers.LocationMarkSerializer


class UserLocationMarkView(generics.CreateAPIView, LocationMarkView):
    filter_class = filters.UserLocationMarkFilterSet
    required_scopes = ['set-location']
    serializer_class = serializers.UserLocationMarkSerializer

    def get_queryset(self):
        # return LocationMark.objects.filter(user=self.request.user)
        return LocationMark.objects.all().order_by('-created')


@api_view(['POST'])
def upload_image(request):
    bname = settings.AWS_BUCKET_UPLOAD
    bprefix = generate_upload_prefix()
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

    client = boto3.client('sts', verify=settings.AWS_VERIFY)
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

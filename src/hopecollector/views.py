import boto3
import json

from django.conf import settings
from django.http import Http404
from django.core.exceptions import PermissionDenied

from rest_framework import generics, status
from rest_framework.filters import DjangoFilterBackend, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import api_view

from hopecollector import serializers, filters
from hopecollector.utils import generate_upload_prefix
from hopebase import permissions
from hopespace.models import LocationMark


class LocationMarkView(generics.ListAPIView):
    permission_classes = [getattr(permissions, p) for p in settings.LOCATION_PERMS]
    queryset = LocationMark.objects.filter(hidden=None)
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
        return LocationMark.objects.filter(user=self.request.user).order_by('-created')


@api_view(['PUT'])
def upload_image(request, pk=None):
    try:
        mark = LocationMark.objects.get(pk=pk)
    except LocationMark.DoesNotExist:
        raise Http404("Location Mark {mark_id} does not exists".format(mark_id=pk))
    if mark.user != request.user:
        raise PermissionDenied("You do not have permission for Mark {mark_id}".format(mark_id=pk))
    if mark.picture:
        mark.picture.delete()
    serializer = serializers.MarkPictureSerializer(mark, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

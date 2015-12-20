from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions

from hopecollector import serializers
from hopespace.models import LocationMark


class LocationMarkSubmitView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = LocationMark
    serializer_class = serializers.LocationMarkSerializer

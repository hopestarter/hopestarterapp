from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions

from hopecollector import serializers
from hopecollector.permissions import OptionalTokenHasScope
from hopespace.models import LocationMark


class LocationMarkSubmitView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, OptionalTokenHasScope)
    required_scopes = ['set-location']
    model = LocationMark
    serializer_class = serializers.LocationMarkSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

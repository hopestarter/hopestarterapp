from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers

from hopespace.models import LocationMark

create_only_user = serializers.CreateOnlyDefault(serializers.CurrentUserDefault())

class LocationMarkSerializer(GeoFeatureModelSerializer):
    """ A class to serialize location marks as GeoJSON compatible data """

    user = serializers.HiddenField(default=create_only_user)

    class Meta:
        model = LocationMark
        geo_field = "point"
        fields = ('created', 'point', 'user')

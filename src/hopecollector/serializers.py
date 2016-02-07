from rest_framework_gis.serializers import GeoFeatureModelSerializer

from hopespace.models import LocationMark

class LocationMarkSerializer(GeoFeatureModelSerializer):
    """ A class to serialize location marks as GeoJSON compatible data """

    class Meta:
        model = LocationMark
        geo_field = "point"
        fields = ('created', 'point')

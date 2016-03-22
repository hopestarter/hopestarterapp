from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers

from hopespace.models import LocationMark, LocationImageUpload
from hopebase import fields

create_only_user = serializers.CreateOnlyDefault(serializers.CurrentUserDefault())

class LocationMarkSerializer(GeoFeatureModelSerializer):
    """ A class to serialize location marks as GeoJSON compatible data """

    user = serializers.HiddenField(default=create_only_user)

    class _ImageSerializer(serializers.HyperlinkedModelSerializer):
        url = fields.ProfileURLField(max_length=200, allow_blank=True)

        class Meta:
            model = LocationImageUpload
            exclude = ('mark', 'modified', 'created')

    picture = _ImageSerializer(many=True, required=False)

    def to_representation(self, obj):
        r = super(LocationMarkSerializer, self).to_representation(obj)
        if r and 'picture' in r['properties'] and not r['properties']['picture']:
            del r['properties']['picture']
        return r


    def create(self, validated_data):
        pictures = validated_data.pop('picture', [])
        mark = LocationMark.objects.create(**validated_data)
        for picture in pictures:
            LocationImageUpload.objects.create(mark=mark, **picture)
        return mark

    class Meta:
        model = LocationMark
        geo_field = "point"
        depth = 1
        fields = ('created', 'point', 'user', 'picture')

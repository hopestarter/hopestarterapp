from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers

from hopespace.models import LocationMark
from hopebase.serializers import UserSerializer

create_only_user = serializers.CreateOnlyDefault(serializers.CurrentUserDefault())


class LocationMarkSerializer(GeoFeatureModelSerializer):
    """ A class to serialize location marks as GeoJSON compatible data """
    user = UserSerializer()
    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        if not obj.picture:
            return {
                'large': None,
                'medium': None,
                'small': None,
                'thumbnail': None
            }
        return {
            'large': obj.large_picture.url,
            'medium': obj.medium_picture.url,
            'small': obj.small_picture.url,
            'thumbnail': obj.thumbnail_picture.url
        }

    class Meta:
        model = LocationMark
        geo_field = "point"
        depth = 1
        exclude = ('picture', 'large_picture', 'medium_picture',
                   'small_picture', 'thumbnail_picture',
                  )
        read_only_fields = ('created', 'photo')


class UserLocationMarkSerializer(LocationMarkSerializer):
    """ A class to serialize location marks as GeoJSON compatible data """
    user = serializers.HiddenField(default=create_only_user)

    class Meta(LocationMarkSerializer.Meta):
        pass


class MarkPictureSerializer(serializers.HyperlinkedModelSerializer):
    """
    Shows picture upload result
    """

    class Meta:
        model = LocationMark
        fields = ('pk', 'picture')

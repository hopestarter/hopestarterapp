from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse

from hopebase import models


class UserProfileSerializer(serializers.ModelSerializer):
    """ A class to serialize the user profile """
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
        model = models.UserProfile
        exclude = ('user', 'id', 'modified', 'picture', 'large_picture',
                   'medium_picture', 'small_picture', 'thumbnail_picture',
                   )
        read_only_fields = ('created', 'photo')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer()
    ethnicities = serializers.StringRelatedField(many=True)
    mark = serializers.SerializerMethodField()

    def get_mark(self, obj):
        request = self.context.get('request', None)
        if request is not None and request.user == obj:
            return reverse('base:user_marks', request=request)
        return "{}?user={}".format(
            reverse('collector:locationmark', request=request), obj.id)

    class Meta:
        model = get_user_model()
        fields = ('username', 'profile', 'ethnicities', 'mark')
        read_only_fields = ('username',)


class PictureSerializer(serializers.HyperlinkedModelSerializer):
    """
    Shows picture upload result
    """

    class Meta:
        model = models.UserProfile
        fields = ('pk', 'picture')

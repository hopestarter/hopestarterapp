from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse

from hopebase import models, fields


class UserProfileSerializer(serializers.ModelSerializer):
    """ A class to serialize the user profile """

    picture = fields.ProfileURLField(max_length=200, allow_blank=True)

    class Meta:
        model = models.UserProfile
        exclude = ('user', 'id', 'modified')
        read_only_fields = ('created')


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

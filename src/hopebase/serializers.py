from django.contrib.auth.models import User
from rest_framework import serializers

from hopebase import models, fields


class UserProfileSerializer(serializers.ModelSerializer):
    """ A class to serialize the user profile """

    picture = fields.ProfileURLField(max_length=200, allow_blank=True)

    class Meta:
        model = models.UserProfile
        exclude = ('user', 'id')
        read_only_fields = ('created', 'modified')


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    ethnicities = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ('username', 'profile', 'ethnicities')

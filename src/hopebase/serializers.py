from rest_framework import serializers

from hopebase import models

class UserProfileSerializer(serializers.ModelSerializer):
    """ A class to serialize the user profile """

    class Meta:
        model = models.UserProfile
        exclude = ('user', 'id')
        read_only_fields = ('created', 'modified')

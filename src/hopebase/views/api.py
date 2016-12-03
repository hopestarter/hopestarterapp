from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import Http404

from rest_framework import generics, mixins
from rest_framework import status
from rest_framework.response import Response

from hopebase import serializers, permissions
from hopebase.models import UserProfile, UserStats


class UserView(generics.RetrieveAPIView):
    permission_classes = [getattr(permissions, p) for p in settings.ETHNICITY_PERMS]
    required_scopes = ['account']
    model = User

    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [getattr(permissions, p) for p in settings.PROFILE_PERMS]
    required_scopes = ['update-profile']
    model = UserProfile
    serializer_class = serializers.UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj


class UserStatsView(generics.RetrieveAPIView):
    permission_classes = [getattr(permissions, p) for p in settings.USER_STATS_PERMS]
    model = UserStats
    serializer_class = serializers.UserStatsSerializer

    def get_queryset(self):
        return UserStats.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj


class UploadPictureView(generics.RetrieveUpdateAPIView):
    permission_classes = [getattr(permissions, p) for p in settings.PROFILE_PERMS]
    required_scopes = ['update-profile']
    serializer_class = serializers.PictureSerializer
    model = UserProfile

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj

    def put(self, request, format=None):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            raise Http404("Profile does not exists")
        if profile.picture:
            profile.picture.delete()
        # if profile.thumbnail:
            # profile.thumbnail.delete()
        serializer = serializers.PictureSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

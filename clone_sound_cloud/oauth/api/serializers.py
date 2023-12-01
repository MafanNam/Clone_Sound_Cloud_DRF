from rest_framework import serializers

from oauth.models import UserProfile

from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name', 'password')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'country', 'city', 'bio', 'display_name',)
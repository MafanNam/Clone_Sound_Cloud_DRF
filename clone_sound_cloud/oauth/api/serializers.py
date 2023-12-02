from rest_framework import serializers

from oauth.models import UserProfile, SocialLink

from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name', 'password')


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ('id', 'link',)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'avatar', 'country',
                  'city', 'bio', 'display_name',)


class AuthorSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(many=False)
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ('id',  'email', 'first_name', 'last_name',
                  'user_profile', 'social_links',)

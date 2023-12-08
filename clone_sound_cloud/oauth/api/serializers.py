from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from oauth.models import UserProfile, SocialLink, UserFollowing

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


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ('id', 'following_user', 'created_at',)


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = ('id', 'user', 'created_at',)


class UserProfileSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('id', 'avatar', 'country',
                  'city', 'bio', 'display_name',
                  'following', 'followers',)

    @extend_schema_field(FollowingSerializer)
    def get_following(self, obj):
        return FollowingSerializer(obj.user.following.all(), many=True).data

    @extend_schema_field(FollowersSerializer)
    def get_followers(self, obj):
        return FollowersSerializer(obj.user.followers.all(), many=True).data


class AuthorSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(many=False)
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name',
                  'user_profile', 'social_links',)

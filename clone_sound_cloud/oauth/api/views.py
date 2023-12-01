from django.shortcuts import render
from rest_framework import viewsets, parsers, permissions

from base.permissions import IsAuthor
from . import serializers
from oauth.models import UserProfile


def login_spotify(request):
    return render(request, 'login_spotify.html')


class UserProfileView(viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.get(user=self.request.user)

    def get_object(self):
        return self.get_queryset()


class AuthorView(viewsets.ReadOnlyModelViewSet):
    """List authors"""
    queryset = UserProfile.objects.all().prefetch_related('social_links')
    serializer_class = serializers.UserProfileSerializer


class SocialLinkView(viewsets.ModelViewSet):
    """CRUD social link user"""
    serializer_class = serializers.SocialLinkSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return self.request.user.social_links.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

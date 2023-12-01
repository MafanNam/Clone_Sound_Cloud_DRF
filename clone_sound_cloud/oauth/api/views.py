from django.shortcuts import render
from rest_framework import viewsets, parsers, permissions

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


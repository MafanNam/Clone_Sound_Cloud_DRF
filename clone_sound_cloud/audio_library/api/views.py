from rest_framework import generics, viewsets

from audio_library import models
from audio_library.api import serializers
from base.permissions import IsAuthor


class GenreView(generics.ListAPIView):
    """List genre"""
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class LicenseView(viewsets.ModelViewSet):
    """CRUD license user"""
    serializer_class = serializers.LicenseSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return models.License.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)









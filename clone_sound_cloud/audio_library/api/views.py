import os.path
from django.utils import timezone
from django.http import FileResponse, Http404
from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.filter_backends import (
    SuggesterFilterBackend, FunctionalSuggesterFilterBackend,
    CompoundSearchFilterBackend)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from rest_framework import generics, viewsets, parsers, views, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from audio_library import models
from audio_library.api import serializers
from audio_library.documents import TrackDocument
from base.classes import MixedSerializer, TrackAPIListPagination
from base.permissions import IsAuthor
from base.services import delete_old_file


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


class AlbumView(viewsets.ModelViewSet):
    """CRUD album user"""
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializers.AlbumSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return models.Album.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class PublicAlbumView(generics.ListAPIView):
    """List public album for user"""
    serializer_class = serializers.AlbumSerializer

    def get_queryset(self):
        return models.Album.objects.filter(user__id=self.kwargs.get('pk'),
                                           private=False)


class TrackView(MixedSerializer, viewsets.ModelViewSet):
    """CRUD tracks"""
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthor]
    serializer_class = serializers.CreateAuthorTrackSerializer
    serializer_classes_by_action = {
        'list': serializers.AuthorTrackSerializer,
    }

    def get_queryset(self):
        return (models.Track.objects.filter(user=self.request.user)
                .prefetch_related('user', 'user__following', 'user__followers',
                                  'user__social_links', 'license', 'genre')
                .select_related('license', 'user__user_profile', 'album'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        delete_old_file(instance.file.path)
        instance.delete()


class PlayListView(MixedSerializer, viewsets.ModelViewSet):
    """CRUD playlist for user"""
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthor]
    serializer_class = serializers.CreatePlayListSerializer
    serializer_classes_by_action = {
        'list': serializers.PlayListSerializer,
    }

    def get_queryset(self):
        return (models.Playlist.objects.filter(user=self.request.user)
                .prefetch_related('tracks__user', 'tracks__user__following',
                                  'tracks__user__followers', 'tracks__user__social_links',
                                  'tracks__license', 'tracks__genre'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class TrackListView(generics.ListAPIView):
    """List all track"""
    queryset = (models.Track.objects.filter(private=False).order_by('-id')
                .prefetch_related('user', 'user__following', 'user__followers',
                                  'user__social_links', 'license', 'genre')
                .select_related('license', 'user__user_profile', 'album'))
    serializer_class = serializers.AuthorTrackSerializer
    pagination_class = TrackAPIListPagination
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('title', 'user')
    ordering_fields = (
        'create_at', 'play_count', 'download', 'user',)
    filterset_fields = ['title', 'user__user_profile__display_name',
                        'album__name', 'genre__name', ]


@extend_schema(tags=['ElasticSearch'])
class SearchTrackView(DocumentViewSet):
    """NOT COMPLETE API ENDPOINT!!!"""
    pagination_class = TrackAPIListPagination
    serializer_class = serializers.TrackDocumentSerializer
    document = TrackDocument

    filter_backends = [
        CompoundSearchFilterBackend,
        FunctionalSuggesterFilterBackend,
        SuggesterFilterBackend,
    ]

    search_fields = (
        'title',
    )

    suggester_fields = {
        'title': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
    }

    # functional_suggester_fields = {
    #
    # }


class TrackRecentlyPlayedView(generics.ListAPIView):
    """List all recently played track"""
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AuthorTrackSerializer

    def get_queryset(self):
        return (models.Track.objects.filter(
            private=False, played_track__user=self.request.user).order_by(
            '-played_track__played_at')[:10]
                .prefetch_related('user', 'user__following', 'user__followers',
                                  'user__social_links', 'license', 'genre')
                .select_related('license', 'user__user_profile', 'album'))


class AuthorTrackListView(generics.ListAPIView):
    """List all track user"""
    serializer_class = serializers.AuthorTrackSerializer
    pagination_class = TrackAPIListPagination
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('title', 'user')
    ordering_fields = (
        'create_at', 'play_count', 'download', 'user',)
    filterset_fields = ['title', 'album__name', 'genre__name']

    def get_queryset(self):
        return (models.Track.objects.filter(
            user__id=self.kwargs.get('pk'),
            private=False).order_by('-id')
                .prefetch_related('user', 'license', 'user__following',
                                  'user__followers', 'user__social_links', 'genre')
                .select_related('user', 'user__user_profile'))


class StreamingFileView(views.APIView):
    """Listen track"""
    serializer_class = None

    def set_play(self):
        self.track.plays_count += 1
        self.track.save()

    def get(self, request, pk):
        self.track = get_object_or_404(models.Track, id=pk, private=False)
        if os.path.exists(self.track.file.path):
            self.set_play()
            if request.user.is_authenticated:
                played_instance, created = models.PlayedUserTrack.objects.get_or_create(
                    user_id=request.user.id,
                    track=self.track,
                )

                played_instance.played_at = timezone.now()
                played_instance.save()

            return FileResponse(open(self.track.file.path, 'rb'),
                                filename=self.track.file.name)
        else:
            return Http404


class StreamingFileAuthorView(views.APIView):
    """Listen track user"""
    serializer_class = None
    permission_classes = [IsAuthor]

    def set_play(self):
        self.track.plays_count += 1
        self.track.save()

    def get(self, request, pk):
        self.track = get_object_or_404(models.Track, id=pk)
        if os.path.exists(self.track.file.path):
            self.set_play()
            return FileResponse(open(self.track.file.path, 'rb'),
                                filename=self.track.file.name)
        else:
            return Http404


class DownloadTrackView(views.APIView):
    """Download track"""
    serializer_class = None

    def set_download(self):
        self.track.download += 1
        self.track.save()

    def get(self, request, pk):
        self.track = get_object_or_404(models.Track, id=pk, private=False)
        if os.path.exists(self.track.file.path):
            self.set_download()
            return FileResponse(
                open(self.track.file.path, 'rb'),
                filename=self.track.file.name, as_attachment=True
            )
        else:
            return Http404


class CommentAuthorView(viewsets.ModelViewSet):
    """CRUD comment user"""
    serializer_class = serializers.CommentAuthorSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return models.Comment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentView(viewsets.ModelViewSet):
    """Comment for track"""
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return (models.Comment.objects.filter(track_id=self.kwargs.get('pk'))
                .prefetch_related('user', 'user__user_profile', 'user__following',
                                  'user__followers', 'user__social_links')
                .select_related('user'))


class TrackLikeView(views.APIView):
    """Track like for authenticated user"""
    serializer_class = None
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """Set like for a track"""
        track = get_object_or_404(models.Track, id=pk, private=False)
        if track.user == request.user:
            return Response({'message': 'You can not like own track.'},
                            status=status.HTTP_403_FORBIDDEN)
        if request.user.likes_of_tracks.filter(id=track.id).exists():
            return Response({'message': 'You already like this track.'},
                            status=status.HTTP_400_BAD_REQUEST)

        track.user_of_likes.add(request.user.id)
        track.likes_count += 1
        track.save()

        return Response({'message': 'You like track.'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """Remove like from track"""
        track = get_object_or_404(models.Track, id=pk, private=False)
        if not request.user.likes_of_tracks.filter(id=track.id).exists():
            return Response(
                {'message': 'You dont like this track for removing.'},
                status=status.HTTP_403_FORBIDDEN)

        track.user_of_likes.remove(request.user.id)
        track.likes_count -= 1
        track.save()

        return Response({'message': 'Remove like track.'}, status=status.HTTP_204_NO_CONTENT)

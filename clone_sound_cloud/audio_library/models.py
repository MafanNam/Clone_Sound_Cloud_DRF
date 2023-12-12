from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from base.services import (
    get_path_upload_cover_album, validate_size_image,
    validate_size_audio, get_path_upload_track,
    get_path_upload_cover_playlist, get_path_upload_cover_track,
)


class License(models.Model):
    """Model licence audio user"""
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='licenses')
    text = models.TextField(max_length=1000)

    def __str__(self):
        return f"License-{self.id}"


class Genre(models.Model):
    """Model of genre audio"""
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    """Model album for audio"""
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='albums')
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    private = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to=get_path_upload_cover_album, blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']),
                    validate_size_image]
    )

    def __str__(self):
        return f"{self.name} - {self.user}"


class Track(models.Model):
    """Model track"""
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=100)
    license = models.ForeignKey(
        License, on_delete=models.PROTECT, related_name='license_tracks')
    genre = models.ManyToManyField(Genre, related_name='track_genres')
    album = models.ForeignKey(
        Album, on_delete=models.SET_NULL, blank=True, null=True)
    link_of_author = models.CharField(max_length=500, blank=True, null=True)
    file = models.FileField(
        upload_to=get_path_upload_track,
        validators=[
            FileExtensionValidator(allowed_extensions=['mp3', 'wav']),
            validate_size_audio]
    )
    create_at = models.DateTimeField(auto_now_add=True)
    plays_count = models.PositiveIntegerField(default=0)
    download = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    user_of_likes = models.ManyToManyField(
        get_user_model(), related_name='likes_of_tracks', blank=True)
    private = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to=get_path_upload_cover_track, blank=True, null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg']),
            validate_size_image]
    )

    def __str__(self):
        return f"{self.user} - {self.title}"


class PlayedUserTrack(models.Model):
    """Played user track data"""
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='user_played_track')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='played_track')
    played_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} played {self.track.title} at {self.played_at }"


class Comment(models.Model):
    """Model comment for track"""
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='comments')
    track = models.ForeignKey(
        Track, on_delete=models.CASCADE, related_name='track_comments')
    text = models.TextField(max_length=1000)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.track.title}"


class Playlist(models.Model):
    """Model playlist user"""
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='playlists')
    title = models.CharField(max_length=50)
    tracks = models.ManyToManyField(Track, related_name='playlist_tracks')
    cover = models.ImageField(
        upload_to=get_path_upload_cover_playlist, blank=True, null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg']),
            validate_size_image]
    )

    def __str__(self):
        return f"{self.user} - {self.title}"

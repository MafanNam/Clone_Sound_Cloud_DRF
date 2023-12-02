from django.contrib import admin

from . import models


@admin.register(models.License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)
    list_display_links = ('user',)
    list_filter = ('user',)


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('name',)


@admin.register(models.Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name')
    list_display_links = ('user',)
    list_filter = ('user',)


@admin.register(models.Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'create_at')
    list_display_links = ('user',)
    list_filter = ('genre', 'create_at')
    search_fields = ('user', 'genre__name')


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'track')
    list_display_links = ('user',)


@admin.register(models.Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title',)
    list_display_links = ('user',)
    search_fields = ('user', 'track__title')

from django.urls import path

from rest_framework import routers

from . import views

app_name = 'audio'

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'track-search', views.SearchTrackView, basename='track-search')

urlpatterns = [
    path('genre/', views.GenreView.as_view(), name='genre'),

    path('license/', views.LicenseView.as_view(
        {'get': 'list', 'post': 'create'}), name='license'),
    path('license/<int:pk>', views.LicenseView.as_view(
        {'put': 'update', 'delete': 'destroy'}), name='license_detail'),

    path('album/', views.AlbumView.as_view(
        {'get': 'list', 'post': 'create'}), name='album'),
    path('album/<int:pk>/', views.AlbumView.as_view(
        {'put': 'update', 'delete': 'destroy'}), name='album_detail'),

    path('author-album/<int:pk>/', views.PublicAlbumView.as_view(),
         name='author_album'),

    path('track/', views.TrackView.as_view(
        {'get': 'list', 'post': 'create'}), name='track'),
    path('track/<int:pk>/', views.TrackView.as_view({
        'put': 'update', 'delete': 'destroy'}), name='track_detail'),
    path('track/<int:pk>/like/', views.TrackLikeView.as_view(),
         name='track_like'),
    path('track/recently-played/', views.TrackRecentlyPlayedView.as_view(),
         name='tracks_recently_played'),

    path('stream-track/<int:pk>/', views.StreamingFileView.as_view(),
         name='stream_track'),
    path('stream-author-track/<int:pk>/', views.StreamingFileAuthorView.as_view(),
         name='stream_author_track'),
    path('download-track/<int:pk>/', views.DownloadTrackView.as_view(),
         name='download_track'),

    path('track-list/', views.TrackListView.as_view(), name='track_list'),
    path('author-track-list/<int:pk>/', views.AuthorTrackListView.as_view(),
         name='author_track_list'),

    path('comments/', views.CommentAuthorView.as_view(
        {'get': 'list', 'post': 'create'}), name='comments'),
    path('comments/<int:pk>/', views.CommentAuthorView.as_view({
        'put': 'update', 'delete': 'destroy'}), name='comments_detail'),

    path('comments-by-track/<int:pk>/', views.CommentView.as_view(
        {'get': 'list'}), name='comments_by_track'),

    path('playlist/', views.PlayListView.as_view(
        {'get': 'list', 'post': 'create'}), name='playlist'),
    path('playlist/<int:pk>/', views.PlayListView.as_view(
        {'put': 'update', 'delete': 'destroy'}), name='playlist_detail'),

]

urlpatterns += router.urls

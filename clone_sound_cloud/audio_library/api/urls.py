from django.urls import path

from . import views

app_name = 'audio'

urlpatterns = [
    path('genre/', views.GenreView.as_view(), name='genre'),

    path('license/', views.LicenseView.as_view(
        {'get': 'list', 'post': 'create'})),
    path('license/<int:pk>', views.LicenseView.as_view(
        {'put': 'update', 'delete': 'destroy'})),

    path('album/', views.AlbumView.as_view(
        {'get': 'list', 'post': 'create'})),
    path('album/<int:pk>/', views.AlbumView.as_view(
        {'put': 'update', 'delete': 'destroy'})),

    path('author-album/<int:pk>/', views.PublicAlbumView.as_view(),
         name='author_album'),

    path('track/', views.TrackView.as_view(
        {'get': 'list', 'post': 'create'})),
    path('track/<int:pk>/', views.TrackView.as_view({
        'put': 'update', 'delete': 'destroy'})),
    path('track/<int:pk>/like/', views.TrackLikeView.as_view()),

    path('stream-track/<int:pk>/', views.StreamingFileView.as_view(),
         name='stream_track'),
    path('stream-author-track/<int:pk>/', views.StreamingFileAuthorView.as_view()),
    path('download-track/<int:pk>/', views.DownloadTrackView.as_view()),

    path('track-list/', views.TrackListView.as_view(), name='track_list'),
    path('track-list/recently-played/', views.TrackListRecentlyPlayedView.as_view()),
    path('author-track-list/<int:pk>/', views.AuthorTrackListView.as_view(),
         name='author_track_list'),

    path('comments/', views.CommentAuthorView.as_view(
        {'get': 'list', 'post': 'create'})),
    path('comments/<int:pk>/', views.CommentAuthorView.as_view({
        'put': 'update', 'delete': 'destroy'})),

    path('comments-by-track/<int:pk>/', views.CommentView.as_view({'get': 'list'}),
         name='comments_by_track'),

    path('playlist/', views.PlayListView.as_view(
        {'get': 'list', 'post': 'create'})),
    path('playlist/<int:pk>/', views.PlayListView.as_view(
        {'put': 'update', 'delete': 'destroy'})),

]

from django.urls import path

from . import views


urlpatterns = [
    path('genre/', views.GenreView.as_view()),

    path('license/', views.LicenseView.as_view({'get': 'list', 'post': 'create'})),
    path('license/<int:pk>', views.LicenseView.as_view({'put': 'update', 'delete': 'destroy'})),

    path('album/', views.AlbumView.as_view({'get': 'list', 'post': 'create'})),
    path('album/<int:pk>/', views.AlbumView.as_view({'put': 'update', 'delete': 'destroy'})),

    path('author-album/<int:pk>/', views.PublicAlbumView.as_view()),

    path('track/', views.TrackView.as_view({'get': 'list', 'post': 'create'})),
    path('track/<int:pk>/', views.TrackView.as_view({'put': 'update', 'delete': 'destroy'})),

]



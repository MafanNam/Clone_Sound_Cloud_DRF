from django.urls import path, include
from . import views

urlpatterns = [
    path('user-profile/', views.UserProfileView.as_view(
        {'get': 'retrieve', 'put': 'update'})),

    path('author/', views.AuthorView.as_view({'get': 'list'})),
    path('author/<int:pk>/', views.AuthorView.as_view({'get': 'retrieve'})),
    path('author/<int:pk>/follow-unfollow/', views.FollowAuthorView.as_view()),
    # path('author/<int:pk>/unfollow/', views.AuthorView.as_view()),

    path('social-link/', views.SocialLinkView.as_view(
        {'get': 'list', 'post': 'create'})),
    path('social-link/<int:pk>/', views.SocialLinkView.as_view(
        {'put': 'update', 'delete': 'destroy'})),

    path('spotify/', views.login_spotify),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),

    # re_path(r'^auth-social/', include('drf_social_oauth2.urls',
    # namespace='drf')),
    # path('auth/', include('djoser.urls.authtoken')),
]

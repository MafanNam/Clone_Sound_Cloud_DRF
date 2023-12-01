from django.urls import path, include
from . import views


urlpatterns = [
    path('user-profile/', views.UserProfileView.as_view({'get': 'retrieve', 'put': 'update'})),

    path('spotify/', views.login_spotify),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),

    # re_path(r'^auth-social/', include('drf_social_oauth2.urls', namespace='drf')),
    # path('auth/', include('djoser.urls.authtoken')),
]






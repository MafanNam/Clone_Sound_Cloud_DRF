from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'oauth'


router = DefaultRouter()
router.register("users", views.CustomUserViewSet)

urlpatterns = [
    path('celery-test/', views.test),
    path('send-spam-onse-week-email/', views.send_spam_email_ones_week_celery),

    path('user-profile/', views.UserProfileView.as_view(
        {'get': 'retrieve', 'put': 'update'}), name='user_profile'),

    path('author/', views.AuthorView.as_view({'get': 'list'}), name='author'),
    path('author/<int:pk>/', views.AuthorView.as_view({'get': 'retrieve'})),
    path('author/<int:pk>/follow-unfollow/', views.FollowAuthorView.as_view(),
         name='author_follow_unfollow'),

    path('social-link/', views.SocialLinkView.as_view(
        {'get': 'list', 'post': 'create'}), name='social_link'),
    path('social-link/<int:pk>/', views.SocialLinkView.as_view(
        {'put': 'update', 'delete': 'destroy'}), name='social_link_detail'),

    path('spotify/', views.login_spotify),
    path('auth/', include(router.urls)),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt')),
    # path('auth/', include('djoser.social.urls')),
]

from django.urls import path, re_path, include
from . import views, auth_view


urlpatterns = [
    re_path(r'^auth/', include('drf_social_oauth2.urls', namespace='drf')),

]




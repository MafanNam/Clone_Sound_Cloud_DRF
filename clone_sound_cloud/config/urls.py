from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("oauth.api.urls")),
    path("api/audio/", include("audio_library.api.urls")),
    path("api/social/", include("social_django.urls")),
    path(
        ".well-known/assetlinks.json",
        TemplateView.as_view(
            template_name="assetlinks.json", content_type="application/json"
        ),
    ),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("__debug__/", include("debug_toolbar.urls")),
]

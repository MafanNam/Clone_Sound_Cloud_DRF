from drf_spectacular.contrib.django_oauth_toolkit import DjangoOAuthToolkitScheme
from drf_social_oauth2.authentication import SocialAuthentication


class DjangoOAuthToolkitUserScheme(DjangoOAuthToolkitScheme):
    target_class = SocialAuthentication

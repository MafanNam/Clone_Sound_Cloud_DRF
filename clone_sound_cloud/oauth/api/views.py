from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from djoser import signals
from djoser.compat import get_user_email
from djoser.conf import settings

from rest_framework import viewsets, parsers, permissions, views
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from djoser.views import UserViewSet

from oauth.tasks import send_activate_email, test_funk

from base.permissions import IsAuthor
from . import serializers
from oauth.models import UserProfile, UserFollowing


def login_spotify(request):
    return render(request, 'login_spotify.html')


def test(request):
    test_funk.delay()
    return HttpResponse('Done')


class CustomUserViewSet(UserViewSet):
    def perform_create(self, serializer, *args, **kwargs):
        user = serializer.save(*args, **kwargs)
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )

        context = {"user": user}
        to = [get_user_email(user)]

        if settings.SEND_ACTIVATION_EMAIL:
            send_activate_email.delay(
                {
                    'user_id': user.id,
                    'domain': self.request.get_host(),
                    'protocol': 'https' if self.request.is_secure() else 'http',
                    'site_name': self.request.get_host()
                },
                [get_user_email(user)]
            )
        elif settings.SEND_CONFIRMATION_EMAIL:
            settings.EMAIL.confirmation(self.request, context).send(to)


class UserProfileView(viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.get(user=self.request.user)

    def get_object(self):
        return self.get_queryset()


class AuthorView(viewsets.ReadOnlyModelViewSet):
    """List authors"""
    queryset = get_user_model().objects.all().prefetch_related('social_links')
    serializer_class = serializers.AuthorSerializer


class SocialLinkView(viewsets.ModelViewSet):
    """CRUD social link user"""
    serializer_class = serializers.SocialLinkSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return self.request.user.social_links.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FollowAuthorView(views.APIView):
    """Follow author"""
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def post(self, request, pk):
        author = get_object_or_404(get_user_model(), id=pk)

        if request.user == author:
            return Response({'message': 'You can not follow yourself'}, status=200)

        following_instance, created = UserFollowing.objects.get_or_create(
            user=request.user,
            following_user=author
        )
        if not created:
            return Response({'message': 'Already following this user'}, status=200)
        return Response({'message': 'Now following this user'}, status=201)

    def delete(self, request, pk):
        author = get_object_or_404(get_user_model(), id=pk)
        try:
            following_instance = UserFollowing.objects.get(
                user=request.user,
                following_user=author
            )
            following_instance.delete()
            return Response({'message': 'Unfollowed successfully'}, status=204)
        except UserFollowing.DoesNotExist:
            return Response({'error': 'You were not following this user'}, status=404)

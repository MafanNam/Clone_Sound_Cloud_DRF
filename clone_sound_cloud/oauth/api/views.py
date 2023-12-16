from django.contrib.auth import get_user_model, update_session_auth_hash
from django.utils.timezone import now
from django.http import HttpResponse
from django.shortcuts import render

from djoser import signals, utils
from djoser.compat import get_user_email
from djoser.conf import settings
from djoser.views import UserViewSet

from rest_framework import parsers, permissions, status, views, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from oauth.tasks import send_email_celery_task, send_spam_email_celery_task

from oauth.models import UserProfile, UserFollowing
from base.permissions import IsAuthor
from . import serializers

User = get_user_model()


def login_spotify(request):
    return render(request, 'login_spotify.html')


def test(request):
    send_spam_email_celery_task.delay()
    return HttpResponse('Done')


class CustomUserViewSet(UserViewSet):
    def perform_create(self, serializer, *args, **kwargs):
        user = serializer.save(*args, **kwargs)
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )

        email_to = [get_user_email(user)]
        context = {
            'user_id': user.id,
            'domain': self.request.get_host(),
            'protocol': 'https' if self.request.is_secure() else 'http',
            'site_name': self.request.get_host()
        }

        if settings.SEND_ACTIVATION_EMAIL:
            send_email_celery_task.delay(context, email_to, 'ActivationEmail')
        elif settings.SEND_CONFIRMATION_EMAIL:
            send_email_celery_task.delay(context, email_to, 'ConfirmationEmail')

    def perform_update(self, serializer, *args, **kwargs):
        serializer.save()
        user = serializer.instance
        signals.user_updated.send(
            sender=self.__class__, user=user, request=self.request
        )

        if settings.SEND_ACTIVATION_EMAIL and not user.is_active:
            email_to = [get_user_email(user)]
            context = {
                'user_id': user.id,
                'domain': self.request.get_host(),
                'protocol': 'https' if self.request.is_secure() else 'http',
                'site_name': self.request.get_host()
            }
            send_email_celery_task.delay(context, email_to, 'ActivationEmail')

    @action(["post"], detail=False)
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()

        signals.user_activated.send(
            sender=self.__class__, user=user, request=self.request
        )

        if settings.SEND_CONFIRMATION_EMAIL:
            email_to = [get_user_email(user)]
            context = {
                'user_id': user.id,
                'domain': self.request.get_host(),
                'protocol': 'https' if self.request.is_secure() else 'http',
                'site_name': self.request.get_host()
            }
            send_email_celery_task.delay(context, email_to, 'ConfirmationEmail')

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False)
    def resend_activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user(is_active=False)

        if not settings.SEND_ACTIVATION_EMAIL:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if user:
            email_to = [get_user_email(user)]
            context = {
                'user_id': user.id,
                'domain': self.request.get_host(),
                'protocol': 'https' if self.request.is_secure() else 'http',
                'site_name': self.request.get_host()
            }
            send_email_celery_task.delay(context, email_to, 'ActivationEmail')

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False)
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()

        if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            email_to = [get_user_email(self.request.user)]
            context = {
                'user_id': self.request.user.id,
                'domain': self.request.get_host(),
                'protocol': 'https' if self.request.is_secure() else 'http',
                'site_name': self.request.get_host()
            }
            send_email_celery_task.delay(context, email_to, 'PasswordChangedConfirmationEmail')

        if settings.LOGOUT_ON_PASSWORD_CHANGE:
            utils.logout_user(self.request)
        elif settings.CREATE_SESSION_ON_LOGIN:
            update_session_auth_hash(self.request, self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()

        if user:
            email_to = [get_user_email(user)]
            context = {
                'user_id': user.id,
                'domain': self.request.get_host(),
                'protocol': 'https' if self.request.is_secure() else 'http',
                'site_name': self.request.get_host()
            }
            send_email_celery_task.delay(context, email_to, 'PasswordResetEmail')

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False)
    def reset_password_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.user.set_password(serializer.data["new_password"])
        if hasattr(serializer.user, "last_login"):
            serializer.user.last_login = now()
        serializer.user.save()

        if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            email_to = [get_user_email(serializer.user)]
            context = {
                'user_id': serializer.user.id,
                'domain': self.request.get_host(),
                'protocol': 'https' if self.request.is_secure() else 'http',
                'site_name': self.request.get_host()
            }
            send_email_celery_task.delay(context, email_to, 'PasswordChangedConfirmationEmail')
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False, url_path=f"set_{User.USERNAME_FIELD}")
    def set_username(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        new_username = serializer.data["new_" + User.USERNAME_FIELD]

        setattr(user, User.USERNAME_FIELD, new_username)
        user.save()
        if settings.USERNAME_CHANGED_EMAIL_CONFIRMATION:
            email_to = [get_user_email(user)]
            context = {
                'user_id': user.id,
                'domain': self.request.get_host(),
                'protocol': 'https' if self.request.is_secure() else 'http',
                'site_name': self.request.get_host()
            }
            send_email_celery_task.delay(context, email_to, 'UsernameChangedConfirmationEmail')
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False, url_path=f"reset_{User.USERNAME_FIELD}")
    def reset_username(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()

        if user:
            email_to = [get_user_email(user)]
            context = {
                'user_id': user.id,
                'domain': self.request.get_host(),
                'protocol': 'https' if self.request.is_secure() else 'http',
                'site_name': self.request.get_host()
            }
            send_email_celery_task.delay(context, email_to, 'UsernameResetEmail')

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False, url_path=f"reset_{User.USERNAME_FIELD}_confirm")
    def reset_username_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_username = serializer.data["new_" + User.USERNAME_FIELD]

        setattr(serializer.user, User.USERNAME_FIELD, new_username)
        if hasattr(serializer.user, "last_login"):
            serializer.user.last_login = now()
        serializer.user.save()

        if settings.USERNAME_CHANGED_EMAIL_CONFIRMATION:
            email_to = [get_user_email(serializer.user)]
            context = {
                'user_id': serializer.user.id,
                'domain': self.request.get_host(),
                'protocol': 'https' if self.request.is_secure() else 'http',
                'site_name': self.request.get_host()
            }
            send_email_celery_task.delay(context, email_to, 'UsernameChangedConfirmationEmail')
        return Response(status=status.HTTP_204_NO_CONTENT)


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
    queryset = User.objects.all().prefetch_related('social_links')
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
        author = get_object_or_404(User, id=pk)

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
        author = get_object_or_404(User, id=pk)
        try:
            following_instance = UserFollowing.objects.get(
                user=request.user,
                following_user=author
            )
            following_instance.delete()
            return Response({'message': 'Unfollowed successfully'}, status=204)
        except UserFollowing.DoesNotExist:
            return Response({'error': 'You were not following this user'}, status=404)

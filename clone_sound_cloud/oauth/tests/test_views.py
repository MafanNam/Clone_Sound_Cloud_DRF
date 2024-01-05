from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from oauth import models

USERS_URL = reverse("oauth:user-list")
USER_PROFILE_URL = reverse("oauth:user_profile")


def detail_users_url(user_id):
    """Users detail URL."""
    return reverse("oauth:user-detail", args=[user_id])


def detail_author_follow_url(author_id):
    """Author follow and unfollow detail URL."""
    return reverse("oauth:author_follow_unfollow", args=[author_id])


def create_user(
    first_name="test_first",
    last_name="test_last",
    email="test@gmail.com",
    password="testpass123",
    is_active=False,
):
    """Create and return a new user."""
    user = get_user_model().objects.create_user(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        is_active=is_active,
    )
    user.save()
    return user


def create_superuser(
    first_name="test_first",
    last_name="test_last",
    email="admin@gmail.com",
    password="testpass123",
):
    """Create and return a new user."""
    user = get_user_model().objects.create_superuser(
        first_name=first_name, last_name=last_name, email=email, password=password
    )
    user.save()
    return user


class PublicTestAuthenticationViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = create_user(is_active=True)

    def test_jwt_create_refresh_verify_token(self):
        # CREATE JWT
        payload = {
            "email": "test@gmail.com",
            "password": "testpass123",
        }
        res = self.client.post(reverse("oauth:jwt-create"), payload)
        access_jwt = res.data["access"]
        refresh_jwt = res.data["refresh"]
        self.assertEqual(res.status_code, 200)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_jwt)

        res = self.client.get(detail_users_url(self.user1.id))
        self.assertEqual(res.status_code, 200)

        # REFRESH JWT
        payload = {
            "refresh": refresh_jwt,
        }
        res = self.client.post(reverse("oauth:jwt-refresh"), payload)
        access_jwt = res.data["access"]
        self.assertEqual(res.status_code, 200)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_jwt)

        res = self.client.get(detail_users_url(self.user1.id))
        self.assertEqual(res.status_code, 200)

        # VERIFY JWT
        payload = {
            "token": access_jwt,
        }
        res = self.client.post(reverse("oauth:jwt-verify"), payload)
        self.assertEqual(res.status_code, 200)

    def test_list_users_unauthorized(self):
        res = self.client.get(USERS_URL)
        self.assertEqual(res.status_code, 401)

    def test_get_user_unauthorized(self):
        res = self.client.get(detail_users_url(self.user1.id))
        self.assertEqual(res.status_code, 401)

    def test_get_userprofile_unauthorized(self):
        res = self.client.get(USER_PROFILE_URL)
        self.assertEqual(res.status_code, 401)

    def test_get_sociallink_unauthorized_and_author(self):
        res = self.client.get(reverse("oauth:social_link"))
        self.assertEqual(res.status_code, 401)

    def test_register_user(self):
        payload = {
            "first_name": "string",
            "last_name": "string",
            "email": "user@example.com",
            "password": "testpass123",
            "re_password": "testpass123",
        }

        res = self.client.post(USERS_URL, payload)
        self.assertEqual(res.status_code, 201)

    def test_get_author_unauthorized(self):
        res = self.client.get(reverse("oauth:author"))
        self.assertEqual(res.status_code, 200)

    def test_follow_author_unauthorized(self):
        res = self.client.get(detail_author_follow_url(self.user1.id))
        self.assertEqual(res.status_code, 401)

    def test_spam_email_on_unauthorized(self):
        res = self.client.post(reverse("oauth:spam_email_once_week"))
        self.assertEqual(res.status_code, 401)


class PrivateTestAuthenticationViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = create_user()
        self.user2 = create_user(email="test2@gmail.com")
        self.client.force_authenticate(self.user1)
        self.social_link = models.SocialLink.objects.create(
            user=self.user1, link="http://test2.com"
        )

    def test_list_users(self):
        res = self.client.get(USERS_URL)
        self.assertEqual(res.status_code, 200)

    def test_detail_users(self):
        res = self.client.get(detail_users_url(self.user1.id))
        self.assertEqual(res.status_code, 200)

    def test_detail_user_me(self):
        res = self.client.get(reverse("oauth:user-me"))
        self.assertEqual(res.status_code, 200)

    def test_detail_userprofile(self):
        res = self.client.get(USER_PROFILE_URL)
        self.assertEqual(res.status_code, 200)

    def test_create_social_link(self):
        payload = {"link": "http://test.com"}
        res = self.client.post(reverse("oauth:social_link"), payload)
        self.assertEqual(res.status_code, 201)

    def test_list_social_link(self):
        res = self.client.get(reverse("oauth:social_link"))
        self.assertEqual(res.status_code, 200)

    def test_delete_social_link(self):
        res = self.client.delete(
            reverse("oauth:social_link_detail", args=[self.social_link.id])
        )
        self.assertEqual(res.status_code, 204)

    def test_follow_unfollow_user(self):
        res = self.client.post(detail_author_follow_url(self.user2.id))
        self.assertEqual(res.status_code, 201)

        res = self.client.delete(detail_author_follow_url(self.user2.id))
        self.assertEqual(res.status_code, 204)

    def test_mark_spam_email_once_week_user(self):
        res = self.client.post(reverse("oauth:spam_email_once_week"))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(self.user1.is_spam_email)

        res = self.client.delete(reverse("oauth:spam_email_once_week"))
        self.assertEqual(res.status_code, 200)

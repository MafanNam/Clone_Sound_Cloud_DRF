from django.contrib.auth import get_user_model
from django.test import TestCase

from oauth import models


def create_user(
        first_name='fir_test', last_name='las_test',
        email='test@email.com', password='testpass123',
        is_active=False):
    return get_user_model().objects.create_user(
        first_name=first_name, last_name=last_name,
        email=email, password=password, is_active=is_active,
    )


class UserManagerTests(TestCase):

    def test_create_user_and_userprofile(self):
        """Test creating a user and signal userprofile is successful."""
        user = create_user(email='goood@email.com')

        self.assertEquals(user.email, 'goood@email.com')

        userprofile = models.UserProfile.objects.filter(user=user).exists()
        self.assertTrue(userprofile)

        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test create super user."""
        admin_user = get_user_model().objects.create_superuser(
            email='admin@gmail.com', password='testpass123'
        )
        self.assertEqual(admin_user.email, 'admin@gmail.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_delete_user_and_userprofile(self):
        """Test delete user and signal userprofile."""
        user = create_user()
        userprofile = models.UserProfile.objects.filter(user=user).exists()
        self.assertTrue(userprofile)

        user.delete()
        userprofile = models.UserProfile.objects.filter(user=user).exists()
        self.assertFalse(userprofile)

    def test_create_user_following(self):
        """Test create user following model"""
        user1 = create_user(email='user1@gmail.com')
        user2 = create_user(email='user2@gmail.com')
        user3 = create_user(email='user3@gmail.com')
        user4 = create_user(email='user4@gmail.com')

        models.UserFollowing.objects.create(
            user=user1, following_user=user2)
        models.UserFollowing.objects.create(
            user=user1, following_user=user3)
        models.UserFollowing.objects.create(
            user=user1, following_user=user4)

        user_follow = models.UserFollowing.objects.filter(user=user1)

        self.assertEqual(user_follow.count(), 3)

    def test_delete_use_following(self):
        """Test delete user following model."""
        user1 = create_user(email='user1@gmail.com')
        user2 = create_user(email='user2@gmail.com')

        models.UserFollowing.objects.create(
            user=user1, following_user=user2)

        user_follow = models.UserFollowing.objects.filter(user=user1).exists()

        self.assertTrue(user_follow)

        # del user CASCADE del user_following
        user1.delete()

        user_follow = models.UserFollowing.objects.filter(user=user1).exists()

        self.assertFalse(user_follow)

        # del user_following model
        user1 = create_user(email='user1@gmail.com')

        models.UserFollowing.objects.create(
            user=user1, following_user=user2)

        user_follow = models.UserFollowing.objects.filter(user=user1)
        self.assertTrue(user_follow.exists())
        user_follow.delete()
        user_follow = models.UserFollowing.objects.filter(user=user1).exists()
        self.assertFalse(user_follow)

    def test_create_social_link(self):
        """Test create social link."""
        user = create_user()

        models.SocialLink.objects.create(user=user, link='http://test.com')
        social_link = models.SocialLink.objects.filter(user=user)
        self.assertTrue(social_link.exists())
        self.assertEqual(social_link[0].user, user)
        self.assertEqual(social_link[0].link, 'http://test.com')

    def test_delete_social_link(self):
        """Test delete social link model"""
        user = create_user()

        models.SocialLink.objects.create(user=user, link='http://test.com')
        social_link = models.SocialLink.objects.filter(user=user).exists()
        self.assertTrue(social_link)

        # del user CASCADE del social link
        user.delete()
        social_link = models.SocialLink.objects.filter(user=user).exists()
        self.assertFalse(social_link)

        # del social link model
        user = create_user()

        models.SocialLink.objects.create(user=user, link='http://test.com')
        social_link = models.SocialLink.objects.filter(user=user)
        self.assertTrue(social_link.exists())
        social_link.delete()
        social_link = models.SocialLink.objects.filter(user=user)
        self.assertFalse(social_link.exists())

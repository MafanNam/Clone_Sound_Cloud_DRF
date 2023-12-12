from django.test import TestCase

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from oauth.tests.test_views import create_user, create_superuser

from audio_library import models
from audio_library.api import serializers
from audio_library.tests.test_models import (
    create_file, create_playlist, create_comment,
    create_track
)


class PublicTestAudioLibraryViews(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = create_user(is_active=True)
        self.user2 = create_user(is_active=True, email='test2@gmail.com')
        # self.admin = create_superuser()
        self.genre1 = models.Genre.objects.create(name='g1')
        self.genre2 = models.Genre.objects.create(name='g2')
        self.license = models.License.objects.create(user=self.user1, text='test')
        self.album = models.Album.objects.create(
            user=self.user1, name='test_name', description='d1',
            cover=create_file(),
        )
        self.track = create_track(
            user=self.user1, license_=self.license, genre=self.genre1,
            album=self.album, cover=create_file(), file=create_file('mp3'),
            title='t2')
        self.comment = create_comment(user=self.user2, track=self.track)
        self.playlist = create_playlist(
            user=self.user2, tracks=self.track, cover=create_file())

    def test_list_genre(self):
        res = self.client.get(reverse('audio:genre'))

        s1 = serializers.GenreSerializer(self.genre1)
        s2 = serializers.GenreSerializer(self.genre2)

        self.assertEqual(res.status_code, 200)
        self.assertNotEquals(res.json, None)
        self.assertEqual(len(res.data), 2)
        self.assertIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)

    def test_get_author_album(self):
        res = self.client.get(reverse('audio:author_album', args=[self.user1.id]))

        self.assertEqual(res.status_code, 200)
        self.assertNotEquals(res.json, None)
        self.assertEqual(len(res.data), 1)

    def test_list_track(self):
        res = self.client.get(reverse('audio:track_list'))

        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res.json, None)

    def test_author_track_list(self):
        res = self.client.get(reverse('audio:author_track_list', [self.user1.id]))

        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res.json, None)

    def test_comments_by_track(self):
        res = self.client.get(reverse('audio:comments_by_track', [self.track.id]))

        s1 = serializers.CommentSerializer(self.comment)
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res.json, None)
        self.assertIn(s1.data, res.data)


from django.test import TestCase

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from oauth.tests.test_views import create_user

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

    # Permission required
    def test_list_license_unauthorized(self):
        res = self.client.get(reverse('audio:license'))

        self.assertEqual(res.status_code, 401)

    def test_create_license_unauthorized(self):
        payload = {
            'text': 'create text',
        }
        res = self.client.post(reverse('audio:license'), payload)

        self.assertEqual(res.status_code, 401)

    def test_update_license_unauthorized(self):
        payload = {
            'text': 'updated text'
        }
        res = self.client.put(reverse(
            'audio:license_detail', [self.license.id]), payload)

        self.assertEqual(res.status_code, 401)

    def test_delete_license_unauthorized(self):
        res = self.client.delete(reverse('audio:license_detail', [self.license.id]))

        self.assertEqual(res.status_code, 401)

    def test_list_album_unauthorized(self):
        res = self.client.get(reverse('audio:album'))

        self.assertEqual(res.status_code, 401)

    def test_create_album_unauthorized(self):
        payload = {
            'name': 'create name',
            'description': 'create desc',
        }
        res = self.client.post(reverse(
            'audio:album'), payload)

        self.assertEqual(res.status_code, 401)

    def test_update_album_unauthorized(self):
        payload = {
            'name': 'updated name',
            'description': 'updated desc',
        }
        res = self.client.put(reverse(
            'audio:album_detail', [self.album.id]), payload)

        self.assertEqual(res.status_code, 401)

    def test_delete_album_unauthorized(self):
        res = self.client.delete(reverse('audio:album_detail', [self.album.id]))

        self.assertEqual(res.status_code, 401)

    def test_list_track_unauthorized(self):
        res = self.client.get(reverse('audio:track'))

        self.assertEqual(res.status_code, 401)

    def test_create_track_unauthorized(self):
        payload = {
            'title': 'test title',
            'license': self.license.id,
            'genre': self.genre1.id,
            'file': create_file('mp3'),
        }
        res = self.client.post(reverse('audio:track'), payload)

        self.assertEqual(res.status_code, 401)

    def test_update_track_unauthorized(self):
        payload = {
            'title': 'updated title',
        }
        res = self.client.put(reverse(
            'audio:track_detail', [self.track.id]), payload)

        self.assertEqual(res.status_code, 401)

    def test_delete_track_unauthorized(self):
        res = self.client.delete(reverse('audio:track_detail', [self.track.id]))

        self.assertEqual(res.status_code, 401)

    def test_like_track_unauthorized(self):
        res = self.client.post(reverse('audio:track_like', [self.track.id]))

        self.assertEqual(res.status_code, 401)

    def test_delete_like_track_unauthorized(self):
        res = self.client.delete(reverse('audio:track_like', [self.track.id]))

        self.assertEqual(res.status_code, 401)

    def test_tracks_recently_played_unauthorized(self):
        res = self.client.get(reverse('audio:tracks_recently_played'))

        self.assertEqual(res.status_code, 401)

    def test_list_comments_unauthorized(self):
        res = self.client.get(reverse('audio:comments'))

        self.assertEqual(res.status_code, 401)

    def test_create_comments_unauthorized(self):
        payload = {
            'text': 'test text'
        }
        res = self.client.post(reverse('audio:comments'), payload)

        self.assertEqual(res.status_code, 401)

    def test_update_comments_unauthorized(self):
        payload = {
            'text': 'update text'
        }
        res = self.client.put(
            reverse('audio:comments_detail', [self.comment.id]), payload)

        self.assertEqual(res.status_code, 401)

    def test_delete_comments_unauthorized(self):
        res = self.client.delete(
            reverse('audio:comments_detail', [self.comment.id]))

        self.assertEqual(res.status_code, 401)

    def test_list_playlist_unauthorized(self):
        res = self.client.get(reverse('audio:playlist'))

        self.assertEqual(res.status_code, 401)

    def test_create_playlist_unauthorized(self):
        payload = {
            'title': 'test title',
            'track': self.track.id,
        }
        res = self.client.post(reverse('audio:playlist'), payload)

        self.assertEqual(res.status_code, 401)

    def test_update_playlist_unauthorized(self):
        payload = {
            'title': 'update text',
            'track': self.track.id,
        }
        res = self.client.put(
            reverse('audio:playlist_detail', [self.playlist.id]), payload)

        self.assertEqual(res.status_code, 401)

    def test_delete_playlist_unauthorized(self):
        res = self.client.delete(
            reverse('audio:playlist_detail', [self.playlist.id]))

        self.assertEqual(res.status_code, 401)


class PrivateTestAudioLibraryViews(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = create_user(is_active=True)
        self.user2 = create_user(is_active=True, email='test2@gmail.com')
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

    def test_list_license_user_author(self):
        self.client.force_authenticate(self.user1)
        res = self.client.get(reverse('audio:license'))

        self.assertEqual(res.status_code, 200)

    def test_create_license_user_author(self):
        self.client.force_authenticate(self.user1)
        payload = {
            'text': 'create text',
        }
        res = self.client.post(reverse('audio:license'), payload)
        license2 = models.License.objects.get(user=self.user1, text='create text')
        s1 = serializers.LicenseSerializer(license2)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['text'], license2.text)
        self.assertEqual(s1.data, res.data)

    def test_update_license_user_author(self):
        self.client.force_authenticate(self.user1)
        payload = {
            'text': 'update text',
        }
        res = self.client.put(reverse(
            'audio:license_detail', [self.license.id]), payload)
        self.license.refresh_from_db()
        s1 = serializers.LicenseSerializer(self.license)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['text'], 'update text')
        self.assertEqual(s1.data, res.data)

    def test_delete_license_user_author(self):
        self.client.force_authenticate(self.user1)
        license2 = models.License.objects.create(user=self.user1, text='test2')
        res = self.client.delete(reverse(
            'audio:license_detail', [license2.id]))
        license2 = models.License.objects.filter(user=self.user1, text='test2').exists()

        self.assertEqual(res.status_code, 204)
        self.assertFalse(license2)

    def test_update_license_user_not_author(self):
        self.client.force_authenticate(self.user2)
        payload = {
            'text': 'update text',
        }
        res = self.client.put(reverse(
            'audio:license_detail', [self.license.id]), payload)

        self.assertEqual(res.status_code, 404)

    def test_delete_license_user_not_author(self):
        self.client.force_authenticate(self.user2)
        res = self.client.delete(reverse(
            'audio:license_detail', [self.license.id]))

        self.assertEqual(res.status_code, 404)

    def test_list_album_author(self):
        self.client.force_authenticate(self.user1)
        res = self.client.get(reverse('audio:album'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data[0]['id'], self.album.id)
        self.assertEqual(res.data[0]['name'], self.album.name)

    def test_create_album_author(self):
        self.client.force_authenticate(self.user1)
        payload = {
            'name': 'create name',
            'description': 'create desc',
        }
        res = self.client.post(reverse(
            'audio:album'), payload)

        s1 = serializers.AlbumSerializer(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(s1.data, res.data)
        self.assertEqual(s1.data['name'], 'create name')

    # def test_update_album_author(self):
    #     self.client.force_authenticate(self.user1)
    #     payload = {
    #         'name': 'updated name',
    #         'description': 'updated desc',
    #     }
    #     res = self.client.put(reverse(
    #         'audio:album_detail', [self.album.id]), payload)
    #
    #     self.assertEqual(res.status_code, 200)
    #
    # def test_delete_album_author(self):
    #     self.client.force_authenticate(self.user1)
    #     res = self.client.delete(reverse('audio:album_detail', [self.album.id]),
    #                              format='multipart')
    #
    #     self.assertEqual(res.status_code, 204)

    def test_list_track_author(self):
        self.client.force_authenticate(self.user1)
        res = self.client.get(reverse('audio:track'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data[0]['id'], self.track.id)
        self.assertEqual(res.data[0]['title'], self.track.title)

    # def test_create_track_author(self):
    #     self.client.force_authenticate(self.user1)
    #     payload = {
    #         'title': 'test title',
    #         'license': self.license.id,
    #         'genre': self.genre1.id,
    #         'file': create_file('mp3'),
    #     }
    #     res = self.client.post(reverse('audio:track'), payload)
    #
    #     self.assertEqual(res.status_code, 201)

    # def test_update_track_unauthorized(self):
    #     payload = {
    #         'title': 'updated title',
    #     }
    #     res = self.client.put(reverse(
    #         'audio:track_detail', [self.track.id]), payload)
    #
    #     self.assertEqual(res.status_code, 401)
    #
    # def test_delete_track_unauthorized(self):
    #     self.client.force_authenticate(self.user1)
    #     res = self.client.delete(reverse('audio:track_detail', [self.track.id]))
    #
    #     self.assertEqual(res.status_code, 401)
    #
    def test_like_track_user(self):
        self.client.force_authenticate(self.user2)
        res = self.client.post(reverse('audio:track_like', [self.track.id]))

        self.assertEqual(res.status_code, 201)

    def test_delete_like_track_user(self):
        self.client.force_authenticate(self.user2)
        self.client.post(reverse('audio:track_like', [self.track.id]))

        res = self.client.delete(reverse('audio:track_like', [self.track.id]))

        self.assertEqual(res.status_code, 204)

    def test_like_author_track(self):
        self.client.force_authenticate(self.user1)
        res = self.client.post(reverse('audio:track_like', [self.track.id]))

        self.assertEqual(res.status_code, 403)

    def test_delete_like_author_track(self):
        self.client.force_authenticate(self.user1)
        self.client.post(reverse('audio:track_like', [self.track.id]))

        res = self.client.delete(reverse('audio:track_like', [self.track.id]))

        self.assertEqual(res.status_code, 403)

    def test_list_comments_author(self):
        self.client.force_authenticate(self.user1)
        res = self.client.get(reverse('audio:comments'))

        self.assertEqual(res.status_code, 200)

    def test_create_comments_user(self):
        self.client.force_authenticate(self.user2)
        payload = {
            'text': 'test text2',
            'track': self.track.id,
        }
        res = self.client.post(reverse('audio:comments'), payload)

        com = models.Comment.objects.get(user=self.user2, text=payload['text'])

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['text'], com.text)
        self.assertEqual(res.data['track'], com.track.id)

    def test_update_comments_user(self):
        self.client.force_authenticate(self.user2)
        payload = {
            'text': 'update text',
            'track': self.track.id,
        }
        res = self.client.put(
            reverse('audio:comments_detail', [self.comment.id]), payload)

        self.assertEqual(res.status_code, 200)

    def test_delete_comments_unauthorized(self):
        self.client.force_authenticate(self.user2)
        res = self.client.delete(
            reverse('audio:comments_detail', [self.comment.id]))

        self.assertEqual(res.status_code, 204)

    def test_list_playlist_author(self):
        self.client.force_authenticate(self.user1)
        res = self.client.get(reverse('audio:playlist'))

        self.assertEqual(res.status_code, 200)

    def test_create_playlist_user(self):
        self.client.force_authenticate(self.user1)
        payload = {
            'title': 'test title',
            'tracks': [self.track.id],
        }
        res = self.client.post(reverse('audio:playlist'), payload)

        self.assertEqual(res.status_code, 201)

    # def test_update_playlist_user(self):
    #     self.client.force_authenticate(self.user2)
    #     payload = {
    #         'title': 'update text',
    #         'tracks': [self.track.id],
    #     }
    #     res = self.client.put(
    #         reverse('audio:playlist_detail', [self.playlist.id]), payload)
    #
    #     self.assertEqual(res.status_code, 200)

    # def test_delete_playlist_user(self):
    #     self.client.force_authenticate(self.user2)
    #     res = self.client.delete(
    #         reverse('audio:playlist_detail', [self.playlist.id]))
    #
    #     self.assertEqual(res.status_code, 204)

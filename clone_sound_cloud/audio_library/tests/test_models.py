import tempfile

from django.test import TestCase

from audio_library import models
from oauth.tests.test_models import create_user


def create_track(
    user,
    license_,
    genre,
    album,
    cover,
    file,
    title="t1",
):
    track = models.Track.objects.create(
        user=user, license=license_, album=album, cover=cover, file=file, title=title
    )
    track.genre.set([genre])
    track.save()
    return track


def create_comment(user, track, text="t1"):
    comment = models.Comment.objects.create(user=user, track=track, text=text)
    comment.save()
    return comment


def create_playlist(user, tracks, cover, title="t1"):
    playlist = models.Playlist.objects.create(user=user, cover=cover, title=title)
    playlist.tracks.set([tracks])
    playlist.save()
    return playlist


def create_file(format_="jpg"):
    return tempfile.NamedTemporaryFile(suffix=f".{format_}").name


class AudioLibraryTests(TestCase):
    def setUp(self):
        self.user1 = create_user(is_active=True)
        self.user2 = create_user(is_active=True, email="test2@gmail.com")
        self.genre = models.Genre.objects.create(name="g1")
        self.license = models.License.objects.create(user=self.user1, text="test")
        self.album = models.Album.objects.create(
            user=self.user1,
            name="test_name",
            description="d1",
            cover=create_file(),
        )
        self.track = create_track(
            user=self.user1,
            license_=self.license,
            genre=self.genre,
            album=self.album,
            cover=create_file(),
            file=create_file("mp3"),
            title="t2",
        )
        self.comment = create_comment(user=self.user2, track=self.track)
        self.playlist = create_playlist(
            user=self.user2, tracks=self.track, cover=create_file()
        )

    def test_create_license(self):
        license_ = models.License.objects.create(user=self.user1, text="test_text")

        self.assertEqual(license_.user, self.user1)
        self.assertEqual(license_.text, "test_text")

    def test_create_genre(self):
        genre = models.Genre.objects.create(name="g2")

        self.assertEqual(genre.name, "g2")

    def test_create_album(self):
        image = create_file()

        album = models.Album.objects.create(
            user=self.user1,
            name="test_name2",
            description="d2",
            cover=image,
        )

        self.assertEqual(album.user, self.user1)
        self.assertEqual(album.cover, image)
        self.assertEqual(album.name, "test_name2")
        self.assertEqual(album.description, "d2")

    def test_create_track(self):
        image = create_file()
        file = create_file("mp3")
        track = create_track(
            user=self.user1,
            license_=self.license,
            genre=self.genre,
            album=self.album,
            cover=image,
            file=file,
        )

        self.assertEqual(track.user, self.user1)
        self.assertEqual(track.license, self.license)
        self.assertEqual(track.genre.get(track_genres=track), self.genre)
        self.assertEqual(track.album, self.album)
        self.assertEqual(track.cover, image)
        self.assertEqual(track.plays_count, 0)
        self.assertEqual(track.download, 0)
        self.assertEqual(track.likes_count, 0)
        self.assertEqual(track.private, False)

    def test_create_comment(self):
        comment = create_comment(self.user2, self.track, text="aga")

        self.assertEqual(comment.user, self.user2)
        self.assertEqual(comment.track, self.track)
        self.assertEqual(comment.text, "aga")

    def test_create_playlist(self):
        image = create_file()
        playlist = create_playlist(self.user2, self.track, cover=image, title="t3")

        self.assertEqual(playlist.user, self.user2)
        self.assertEqual(playlist.tracks.get(playlist_tracks=playlist), self.track)
        self.assertEqual(playlist.title, "t3")
        self.assertEqual(playlist.cover, image)

    def test_str_license(self):
        self.assertEqual(self.license.__str__(), f"License-{self.license.id}")

    def test_str_genre(self):
        self.assertEqual(self.genre.__str__(), self.genre.name)

    def test_str_album(self):
        self.assertEqual(self.album.__str__(), f"{self.album.name} - {self.album.user}")

    def test_str_track(self):
        self.assertEqual(
            self.track.__str__(), f"{self.track.user} - {self.track.title}"
        )

    def test_str_comment(self):
        self.assertEqual(
            self.comment.__str__(), f"{self.comment.user} - {self.comment.track.title}"
        )

    def test_str_playlist(self):
        self.assertEqual(
            self.playlist.__str__(), f"{self.playlist.user} - {self.playlist.title}"
        )

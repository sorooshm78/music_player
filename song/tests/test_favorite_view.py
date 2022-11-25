from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from album.models import Album
from song.models import Song


class TestSongFavoriteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create(username="user1", password="a/@1234567")
        self.user2 = User.objects.create(username="user2", password="a/@1234567")

    def test_favorite_song_without_authentication(self):
        test_song_id = 1
        url = reverse("favorite", args=[test_song_id])
        response = self.client.get(url)

        # Redirect to login page
        self.assertEqual(response.status_code, 302)

    def test_favorite_song(self):
        album = self.create_album(user=self.user1)
        song = self.create_song(album)
        url = reverse("favorite", args=[song.id])

        self.client.force_login(self.user1)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Song.objects.get(id=song.id).is_favorite)

    def test_favorite_song_and_not_access_another_user(self):
        # user1
        album = self.create_album(self.user1)
        song = self.create_song(album)

        # user2
        url = reverse("favorite", args=[song.id])
        self.client.force_login(self.user2)
        response = self.client.get(url)
        self.client.logout()

        self.assertEqual(response.status_code, 404)

    def create_album(
        self,
        user,
        album_title="test_title",
        artist="test_artist",
        genre="test_genre",
    ):
        return Album.objects.create(
            user=user,
            album_title=album_title,
            artist=artist,
            genre=genre,
        )

    def create_song(
        self,
        album,
        title="test_song",
        audio_file="test_file",
    ):
        return Song.objects.create(
            album=album,
            song_title=title,
            audio_file=audio_file,
        )

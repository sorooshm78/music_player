from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from album.models import Album
from song.models import Song


class TestSongListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create(username="user1", password="a/@1234567")
        self.user2 = User.objects.create(username="user2", password="a/@1234567")
        self.all_songs_url = reverse("songs", args=["all"])
        self.favorite_songs_url = reverse("songs", args=["favorites"])
        self.album = self.create_album(user=self.user1)
        self.song = self.create_song(self.album)

    def test_get_list_songs_without_authentication(self):
        response = self.client.get(self.all_songs_url)

        # Redirect to login page
        self.assertEqual(response.status_code, 302)

    def test_get_list_all_songs(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.all_songs_url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.song.song_title)
        self.assertContains(response, self.song.album.artist)

    def test_get_list_favorite_songs(self):
        self.song.is_favorite = True
        self.song.save()

        self.client.force_login(self.user1)
        response = self.client.get(self.favorite_songs_url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.song.song_title)
        self.assertContains(response, self.song.album.artist)

    def test_get_list_all_song_and_not_access_another_user(self):
        # user1
        album = self.create_album(self.user1)

        # user2
        self.client.force_login(self.user2)
        response = self.client.get(self.all_songs_url)
        self.client.logout()

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, album.album_title)
        self.assertNotContains(response, album.artist)

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

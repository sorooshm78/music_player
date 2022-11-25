from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from album.models import Album
from song.models import Song


class TestSongCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create(username="user1", password="a/@1234567")
        self.user2 = User.objects.create(username="user2", password="a/@1234567")
        self.audio_file = SimpleUploadedFile("TestAudioFile.mp3", b"test_content")
        self.album_create_by_user1 = self.create_album(self.user1)
        self.url = reverse("create_song", args=[self.album_create_by_user1.id])

    def tearDown(self):
        songs = Song.objects.all()
        for song in songs:
            delete_url = reverse(
                "delete_song", args=[self.album_create_by_user1.id, song.id]
            )
            self.client.post(delete_url)

    def test_create_song_without_authentication(self):
        response = self.client.get(self.url)

        # Redirect to login page
        self.assertEqual(response.status_code, 302)

    def test_create_song(self):
        self.client.force_login(self.user1)
        data = {
            "song_title": "test_title",
            "audio_file": self.audio_file,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)

        song_created = Song.objects.get(id=1)
        self.assertEqual(song_created.song_title, data["song_title"])
        self.assertEqual(song_created.album, self.album_create_by_user1)

    def test_create_song_with_empty_title(self):
        self.client.force_login(self.user1)
        data = {
            "audio_file": self.audio_file,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")

    def test_create_song_with_empty_audio(self):
        self.client.force_login(self.user1)
        data = {
            "song_title": "test_title",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")

    def test_not_create_song_by_another_user_album(self):
        url = reverse("create_song", args=[self.album_create_by_user1.id])
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

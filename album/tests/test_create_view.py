from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from album.models import Album


class TestAlbumDeleteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create(username="user1", password="a/@1234567")
        self.user2 = User.objects.create(username="user2", password="a/@1234567")
        self.url = reverse("create_album")

    def test_create_album_without_authentication(self):
        response = self.client.get(self.url)

        # Redirect to login page
        self.assertEqual(response.status_code, 302)

    def test_create_album(self):
        self.client.force_login(self.user1)
        data = {
            "album_title": "test_title",
            "artist": "test_artist",
            "genre": "test_genre",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)

        album_created = Album.objects.get(id=1)
        self.assertEqual(album_created.album_title, data["album_title"])
        self.assertEqual(album_created.artist, data["artist"])
        self.assertEqual(album_created.genre, data["genre"])

    def test_create_album_with_empty_title(self):
        self.client.force_login(self.user1)
        data = {
            "artist": "test_artist",
            "genre": "test_genre",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")

    def test_create_album_with_empty_artist(self):
        self.client.force_login(self.user1)
        data = {
            "album_title": "test_title",
            "genre": "test_genre",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")

    def test_create_album_with_empty_genre(self):
        self.client.force_login(self.user1)
        data = {
            "album_title": "test_title",
            "artist": "test_artist",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")

    def test_create_album_and_not_access_another_user(self):
        # user1
        self.client.force_login(self.user1)
        data = {
            "album_title": "test_title",
            "artist": "test_artist",
            "genre": "test_genre",
        }
        response = self.client.post(self.url, data=data)
        self.client.logout()
        self.assertEqual(response.status_code, 302)

        # user2
        album_created = Album.objects.get(id=1)
        url = reverse("detail", args=[album_created.id])
        self.client.force_login(self.user2)
        response = self.client.get(url)
        self.client.logout()

        self.assertEqual(response.status_code, 404)

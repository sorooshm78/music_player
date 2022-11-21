from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from album.models import Album


class TestAlbumDetailView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create(username="user1", password="a/@1234567")
        self.user2 = User.objects.create(username="user2", password="a/@1234567")
        self.album_create_by_user1 = Album.objects.create(
            user=self.user1,
            album_title="test_album_title",
            artist="test_artist",
            genre="test_genre",
        )
        self.url = reverse("detail", args=[self.album_create_by_user1.id])

    def test_get_detail_album_without_authentication(self):
        response = self.client.get(self.url)

        # Redirect to login page
        self.assertEqual(response.status_code, 302)

    def test_get_detail_album(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.album_create_by_user1.album_title)
        self.assertContains(response, self.album_create_by_user1.artist)
        self.assertContains(response, self.album_create_by_user1.genre)

    def test_get_detail_album_and_not_access_another_user(self):
        # user1
        self.client.force_login(self.user1)
        response = self.client.get(self.url)
        self.client.logout()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.album_create_by_user1.album_title)
        self.assertContains(response, self.album_create_by_user1.artist)
        self.assertContains(response, self.album_create_by_user1.genre)

        # user2
        self.client.force_login(self.user2)
        response = self.client.get(self.url)
        self.client.logout()

        self.assertEqual(response.status_code, 404)

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from album.models import Album


class TestAlbumListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create(username="user1", password="a/@1234567")
        self.user2 = User.objects.create(username="user2", password="a/@1234567")
        self.url = reverse("index")

    def test_get_list_album_without_authentication(self):
        response = self.client.get(self.url)

        # Redirect to login page
        self.assertEqual(response.status_code, 302)

    def test_get_list_album(self):
        album = self.create_album(user=self.user1)

        self.client.force_login(self.user1)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, album.album_title)
        self.assertContains(response, album.artist)

    def test_get_list_album_and_not_authorized_another_user(self):
        # user1
        album = self.create_album(self.user1)

        self.client.force_login(self.user1)
        response = self.client.get(self.url)
        self.client.logout()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, album.album_title)

        # user2
        self.client.force_login(self.user2)
        response = self.client.get(self.url)
        self.client.logout()

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, album.album_title)

    def test_each_user_access_own_albums(self):
        album_user1 = self.create_album(self.user1, album_title="user1")
        album_user2 = self.create_album(self.user2, album_title="user2")

        # user1
        self.client.force_login(self.user1)
        response = self.client.get(self.url)
        self.client.logout()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, album_user1.album_title)
        self.assertNotContains(response, album_user2.album_title)

        # user2
        self.client.force_login(self.user2)
        response = self.client.get(self.url)
        self.client.logout()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, album_user2.album_title)
        self.assertNotContains(response, album_user1.album_title)

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

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album_title = models.CharField(max_length=250)
    album_logo = models.ImageField(
        upload_to="media/albums",
        default="media/default/album.png",
    )
    artist = models.CharField(max_length=250)
    genre = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)
    audio_file = models.FileField(
        upload_to="media/songs",
    )

    def __str__(self):
        return f"{self.album.album_title} -> {self.song_title}"

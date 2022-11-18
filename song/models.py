from django.db import models
from django.contrib.auth.models import User

from album.models import Album


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)
    audio_file = models.FileField(
        upload_to="media/songs",
    )

    def __str__(self):
        return f"{self.album.album_title} -> {self.song_title}"

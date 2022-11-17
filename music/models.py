from django.db import models

# Create your models here.
class Album(models.Model):
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
    audio_file = models.FileField(null=True, blank=True)

    def __str__(self):
        return f"{self.album.album_title} -> {self.song_title}"

import os

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

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


@receiver(post_delete, sender=Song)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding 'Song' object is deleted.
    """
    audio_path = str(instance.audio_file)
    if os.path.isfile(audio_path):
        os.remove(audio_path)

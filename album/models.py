import os

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

DEFAULT_PATH_ALBUM_LOGO = "media/default/album.png"


class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album_title = models.CharField(max_length=250)
    album_logo = models.ImageField(
        upload_to="media/albums",
        default=DEFAULT_PATH_ALBUM_LOGO,
    )
    artist = models.CharField(max_length=250)
    genre = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title


@receiver(post_delete, sender=Album)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding 'Album' object is deleted and not default image.
    """
    image_path = str(instance.album_logo)
    if image_path != DEFAULT_PATH_ALBUM_LOGO:
        if os.path.isfile(image_path):
            os.remove(image_path)

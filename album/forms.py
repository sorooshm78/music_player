from django.forms import ModelForm

from .models import Album


class AlbumModelForm(ModelForm):
    class Meta:
        model = Album
        fields = ["artist", "album_title", "genre", "album_logo"]

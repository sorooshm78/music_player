from django.forms import ModelForm

from .models import Album


class AlbumModelForm(ModelForm):
    class Meta:
        model = Album
        fields = ["album_title", "album_logo", "artist", "genre"]

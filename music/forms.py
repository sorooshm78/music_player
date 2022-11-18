from django.forms import ModelForm

from .models import Album, Song


class AlbumModelForm(ModelForm):
    class Meta:
        model = Album
        fields = ["artist", "album_title", "genre", "album_logo"]


class SongModelForm(ModelForm):
    class Meta:
        model = Song
        fields = ["song_title", "audio_file"]

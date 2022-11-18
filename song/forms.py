from django.forms import ModelForm

from .models import Song


class SongModelForm(ModelForm):
    class Meta:
        model = Song
        fields = ["song_title", "audio_file"]

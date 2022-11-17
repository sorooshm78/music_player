from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class Home(TemplateView):
    template_name = "music/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["albums"] = [
            {
                "id": "5",
                "album_logo": "",
                "album_title": "shecast eshgi",
                "artist": "Dj soroosh",
            },
            {
                "id": "6",
                "album_logo": "",
                "album_title": "ghafas",
                "artist": "Dj mehran",
            },
        ]
        context["user"] = {"username": "sina"}
        return context


class Detail(TemplateView):
    template_name = "music/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["album"] = {
            "id": "5",
            "album_logo": "",
            "album_title": "shecast eshgi",
            "artist": "Dj soroosh",
            "song_set": {
                "all": [
                    {
                        "song_title": "jjjj",
                        "file_type": "mp3",
                        "is_favorite": True,
                    },
                ]
            },
        }
        return context

from django.views import generic
from django.urls import reverse
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


from .models import Album, Song
from .forms import AlbumModelForm, SongModelForm

# Create your views here.
class AlbumList(generic.ListView):
    template_name = "music/index.html"
    model = Album
    context_object_name = "albums"


class AlbumDetail(generic.DetailView):
    template_name = "music/detail.html"
    model = Album


class AlbumDelete(generic.DeleteView):
    model = Album

    def get_success_url(self):
        return reverse("music:index")


class AlbumCreate(generic.CreateView):
    form_class = AlbumModelForm
    template_name = "music/create_album.html"

    def get_success_url(self):
        return reverse("music:index")


class AlbumFavorite(View):
    def get(self, request, pk):
        album = get_object_or_404(Album, pk=pk)
        album.is_favorite = not album.is_favorite
        album.save()
        return JsonResponse({"success": True})


class SongList(generic.ListView):
    model = Song
    context_object_name = "songs"
    template_name = "music/songs.html"


# class SongCreate(generic.CreateView):
#     form_class = SongModelForm
#     template_name = "music/create_song.html"

#     def get_success_url(self):
#         return reverse("music:index")


# class SongFavorite(View):
#     def get(self, request, pk):
#         song = get_object_or_404(Song, pk=pk)
#         song.is_favorite = not song.is_favorite
#         song.save()
#         return JsonResponse({"success": True})

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


class SongCreate(generic.CreateView):
    form_class = SongModelForm
    template_name = "music/create_song.html"

    def initial_album(self):
        self.album_id = self.kwargs.get("album_id")
        self.album = get_object_or_404(Album, pk=self.album_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.initial_album()

        context["album"] = self.album
        return context

    def form_valid(self, form):
        self.initial_album()
        form.instance.album = self.album
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("music:detail", args=[self.album_id])


class SongFavorite(View):
    def get(self, request, pk):
        song = get_object_or_404(Song, pk=pk)
        song.is_favorite = not song.is_favorite
        song.save()
        return JsonResponse({"success": True})


class SongDelete(generic.DeleteView):
    model = Song

    def get_object(self):
        self.album_id = self.kwargs.get("album_id")
        self.song_id = self.kwargs.get("song_id")

        return get_object_or_404(self.model, id=self.song_id, album_id=self.album_id)

    def get_success_url(self):
        return reverse("music:detail", args=self.album_id)

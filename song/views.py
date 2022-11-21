from django.views import generic
from django.urls import reverse
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Song
from .forms import SongModelForm
from .mixins import UserSongFilterMixin

from album.models import Album
from album.mixins import UserAlbumFilterMixin


class SongList(LoginRequiredMixin, UserSongFilterMixin, generic.ListView):
    model = Song
    context_object_name = "song_list"
    template_name = "music/songs.html"


class SongCreate(LoginRequiredMixin, UserAlbumFilterMixin, generic.CreateView):
    form_class = SongModelForm
    template_name = "music/create_song.html"
    model = Album

    def initial_album(self):
        self.album_id = self.kwargs.get("album_id")
        self.album = get_object_or_404(self.get_queryset(), pk=self.album_id)

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
        return reverse("detail", args=[self.album_id])


class SongFavorite(LoginRequiredMixin, View):
    def get(self, request, pk):
        song = get_object_or_404(Song, pk=pk, album__user=self.request.user)
        song.is_favorite = not song.is_favorite
        song.save()
        return JsonResponse({"success": True})


class SongDelete(LoginRequiredMixin, UserSongFilterMixin, generic.DeleteView):
    model = Song

    def get_object(self):
        self.album_id = self.kwargs.get("album_id")
        self.song_id = self.kwargs.get("song_id")

        return get_object_or_404(
            self.get_queryset(), id=self.song_id, album_id=self.album_id
        )

    def get_success_url(self):
        return reverse("detail", args=self.album_id)

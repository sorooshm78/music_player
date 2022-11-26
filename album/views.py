from django.views import generic
from django.urls import reverse
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Album
from .forms import AlbumModelForm
from .mixins import UserAlbumFilterMixin

from song.models import Song


class AlbumList(LoginRequiredMixin, UserAlbumFilterMixin, generic.ListView):
    template_name = "music/index.html"
    model = Album
    context_object_name = "albums"

    def get_queryset(self):
        query = super().get_queryset()

        self.search = self.request.GET.get("q", None)

        if (self.search is not None) and (self.search is not ""):
            query = query.filter(
                Q(album_title__icontains=self.search) | Q(artist__icontains=self.search)
            )

        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if (self.search is not None) and (self.search is not ""):
            context["songs"] = Song.objects.filter(song_title__icontains=self.search)

        return context


class AlbumDetail(LoginRequiredMixin, UserAlbumFilterMixin, generic.DetailView):
    template_name = "music/detail.html"
    model = Album


class AlbumDelete(LoginRequiredMixin, UserAlbumFilterMixin, generic.DeleteView):
    model = Album

    def get_success_url(self):
        return reverse("index")


class AlbumCreate(LoginRequiredMixin, generic.CreateView):
    form_class = AlbumModelForm
    template_name = "music/create_album.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("index")


class AlbumFavorite(LoginRequiredMixin, View):
    def get(self, request, pk):
        album = get_object_or_404(Album, pk=pk, user=self.request.user)
        album.is_favorite = not album.is_favorite
        album.save()
        return JsonResponse({"success": True})


# class AlbumFavorite(LoginRequiredMixin, UserAlbumFilterMixin, generic.DetailView):
#     model = Album

#     def get(self, request, pk):
#         album = self.get_object()
#         album.is_favorite = not album.is_favorite
#         album.save()
#         return JsonResponse({"success": True})

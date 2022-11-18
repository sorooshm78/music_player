from django.views import generic
from django.urls import reverse
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Album
from .forms import AlbumModelForm


class UserAlbumFilterMixin:
    def get_queryset(self):
        query = super().get_queryset()
        user = self.request.user
        return query.filter(user=user)


class AlbumList(LoginRequiredMixin, UserAlbumFilterMixin, generic.ListView):
    template_name = "music/index.html"
    model = Album
    context_object_name = "albums"


class AlbumDetail(LoginRequiredMixin, UserAlbumFilterMixin, generic.DetailView):
    template_name = "music/detail.html"
    model = Album


class AlbumDelete(LoginRequiredMixin, UserAlbumFilterMixin, generic.DeleteView):
    model = Album

    def get_success_url(self):
        return reverse("music:index")


class AlbumCreate(LoginRequiredMixin, generic.CreateView):
    form_class = AlbumModelForm
    template_name = "music/create_album.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("music:index")


class AlbumFavorite(LoginRequiredMixin, View):
    def get(self, request, pk):
        album = get_object_or_404(Album, pk=pk, user=self.request.user)
        album.is_favorite = not album.is_favorite
        album.save()
        return JsonResponse({"success": True})

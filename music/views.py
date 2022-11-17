from django.views import generic
from django.urls import reverse

from .models import Album
from .forms import AlbumModelForm

# Create your views here.
class ListAlbum(generic.ListView):
    template_name = "music/index.html"
    model = Album
    context_object_name = "albums"


class DetailAlbum(generic.DetailView):
    template_name = "music/detail.html"
    model = Album


class DeleteAlbum(generic.DeleteView):
    model = Album

    def get_success_url(self):
        return reverse("music:index")


class CreateAlbum(generic.CreateView):
    form_class = AlbumModelForm
    template_name = "music/create_album.html"

    def get_success_url(self):
        return reverse("music:index")

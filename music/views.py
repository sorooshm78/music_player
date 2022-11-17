from django.views import generic

from .models import Album

# Create your views here.
class ListAlbum(generic.ListView):
    template_name = "music/index.html"
    model = Album
    context_object_name = "albums"

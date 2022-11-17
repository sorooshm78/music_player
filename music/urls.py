from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = "music"

urlpatterns = [
    path("", views.ListAlbum.as_view(), name="index"),
    path("detail/<pk>/", views.DetailAlbum.as_view(), name="detail"),
    path("delete/album/<pk>/", views.DeleteAlbum.as_view(), name="delete_album"),
    path("create/album/", views.CreateAlbum.as_view(), name="create_album"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

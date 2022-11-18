from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = "music"

urlpatterns = [
    # Album
    path("", views.AlbumList.as_view(), name="index"),
    path("album/detail/<pk>/", views.AlbumDetail.as_view(), name="detail"),
    path("album/delete/<pk>/", views.AlbumDelete.as_view(), name="delete_album"),
    path("album/create/", views.AlbumCreate.as_view(), name="create_album"),
    path("album/favorite/<pk>/", views.AlbumFavorite.as_view(), name="favorite_album"),
    # Song
    path("songs/<all>/", views.SongList.as_view(), name="songs"),
    path("songs/create/<album_id>/", views.SongCreate.as_view(), name="create_song"),
    path("songs/favorite/<pk>/", views.SongFavorite.as_view(), name="favorite"),
    path(
        "songs/delete/<album_id>/<song_id>",
        views.SongDelete.as_view(),
        name="delete_song",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

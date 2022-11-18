from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = "music"

urlpatterns = [
    path("song/<all>/", views.SongList.as_view(), name="songs"),
    path("song/create/<album_id>/", views.SongCreate.as_view(), name="create_song"),
    path("song/favorite/<pk>/", views.SongFavorite.as_view(), name="favorite"),
    path(
        "song/delete/<album_id>/<song_id>",
        views.SongDelete.as_view(),
        name="delete_song",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

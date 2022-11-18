from django.urls import path

from . import views


urlpatterns = [
    path("<all>/", views.SongList.as_view(), name="songs"),
    path("create/<album_id>/", views.SongCreate.as_view(), name="create_song"),
    path("favorite/<pk>/", views.SongFavorite.as_view(), name="favorite"),
    path(
        "delete/<album_id>/<song_id>",
        views.SongDelete.as_view(),
        name="delete_song",
    ),
]

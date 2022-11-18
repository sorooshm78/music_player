from django.urls import path

from . import views


urlpatterns = [
    path("", views.AlbumList.as_view(), name="index"),
    path("detail/<pk>/", views.AlbumDetail.as_view(), name="detail"),
    path("delete/<pk>/", views.AlbumDelete.as_view(), name="delete_album"),
    path("create/", views.AlbumCreate.as_view(), name="create_album"),
    path("favorite/<pk>/", views.AlbumFavorite.as_view(), name="favorite_album"),
]

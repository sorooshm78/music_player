from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = "music"

urlpatterns = [
    path("", views.ListAlbum.as_view(), name="index"),
    # path("detail/<id>", views.Detail.as_view(), name="detail"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

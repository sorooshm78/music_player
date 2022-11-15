from django.urls import path

from . import views

app_name = 'music'

urlpatterns = [
    path("", views.Home.as_view(), name="index"),
    path("detail/<id>", views.Detail.as_view(), name="detail"),
]

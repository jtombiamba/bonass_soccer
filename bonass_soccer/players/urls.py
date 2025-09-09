# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("slider/", views.slider_view, name="slider"),
    path("randomize/", views.randomize_players, name="randomize")
]

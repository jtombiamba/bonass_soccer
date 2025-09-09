from django.urls import path
from . import views


urlpatterns = [
    path("", views.jambo_view, name="jambo_index"),
    ]
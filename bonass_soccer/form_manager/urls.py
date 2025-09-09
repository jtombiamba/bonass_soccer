from bonass_soccer.form_manager import views
from django.urls import path

urlpatterns = [
    path("", views.form_view, name="index"),
    # path("randomize/", views.randomize_players, name="randomize")
]
from django.urls import path
from .views import token_view, artists_view, songs_view

urlpatterns = [
    path("token/", token_view),
    path("artists/", artists_view),
    path("songs/", songs_view),
]

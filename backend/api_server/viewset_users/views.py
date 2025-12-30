from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import User, Artist, Song
from .serializer import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    @action(detail=True, methods=['post'], url_path='add-artist')
    def add_artist(self, request, id=None):
        user = self.get_object()
        artist_name = request.data.get("artist_name")

        if not artist_name:
            return Response(
                {"error": "artist_name is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        artist, created = Artist.objects.get_or_create(
            name=artist_name.strip()
        )

        user.favorite_artists.add(artist)

        return Response(
            {
                "user": user.username,
                "artist": artist.name,
                "created": created
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'], url_path='add-song')
    def add_song(self, request, id=None):
        user = self.get_object()
        artist_name = request.data.get("artist_name")
        song_name = request.data.get("song_name")

        if not artist_name or not song_name:
            return Response(
                {"error": "artist_name and song_name are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        artist, _ = Artist.objects.get_or_create(
            name=artist_name.strip()
        )

        song, created = Song.objects.get_or_create(
            name=song_name.strip(),
            artist=artist
        )

        user.favorite_songs.add(song)

        return Response(
            {
                "user": user.username,
                "artist": artist.name,
                "song": song.name,
                "created": created
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['delete'], url_path='remove-artist/(?P<artist_id>[^/.]+)')
    def remove_artist(self, request, id=None, artist_id=None):
        user = self.get_object()

        try:
            artist = user.favorite_artists.get(id=artist_id)
        except:
            return Response(
                {"error": "Artist not found for this user"},
                status=status.HTTP_404_NOT_FOUND
            )

        user.favorite_artists.remove(artist)

        return Response(
            {
                "user": user.username,
                "artist_removed": artist.name
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['delete'], url_path='remove-song/(?P<song_id>[^/.]+)')
    def remove_song(self, request, id=None, song_id=None):
        user = self.get_object()

        try:
            song = user.favorite_songs.get(id=song_id)
        except:
            return Response(
                {"error": "Song not found for this user"},
                status=status.HTTP_404_NOT_FOUND
            )

        user.favorite_songs.remove(song)

        return Response(
            {
                "user": user.username,
                "song_removed": song.name
            },
            status=status.HTTP_200_OK
        )

from django.shortcuts import get_object_or_404
from .models import User, Artist, Song

def add_artist_to_user(user_id, artist_name):
    user = get_object_or_404(User, id=user_id)

    artist, created = Artist.objects.get_or_create(
        name=artist_name.strip()
    )

    user.favorite_artists.add(artist)

    return {
        "artist": artist.name,
        "created": created
    }

def add_song_to_user(user_id, artist_name, song_name):
    user = get_object_or_404(User, id=user_id)

    artist, _ = Artist.objects.get_or_create(
        name=artist_name.strip()
    )

    song, created = Song.objects.get_or_create(
        name=song_name.strip(),
        artist=artist
    )

    user.favorite_songs.add(song)

    return {
        "artist": artist.name,
        "song": song.name,
        "created": created
    }

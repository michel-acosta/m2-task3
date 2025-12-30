from rest_framework import serializers
from .models import User, Artist, Song

class FavoriteArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name']
        read_only_fields = ['id']
    
    def validate_artist_name(self, value):
        if value is None or len(value) == 0:
            raise serializers.ValidationError("Artist name cannot be empty.")            
        return value

class FavoriteSongSerializer(serializers.ModelSerializer):
    artist_id = serializers.IntegerField(source="artist.id", read_only=True)
    artist_name = serializers.CharField(source="artist.name", read_only=True)

    class Meta:
        model = Song
        fields = ['id', 'name', "artist_id", "artist_name"]
        read_only_fields = ['id']
    
    def validate_artist_name(self, value):
        if value is None or len(value) == 0:
            raise serializers.ValidationError("Artist name cannot be empty.")            
        return value

    def validate_song_name(self, value):
        if value is None or len(value) == 0:
            raise serializers.ValidationError("Song name cannot be empty.")            
        return value
    
class UserSerializer(serializers.ModelSerializer):
    favorite_artists = FavoriteArtistSerializer(many=True, read_only=True)
    favorite_songs = FavoriteSongSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'favorite_artists', 'favorite_songs']
        read_only_fields = ['id']

    def validate_username(self, value):
        if value is None or len(value) == 0:
            raise serializers.ValidationError("Username cannot be empty.")            
        return value
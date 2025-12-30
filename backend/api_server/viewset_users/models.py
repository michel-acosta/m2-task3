from django.db import models

# Definición del modelo de usuario
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    favorite_artists = models.ManyToManyField('Artist', related_name='users', blank=True)
    favorite_songs = models.ManyToManyField('Song', related_name='users', blank=True)

    def __str__(self):
        return self.username
    
# Definición de los artistas favoritos del usuario
class Artist(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Definición de las canciones favoritas del usuario
class Song(models.Model):    
    name = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.artist.name} - {self.name}"
from django.db import models

# Modelo para almacenar un token de Spotify y una fecha de expiración del mismo
class SpotifyToken(models.Model):
    access_token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Token expira en {self.expires_at}"
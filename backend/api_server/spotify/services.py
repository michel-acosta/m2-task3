import base64
import requests
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from .models import SpotifyToken

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"

# ============================
# TOKEN (CLIENT CREDENTIALS)
# ============================

def get_token_from_db():
    token = SpotifyToken.objects.first()
    if token and token.expires_at > timezone.now():
        return token.access_token
    return None

def save_token_to_db(access_token, expires_in):
    expires_at = timezone.now() + timedelta(seconds=expires_in - 10)
    SpotifyToken.objects.all().delete()  # solo uno activo
    SpotifyToken.objects.create(
        access_token=access_token,
        expires_at=expires_at
    )

def request_new_token():
    auth_header = base64.b64encode(
        f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}".encode()
    ).decode()

    data = {"grant_type": "client_credentials"}
    headers = {"Authorization": f"Basic {auth_header}"}

    response = requests.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)
    response.raise_for_status()

    token_info = response.json()
    save_token_to_db(
        token_info["access_token"],
        token_info.get("expires_in", 3600)
    )

    return token_info["access_token"]

def get_access_token():
    token = get_token_from_db()
    if token:
        return token
    return request_new_token()

# ============================
# LLAMADAS A SPOTIFY
# ============================

def spotify_get(endpoint, params=None):
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        f"{SPOTIFY_API_URL}{endpoint}",
        headers=headers,
        params=params
    )

    if response.status_code == 401:
        token = request_new_token()
        headers["Authorization"] = f"Bearer {token}"
        response = requests.get(
            f"{SPOTIFY_API_URL}{endpoint}",
            headers=headers,
            params=params
        )

    response.raise_for_status()
    return response.json()

def search_artists(query="jamiroquai"):
    params = {
        "q": query,
        "type": "artist",
        "limit": 10
    }
    return spotify_get("/search", params)

def search_songs(query="virtual insanity"):
    params = {
        "q": query,
        "type": "track",
        "limit": 10
    }
    return spotify_get("/search", params)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import search_artists, search_songs, get_access_token

@api_view(["GET"])
def token_view(request):
    token = get_access_token()
    return Response({
        "access_token": token
    })

@api_view(["GET"])
def artists_view(request):
    q = request.query_params.get("q", "jamiroquai")
    data = search_artists(q)
    return Response(data)

@api_view(["GET"])
def songs_view(request):
    q = request.query_params.get("q", "virtual insanity")
    data = search_songs(q)
    return Response(data)

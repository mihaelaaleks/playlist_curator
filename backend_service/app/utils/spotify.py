import os

from dotenv import load_dotenv
from spotipy import Spotify, SpotifyOAuth

load_dotenv()

CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_API")


def create_spotify(scope: str = "user-library-read user-top-read") -> Spotify:
    return Spotify(auth_manager=SpotifyOAuth(scope=scope))


def create_spotify_for_playlist_modification(
    scope: str = "user-library-read user-top-read playlist-modify-private",
) -> Spotify:
    return Spotify(auth_manager=SpotifyOAuth(scope=scope))

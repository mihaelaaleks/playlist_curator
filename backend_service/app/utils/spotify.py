from spotipy import Spotify, SpotifyOAuth


def create_spotify(scope: str = "user-library-read user-top-read") -> Spotify:
    return Spotify(auth_manager=SpotifyOAuth(scope=scope))

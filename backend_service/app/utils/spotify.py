from spotipy import Spotify, SpotifyOAuth


def create_spotify(
    scope: str = "user-library-read user-top-read",
) -> Spotify:
    return Spotify(auth_manager=SpotifyOAuth(scope=scope))


def create_spotify_for_playlist_modification(
    scope: str = "user-library-read user-top-read playlist-modify-private",
) -> Spotify:
    return Spotify(auth_manager=SpotifyOAuth(scope=scope))

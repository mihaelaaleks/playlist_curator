import spotipy
from spotipy.oauth2 import SpotifyOAuth

from dotenv import load_dotenv


# For the scopes, if they're a known constant elements, do an enum
def create_spotify(scope: str = "user-library-read user-top-read") -> spotipy.Spotify:
    load_dotenv()
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


# TO DO
def get_request_date():
    return


def get_playlists_tracks(playlist_ids: list, spotify: spotipy.Spotify):
    id_map = {}
    for id in playlist_ids:
        res = spotify.playlist_tracks(id)
        id_map[id] = res

    return id_map


def get_recently_played(limit: int, spotify: spotipy.Spotify):
    """get top recently played tracks from users Spotify

    Args:
        limit (int): number of items to retrieve, must be less than 100
        spotify (spotipy.Spotify): _description_

    Returns:
        dict: Json response
    """
    if limit >= 100:
        raise ValueError("Limit must not exceed 100")
    response = spotify.current_user_recently_played(limit=limit)
    return response


def get_audio_features(track_ids, spotify):
    # api call can do max 100 ids
    if len(track_ids) > 100:
        raise Exception("Track input list has too many entries (>100)")

    response = spotify.audio_features(track_ids)
    return response


def get_artist(artist_url, spotify):
    response = spotify.artist(artist_url)
    print(response)
    return response

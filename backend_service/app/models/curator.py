from spotipy import Spotify


def get_recommendation_tracks(
    spotify: Spotify,
    genres: list,
):
    response = spotify.recommendations(seed_genres=genres)
    if response is not None:
        recommended = response["tracks"]
    return recommended

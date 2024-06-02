from spotipy import Spotify

# Taken from spotipy.client.Spotify.recommendations.
ALL_RECOMMENDATION_ATTRIBUTES = [
    "acousticness",
    "danceability",
    "duration_ms",
    "energy",
    "instrumentalness",
    "key",
    "liveness",
    "loudness",
    "mode",
    "popularity",
    "speechiness",
    "tempo",
    "time_signature",
    "valence",
]

NUMERIC_RANGE_ATTRIBUTES = [
    "acousticness",
    "danceability",
    "energy",
    "instrumentalness",
    "liveness",
    "popularity",
    "speechiness",
]


def get_all_attributes() -> list[str]:
    return ALL_RECOMMENDATION_ATTRIBUTES


def get_all_numeric_range_attributes() -> list[str]:
    return NUMERIC_RANGE_ATTRIBUTES


def get_recommendation_tracks(
    spotify: Spotify,
    genres: list,
):
    response = spotify.recommendations(seed_genres=genres)
    if response is not None:
        recommended = response["tracks"]
    return recommended

from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from re import split
from typing import Any

import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from plotly_flask.models.track import Track

_T_SPOTIFY_TRACK = Any

DEFAULT_N_SAMPLE = 4


def split_into_chunks(lst: list, chunk_size: int = 4):
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def create_spotify(scope: str = "user-library-read user-top-read") -> spotipy.Spotify:
    # TODO: Fix when case of other new input users to be authenticated for the first time.
    #   i.e. currently e-mails have to be whitelisted, this will need to be looked into.
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


def get_genre_seeds(spotify: spotipy.Spotify) -> list:
    response = spotify.recommendation_genre_seeds()
    if response is not None:
        genres = response["genres"]
    return genres


def get_multi_recommendation_tracks(
    spotify: spotipy.Spotify, genre_list
) -> list[Track]:
    chunked_genres = split_into_chunks(genre_list)
    tracks_chunks = []
    for chunk in chunked_genres:
        track_data = get_recommendation_tracks(spotify=spotify, genres=chunk)
        tracks_chunk = create_list_of_tracks(track_data)
        tracks_chunks.append(tracks_chunk)
    return list(chain(*tracks_chunks))


def get_recommendation_tracks(
    spotify: spotipy.Spotify,
    genres: list,
):
    """Given a list of genres get back a list of recommended tracks.

    Tracks are in a shape like:
    https://developer.spotify.com/documentation/web-api/reference/get-track
    """
    # TODO: looking at the recommendations there's probably some interesting room to
    # play here too.
    response = spotify.recommendations(seed_genres=genres)
    if response is not None:
        recommended = response["tracks"]
    return recommended


def get_sample_of_recommendation_from_tracks(
    spotify: spotipy.Spotify, tracks: list, n_sample: int = DEFAULT_N_SAMPLE
):
    seed_tracks = np.random.choice(tracks, size=n_sample)
    response = spotify.recommendations(seed_tracks=list(seed_tracks))
    if response is not None:
        recommended = response["tracks"]
    return recommended


def create_list_of_tracks(track_data: _T_SPOTIFY_TRACK) -> list[Track]:
    tracks = []
    for item in track_data:
        track = Track(
            id=item["id"],
            name=item["name"],
            url=item["external_urls"]["spotify"],
            artists=item["artists"],
            album_image=item["album"]["images"],
            album_id=item["album"]["id"],
            track_popularity=item["popularity"],
        )
        tracks.append(track)
    return tracks

from dataclasses import dataclass
from re import split
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from pathlib import Path
from plotly_flask.models.track import Track

# TODO:
# make the "t_" numeric values into some dataclass thing
#   like class RecommendParams:
# then you can build in the "percent" convert there.
#   Then the "get_cleaned_recommendations" and "get_recommendation_tracks"
#   could be methods of this "RecommendParams"
#   so you'd call like
#   params = RecommendParams(<numeric_parts>)
#
#   # Object Oriented
#   recommendations = params.get_recommendations(spotify, limit)
#
#   # DependencyInjection
#   recommendations = get_cleaned_recommendations(
#       spotify=spotify,
#       limit=limit,
#       recommend_params= params,
#   )
#   tracks = get_recommendation_tracks(
#       spotify=spotify,
#       limit=limit,
#       recommend_params= params,
#   )
#


def split_into_chunks(lst: list, chunk_size: int = 4):
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def create_spotify(scope: str = "user-library-read user-top-read") -> spotipy.Spotify:
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


def get_genre_seeds(spotify: spotipy.Spotify) -> list:
    response = spotify.recommendation_genre_seeds()
    if response is not None:
        genres = response["genres"]
    return genres


def get_multi_recommendation_tracks(spotify, genre_list):
    chunked_genres = split_into_chunks(genre_list)
    tracklist = []
    for chunk in chunked_genres:
        track_data = get_recommendation_tracks(spotify=spotify, genres=chunk)
        track_df = clean_track_recommendations(track_data)
        tracklist = df_to_track_obj(track_df)
    return tracklist


def get_recommendation_tracks(
    spotify: spotipy.Spotify,
    genres: list,
):
    response = spotify.recommendations(seed_genres=genres)
    if response is not None:
        recommended = response["tracks"]
    return recommended


def clean_track_recommendations(track_data):
    cleaned_track_list = {}
    dfs = []
    for item in track_data:
        cleaned_track_list["track_id"] = item["id"]
        cleaned_track_list["track_name"] = item["name"]
        cleaned_track_list["track_url"] = item["external_urls"]["spotify"]
        # temporary fix
        # takes the first artist in a list
        cleaned_track_list["artist_name"] = item["artists"][0]
        cleaned_track_list["album_id"] = item["album"]["id"]
        cleaned_track_list["image"] = item["album"]["images"]
        cleaned_track_list["track_popularity"] = item["popularity"]
        df = pd.DataFrame([cleaned_track_list])
        dfs.append(df)
    recommended_tracks_df = pd.concat(dfs)
    return recommended_tracks_df


def df_to_track_obj(tracklist_df):
    track_rec_list = []
    for index, row in tracklist_df.iterrows():
        track_id = row["track_id"]
        track_name = row["track_name"]
        track_url = row["track_url"]
        artist_name = row["artist_name"]
        album_id = row["album_id"]
        track_image = row["image"]
        track_popularity = row["track_popularity"]
        track = Track(
            track_name=track_name,
            track_id=track_id,
            track_url=track_url,
            track_popularity=track_popularity,
            image=track_image,
            artist_name=artist_name,
            album_id=album_id,
        )
        track_rec_list.append(track)
    return track_rec_list

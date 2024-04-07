import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from pathlib import Path


from plotly_flask.models.track import Track
from app.utils import get_tag


def create_spotify(scope: str = "user-library-read user-top-read") -> spotipy.Spotify:
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


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


def get_recommendation(
    limit: int,
    spotify: spotipy.Spotify,
    t_acousticness: int,
    t_danceability: int,
    t_energy: int,
    t_instrumentalness: int,
):
    """get a list of recommended tracks based on attributes

    Args:
        limit (int): number of items to retrieve, must be less than 100
        spotify (spotipy.Spotify): spotify instance
        target_<attr>: audio features for generating recommendation

    Returns:
        dict: Json response
    """
    s_artists = ["6XYvaoDGE0VmRt83Jss9Sn", "07b9qW7pabKGO29JPWXn9m"]
    if limit >= 100:
        raise ValueError("Limit must not exceed 100")
    response = spotify.recommendations(
        limit=limit,
        seed_artists=s_artists,
        target_acousticness=t_acousticness / 100,
        target_danceability=t_danceability / 100,
        target_energy=t_energy / 100,
        target_instrumentalness=t_instrumentalness / 100,
    )
    return response


def clean_track_recommendations(track_data):
    cleaned_track_list = {}
    dfs = []
    for item in track_data:
        cleaned_track_list["track_id"] = item["id"]
        cleaned_track_list["track_name"] = item["name"]
        cleaned_track_list["track_url"] = item["external_urls"]["spotify"]
        cleaned_track_list["artist_name"] = item["artists"]
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


def get_cleaned_recommendations(
    limit: int,
    spotify: spotipy.Spotify,
    t_acousticness: int,
    t_danceability: int,
    t_energy: int,
    t_instrumentalness: int,
):
    recommendation = get_recommendation(
        limit=limit,
        spotify=spotify,
        t_acousticness=t_acousticness,
        t_danceability=t_danceability,
        t_energy=t_energy,
        t_instrumentalness=t_instrumentalness,
    )
    track_data = recommendation["tracks"]
    rec_df = clean_track_recommendations(track_data=track_data)
    rec_df["image"] = rec_df["image"].apply(lambda x: get_tag(x, "url"))
    rec_df["artist_name"] = rec_df["artist_name"].apply(lambda x: get_tag(x, "name"))

    track_list = df_to_track_obj(rec_df)
    return track_list

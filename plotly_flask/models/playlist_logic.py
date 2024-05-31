from pathlib import Path

import pandas as pd

from plotly_flask.models.playlist import Playlist

file_dir_path = Path(__file__).parent.parent.parent / Path("data")

playlist_file_name = Path("my_presentable_playlists.pkl")
track_playlist_map = Path("playlist_id_map.pkl")

PLAYLIST_PATH = file_dir_path / playlist_file_name
track_path = file_dir_path / track_playlist_map


def read_pickle_playlist(playlist_path: Path = PLAYLIST_PATH) -> pd.DataFrame:
    return pd.read_pickle(playlist_path)


def df_to_playlist_obj():
    playlist_df = pd.read_pickle(PLAYLIST_PATH)
    playlist_obj_list = []
    for _, row in playlist_df.iterrows():
        playlist_name = row["name"]
        playlist_id = row["id"]
        playlist_image = row["images"]
        playlist = Playlist(
            name=playlist_name, playlist_id=playlist_id, image=playlist_image
        )
        playlist_obj_list.append(playlist)
    return playlist_obj_list


def get_tracklist(playlist_id: str) -> list:
    df = pd.read_pickle(track_path)
    entries = df.loc[df["playlist_id"] == playlist_id].values
    return entries.tolist()


def get_tracks_df_from_playlist_id(playlist_id: str):
    df = pd.read_pickle(track_path)
    df = df.rename(
        columns={
            "1": "track_id",
            "2": "track_name",
            "3": "artist_id",
            "4": "artist_name",
            "5": "popularity",
        }
    )
    df = df.loc[df["playlist_id"] == playlist_id]
    return df


def get_avg_popularity(tracklist: list):
    df = pd.DataFrame.from_records(
        tracklist,
        columns=[
            "track_id",
            "track_name",
            "artist_id",
            "artist_name",
            "popularity",
            "playlist_id",
        ],
    )
    avg = df["popularity"].mean()
    return int(avg)

import pandas as pd
from pathlib import Path
from plotly_flask.models.playlist import Playlist

file_dir_path = Path(__file__).parent.parent.parent / Path("data")

playlist_file_name = Path("my_presentable_playlists.pkl")

playlist_path = file_dir_path / playlist_file_name


def df_to_playlist_obj():
    playlist_df = pd.read_pickle(playlist_path)
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

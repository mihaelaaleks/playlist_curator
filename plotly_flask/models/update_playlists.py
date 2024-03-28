from app.spotipy_requests import create_spotify
from app import utils
import json
from pathlib import Path
import pandas as pd
import logging

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger(__name__)

# set output path for playlist response
data_filepath = utils.set_output_path("my_playlists.json")
logger.info(f"Defined output path:{data_filepath}")

# create spotify instance
spotify = create_spotify()
logger.info("Created spotipy instance")
logger.info(data_filepath)

# fetch playlists and save them 
my_playlists = spotify.current_user_playlists()
utils.save_playlist_json(my_playlists, data_filepath)

# get only playlist items from response
cleaned_playlists = utils.clean_playlist_objects(my_playlists)
clean_playlist_path = utils.set_output_path("my_cleaned_playlists.json")
utils.save_playlist_json(cleaned_playlists, clean_playlist_path)
playlist_df = pd.DataFrame.from_records(cleaned_playlists)

# get first entry for image and external_urls
# drop unnecessary columns
playlist_df["images"] = playlist_df["images"].apply(lambda x: utils.get_link(x))
playlist_df["external_urls"] = playlist_df["external_urls"].apply(
    lambda x: utils.get_link_from_tag(x, "spotify")
)
playlist_df = playlist_df.drop(columns=["primary_color", "uri"])

# set filepath for final cleaned playlists
# save df as pickle
final_pkl_filepath = utils.set_output_path("my_presentable_playlists.pkl")
playlist_df.to_pickle(final_pkl_filepath)

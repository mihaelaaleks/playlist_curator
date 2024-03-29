from pathlib import Path
import json


def set_output_path(filename: str) -> Path:
    data_filepath = Path(__file__).parent / Path("data") / Path(filename)
    return data_filepath


def save_playlist_json(playlists, filepath):
    playlist_json = json.dumps(playlists)

    with open(filepath, "w") as outfile:
        outfile.write(playlist_json)


def clean_playlist_objects(playlists):
    cleaned_playlists = []

    for _, item in enumerate(playlists["items"]):
        cleaned_playlists.append(item)

    return cleaned_playlists


def get_link_from_tag(row, tag):
    first_entry = row[tag]
    return first_entry


def get_link(from_image_row):
    if len(from_image_row) == 0:
        return None
    first_entry = from_image_row[0]
    return first_entry["url"]

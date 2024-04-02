from pathlib import Path
import pandas as pd
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


def get_tag(row, tag):
    first_entry = row[tag]
    return first_entry


def get_link(from_image_row):
    if len(from_image_row) == 0:
        return None
    first_entry = from_image_row[0]
    return first_entry["url"]


def get_playlist_track_artist_map(playlist_tracks: dict) -> list:
    track_references = []
    for _, item in playlist_tracks.items():
        items = item["items"]
        for item in items:
            track = item["track"]
            id = track["id"]
            name = track["name"]
            # take the first artist
            artist_id = track["artists"][0]["id"]
            artist_name = track["artists"][0]["name"]
            playlist_id = _
            popularity = track["popularity"]
            track_references.append(
                {
                    "track_id": id,
                    "track_name": name,
                    "artist_id": artist_id,
                    "artist_name": artist_name,
                    "popularity": popularity,
                    "playlist_id": playlist_id,
                }
            )
    return track_references


# TODO: lookup how i had set up the tempo again
def get_audio_features(audio_features: dict):
    audio_df = pd.DataFrame(audio_features)
    MAX_TEMPO_SCALER = 240
    audio_df["normalized_tempo"] = audio_df["tempo"] / MAX_TEMPO_SCALER
    return audio_df.to_json(orient="records")

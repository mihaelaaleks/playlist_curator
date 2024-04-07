from pathlib import Path
import json

file_dir_path = Path(__file__).parent.parent.parent / Path("data")

genre_file_name = Path("spotify_genre_seeds.json")
genre_path = file_dir_path / genre_file_name


def genre_json_to_list():
    genres = {}
    with open(genre_path) as f:
        genres = json.load(f)

    genre_list = genres["genres"]
    return genre_list

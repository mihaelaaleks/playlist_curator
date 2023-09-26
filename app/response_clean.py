import json
import pathlib
import pprint

test_file = 'recently_played_170923'

def open_recently_played_json(filename): 
    filepath = pathlib.Path(__file__).parent / pathlib.Path('data') / pathlib.Path(f'{filename}.json')
    if filepath.is_file() is False:
        raise Exception("Filepath incorrect or does not exist")
    
    with open(filepath, 'r') as file: 
        json_data = json.loads(file.read())
    # json data is a dict
    items_data = json_data['items']
    # items data is a list
    return items_data

# takes the tracks first
# then takes fields we need from track information
def clean_recently_played(recently_played_items):
    # what happens if input isn't quite correct
    tracks = []
    track_df_items = []
    # get only track information for now
    for item in recently_played_items:
        tracks.append(item["track"])
    
    for track in tracks:
        track_id = track["id"]
        track_name = track["name"]
        artist_id = track["artists"][0]["id"]
        artist_name = track["artists"][0]["name"]
        entry = {
            "track_id": track_id,
            "track_name": track_name,
            "artist_id": artist_id, 
            "artist_name": artist_name
        }
        
        track_df_items.append(entry)
        
    return track_df_items


def get_id_recently_played(recently_played_items):
    # what happens if input isn't quite correct
    track_ids = []
    # get only track information for now
    for item in recently_played_items:
        track_ids.append(item["track"]["id"])
        
    return track_ids

# recent_tracks = open_recently_played_json(test_file)
# cleaned_tracks = get_id_recently_played(recent_tracks)
# pprint.pprint(cleaned_tracks)
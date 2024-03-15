import pandas as pd
from pathlib import Path
import json

data_path = Path(__file__).parent.parent / Path('data')

df = pd.read_pickle(data_path / Path('audio_analysis_df.pkl'))

def get_most_played_artists():
    most_played_artists = df['artist_name'].value_counts().to_frame()
    top_6 = most_played_artists.iloc[:5]
    print(top_6)
    return top_6


def get_playlist_data():
    with open(data_path / Path('my_cleaned_playlists.json'), 'r') as fp:
        playlist_data = json.load(fp)
    # lame but currently the keys are converted to strings
    return playlist_data



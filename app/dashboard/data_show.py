import pandas as pd
import pathlib

data_path = pathlib.Path(__file__).parent.parent / pathlib.Path('data')

df = pd.read_pickle(data_path / pathlib.Path('audio_analysis_df.pkl'))

def get_most_played_artists():
    most_played_artists = df['artist_name'].value_counts().to_frame()
    top_6 = most_played_artists.iloc[:5]
    print(top_6)
    return top_6


get_most_played_artists()
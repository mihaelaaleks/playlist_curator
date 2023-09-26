import response_clean
import spotipy_requests
import pprint
import pandas as pd
import pathlib

# testing for now
# this should be wrapped up in a function from a facade somewhere
test_file = 'recently_played_170923'    
data_filepath = pathlib.Path(__file__).parent / pathlib.Path('data')


# needs just the path of the recently played and gets the 
def pull_audio_features_df(test_file):
    recent_tracks = response_clean.open_recently_played_json(test_file)
    cleaned_tracks = response_clean.clean_recently_played(recent_tracks)
    cleaned_ids = response_clean.get_id_recently_played(recent_tracks)
    audio_features = spotipy_requests.get_audio_features(cleaned_ids)
    pprint.pprint(audio_features)
    # save to pickle for now
    pd.DataFrame(audio_features).to_pickle(data_filepath / pathlib.Path('audio_features.pkl'))
    pd.DataFrame(cleaned_tracks).to_pickle(data_filepath / pathlib.Path(f'{test_file}.pkl'))


# uncomment to get audio features of tracks per IDs    
# pull_audio_features_df(test_file)


# pull artist data

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint
import data_store
import response_clean
import pandas as pd

# need authentication scope
# need to find the way to set the scope flexibly
# would be baller
scope = "user-read-recently-played"
# initial authorisation code
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope = scope))

# TO DO 
def get_request_date():
    return

def get_recently_played(limit):
    response = spotify.current_user_recently_played(limit = limit)
    data_store.store_data_as_json(response, 'recently_played_190923')
    # clean_response = response_clean.clean_recently_played(response)
    pprint.pprint(type(response))
    pprint.pprint(len(response))
    print(response)
    return response


# get_recently_played(50)
# TO DO 
# trakc ids is a list 
def get_audio_features(track_ids):
    #api call can do max 100 ids
    if len(track_ids)> 100:
        raise Exception("Track input list has too many entries (>100)")
    
    response = spotify.audio_features(track_ids)
    return response

# ideally ---> 
# pull recently played tracks from spotify
# get artists and track ids 
# from the track ids pull the audio features for each track

# transform the audio features in a df

# half-step point - get the audio features in a df
# do a quick and dirty dash project and visualize the data
# also show most listened to duh

# find a big ass dataset of music data with the spotify features in there
# try to find a match 


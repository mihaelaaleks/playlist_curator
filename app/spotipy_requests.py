import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint
from . import data_store
from . import response_clean
import pandas as pd

from dotenv import load_dotenv

# need authentication scope
# need to find the way to set the scope flexibly
# would be baller

# For the scopes, if they're a known constant elements, do an enum
def create_spotify(scope :str ='user-library-read user-top-read') -> spotipy.Spotify:
    load_dotenv()
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope = scope)) 

# scope = 'user-library-read user-top-read'
# # scope = "user-read-recently-played"
# # initial authorisation code
# spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope = scope))

# TO DO 
def get_request_date():
    return

def get_recently_played(limit:int, spotify: spotipy.Spotify):
    """get_recently_played

    Args:
        limit (int): number of items to retrieve, must be less than 100
        spotify (spotipy.Spotify): _description_

    Returns:
        dict: Json response 
    """
    if limit >= 100:
        raise ValueError("Limit must not exceed 100")    
    response = spotify.current_user_recently_played(limit = limit)
    return response
    data_store.store_data_as_json(response, 'recently_played_190923')
    # clean_response = response_clean.clean_recently_played(response)
    pprint.pprint(type(response))
    pprint.pprint(len(response))
    print(response)
    return response



# track ids is a list 
def get_audio_features(track_ids, spotify):
    #api call can do max 100 ids
    if len(track_ids) > 100:
        raise Exception("Track input list has too many entries (>100)")
    
    response = spotify.audio_features(track_ids)
    return response

def get_artist(artist_url, spotify): 
    response = spotify.artist(artist_url)
    print(response)
    return response


# response = spotify.current_user_top_artists(limit=5, offset=0, time_range='short_term')

# pprint.pprint(response)

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


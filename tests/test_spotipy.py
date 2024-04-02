import pytest
from spotipy import Spotify
from app.spotipy_requests import (
    create_spotify,
    get_recently_played,
    get_playlists_tracks,
)


@pytest.fixture
def spotify():
    return create_spotify()


def test_create_spotify_returns_spotify(spotify):
    assert isinstance(spotify, Spotify)


def test_get_recently_played_has_proper_keys(spotify):
    response = get_recently_played(limit=10, spotify=spotify)
    assert isinstance(response, dict)
    needed_keys_from_response = ["items", "href"]
    for key in needed_keys_from_response:
        assert key in response.keys()


def test_does_recently_played_limit_return_correct_items(spotify):
    intereted_limits = [
        3,
        5,
        9,
    ]
    for limit in intereted_limits:
        response = get_recently_played(limit=limit, spotify=spotify)
        actual_num_items = len(response["items"])
        assert actual_num_items == limit


def test_get_recently_played_above_100_raises_error(spotify):
    big_limit = 101
    with pytest.raises(ValueError):
        get_recently_played(big_limit, spotify)


##########################################################################################
#   Fake test for nested json
##########################################################################################


def test_items_json_nesting(spotify):
    big_limit = 1
    response = get_recently_played(big_limit, spotify)
    item = response["items"][0]
    needed_top_keys = ["track", "played_at", "context"]

    missing_keys = set(needed_top_keys) - set(item.keys())
    assert len(missing_keys) == 0

    track = item["track"]
    needed_track_keys = ["album", "artists", "name", "id"]
    missing_keys = set(needed_track_keys) - set(track.keys())


def test_get_playlist_tracks(spotify):
    id_list = [
        "7ryAqRhEED5CNarJgIXxgd",
        "0e8tuDsddlctM6tBDEYPJ2",
        "7doP9xG2n6DXnflGTmURsC",
    ]
    playlist_id_map = get_playlists_tracks(id_list, spotify)
    assert len(id_list) == len(playlist_id_map)


# The other type of test
# This first api call is to "get_recently_played"
# This gives us a bit of a issue to test, because it'll be different every time it's ran
# as that means we should only really test the keys
#
# something like get_artist_info("artist_name")
# is more testable
#   you'd do the same thing, checking the keys
#   BUT you'd know information about them before hand, like the expected
#   sure maybe KGLW releases a new album, so don't write a test for them based on num of albums
#   Be reasonable with the kinds of data you pull
#   testing historic stuff is the best:
#       first album
#       release date strings
#       duration of song names
#
#
# Other unit tests can check combinations of flows (functional test)
#   get_artist_albums()
#   -> song_name = get_first_song()
#   -> song_info = get_song_info_from_spotify(song_name)
#   -> is song_info["album"] the same as the album that the song was found in
#    though this seems obvious, it makes for a good test of connections in a system
#
# integration test would test communication between separate interfaces
#   i.e.
#       connect to spotify
#       -> get user data
#       -> transform user data
#       -> save data to database
#       -> query database

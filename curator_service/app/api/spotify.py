import os

from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from spotipy import Spotify, SpotifyOAuth

from ..models import curator
from ..models.spotify import (
    Attribute,
    CurrateInput,
    Genre,
    Playlist,
    PlaylistCreator,
    Track,
)

load_dotenv()

CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI")


def create_spotify(
    scope: str = "user-library-read user-top-read playlist-modify-private playlist-modify-public",
) -> Spotify:
    return Spotify(
        auth_manager=SpotifyOAuth(scope=scope),
        # The default retry codes includes 429, maybe this causes the API endopint spam
        status_forcelist=(500, 502, 503, 504),
        retries=0,
    )


router = APIRouter(
    prefix="/spotify",
    tags=["spotify"],
    responses={404: {"description": "Not found"}},
)

N_TRACKS_DESIRED = 1
N_LIMIT_RUNS = 2
BUMP_TOLERANCE = 0.6
DEFAULT_START_TOLERANCE = 0.25


@router.get("/get_playlists/me")
async def get_playlists() -> list[Playlist]:
    """For the current logged in user, get the playlists returned
    from a call to the get playlists of spotify.

    Currently, this function will return the 50 playlists. It's still
    tbd if that is the 50 first, or 50 most recent. Also, how and
    to what extent should this API provide control to return more
    playlists needs to be built in the future.

    Returns:
        list[Playlist]: List of playlists returned for the current user.
    """
    spotify = create_spotify()
    playlists_response = spotify.current_user_playlists()
    return [
        Playlist(id=item["id"], name=item["name"], image_url=item["images"][0]["url"])
        for item in playlists_response["items"]
    ]


@router.post("/delete")
async def delete_playlist(playlist: Playlist):
    spotify = create_spotify()
    spotify.current_user_unfollow_playlist(playlist_id=playlist.id)


@router.post("/curate")
async def curate(input: CurrateInput) -> list[Track]:
    """Parse the currate input response body into kwargs to be used by
    the spotify recommendation algorithm.

    This endpoint is meant to provide flexibility to pass in whatever combination
    of currate input a user wants. The returned result will be
    a list of tracks that are recommended by spotify from the input.

    Args:
        input (CurrateInput): JSON response body containing seed and attribute
            information to be used

    Returns:
        list[Track]: Tracks to be sent as part of request body JSON.
    """
    spotify = create_spotify()
    try:
        return get_recommendations(spotify, input)
    except Exception as err:
        # TODO: reraise somehow? maybe to a 400 error?
        raise err


def get_recommendations(
    spotify: Spotify,
    input: CurrateInput,
    n_runs: int = 1,
    tolerance: float = DEFAULT_START_TOLERANCE,
    tolerance_bump: float = BUMP_TOLERANCE,
) -> list[Track]:
    """Recursive call to recommendation with updated tolerance.

    To ensure users always get "SOME" tracks returned.

    If the input attributes result in no tracks recommended, try to recommend again
    but use a higher tolerance.
    This call will happen up to n_runs times.
    Each time, the tolerance is increased by the tolerance bump.

    Args:
        spotify (Spotify): Spotify instance to produce recommendations from.
        input (CurrateInput): Input base model to process attributes from.
        n_runs (int, optional): Number of max runs to attempt. Starts at 1. Defaults to 1.
        tolerance (float, optional): Tolerance to use for applying max, min attributes. Defaults to 0.1.
        tolerance_bump (float, optional): Increase to tolerance to apply for each run. Defaults to 0.1.

    Returns:
        List[Track]: tracks returned by the input recommendation.
    """
    response = spotify.recommendations(
        **input.as_recommendation_kwargs(attribute_tolerance=tolerance)
    )
    tracks = response["tracks"]

    # Just return what we have, we've ran enough times
    if n_runs > N_LIMIT_RUNS:
        return [Track(id=track["id"], name=track["name"]) for track in tracks]

    # We didn't return enough tracks, let's try again.
    if len(tracks) < N_TRACKS_DESIRED:
        tolerance = tolerance + tolerance_bump
        n_runs = n_runs + 1
        return get_recommendations(spotify, input, n_runs=n_runs, tolerance=tolerance)
    else:
        track_list = [Track(id=track["id"], name=track["name"]) for track in tracks]
        return track_list


@router.get("/get_genres")
async def get_genres() -> list[Genre]:
    spotify = create_spotify()
    genres = spotify.recommendation_genre_seeds()
    return [Genre(name=name) for name in genres["genres"]]


@router.get("/get_recommendation_attributes/all")
async def get_all_attributes() -> list[str]:
    """Endpoint function to get a list of string names to be used
    for gathering up all possible attributes.

    Returns:
        list[str]: Names of attributes that can be used.
    """
    return curator.get_all_attributes()


@router.get("/get_recommendation_attributes/number_range")
async def get_number_range_recommendation_attributes() -> list[str]:
    """Endpoint function to get a list of string names to be used
    for gathering up the attributes.

    For all the attributes listed here, float values between 0-1 are allowed as input.
    The API for curation will process those attributes into their correct min/max/target format.

    Returns:
        list[str]: Names of attributes that can be used with numeric range values.
    """
    return curator.get_all_numeric_range_attributes()


@router.get("/get_recommendation_attributes/me")
async def get_attributes() -> list[Attribute]:
    # TODO: This shouldn't be from a user id, this should be
    # from the "/me" and then we get back their prefered default
    # settings or something.
    return RedirectResponse(url="/spotify/get_recommendation_attributes/all")


@router.post("/create_playlist")
async def create_playlist(creator: PlaylistCreator):
    spotify = create_spotify()
    user = spotify.current_user()
    playlist_response = spotify.user_playlist_create(user=user["id"], name=creator.name)
    playlist_id = playlist_response["id"]
    tracks = [track.id for track in creator.tracks]
    spotify.playlist_add_items(playlist_id, tracks)

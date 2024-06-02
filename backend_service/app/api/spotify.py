from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from ..models import curator
from ..models.spotify import (
    Attribute,
    CurrateInput,
    Genre,
    Playlist,
    PlaylistCreator,
    Track,
)
from ..utils.spotify import create_spotify, create_spotify_for_playlist_modification

router = APIRouter(
    prefix="/spotify",
    tags=["spotify"],
    responses={404: {"description": "Not found"}},
)


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
    response = spotify.recommendations(**input.as_recommendation_kwargs())
    tracks = response["tracks"]
    return [Track(id=track["id"], name=track["name"]) for track in tracks]


@router.get("/get_genres")
async def get_genres() -> list[Genre]:
    """Endpoint get the list of all possible recommendation genre seeds
    available from the spotify API.

    Returns:
        list[Genre]: List of genres usable as recommendation seeds.
    """
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
    """Endpoint function for getting attributes specific to the logged in user.

    TBD, this is still a work in progress. Eventually, it'd be cool to have
    a logged in user configure which attributes they like to play with on the
    UI. Hence, this endpoint exists to return the attributes for that user.

    Returns:
        list[Attribute]: List of attributes for the logged in user.
    """
    return RedirectResponse(url="/spotify/get_recommendation_attributes/number_range")


@router.post("/create_playlist")
async def create_playlist(creator: PlaylistCreator):
    spotify = create_spotify_for_playlist_modification()
    user = spotify.current_user()
    playlist_response = spotify.user_playlist_create(user=user["id"], name=creator.name)
    playlist_id = playlist_response["id"]
    tracks = [track.id for track in creator.tracks]
    spotify.playlist_add_items(playlist_id, tracks)

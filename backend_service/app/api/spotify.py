from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from ..models.spotify import (
    Attribute,
    CurrateInput,
    CurrateSeeder,
    Genre,
    Playlist,
    Track,
)
from ..utils.spotify import create_spotify

# Taken from spotipy.client.Spotify.recommendations.
RECOMMENDATION_ATTRIBUTES = [
    "acousticness",
    "danceability",
    "duration_ms",
    "energy",
    "instrumentalness",
    "key",
    "liveness",
    "loudness",
    "mode",
    "popularity",
    "speechiness",
    "tempo",
    "time_signature",
    "valence",
]
router = APIRouter(
    prefix="/spotify",
    tags=["spotify"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get_playlists/me")
async def get_playlists() -> list[Playlist]:
    spotify = create_spotify()
    # Default to just get the first 50 playlists from the user.
    # It'd be nice to use the `spotify.user_playlists` to try to get the like
    #   20 most recently created playlists or something.
    playlists_response = spotify.current_user_playlists()
    return [
        Playlist(id=item["id"], name=item["name"], image_url=item["images"][0]["url"])
        for item in playlists_response["items"]
    ]


@router.post("/curate")
async def curate(input: CurrateInput) -> list[Track]:
    spotify = create_spotify()
    response = spotify.recommendations(**input.as_recommendation_kwargs())
    tracks = response["tracks"]
    return [Track(id=track["id"], name=track["name"]) for track in tracks]


@router.get("/get_genres")
async def get_genres() -> list[Genre]:
    spotify = create_spotify()
    genres = spotify.recommendation_genre_seeds()
    return [Genre(name=name) for name in genres["genres"]]


@router.get("/get_recommendation_attributes/all")
async def get_all_recommendation_attributes() -> list[Attribute]:
    return [
        Attribute(name=name, target=0.5, tolerance=0.2)
        for name in RECOMMENDATION_ATTRIBUTES
    ]


@router.get("/get_recommendation_attributes/me")
async def get_attributes() -> list[Attribute]:
    # TODO: This shouldn't be from a user id, this should be
    # from the "/me" and then we get back their prefered default
    # settings or something.
    return RedirectResponse(url="/spotify/get_recommendation_attributes/all")

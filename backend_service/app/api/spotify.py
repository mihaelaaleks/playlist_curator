from fastapi import APIRouter

from ..models.spotify import Attribute, CurrateInput, Genre, Playlist, Track

router = APIRouter(
    prefix="/spotify",
    tags=["spotify"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get_playlists/{user_id}")
async def get_playlists(user_id: str) -> Playlist:
    dummy = Playlist(
        id="fake",
        tracks=[
            Track(id="fake_track", name="who", artists=["me"], image_id="image_id")
        ],
    )
    return dummy


@router.post("/curate")
async def curate(input: CurrateInput) -> list[Track]:
    return [Track(id="fake_track", name="who", artists=["me"], image_id="image_id")]


@router.get("/get_genres")
async def get_genres() -> list[Genre]:
    return [Genre("woo")]


@router.get("/get_attributes")
async def get_attributes() -> list[Attribute]:
    return [Attribute(name="woo", target=0.5, tolerance=0.2)]


@router.get("/get_attributes/{user_id}")
async def get_attributes(user_id: str) -> list[Attribute]:
    return [Attribute(name="woo", target=0.5, tolerance=0.2)]

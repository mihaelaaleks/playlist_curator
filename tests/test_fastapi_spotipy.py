import pytest
from httpx import AsyncClient, Response

from backend_service.app.models import spotify as spotify_models
from backend_service.main import app


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/docs")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_genres_returns_list_of_genres():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/spotify/get_genres")
        validate_return_type_collection(response, spotify_models.Genre)


@pytest.mark.asyncio
async def test_get_playlists_returns_list_of_playlists():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/spotify/get_playlists/me")
        validate_return_type_collection(response, spotify_models.Playlist)


def make_curate_params() -> list[spotify_models.CurrateInput]:
    # This function could be used to create more curate inputs if needed for testing.
    return [
        spotify_models.CurrateInput(
            seed=spotify_models.CurrateSeeder(id="genres", values=["blues"]),
            attributes=[spotify_models.Attribute(name="liveness", target=50.0)],
        )
    ]


@pytest.mark.parametrize("param", make_curate_params(), ids=str)
@pytest.mark.asyncio
async def test_post_curation(param: spotify_models.CurrateInput):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/spotify/curate", json=param.model_dump())
        validate_return_type_collection(response, spotify_models.Track)


@pytest.mark.asyncio
async def test_integration():
    fake_playlist_name = "My fakeplaylist used for testing"
    param = make_curate_params()[0]
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/spotify/get_playlists/me")
        start_playlist_json = response.json()
        response = await client.post("/spotify/curate", json=param.model_dump())
        track_json = response.json()
        tracks = [spotify_models.Track(**track) for track in track_json]
        playlist_creator = spotify_models.PlaylistCreator(
            name=fake_playlist_name, tracks=tracks
        )
        response = await client.post(
            "/spotify/create_playlist", json=playlist_creator.model_dump()
        )
        response = await client.get("/spotify/get_playlists/me")
        end_playlist_json = response.json()
        # Ensure a playlist was created
        assert len(end_playlist_json) == len(start_playlist_json) + 1
        delete_playlist_id = [
            playlist["id"]
            for playlist in end_playlist_json
            if playlist["name"] == fake_playlist_name
        ][0]
        playlist = spotify_models.Playlist(id=delete_playlist_id)
        response = await client.post("/spotify/delete", json=playlist.model_dump())
        response = await client.get("/spotify/get_playlists/me")
        after_delete_playlist_json = response.json()
        assert len(after_delete_playlist_json) == len(start_playlist_json)


def validate_return_type_collection(
    response: Response, _type: type[spotify_models.BaseModel]
):
    """Assert the response status is valid, and validate that the
    response body json contains a list of objects that can be converted to `_type`.

    Args:
        response (Response): Response from a request with JSON in it's body
            of a list of objects.
        _type (type[spotify_models.BaseModel]): Type of object to validate
            each entry in the list of the JSON.
    """
    assert response.status_code == 200
    json_items = response.json()
    for item in json_items:
        entity = _type(**item)
        assert isinstance(entity, _type)

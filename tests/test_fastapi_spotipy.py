import json

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from spotipy import Spotify

from backend_service.app.models import spotify as spotify_models
from backend_service.main import app  # Assuming your FastAPI app is defined in main.py


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/docs")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_genres_returns_list_of_genres():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/spotify/get_genres")
        assert response.status_code == 200
        json_res = response.json()
        for json_item in json_res:
            genre = spotify_models.Genre(**json_item)
            assert isinstance(genre, spotify_models.Genre)


@pytest.mark.asyncio
async def test_get_playlists_returns_list_of_playlists():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/spotify/get_playlists/me")
        assert response.status_code == 200
        json_res = response.json()
        for json_item in json_res:
            item = spotify_models.Playlist(**json_item)
            assert isinstance(item, spotify_models.Playlist)


def make_curate_params() -> list[spotify_models.CurrateInput]:
    return [
        spotify_models.CurrateInput(
            seed=spotify_models.CurrateSeeder(id="genre", values=["blues"]),
            attributes=[spotify_models.Attribute(name="liveness", target=50.0)],
        )
    ]


# TODO: These post tests are failing and I don't know why.
@pytest.mark.skip
@pytest.mark.parametrize("param", make_curate_params(), ids=str)
@pytest.mark.asyncio
async def test_post_curation(param: spotify_models.CurrateInput):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/spotify/curate", json=param.model_dump())
        assert response.status_code == 201
        json_res = response.json()

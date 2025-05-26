import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, Response
from unittest.mock import MagicMock, patch
import json

from curator_service.app.models import spotify as spotify_model
from curator_service.main import app

# create test client once
client = TestClient(app)

# mock data for testing
MOCK_USER_PLAYLISTS = {
    "items": [
        {
            "id": "playlist1",
            "name": "My Playlist",
            "images": [{"url": "https://example.com/image.jpg"}]
        },
        {
            "id": "playlist2", 
            "name": "Another Playlist",
            "images": []
        }
    ]
}

MOCK_GENRES = {
    "genres": ["blues", "rock", "jazz", "pop"]
}

MOCK_RECOMMENDATIONS = {
    "tracks": [
        {"id": "track1", "name": "Test Song 1"},
        {"id": "track2", "name": "Test Song 2"}
    ]
}

MOCK_USER = {
    "id": "user123"
}

MOCK_CREATED_PLAYLIST = {
    "id": "new_playlist_id"
}

MOCK_TOKEN = "mock_access_token"

@pytest.fixture
def mock_token():
    """Mock the OAuth2 token dependency"""
    with patch("curator_service.app.api.spotify_authenticate.get_current_token") as mock:
        mock.return_value = MOCK_TOKEN
        yield mock

@pytest.fixture
def mock_spotify_client():
    """Mock the SpotifyClient with all its methods"""
    with patch("curator_service.app.services.spotify_client.SpotifyClient") as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        # Configure mock methods
        mock_client.get_user_playlists.return_value = MOCK_USER_PLAYLISTS
        mock_client.get_available_genres.return_value = MOCK_GENRES
        mock_client.get_recommendations.return_value = MOCK_RECOMMENDATIONS
        mock_client.get_current_user.return_value = MOCK_USER
        mock_client.create_playlist.return_value = MOCK_CREATED_PLAYLIST
        mock_client.add_tracks_to_playlist.return_value = None
        mock_client.unfollow_playlist.return_value = None
        
        yield mock_client

@pytest.mark.asyncio
async def test_app_works():
    """Just test that we can reach the app"""
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.get("/docs")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_unauthorized_access():
    """Test that unauthorized access returns a 401 status"""
    response = client.get("/spotify/get_playlists/me")
    assert response.status_code == 401

class TestSpotifyAuthentication:
    """Test auth endpoints"""

    def test_login_returns_auth_url(self):
        """Test login endpoint returns proper URL"""
        response = client.get("/auth_spotify/login?code_challenge=test_challenge")
        assert response.status_code == 200
        data = response.json()
        assert "auth_url" in data
        assert "accounts.spotify.com/authorize" in data["auth_url"]

    # todo fix this
    # im not sure what about the assertion here breaks I think its the patch objects
    def test_token_exchange_success(self):
        """Test successful token exchange"""
    mock_response = {
        "access_token": "mock_token",
        "token_type": "Bearer",
        "expires_in": 3600, 
        "refresh_token": "mock_refresh_token"
    }

    with patch("requests.post") as mock_post: 
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response

        # FIX: Send as query parameters
        response = client.post("/auth_spotify/token?code=test_code&code_verifier=test_verifier")
        assert response.status_code == 200
        assert response.json() == mock_response

    def test_token_exchange_failure(self):
        """Test failed token exchange"""
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 400
            mock_post.return_value.json.return_value = {"error_description": "Invalid code"}
            
            response = client.post("/auth_spotify/token?code=invalid_code&code_verifier=test_verifier")
            assert response.status_code == 400

    def test_refresh_token_success(self):
        """Test successful token refresh"""
        mock_response = {
            "access_token": "new_mock_token",
            "token_type": "Bearer",
            "expires_in": 3600
        }
        
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = mock_response
            
            response = client.post("/auth_spotify/refresh?refresh_token=mock_refresh_token")
            assert response.status_code == 200
            assert response.json() == mock_response

# todo: 
    # test get genres/ return a list of genres
    # test get playlists/ return a list of playlists
    # test curate endpoint with
        # artist seed
        # track seed
        # "playlist" seed --> which is to say a bunch of passes with track seed
    # validate returning parameters
    # test create playlist endpoint

# class TestSpotifyAPI:
#     """Test Spotify API endpoints"""

#     def test_get_playlists_success(self, mock_token, mock_spotify_client):
#         """Test getting user playlists"""
#         response = client.get("/spotify/get_playlists/me",
#                               headers={"Authorization": f"Bearer {MOCK_TOKEN}"})
#         assert response.status_code == 200
#         playlists = response.json()
#         assert len(playlists) == 2
#         assert playlists[0]["id"] == "playlist1"
#         assert playlists[0]["name"] == "My Playlist"
#         assert playlists[1]["image_url"] is None # no image for second playlist



# @pytest.mark.asyncio
# async def test_get_genres_returns_list_of_genres():
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.get("/spotify/get_genres")
#         validate_return_type_collection(response, spotify_model.Genre)


# @pytest.mark.asyncio
# async def test_get_playlists_returns_list_of_playlists():
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.get("/spotify/get_playlists/me")
#         validate_return_type_collection(response, spotify_model.Playlist)


# def make_curate_params() -> list[spotify_model.CurrateInput]:
#     # This function could be used to create more curate inputs if needed for testing.
#     return [
#         spotify_model.CurrateInput(
#             seed=spotify_model.CurrateSeeder(id="genres", values=["blues"]),
#             attributes=[spotify_model.Attribute(name="liveness", target=50.0)],
#         )
#     ]


# @pytest.mark.parametrize("param", make_curate_params(), ids=str)
# @pytest.mark.asyncio
# async def test_post_curation(param: spotify_model.CurrateInput):
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.post("/spotify/curate", json=param.model_dump())
#         validate_return_type_collection(response, spotify_model.Track)


# @pytest.mark.asyncio
# async def test_integration():
#     fake_playlist_name = "My fakeplaylist used for testing"
#     param = make_curate_params()[0]
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.get("/spotify/get_playlists/me")
#         start_playlist_json = response.json()
#         response = await client.post("/spotify/curate", json=param.model_dump())
#         track_json = response.json()
#         tracks = [spotify_model.Track(**track) for track in track_json]
#         playlist_creator = spotify_model.PlaylistCreator(
#             name=fake_playlist_name, tracks=tracks
#         )
#         response = await client.post(
#             "/spotify/create_playlist", json=playlist_creator.model_dump()
#         )
#         response = await client.get("/spotify/get_playlists/me")
#         end_playlist_json = response.json()
#         # Ensure a playlist was created
#         assert len(end_playlist_json) == len(start_playlist_json) + 1
#         delete_playlist_id = [
#             playlist["id"]
#             for playlist in end_playlist_json
#             if playlist["name"] == fake_playlist_name
#         ][0]
#         playlist = spotify_model.Playlist(id=delete_playlist_id)
#         response = await client.post("/spotify/delete", json=playlist.model_dump())
#         response = await client.get("/spotify/get_playlists/me")
#         after_delete_playlist_json = response.json()
#         assert len(after_delete_playlist_json) == len(start_playlist_json)


# def validate_return_type_collection(
#     response: Response, _type: type[spotify_model.BaseModel]
# ):
#     """Assert the response status is valid, and validate that the
#     response body json contains a list of objects that can be converted to `_type`.

#     Args:
#         response (Response): Response from a request with JSON in it's body
#             of a list of objects.
#         _type (type[spotify_models.BaseModel]): Type of object to validate
#             each entry in the list of the JSON.
#     """
#     assert response.status_code == 200
#     json_items = response.json()
#     for item in json_items:
#         entity = _type(**item)
#         assert isinstance(entity, _type)

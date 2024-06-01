import spotipy
from fastapi import APIRouter, Request, Response
from spotipy.oauth2 import SpotifyOAuth

# TODO:
# Also when auth is working, but the client id and secret should
# be handled via the .env call.
#   the "create_spotify" can already do that. But it's not
#   clear to me how we'd even begin testing authentication since
#   the computer knows its me already lol.
CLIENT_ID = "a1d01cfdcbf64f74a10ed7a68b5c388d"
CLIENT_SECRET = "0d891767d4a042f59d0615a16a844700"
REDIRECT_URI = "https://localhost:8000/callback"


# TODO: this was just "suggested" by GPT as a way to store the
# current users in ram. In principle, for a basic POC of logging
# with spotify functioning as expected, that'd likely be too naive.
#   Keeping this here to delete in the future when auth is working.
class UserData:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id, access_token, refresh_token, scope):
        self.users[user_id] = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "scope": scope,
        }

    def get_user(self, user_id):
        return self.users.get(user_id)


user_data = UserData()

router = APIRouter(
    prefix="/auth_spotify",
    tags=["auth_spotify"],
    responses={404: {"description": "Not found"}},
)


@router.get("/auth")
async def authenticate(response: Response):
    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-library-read user-top-read",
    )
    auth_url = sp_oauth.get_authorize_url()
    response.headers["Location"] = auth_url
    response.status_code = 302  # Redirect status code


@router.get("/callback")
async def callback(request: Request):
    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-library-read user-top-read",
    )
    code = request.query_params.get("code")
    token_info = sp_oauth.get_access_token(code)

    access_token = token_info["access_token"]
    refresh_token = token_info["refresh_token"]
    scope = token_info["scope"]

    # Create Spotipy client instance
    sp = spotipy.Spotify(auth=access_token)
    current_user = sp.current_user()
    user_id = current_user["id"]

    # Store user data in the in-memory data store
    user_data.add_user(user_id, access_token, refresh_token, scope)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "scope": scope,
        "user_id": user_id,
    }

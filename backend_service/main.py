from typing import Dict
from urllib.parse import urlencode

import spotipy
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from spotipy.oauth2 import SpotifyOAuth

from app.api import spotify

app = FastAPI()
origins = [
    "https://localhost",
    "https://localhost:8888",
    "http://localhost",
    "http://localhost:8888",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(spotify.router)

# Replace with your Spotify app credentials
CLIENT_ID = "a1d01cfdcbf64f74a10ed7a68b5c388d"
CLIENT_SECRET = "0d891767d4a042f59d0615a16a844700"
REDIRECT_URI = "https://localhost:8888/callback"  # Replace with your redirect URI


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


@app.get("/auth")
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


@app.get("/callback")
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)

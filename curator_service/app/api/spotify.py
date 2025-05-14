import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from typing import List, Optional

from ..models import curator
from ..models.spotify import (
    Attribute,
    CurrateInput,
    Genre,
    Playlist,
    PlaylistCreator,
    Track,
)
from ..services.spotify_client import SpotifyClient
from .spotify_authenticate import get_current_token

load_dotenv()

router = APIRouter(
    prefix="/spotify",
    tags=["spotify"],
    responses={404: {"description": "Not found"}},
)

# New implementation using SpotifyClient
async def get_spotify_client(token: str = Depends(get_current_token)) -> SpotifyClient:
    """Get a configured SpotifyClient instance using the current user's token."""
    return SpotifyClient(token)

@router.get("/get_playlists/me")
async def get_playlists(spotify: SpotifyClient = Depends(get_spotify_client)) -> List[Playlist]:
    """Get the current user's playlists."""
    try:
        response = spotify.get_user_playlists()
        return [
            Playlist(
                id=item["id"],
                name=item["name"],
                image_url=item["images"][0]["url"] if item["images"] else None
            )
            for item in response["items"]
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/delete")
async def delete_playlist(playlist: Playlist, spotify: SpotifyClient = Depends(get_spotify_client)):
    """Unfollow/delete a playlist."""
    try:
        spotify.unfollow_playlist(playlist.id)
        return JSONResponse(content={"message": "Playlist unfollowed successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/curate")
async def curate(input: CurrateInput, spotify: SpotifyClient = Depends(get_spotify_client)) -> List[Track]:
    """Get track recommendations based on input parameters."""
    try:
        # Convert input parameters to Spotify API format
        params = {}
        
        # Add seed parameters
        if input.seed:
            if input.seed.id == "genres":
                params["seed_genres"] = input.seed.values
            elif input.seed.id == "tracks":
                params["seed_tracks"] = input.seed.values
            elif input.seed.id == "artists":
                params["seed_artists"] = input.seed.values

        # Add attribute parameters
        if input.attributes:
            for attr in input.attributes:
                params[f"target_{attr.name}"] = attr.target
                if attr.tolerance:
                    params[f"min_{attr.name}"] = max(0, attr.target - attr.tolerance)
                    params[f"max_{attr.name}"] = min(1, attr.target + attr.tolerance)

        response = spotify.get_recommendations(**params)
        return [Track(id=track["id"], name=track["name"]) for track in response["tracks"]]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get_genres")
async def get_genres(spotify: SpotifyClient = Depends(get_spotify_client)) -> List[Genre]:
    """Get available genre seeds."""
    try:
        response = spotify.get_available_genres()
        return [Genre(name=name) for name in response["genres"]]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create_playlist")
async def create_playlist(creator: PlaylistCreator, spotify: SpotifyClient = Depends(get_spotify_client)):
    """Create a new playlist and add tracks to it."""
    try:
        # Get current user's ID
        user = spotify.get_current_user()
        user_id = user["id"]

        # Create the playlist
        playlist = spotify.create_playlist(
            user_id=user_id,
            name=creator.name,
            public=False,
            description="Created by Playlist Curator"
        )

        # Add tracks to the playlist
        if creator.tracks:
            track_uris = [f"spotify:track:{track.id}" for track in creator.tracks]
            spotify.add_tracks_to_playlist(playlist["id"], track_uris)

        return JSONResponse(content={"message": "Playlist created successfully", "playlist_id": playlist["id"]})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get_recommendation_attributes/all")
async def get_all_attributes() -> list[str]:
    """Get all available recommendation attributes."""
    return curator.get_all_attributes()

@router.get("/get_recommendation_attributes/number_range")
async def get_number_range_recommendation_attributes() -> list[str]:
    """Get recommendation attributes that accept numeric range values (0-1)."""
    return curator.get_all_numeric_range_attributes()

@router.get("/get_recommendation_attributes/me")
async def get_attributes() -> list[Attribute]:
    """Get user's preferred recommendation attributes (redirects to all attributes for now)."""
    return RedirectResponse(url="/spotify/get_recommendation_attributes/all")


# TODO: revise this during testing
# --------------------------------
N_TRACKS_DESIRED = 1
N_LIMIT_RUNS = 2
BUMP_TOLERANCE = 0.6
DEFAULT_START_TOLERANCE = 0.25


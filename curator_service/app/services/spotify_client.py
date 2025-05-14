from typing import Optional, Dict, Any, List
import requests
from fastapi import HTTPException

class SpotifyClient:
    BASE_URL = "https://api.spotify.com/v1"
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        })

    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, json: Optional[Dict] = None) -> Dict:
        """Make a request to the Spotify API"""
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = self.session.request(method, url, params=params, json=json)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if response.status_code == 401:
                raise HTTPException(status_code=401, detail="Token expired or invalid")
            raise HTTPException(status_code=response.status_code, detail=str(e))

    def get_current_user(self) -> Dict[str, Any]:
        """Get the current user's profile"""
        return self._make_request("GET", "me")

    def get_user_playlists(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """Get the current user's playlists"""
        return self._make_request("GET", "me/playlists", params={
            "limit": limit,
            "offset": offset
        })

    def create_playlist(self, user_id: str, name: str, public: bool = False, description: str = "") -> Dict[str, Any]:
        """Create a new playlist"""
        return self._make_request("POST", f"users/{user_id}/playlists", json={
            "name": name,
            "public": public,
            "description": description
        })

    def add_tracks_to_playlist(self, playlist_id: str, track_uris: List[str]) -> Dict[str, Any]:
        """Add tracks to a playlist"""
        return self._make_request("POST", f"playlists/{playlist_id}/tracks", json={
            "uris": track_uris
        })

    def get_recommendations(self, seed_tracks: Optional[List[str]] = None,
                          seed_artists: Optional[List[str]] = None,
                          seed_genres: Optional[List[str]] = None,
                          limit: int = 20,
                          **kwargs) -> Dict[str, Any]:
        """Get track recommendations"""
        params = {
            "limit": limit,
            **{k: v for k, v in kwargs.items() if v is not None}
        }
        
        if seed_tracks:
            params["seed_tracks"] = ",".join(seed_tracks)
        if seed_artists:
            params["seed_artists"] = ",".join(seed_artists)
        if seed_genres:
            params["seed_genres"] = ",".join(seed_genres)

        return self._make_request("GET", "recommendations", params=params)

    def get_available_genres(self) -> Dict[str, Any]:
        """Get available genre seeds"""
        return self._make_request("GET", "recommendations/available-genre-seeds")

    def get_track(self, track_id: str) -> Dict[str, Any]:
        """Get track details"""
        return self._make_request("GET", f"tracks/{track_id}")

    def get_several_tracks(self, track_ids: List[str]) -> Dict[str, Any]:
        """Get several tracks' details"""
        return self._make_request("GET", "tracks", params={
            "ids": ",".join(track_ids)
        })

    def get_user_top_tracks(self, limit: int = 20, offset: int = 0, time_range: str = "medium_term") -> Dict[str, Any]:
        """Get user's top tracks"""
        return self._make_request("GET", "me/top/tracks", params={
            "limit": limit,
            "offset": offset,
            "time_range": time_range
        })

    def get_user_saved_tracks(self, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """Get user's saved tracks"""
        return self._make_request("GET", "me/tracks", params={
            "limit": limit,
            "offset": offset
        })

    def unfollow_playlist(self, playlist_id: str) -> None:
        """Unfollow/delete a playlist"""
        self._make_request("DELETE", f"playlists/{playlist_id}/followers") 
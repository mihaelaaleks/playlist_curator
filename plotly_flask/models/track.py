from dataclasses import dataclass
from typing import Any


@dataclass
class Track:
    id: str
    name: str
    url: str
    artists: list
    album_id: str
    album_image: Any
    track_popularity: int

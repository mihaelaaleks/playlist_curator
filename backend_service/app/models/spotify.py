from pydantic import BaseModel


class Genre(BaseModel):
    name: str


class Track(BaseModel):
    id: str
    name: str
    artists: list[str]
    image_id: str


class Playlist(BaseModel):
    id: str
    tracks: list[Track]


class Attribute(BaseModel):
    name: str
    target: float
    tolerance: float


class CurrateInput(BaseModel):
    seed: str  # TODO: use a seed input type here
    attributes: list[Attribute]

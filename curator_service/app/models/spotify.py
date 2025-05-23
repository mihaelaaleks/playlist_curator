from collections import ChainMap
from typing import Optional

from pydantic import BaseModel

class Genre(BaseModel):
    name: str


class Track(BaseModel):
    # TODO: check on front end of embed if current model is correct
    id: str
    name: str


class Playlist(BaseModel):
    id: str
    name: Optional[str] = None
    image_url: Optional[str] = None


class PlaylistCreator(BaseModel):
    name: str
    tracks: list[Track]


# Check if basemodel strategy is correct/still good
class Attribute(BaseModel):
    name: str
    target: float

    def as_recommendation_kwargs(self, tolerance: float = 0.1) -> dict:
        # TODO: These checks have to happen per type of attribute unfortunately.
        # Target is the value between 0 and 1 to
        # use for the named attribute.

        # wait they have to happen per type of attribute but then were abstracting from a base model 
        # KNOWING theyre all different
        # we have to retest how to set the tolerance for these
        # maybe do it individually then we can figure out some way to abstract it neatly
        if 1 <= self.target <= 100:
            self.target = self.target / 100
        assert 0 <= self.target <= 1

        # Min will be target minus standard amount
        min_value = self.target - tolerance
        # If the calculated min is less than zero, set to zero
        min_value = max(0, min_value)

        # Min will be target minus standard amount
        max_value = self.target + tolerance
        # If the calculated max is more than 1, set to 1
        max_value = min(1, max_value)
        return {
            f"min_{self.name}": min_value,
            f"max_{self.name}": max_value,
            f"target_{self.name}": self.target,
        }


class CurrateSeeder(BaseModel):
    id: str
    values: list[str]


class CurrateInput(BaseModel):
    seed: CurrateSeeder
    attributes: list[Attribute] | None = None

    def as_recommendation_kwargs(self, attribute_tolerance: float = 0.1) -> dict:
        seed_name = "seed_" + self.seed.id
        seed_kwargs = {seed_name: self.seed.values}
        attribute_kwarg = self.get_attribute_kwargs(attribute_tolerance)
        # The | can be used to join dictionaries
        return seed_kwargs | attribute_kwarg

    def get_attribute_kwargs(self, tolerance: float = 0.1) -> dict:
        # Return a list of dictionaries of all the items.
        if self.attributes is None:
            return {}
        kwarg_list = [
            attribute.as_recommendation_kwargs(tolerance)
            for attribute in self.attributes
        ]
        # Combine them into one large dictionary
        return dict(ChainMap(*kwarg_list))

from collections import ChainMap

from pydantic import BaseModel


class Genre(BaseModel):
    name: str


class Track(BaseModel):
    # TODO: check on front end of embed. It seems like only the id is needed
    #   hence, no need to pass things like the artists.
    id: str
    name: str


class Playlist(BaseModel):
    id: str
    name: str
    image_url: str


# TODO: So for all the different attributes, they have slightly
#   annoyingly different rules.
#   yeah this will for sure be the most annoying thing to do
#   but doing it well from the python should then make it
#   easy for the front end to communicate
# Leo don't be silly, this is pydantic so you can just build this
# as some "base attribute model" and then pass that.
class Attribute(BaseModel):
    name: str
    target: float
    tolerance: float

    def as_recommendation_kwargs(self) -> dict:
        # TODO: These checks have to happen per type of attribute unfortunately.
        # Target is the value between 0 and 1 to
        # use for the named attribute.
        assert 0 <= self.target <= 1
        # Tolerance is a percentage to apply on target
        assert 0 <= self.tolerance <= 1
        # Get percentage difference down
        min_value = self.target * (1 - self.tolerance)
        # If the calculated min is less than zero, set to zero
        min_value = max(0, min_value)

        # Get percentage difference up
        max_value = self.target * (1 + self.tolerance)
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

    def as_recommendation_kwargs(self) -> dict:
        seed_name = "seed_" + self.seed.id
        seed_kwargs = {seed_name: self.seed.values}
        attribute_kwarg = self.get_attribute_kwargs()
        # The | can be used to join dictionaries
        return seed_kwargs | attribute_kwarg

    def get_attribute_kwargs(self) -> dict:
        # Return a list of dictionaries of all the items.
        if self.attributes is None:
            return {}
        kwarg_list = [
            attribute.as_recommendation_kwargs() for attribute in self.attributes
        ]
        # Combine them into one large dictionary
        return dict(ChainMap(*kwarg_list))

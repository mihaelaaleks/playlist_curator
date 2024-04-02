import pytest
import pandas as pd
from plotly_flask.models.playlist_logic import (
    get_tracklist,
    get_tracklist_w_labels,
)
from app.spotipy_requests import (
    create_spotify,
)


@pytest.fixture
def spotify():
    return create_spotify()


def test_get_tracklist():
    test_id = "7doP9xG2n6DXnflGTmURsC"
    tracklist = get_tracklist(test_id)
    assert isinstance(tracklist, list)


def test_get_tracklist_w_labels():
    test_id = "7doP9xG2n6DXnflGTmURsC"
    tracklist = get_tracklist_w_labels(test_id)
    assert isinstance(tracklist, pd.DataFrame)
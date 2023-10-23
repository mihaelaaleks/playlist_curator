# import app.data_store # module not found cause its not a module yet
import pytest
from app import data_store
from pathlib import Path
from app import response_clean

_path_app_data = Path(__file__).parent.parent.parent / Path('app/data')

@pytest.fixture
def mock_data_content() -> None:
    test_data = {}
    test_data["data"] = ["my data"]
    test_data["mock_response_data"] = {'items': {'track_1': 'abc', 'nonsense': 'aaa'}, 'flag': {'abc': 'aaa', 'cba': 'bbb'}}
    test_data["mock_track_data"] = [{'track': {'id': 1, 'name': '2', 'artists': [{'id': 'blue', 'name': 'fine'}], 'popularity': 34, 'greeble': 180}}, 
                            {'track': {'id': 78, 'name': 'fey', 'artists': [{'id': 'green', 'name': 'not fine'}], 'popularity': 70, 'frumble': 360}}]
    return test_data

def test_check_if_file_exists(mock_data_content):
    file_name = "filename"
    expected_path = _path_app_data / Path(f'{file_name}.json')
    data_store.store_data_as_json(mock_data_content["data"], file_name)
    # i want to check that the path of the file exists
    # if it does return true
    assert(expected_path.is_file())
    # cleanup - remove test file
    expected_path.unlink()

def test_open_recently_played_json(mock_data_content):
        # create the file we will load and clean
    file_name = "filename"
    expected_path = _path_app_data / Path(f'{file_name}.json')
    data_store.store_data_as_json(mock_data_content["mock_response_data"], file_name)
    # use open_recently_played_json() to open the json file
    # per the function the expected result should be just the 'items' dictionary
    # WITHOUT THE 'ITEMS' KEY
    expected_result = {'track_1': 'abc', 'nonsense': 'aaa'}
    item_json_data = response_clean.open_recently_played_json(file_name)
    assert expected_result == item_json_data
    # cleanup - remove test file
    expected_path.unlink()

def test_clean_recently_played(mock_data_content):
    cleaned_recently_played = response_clean.clean_recently_played(
        mock_data_content["mock_track_data"])
    # check if the track_id of the first entry is indeed 1
    # maybe this could be better? 
    assert cleaned_recently_played[0]['track_id'] == 1
    
def test_get_id_recently_played(mock_data_content):
    track_ids = []
    track_ids = response_clean.get_id_recently_played(
            mock_data_content["mock_track_data"])
    assert isinstance(track_ids, list)
    assert len(track_ids) == 2
    assert track_ids[1] == 78

    
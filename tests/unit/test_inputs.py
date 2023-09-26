# import app.data_store # module not found cause its not a module yet

import unittest
from app import data_store
import pathlib
from app import response_clean

class AttemptTestCase(unittest.TestCase):
    
    def setUp(self) -> None:
        self.data = ["my data"]
        self.mock_response_data = {'items': {'track_1': 'abc', 'nonsense': 'aaa'}, 'flag': {'abc': 'aaa', 'cba': 'bbb'}}
        self.mock_track_data = [{'track': {'id': 1, 'name': '2', 'artists': [{'id': 'blue', 'name': 'fine'}], 'popularity': 34, 'greeble': 180}}, 
                                {'track': {'id': 78, 'name': 'fey', 'artists': [{'id': 'green', 'name': 'not fine'}], 'popularity': 70, 'frumble': 360}}]
        self.path = pathlib.Path(__file__).parent.parent.parent / pathlib.Path('app/data')
        return super().setUp()
    
    def test_check_if_file_exists(self):
        file_name = "filename"
        expected_path = self.path / pathlib.Path(f'{file_name}.json')
        data_store.store_data_as_json(self.data, file_name)
        # i want to check that the path of the file exists
        # if it does return true
        self.assertTrue(expected_path.is_file())
        # cleanup - remove test file
        expected_path.unlink()
    
    def test_open_recently_played_json(self):
         # create the file we will load and clean
         file_name = "filename"
         expected_path = self.path / pathlib.Path(f'{file_name}.json')
         data_store.store_data_as_json(self.mock_response_data, file_name)
         # use open_recently_played_json() to open the json file
         # per the function the expected result should be just the 'items' dictionary
         # WITHOUT THE 'ITEMS' KEY
         expected_result = {'track_1': 'abc', 'nonsense': 'aaa'}
         item_json_data = response_clean.open_recently_played_json(file_name)
         self.assertEqual(expected_result, item_json_data)
         # cleanup - remove test file
         expected_path.unlink()
    
    def test_clean_recently_played(self):
        cleaned_recently_played = response_clean.clean_recently_played(self.mock_track_data)
        # check if the track_id of the first entry is indeed 1
        # maybe this could be better? 
        self.assertEqual(cleaned_recently_played[0]['track_id'], 1)
        
    def test_get_id_recently_played(self):
        track_ids = []
        track_ids = response_clean.get_id_recently_played(self.mock_track_data)
        self.assertEqual(len(track_ids), 2)
        self.assertEqual(track_ids[1], 78)
        
        
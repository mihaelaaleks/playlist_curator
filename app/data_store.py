import json
import pathlib
# testing



# json data store
# what happens if the file name already exists? 
# probably gets overwritten right? 
# should probably have a check for that 
def store_data_as_json(data, file_name):
    # these filepath shenanigans can be made way nicer
    filepath = pathlib.Path(__file__).parent / pathlib.Path('data')
    filepath = filepath / pathlib.Path(f'{file_name}.json')
    print(filepath)
    with open(filepath, 'w') as file:
        json.dump(data, file)
    return



# stuff = [{'a': 'b'}, {'a': 'b'}]
# stwing = 'stuff'
# store_data_as_json(stuff, stwing)


# pickle data store



